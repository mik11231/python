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
	"math"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"
)

const expectedSHA = "866b77a4b5e37e19219792c97103a17d24c5f15a9f0bed448c0e6cfd75378beb"
const expectedP1 = "3969"
const expectedP2 = "917"

type Ins struct{ Op, X, Y string }

func resolveInput(provided string) string {
	if provided != "" {
		return provided
	}
	cands := []string{
		"advent2017/Day23/d23_input.txt",
		"Day23/d23_input.txt",
		"../Day23/d23_input.txt",
		"../../Day23/d23_input.txt",
	}
	for _, c := range cands {
		if _, err := os.Stat(c); err == nil {
			return c
		}
	}
	panic("input not found")
}

func hashFile(path string) string {
	b, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	sum := sha256.Sum256(b)
	return hex.EncodeToString(sum[:])
}

func parse(path string) []Ins {
	b, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	out := make([]Ins, 0, 64)
	for _, ln := range regexp.MustCompile(`\r?\n`).Split(string(b), -1) {
		s := strings.TrimSpace(ln)
		if s == "" {
			continue
		}
		p := strings.Fields(s)
		y := "0"
		if len(p) > 2 {
			y = p[2]
		}
		out = append(out, Ins{p[0], p[1], y})
	}
	return out
}

func val(tok string, regs map[string]int64) int64 {
	if v, err := strconv.ParseInt(tok, 10, 64); err == nil {
		return v
	}
	return regs[tok]
}

func solvePart1(prog []Ins) int {
	regs := map[string]int64{}
	ip := int64(0)
	muls := 0
	for ip >= 0 && ip < int64(len(prog)) {
		in := prog[ip]
		switch in.Op {
		case "set":
			regs[in.X] = val(in.Y, regs)
		case "sub":
			regs[in.X] = regs[in.X] - val(in.Y, regs)
		case "mul":
			regs[in.X] = regs[in.X] * val(in.Y, regs)
			muls++
		case "jnz":
			if val(in.X, regs) != 0 {
				ip += val(in.Y, regs)
				continue
			}
		}
		ip++
	}
	return muls
}

func isPrime(n int64) bool {
	if n < 2 {
		return false
	}
	if n%2 == 0 {
		return n == 2
	}
	lim := int64(math.Sqrt(float64(n)))
	for d := int64(3); d <= lim; d += 2 {
		if n%d == 0 {
			return false
		}
	}
	return true
}

func solvePart2(prog []Ins) int {
	b0, _ := strconv.ParseInt(prog[0].Y, 10, 64)
	b := b0*100 + 100000
	c := b + 17000
	cnt := 0
	for x := b; x <= c; x += 17 {
		if !isPrime(x) {
			cnt++
		}
	}
	return cnt
}

func main() {
	part := flag.Int("part", 0, "part")
	input := flag.String("input", "", "input")
	flag.Parse()
	if *part != 1 && *part != 2 {
		panic("--part 1|2 required")
	}
	in := resolveInput(*input)
	if hashFile(in) != expectedSHA {
		panic("checksum mismatch")
	}
	prog := parse(in)

	t0 := time.Now()
	ans := ""
	if *part == 1 {
		ans = strconv.Itoa(solvePart1(prog))
	} else {
		ans = strconv.Itoa(solvePart2(prog))
	}
	exp := expectedP1
	if *part == 2 {
		exp = expectedP2
	}
	if ans != exp {
		panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, exp))
	}
	fmt.Println(ans)
	ms := float64(time.Since(t0).Nanoseconds()) / 1e6
	fmt.Fprintf(os.Stderr, "[go-fancy] day=23 part=%d runtime_ms=%.3f\n", *part, ms)
}
