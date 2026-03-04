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
	"sort"
	"strconv"
	"strings"
	"time"
)

const expectedSHA = "759a25acf919be68478e4d20d3856f488ff79325d0954d8ca5c89cecc2fd8287"
const expectedP1 = "139"
const expectedP2 = "1857134"

func resolveInput(provided string) string {
	if provided != "" {
		return provided
	}
	cands := []string{
		"advent2017/Day21/d21_input.txt",
		"Day21/d21_input.txt",
		"../Day21/d21_input.txt",
		"../../Day21/d21_input.txt",
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

func rotate(p []string) []string {
	n := len(p)
	out := make([]string, n)
	for c := 0; c < n; c++ {
		row := make([]byte, n)
		for r := 0; r < n; r++ {
			row[r] = p[n-1-r][c]
		}
		out[c] = string(row)
	}
	return out
}

func flip(p []string) []string {
	out := make([]string, len(p))
	for i, row := range p {
		b := []byte(row)
		for l, r := 0, len(b)-1; l < r; l, r = l+1, r-1 {
			b[l], b[r] = b[r], b[l]
		}
		out[i] = string(b)
	}
	return out
}

func canonical(p []string) string {
	cur := append([]string(nil), p...)
	var vars []string
	for i := 0; i < 4; i++ {
		vars = append(vars, strings.Join(cur, "/"))
		vars = append(vars, strings.Join(flip(cur), "/"))
		cur = rotate(cur)
	}
	sort.Strings(vars)
	return vars[0]
}

func parseRules(path string) map[string][]string {
	b, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	rules := make(map[string][]string, 1<<9)
	for _, ln := range regexp.MustCompile(`\r?\n`).Split(string(b), -1) {
		s := strings.TrimSpace(ln)
		if s == "" {
			continue
		}
		parts := strings.Split(s, " => ")
		inp := strings.Split(parts[0], "/")
		out := strings.Split(parts[1], "/")
		rules[canonical(inp)] = out
	}
	return rules
}

func enhance(grid []string, rules map[string][]string) []string {
	n := len(grid)
	bs := 3
	if n%2 == 0 {
		bs = 2
	}
	osz := bs + 1
	cnt := n / bs
	newN := cnt * osz
	out := make([][]byte, newN)
	for i := range out {
		out[i] = make([]byte, newN)
		for j := range out[i] {
			out[i][j] = '.'
		}
	}
	for br := 0; br < cnt; br++ {
		for bc := 0; bc < cnt; bc++ {
			sub := make([]string, bs)
			for r := 0; r < bs; r++ {
				sub[r] = grid[br*bs+r][bc*bs : bc*bs+bs]
			}
			rep := rules[canonical(sub)]
			for r := 0; r < osz; r++ {
				for c := 0; c < osz; c++ {
					out[br*osz+r][bc*osz+c] = rep[r][c]
				}
			}
		}
	}
	ans := make([]string, newN)
	for i := range out {
		ans[i] = string(out[i])
	}
	return ans
}

func runIterative(rules map[string][]string, iters int) int {
	grid := []string{".#.", "..#", "###"}
	for i := 0; i < iters; i++ {
		grid = enhance(grid, rules)
	}
	sum := 0
	for _, row := range grid {
		for i := 0; i < len(row); i++ {
			if row[i] == '#' {
				sum++
			}
		}
	}
	return sum
}

func splitBlocks(grid []string, bs int) []string {
	n := len(grid)
	cnt := n / bs
	out := make([]string, 0, cnt*cnt)
	for br := 0; br < cnt; br++ {
		for bc := 0; bc < cnt; bc++ {
			sub := make([]string, bs)
			for r := 0; r < bs; r++ {
				sub[r] = grid[br*bs+r][bc*bs : bc*bs+bs]
			}
			out = append(out, strings.Join(sub, "/"))
		}
	}
	return out
}

func popcountKey(k string) int {
	n := 0
	for i := 0; i < len(k); i++ {
		if k[i] == '#' {
			n++
		}
	}
	return n
}

func runOptimized(rules map[string][]string, iters int) int {
	if iters <= 5 || iters%3 != 0 {
		return runIterative(rules, iters)
	}
	memoExpand := map[string][]string{}
	var expandThreeFrom3 func(string) []string
	expandThreeFrom3 = func(k string) []string {
		if v, ok := memoExpand[k]; ok {
			return v
		}
		g := strings.Split(k, "/")
		g = enhance(g, rules)
		g = enhance(g, rules)
		g = enhance(g, rules)
		v := splitBlocks(g, 3)
		memoExpand[k] = v
		return v
	}

	memoCount := map[string]int{}
	var countCycles func(string, int) int
	countCycles = func(k string, cycles int) int {
		mk := strconv.Itoa(cycles) + "|" + k
		if v, ok := memoCount[mk]; ok {
			return v
		}
		if cycles == 0 {
			v := popcountKey(k)
			memoCount[mk] = v
			return v
		}
		sum := 0
		for _, sub := range expandThreeFrom3(k) {
			sum += countCycles(sub, cycles-1)
		}
		memoCount[mk] = sum
		return sum
	}
	return countCycles(".#./..#/###", iters/3)
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
	rules := parseRules(in)

	t0 := time.Now()
	ans := 0
	if *part == 1 {
		ans = runOptimized(rules, 5)
	} else {
		ans = runOptimized(rules, 18)
	}
	ansS := fmt.Sprintf("%d", ans)
	exp := expectedP1
	if *part == 2 {
		exp = expectedP2
	}
	if ansS != exp {
		panic(fmt.Sprintf("answer mismatch: got %s expected %s", ansS, exp))
	}
	fmt.Println(ansS)
	ms := float64(time.Since(t0).Nanoseconds()) / 1e6
	fmt.Fprintf(os.Stderr, "[go-fancy] day=21 part=%d runtime_ms=%.3f\n", *part, ms)
}
