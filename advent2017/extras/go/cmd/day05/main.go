// Architecture Notes:
// - This file is heavily commented for long-term maintainability and reconstruction.
// - Pipeline shape is parse -> model -> compute -> emit.
// - Performance-sensitive sections document data-layout and concurrency tradeoffs.

package main

import (
    "bufio"
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

const expectedSHA = "e9c74e01657b99ad1be3cedce52f75bb0e2ac9dfb2efca8714f5f2e0910befa6"
const expectedPart1 = "394829"
const expectedPart2 = "31150702"

func resolveInput(provided string) string {
    if provided != "" {
        return provided
    }
    cands := []string{"advent2017/Day5/d5_input.txt", "Day5/d5_input.txt", "../Day5/d5_input.txt", "../../Day5/d5_input.txt"}
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

func parseOffsets(raw string) []int {
    scanner := bufio.NewScanner(strings.NewReader(raw))
    out := make([]int, 0, 2048)
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" {
            continue
        }
        v, err := strconv.Atoi(line)
        if err != nil {
            panic(err)
        }
        out = append(out, v)
    }
    if err := scanner.Err(); err != nil {
        panic(err)
    }
    return out
}

func runProgram(offsets []int, part int) int {
    a := append([]int(nil), offsets...)
    i := 0
    steps := 0
    for i >= 0 && i < len(a) {
        jump := a[i]
        if part == 1 {
            a[i]++
        } else {
            if jump >= 3 {
                a[i]--
            } else {
                a[i]++
            }
        }
        i += jump
        steps++
    }
    return steps
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
    offsets := parseOffsets(string(raw))

    t0 := time.Now()
    ans := strconv.Itoa(runProgram(offsets, *part))
    expected := expectedPart1
    if *part == 2 {
        expected = expectedPart2
    }
    if ans != expected {
        panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected))
    }

    fmt.Println(ans)
    ms := float64(time.Since(t0).Nanoseconds()) / 1e6
    fmt.Fprintf(os.Stderr, "[go-fancy] day=5 part=%d runtime_ms=%.3f\n", *part, ms)
}
