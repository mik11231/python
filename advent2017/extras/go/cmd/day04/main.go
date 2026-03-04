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
    "sort"
    "strconv"
    "strings"
    "time"
)

const expectedSHA = "36d753e40c996a2ec1083c34b8cda3ffa986bc63a44d73be5ee1ed81084c6401"
const expectedPart1 = "451"
const expectedPart2 = "223"

func resolveInput(provided string) string {
    if provided != "" { return provided }
    cands := []string{"advent2017/Day4/d4_input.txt", "Day4/d4_input.txt", "../Day4/d4_input.txt", "../../Day4/d4_input.txt"}
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
    f, err := os.Open(path); if err != nil { panic(err) }
    defer f.Close()
    h := sha256.New()
    if _, err := io.Copy(h, f); err != nil { panic(err) }
    return hex.EncodeToString(h.Sum(nil))
}

func parseLines(raw string) [][]string {
    scanner := bufio.NewScanner(strings.NewReader(raw))
    out := make([][]string, 0, 512)
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" { continue }
        out = append(out, strings.Fields(line))
    }
    if err := scanner.Err(); err != nil { panic(err) }
    return out
}

func canonicalWord(w string) string {
    r := []rune(w)
    sort.Slice(r, func(i, j int) bool { return r[i] < r[j] })
    return string(r)
}

func solvePart1(lines [][]string) int {
    valid := 0
    for _, words := range lines {
        seen := make(map[string]struct{}, len(words))
        ok := true
        for _, w := range words {
            if _, exists := seen[w]; exists { ok = false; break }
            seen[w] = struct{}{}
        }
        if ok { valid++ }
    }
    return valid
}

func solvePart2(lines [][]string) int {
    valid := 0
    for _, words := range lines {
        seen := make(map[string]struct{}, len(words))
        ok := true
        for _, w := range words {
            c := canonicalWord(w)
            if _, exists := seen[c]; exists { ok = false; break }
            seen[c] = struct{}{}
        }
        if ok { valid++ }
    }
    return valid
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
    lines := parseLines(string(raw))

    t0 := time.Now()
    var ans, expected string
    if *part == 1 { ans = strconv.Itoa(solvePart1(lines)); expected = expectedPart1 }
    if *part == 2 { ans = strconv.Itoa(solvePart2(lines)); expected = expectedPart2 }
    if ans != expected { panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected)) }

    fmt.Println(ans)
    ms := float64(time.Since(t0).Nanoseconds()) / 1e6
    fmt.Fprintf(os.Stderr, "[go-fancy] day=4 part=%d runtime_ms=%.3f\n", *part, ms)
}
