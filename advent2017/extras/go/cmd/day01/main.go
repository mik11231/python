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
    "strings"
    "time"
)

const expectedSHA = "ffefe22d570c7077ac45df89cd8a40c99990e1903f6e68a501d75e53038c80ef"
const expectedPart1 = "1158"
const expectedPart2 = "1132"

func resolveInput(provided string) string {
    if provided != "" {
        return provided
    }
    cands := []string{
        "advent2017/Day1/d1_input.txt",
        "Day1/d1_input.txt",
        "../Day1/d1_input.txt",
        "../../Day1/d1_input.txt",
    }
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

func solveWithStep(raw string, step int) int {
    s := strings.TrimSpace(raw)
    if len(s) == 0 {
        return 0
    }
    total := 0
    n := len(s)
    for i := 0; i < n; i++ {
        j := (i + step) % n
        if s[i] == s[j] {
            total += int(s[i] - '0')
        }
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
    if sha256File(in) != expectedSHA {
        panic("checksum mismatch")
    }
    b, err := os.ReadFile(in)
    if err != nil {
        panic(err)
    }

    t0 := time.Now()
    var ans string
    var expected string
    if *part == 1 {
        ans = fmt.Sprintf("%d", solveWithStep(string(b), 1))
        expected = expectedPart1
    } else {
        s := strings.TrimSpace(string(b))
        ans = fmt.Sprintf("%d", solveWithStep(s, len(s)/2))
        expected = expectedPart2
    }
    if ans != expected {
        panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected))
    }

    fmt.Println(ans)
    ms := float64(time.Since(t0).Nanoseconds()) / 1e6
    fmt.Fprintf(os.Stderr, "[go-fancy] day=1 part=%d runtime_ms=%.3f\n", *part, ms)
}
