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
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"
)

const expectedSHA = "48a139f917d7dac161171c28f578d923b212c10108c92bbe05a971f6d8b4fb05"
const expectedP1 = "1656"
const expectedP2 = "1642"

type Comp struct{ A, B int }
type Ret struct{ S, L, LS int }

func resolveInput(provided string) string {
	if provided != "" {
		return provided
	}
	cands := []string{
		"advent2017/Day24/d24_input.txt",
		"Day24/d24_input.txt",
		"../Day24/d24_input.txt",
		"../../Day24/d24_input.txt",
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

func parse(path string) ([]Comp, map[int][]int) {
	b, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	comps := make([]Comp, 0, 64)
	by := map[int][]int{}
	for _, ln := range regexp.MustCompile(`\r?\n`).Split(string(b), -1) {
		s := strings.TrimSpace(ln)
		if s == "" {
			continue
		}
		p := strings.Split(s, "/")
		a, _ := strconv.Atoi(p[0])
		c, _ := strconv.Atoi(p[1])
		i := len(comps)
		comps = append(comps, Comp{a, c})
		by[a] = append(by[a], i)
		if c != a {
			by[c] = append(by[c], i)
		}
	}
	return comps, by
}

func solve(comps []Comp, by map[int][]int) (int, int) {
	used := make([]bool, len(comps))
	var dfs func(int) Ret
	dfs = func(port int) Ret {
		best := Ret{}
		for _, i := range by[port] {
			if used[i] {
				continue
			}
			c := comps[i]
			nxt := c.B
			if c.A != port {
				nxt = c.A
			}
			seg := c.A + c.B
			used[i] = true
			ch := dfs(nxt)
			used[i] = false

			if seg+ch.S > best.S {
				best.S = seg + ch.S
			}
			cl := 1 + ch.L
			cls := seg + ch.LS
			if cl > best.L || (cl == best.L && cls > best.LS) {
				best.L = cl
				best.LS = cls
			}
		}
		return best
	}
	r := dfs(0)
	return r.S, r.LS
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
	comps, by := parse(in)

	t0 := time.Now()
	p1, p2 := solve(comps, by)
	ans := strconv.Itoa(p1)
	if *part == 2 {
		ans = strconv.Itoa(p2)
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
	fmt.Fprintf(os.Stderr, "[go-fancy] day=24 part=%d runtime_ms=%.3f\n", *part, ms)
}
