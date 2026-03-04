// Architecture Notes:
// - This file is heavily commented for long-term maintainability and reconstruction.
// - Pipeline shape is parse -> model -> compute -> emit.
// - Performance-sensitive sections document data-layout and concurrency tradeoffs.

package main

import (
	"crypto/sha256"
	"encoding/hex"
	"flag"
	"fmt"
	"io"
	"math/bits"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
	"sync"
	"time"
)

const expectedSHA = "354ac7a7409ec19ac2561c95f08ba4d0df1a26cdda409bef5ba594cff685eb0a"
const expectedPart1 = "8074"
const expectedPart2 = "1212"

var suffix = []int{17, 31, 73, 47, 23}

func resolveInput(provided string) string {
	if provided != "" {
		return provided
	}
	cands := []string{"advent2017/Day14/d14_input.txt", "Day14/d14_input.txt", "../Day14/d14_input.txt", "../../Day14/d14_input.txt"}
	for _, c := range cands {
		if _, err := os.Stat(c); err == nil {
			abs, err := filepath.Abs(c)
			if err == nil {
				return abs
			}
			return c
		}
	}
	panic("input not found")
}

func sha256File(path string) string {
	f, err := os.Open(path)
	if err != nil {
		panic(err)
	}
	defer f.Close()
	h := sha256.New()
	if _, err := io.Copy(h, f); err != nil {
		panic(err)
	}
	return hex.EncodeToString(h.Sum(nil))
}

func reverseSegment(a []int, start int, length int) {
	n := len(a)
	for i := 0; i < length/2; i++ {
		x := (start + i) % n
		y := (start + length - 1 - i) % n
		a[x], a[y] = a[y], a[x]
	}
}

func knotHashBytes(key string) [16]byte {
	lengths := make([]int, 0, len(key)+len(suffix))
	for _, b := range []byte(key) {
		lengths = append(lengths, int(b))
	}
	lengths = append(lengths, suffix...)

	ring := make([]int, 256)
	for i := 0; i < 256; i++ {
		ring[i] = i
	}

	pos, skip := 0, 0
	for round := 0; round < 64; round++ {
		for _, ln := range lengths {
			reverseSegment(ring, pos, ln)
			pos = (pos + ln + skip) % 256
			skip++
		}
	}

	var out [16]byte
	for b := 0; b < 16; b++ {
		x := 0
		for i := 0; i < 16; i++ {
			x ^= ring[b*16+i]
		}
		out[b] = byte(x)
	}
	return out
}

type rowResult struct {
	r    int
	row  [128]bool
	used int
}

func workerCount() int {
	n := runtime.GOMAXPROCS(0)
	if n < 1 {
		n = 1
	}
	if n > 16 {
		n = 16
	}
	if n > 128 {
		n = 128
	}
	return n
}

func buildGrid(seed string) ([128][128]bool, int) {
	var g [128][128]bool
	used := 0

	jobs := make(chan int, 128)
	results := make(chan rowResult, 128)
	var wg sync.WaitGroup

	workers := workerCount()
	wg.Add(workers)
	for w := 0; w < workers; w++ {
		go func() {
			defer wg.Done()
			for r := range jobs {
				h := knotHashBytes(fmt.Sprintf("%s-%d", seed, r))
				var row [128]bool
				rowUsed := 0
				c := 0
				for _, b := range h {
					rowUsed += bits.OnesCount8(b)
					for bit := 7; bit >= 0; bit-- {
						row[c] = ((b >> uint(bit)) & 1) == 1
						c++
					}
				}
				results <- rowResult{r: r, row: row, used: rowUsed}
			}
		}()
	}

	for r := 0; r < 128; r++ {
		jobs <- r
	}
	close(jobs)
	wg.Wait()
	close(results)

	for res := range results {
		g[res.r] = res.row
		used += res.used
	}
	return g, used
}

func countRegions(g [128][128]bool) int {
	var seen [128][128]bool
	regions := 0
	dx := [4]int{1, -1, 0, 0}
	dy := [4]int{0, 0, 1, -1}

	type P struct{ x, y int }
	for i := 0; i < 128; i++ {
		for j := 0; j < 128; j++ {
			if !g[i][j] || seen[i][j] {
				continue
			}
			regions++
			q := []P{{i, j}}
			seen[i][j] = true
			for len(q) > 0 {
				p := q[0]
				q = q[1:]
				for k := 0; k < 4; k++ {
					nx, ny := p.x+dx[k], p.y+dy[k]
					if nx < 0 || nx >= 128 || ny < 0 || ny >= 128 {
						continue
					}
					if !g[nx][ny] || seen[nx][ny] {
						continue
					}
					seen[nx][ny] = true
					q = append(q, P{nx, ny})
				}
			}
		}
	}
	return regions
}

func solve(seed string) (int, int) {
	g, used := buildGrid(seed)
	return used, countRegions(g)
}

func main() {
	part := flag.Int("part", 0, "part")
	input := flag.String("input", "", "input")
	flag.Parse()
	if *part != 1 && *part != 2 {
		panic("--part 1|2 required")
	}

	in := resolveInput(*input)
	if sha256File(in) != expectedSHA {
		panic("checksum mismatch")
	}
	seed := strings.TrimSpace(string(must(os.ReadFile(in))))

	t0 := time.Now()
	p1, p2 := solve(seed)
	ans := strconv.Itoa(p1)
	if *part == 2 {
		ans = strconv.Itoa(p2)
	}
	expected := expectedPart1
	if *part == 2 {
		expected = expectedPart2
	}
	if ans != expected {
		panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected))
	}

	fmt.Println(ans)
	ms := float64(time.Since(t0).Nanoseconds()) / 1e6
	fmt.Fprintf(os.Stderr, "[go-fancy] day=14 part=%d runtime_ms=%.3f\n", *part, ms)
}

func must[T any](v T, err error) T {
	if err != nil {
		panic(err)
	}
	return v
}
