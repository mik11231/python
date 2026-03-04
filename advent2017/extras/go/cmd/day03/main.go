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
    "os"
    "path/filepath"
    "strconv"
    "strings"
    "time"
)

const expectedSHA = "697301449f3f32ff9e73436c0ee11191f61f63d01afda5637bf644c5aa6042bc"
const expectedPart1 = "371"
const expectedPart2 = "369601"

type pt struct{ x, y int }

func resolveInput(provided string) string {
    if provided != "" {
        return provided
    }
    cands := []string{"advent2017/Day3/d3_input.txt", "Day3/d3_input.txt", "../Day3/d3_input.txt", "../../Day3/d3_input.txt"}
    for _, c := range cands {
        if _, err := os.Stat(c); err == nil {
            abs, err := filepath.Abs(c)
            if err == nil { return abs }
            return c
        }
    }
    panic("input not found")
}

func sha256File(path string) string {
    f, err := os.Open(path)
    if err != nil { panic(err) }
    defer f.Close()
    h := sha256.New()
    if _, err := io.Copy(h, f); err != nil { panic(err) }
    return hex.EncodeToString(h.Sum(nil))
}

func abs(v int) int { if v < 0 { return -v }; return v }

func solvePart1(n int) int {
    if n == 1 { return 0 }
    layer := 0
    for (2*layer+1)*(2*layer+1) < n { layer++ }
    side := 2 * layer
    maxv := (2*layer + 1) * (2*layer + 1)
    best := 1 << 30
    for i := 0; i < 4; i++ {
        mid := maxv - layer - side*i
        d := abs(n - mid)
        if d < best { best = d }
    }
    return layer + best
}

func solvePart2(target int) int {
    nei := []pt{{-1,-1},{-1,0},{-1,1},{0,-1},{0,1},{1,-1},{1,0},{1,1}}
    grid := map[pt]int{{0,0}: 1}
    x, y, step := 0, 0, 1

    sumNei := func(x, y int) int {
        s := 0
        for _, d := range nei {
            s += grid[pt{x + d.x, y + d.y}]
        }
        return s
    }

    for {
        for i := 0; i < step; i++ { x++; v := sumNei(x,y); if v > target { return v }; grid[pt{x,y}] = v }
        for i := 0; i < step; i++ { y++; v := sumNei(x,y); if v > target { return v }; grid[pt{x,y}] = v }
        step++
        for i := 0; i < step; i++ { x--; v := sumNei(x,y); if v > target { return v }; grid[pt{x,y}] = v }
        for i := 0; i < step; i++ { y--; v := sumNei(x,y); if v > target { return v }; grid[pt{x,y}] = v }
        step++
    }
}

func main() {
    part := flag.Int("part", 0, "part")
    input := flag.String("input", "", "input")
    flag.Parse()
    if *part != 1 && *part != 2 { panic("--part 1|2 required") }

    in := resolveInput(*input)
    if sha256File(in) != expectedSHA { panic("checksum mismatch") }
    raw, err := os.ReadFile(in)
    if err != nil { panic(err) }
    n, err := strconv.Atoi(strings.TrimSpace(string(raw)))
    if err != nil { panic(err) }

    t0 := time.Now()
    var ans, expected string
    if *part == 1 {
        ans = strconv.Itoa(solvePart1(n)); expected = expectedPart1
    } else {
        ans = strconv.Itoa(solvePart2(n)); expected = expectedPart2
    }
    if ans != expected { panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected)) }

    fmt.Println(ans)
    ms := float64(time.Since(t0).Nanoseconds()) / 1e6
    fmt.Fprintf(os.Stderr, "[go-fancy] day=3 part=%d runtime_ms=%.3f\n", *part, ms)
}
