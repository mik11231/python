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

const expectedSHA = "489246369534515a9df814e8824f41c427d6c02ab31d7b5c07cbdc935497f2ba"
const expectedPart1 = "12841"
const expectedPart2 = "8038"

func resolveInput(provided string) string {
    if provided != "" {
        return provided
    }
    cands := []string{"advent2017/Day6/d6_input.txt", "Day6/d6_input.txt", "../Day6/d6_input.txt", "../../Day6/d6_input.txt"}
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

func parseBanks(raw string) []int {
    fields := strings.Fields(raw)
    out := make([]int, 0, len(fields))
    for _, f := range fields {
        v, err := strconv.Atoi(f)
        if err != nil {
            panic(err)
        }
        out = append(out, v)
    }
    return out
}

func stateKey(a []int) string {
    var b strings.Builder
    for i, v := range a {
        if i > 0 {
            b.WriteByte(',')
        }
        b.WriteString(strconv.Itoa(v))
    }
    return b.String()
}

func redistribute(a []int) {
    idx := 0
    for i := 1; i < len(a); i++ {
        if a[i] > a[idx] {
            idx = i
        }
    }
    blocks := a[idx]
    a[idx] = 0
    n := len(a)
    q, r := blocks/n, blocks%n
    if q > 0 {
        for i := range a {
            a[i] += q
        }
    }
    for k := 1; k <= r; k++ {
        a[(idx+k)%n]++
    }
}

func solvePart1(banks []int) int {
    a := append([]int(nil), banks...)
    seen := map[string]struct{}{}
    steps := 0
    for {
        key := stateKey(a)
        if _, ok := seen[key]; ok {
            return steps
        }
        seen[key] = struct{}{}
        redistribute(a)
        steps++
    }
}

func solvePart2(banks []int) int {
    a := append([]int(nil), banks...)
    seen := map[string]int{}
    steps := 0
    for {
        key := stateKey(a)
        if prev, ok := seen[key]; ok {
            return steps - prev
        }
        seen[key] = steps
        redistribute(a)
        steps++
    }
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
    banks := parseBanks(string(raw))

    t0 := time.Now()
    var ans string
    if *part == 1 {
        ans = strconv.Itoa(solvePart1(banks))
    } else {
        ans = strconv.Itoa(solvePart2(banks))
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
    fmt.Fprintf(os.Stderr, "[go-fancy] day=6 part=%d runtime_ms=%.3f\n", *part, ms)
}
