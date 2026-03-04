package main

import (
	"crypto/sha256"
	"encoding/hex"
	"flag"
	"fmt"
	"math"
	"os"
	"regexp"
	"sort"
	"strconv"
	"time"
)

const expectedSHA = "9480ad6f4d423780a0542e172e614170ec28d3eb06c80b7c2b452c6ceeecbfb0"
const expectedP1 = "144"
const expectedP2 = "477"

type Vec3 struct{ X, Y, Z int64 }
type Particle struct{ P, V, A Vec3 }
type Pair struct{ I, J int }

var lineRe = regexp.MustCompile(`p=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>, v=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>, a=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>`)

func abs64(v int64) int64 {
	if v < 0 {
		return -v
	}
	return v
}

func manhattan(v Vec3) int64 { return abs64(v.X) + abs64(v.Y) + abs64(v.Z) }

func resolveInput(provided string) string {
	if provided != "" {
		return provided
	}
	cands := []string{
		"advent2017/Day20/d20_input.txt",
		"Day20/d20_input.txt",
		"../Day20/d20_input.txt",
		"../../Day20/d20_input.txt",
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

func parse(path string) []Particle {
	b, err := os.ReadFile(path)
	if err != nil {
		panic(err)
	}
	out := make([]Particle, 0, 1024)
	for _, ln := range regexp.MustCompile(`\r?\n`).Split(string(b), -1) {
		if ln == "" {
			continue
		}
		m := lineRe.FindStringSubmatch(ln)
		if m == nil {
			panic("bad line: " + ln)
		}
		num := make([]int64, 9)
		for i := 0; i < 9; i++ {
			v, e := strconv.ParseInt(m[i+1], 10, 64)
			if e != nil {
				panic(e)
			}
			num[i] = v
		}
		out = append(out, Particle{
			P: Vec3{num[0], num[1], num[2]},
			V: Vec3{num[3], num[4], num[5]},
			A: Vec3{num[6], num[7], num[8]},
		})
	}
	return out
}

func solvePart1(ps []Particle) int {
	bestI := -1
	var ba, bv, bp int64
	for i, p := range ps {
		a := manhattan(p.A)
		v := manhattan(p.V)
		pp := manhattan(p.P)
		if bestI == -1 || a < ba || (a == ba && (v < bv || (v == bv && (pp < bp || (pp == bp && i < bestI))))) {
			bestI = i
			ba, bv, bp = a, v, pp
		}
	}
	return bestI
}

func solveAxis(dp, dv, da int64) (bool, map[int64]struct{}) {
	ts := map[int64]struct{}{}
	if da == 0 && dv == 0 {
		return dp == 0, ts
	}
	if da == 0 {
		if dv != 0 && (-dp)%dv == 0 {
			t := (-dp) / dv
			if t >= 0 {
				ts[t] = struct{}{}
			}
		}
		return false, ts
	}
	b := da + 2*dv
	c := 2 * dp
	disc := b*b - 4*da*c
	if disc < 0 {
		return false, ts
	}
	s := int64(math.Sqrt(float64(disc)))
	for s*s < disc {
		s++
	}
	for s*s > disc {
		s--
	}
	if s*s != disc {
		return false, ts
	}
	den := 2 * da
	nums := []int64{-b + s, -b - s}
	for _, num := range nums {
		if den != 0 && num%den == 0 {
			t := num / den
			if t >= 0 {
				ts[t] = struct{}{}
			}
		}
	}
	return false, ts
}

func intersect(a, b map[int64]struct{}) map[int64]struct{} {
	out := map[int64]struct{}{}
	for k := range a {
		if _, ok := b[k]; ok {
			out[k] = struct{}{}
		}
	}
	return out
}

func pairTimes(p1, p2 Particle) map[int64]struct{} {
	anyX, sx := solveAxis(p1.P.X-p2.P.X, p1.V.X-p2.V.X, p1.A.X-p2.A.X)
	anyY, sy := solveAxis(p1.P.Y-p2.P.Y, p1.V.Y-p2.V.Y, p1.A.Y-p2.A.Y)
	anyZ, sz := solveAxis(p1.P.Z-p2.P.Z, p1.V.Z-p2.V.Z, p1.A.Z-p2.A.Z)

	concrete := make([]map[int64]struct{}, 0, 3)
	if !anyX {
		concrete = append(concrete, sx)
	}
	if !anyY {
		concrete = append(concrete, sy)
	}
	if !anyZ {
		concrete = append(concrete, sz)
	}
	if len(concrete) == 0 {
		return map[int64]struct{}{}
	}
	cur := concrete[0]
	for i := 1; i < len(concrete); i++ {
		cur = intersect(cur, concrete[i])
		if len(cur) == 0 {
			break
		}
	}
	return cur
}

func posAt(p Particle, t int64) Vec3 {
	return Vec3{
		X: p.P.X + p.V.X*t + p.A.X*t*(t+1)/2,
		Y: p.P.Y + p.V.Y*t + p.A.Y*t*(t+1)/2,
		Z: p.P.Z + p.V.Z*t + p.A.Z*t*(t+1)/2,
	}
}

func solvePart2(ps []Particle) int {
	events := map[int64][]Pair{}
	n := len(ps)
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			for t := range pairTimes(ps[i], ps[j]) {
				events[t] = append(events[t], Pair{i, j})
			}
		}
	}
	times := make([]int64, 0, len(events))
	for t := range events {
		times = append(times, t)
	}
	sort.Slice(times, func(i, j int) bool { return times[i] < times[j] })

	alive := make([]bool, n)
	for i := 0; i < n; i++ {
		alive[i] = true
	}
	left := n

	for _, t := range times {
		involved := map[int]struct{}{}
		for _, pr := range events[t] {
			if alive[pr.I] && alive[pr.J] {
				involved[pr.I] = struct{}{}
				involved[pr.J] = struct{}{}
			}
		}
		if len(involved) < 2 {
			continue
		}
		groups := map[Vec3][]int{}
		for i := range involved {
			pos := posAt(ps[i], t)
			groups[pos] = append(groups[pos], i)
		}
		for _, ids := range groups {
			if len(ids) > 1 {
				for _, i := range ids {
					if alive[i] {
						alive[i] = false
						left--
					}
				}
			}
		}
	}
	return left
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
	ps := parse(in)

	t0 := time.Now()
	var ans string
	if *part == 1 {
		ans = strconv.Itoa(solvePart1(ps))
	} else {
		ans = strconv.Itoa(solvePart2(ps))
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
	fmt.Fprintf(os.Stderr, "[go-fancy] day=20 part=%d runtime_ms=%.3f\n", *part, ms)
}
