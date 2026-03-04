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

const expectedSHA = "09a2c42b5b2f5e7e0c325a89194f42c2a9f88efb35cd6dcf61a69005545cc3d1"
const expectedPart1 = "685"
const expectedPart2 = "1457"

func resolveInput(provided string) string {
    if provided != "" {
        return provided
    }
    cands := []string{"advent2017/Day11/d11_input.txt", "Day11/d11_input.txt", "../Day11/d11_input.txt", "../../Day11/d11_input.txt"}
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

func abs(v int) int {
    if v < 0 {
        return -v
    }
    return v
}

func cubeDistance(x int, y int, z int) int {
    d := abs(x)
    if abs(y) > d {
        d = abs(y)
    }
    if abs(z) > d {
        d = abs(z)
    }
    return d
}

func solve(raw string) (int, int) {
    x, y, z := 0, 0, 0
    best := 0

    for _, step0 := range strings.Split(strings.TrimSpace(raw), ",") {
        step := strings.TrimSpace(step0)
        if step == "" {
            continue
        }
        switch step {
        case "n":
            y++
            z--
        case "ne":
            x++
            z--
        case "se":
            x++
            y--
        case "s":
            y--
            z++
        case "sw":
            x--
            z++
        case "nw":
            x--
            y++
        default:
            panic("bad step")
        }
        d := cubeDistance(x, y, z)
        if d > best {
            best = d
        }
    }

    return cubeDistance(x, y, z), best
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
    raw, err := os.ReadFile(in)
    if err != nil {
        panic(err)
    }

    t0 := time.Now()
    p1, p2 := solve(string(raw))
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
    fmt.Fprintf(os.Stderr, "[go-fancy] day=11 part=%d runtime_ms=%.3f\n", *part, ms)
}
