package main

import (
	"crypto/sha256"
	"encoding/hex"
	"flag"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

const expectedSHA = "29581d7567b692271626cc1b3e1448f3456036af5d0bb1e0714fbaf2cf7bc878"
const expectedP1 = "5246"
const expectedP2 = "2512059"

func packPos(r, c int) uint64 {
	return (uint64(uint32(r)) << 32) | uint64(uint32(c))
}

func resolveInput(provided string) string {
	if provided != "" {
		return provided
	}
	cands := []string{
		"advent2017/Day22/d22_input.txt",
		"Day22/d22_input.txt",
		"../Day22/d22_input.txt",
		"../../Day22/d22_input.txt",
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

func parse(path string) map[uint64]struct{} {
	b, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	lines := make([]string, 0, 64)
	for _, ln := range strings.Split(string(b), "\n") {
		s := strings.TrimSpace(strings.TrimSuffix(ln, "\r"))
		if s != "" {
			lines = append(lines, s)
		}
	}
	n := len(lines)
	off := n / 2
	inf := make(map[uint64]struct{}, n*n/3)
	for r, row := range lines {
		for c := 0; c < len(row); c++ {
			if row[c] == '#' {
				inf[packPos(r-off, c-off)] = struct{}{}
			}
		}
	}
	return inf
}

func solvePart1(inf0 map[uint64]struct{}) int {
	inf := make(map[uint64]struct{}, len(inf0)*4+256)
	for p := range inf0 {
		inf[p] = struct{}{}
	}
	r, c := 0, 0
	d := 0
	dr := [4]int{-1, 0, 1, 0}
	dc := [4]int{0, 1, 0, -1}
	made := 0
	for i := 0; i < 10000; i++ {
		p := packPos(r, c)
		if _, ok := inf[p]; ok {
			d = (d + 1) & 3
			delete(inf, p)
		} else {
			d = (d + 3) & 3
			inf[p] = struct{}{}
			made++
		}
		r += dr[d]
		c += dc[d]
	}
	return made
}

func solvePart2(inf0 map[uint64]struct{}) int {
	// 0 clean, 1 weakened, 2 infected, 3 flagged
	state := make(map[uint64]uint8, 1<<20)
	for p := range inf0 {
		state[p] = 2
	}
	r, c := 0, 0
	d := 0
	dr := [4]int{-1, 0, 1, 0}
	dc := [4]int{0, 1, 0, -1}
	made := 0
	for i := 0; i < 10000000; i++ {
		p := packPos(r, c)
		s := state[p]
		switch s {
		case 0:
			d = (d + 3) & 3
			state[p] = 1
		case 1:
			state[p] = 2
			made++
		case 2:
			d = (d + 1) & 3
			state[p] = 3
		default:
			d = (d + 2) & 3
			delete(state, p)
		}
		r += dr[d]
		c += dc[d]
	}
	return made
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
	inf := parse(in)

	t0 := time.Now()
	ans := ""
	if *part == 1 {
		ans = strconv.Itoa(solvePart1(inf))
	} else {
		ans = strconv.Itoa(solvePart2(inf))
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
	fmt.Fprintf(os.Stderr, "[go-fancy] day=22 part=%d runtime_ms=%.3f\n", *part, ms)
}
