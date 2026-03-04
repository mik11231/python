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
	"math/bits"
	"os"
	"strconv"
	"strings"
	"time"
)

const expectedSHA = "6419303e9eeb435a39b6e7d17236cb0d3fdfc9b0c2e5d5da8a9864b527c7e873"
const expectedP1 = "3145"
const expectedP2 = "Merry Christmas"

type Rule struct {
	Write int
	Move  int
	Next  byte
}

func chunkAndBit(pos int) (int, uint) {
	chunk := pos / 64
	rem := pos % 64
	if rem < 0 {
		rem += 64
		chunk--
	}
	return chunk, uint(rem)
}

func resolveInput(provided string) string {
	if provided != "" {
		return provided
	}
	cands := []string{
		"advent2017/Day25/d25_input.txt",
		"Day25/d25_input.txt",
		"../Day25/d25_input.txt",
		"../../Day25/d25_input.txt",
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

func solvePart1(text string) int {
	lines := make([]string, 0, 128)
	for _, ln := range strings.Split(text, "\n") {
		s := strings.TrimSpace(strings.TrimSuffix(ln, "\r"))
		if s != "" {
			lines = append(lines, s)
		}
	}
	start := lines[0][len("Begin in state ")]
	stepsField := strings.Fields(lines[1])[5]
	steps, err := strconv.Atoi(stepsField)
	if err != nil {
		panic(err)
	}

	var trans [26][2]Rule
	for i := 2; i < len(lines); i += 9 {
		st := lines[i][len("In state ")] - 'A'
		w0 := int(lines[i+2][len("- Write the value ")])
		w1 := int(lines[i+6][len("- Write the value ")])
		mv0 := -1
		mv1 := -1
		if lines[i+3][len("- Move one slot to the ")] == 'r' {
			mv0 = 1
		}
		if lines[i+7][len("- Move one slot to the ")] == 'r' {
			mv1 = 1
		}
		n0 := lines[i+4][len("- Continue with state ")]
		n1 := lines[i+8][len("- Continue with state ")]
		trans[st][0] = Rule{w0 - '0', mv0, n0}
		trans[st][1] = Rule{w1 - '0', mv1, n1}
	}

	tape := make(map[int]uint64, steps/1024+16)
	cur := 0
	state := start
	for i := 0; i < steps; i++ {
		chunk, bit := chunkAndBit(cur)
		word := tape[chunk]
		mask := uint64(1) << bit
		v := 0
		if word&mask != 0 {
			v = 1
		}
		r := trans[state-'A'][v]
		if r.Write == 1 {
			tape[chunk] = word | mask
		} else {
			nw := word &^ mask
			if nw == 0 {
				delete(tape, chunk)
			} else {
				tape[chunk] = nw
			}
		}
		cur += r.Move
		state = r.Next
	}
	total := 0
	for _, w := range tape {
		total += bits.OnesCount64(w)
	}
	return total
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
	textB, err := os.ReadFile(in)
	if err != nil {
		panic(err)
	}
	text := string(textB)

	t0 := time.Now()
	ans := ""
	if *part == 1 {
		ans = fmt.Sprintf("%d", solvePart1(text))
	} else {
		ans = expectedP2
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
	fmt.Fprintf(os.Stderr, "[go-fancy] day=25 part=%d runtime_ms=%.3f\n", *part, ms)
}
