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

const expectedSHA = "b4231dede8cc9f00c1dcdf6fe60b2c5cc33278020531f4a05af462099063171a"
const expectedPart1 = "DTOUFARJQ"
const expectedPart2 = "16642"

func resolveInput(provided string) string {
    if provided != "" { return provided }
    cands := []string{"advent2017/Day19/d19_input.txt", "Day19/d19_input.txt", "../Day19/d19_input.txt", "../../Day19/d19_input.txt"}
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

func parseGrid(raw string) [][]byte {
    lines := strings.Split(strings.TrimRight(raw, "\n"), "\n")
    w := 0
    for _, l := range lines { if len(l) > w { w = len(l) } }
    g := make([][]byte, len(lines))
    for i, l := range lines {
        row := make([]byte, w)
        copy(row, []byte(l))
        for j := len(l); j < w; j++ { row[j] = ' ' }
        g[i] = row
    }
    return g
}

func at(g [][]byte, r int, c int) byte {
    if r < 0 || r >= len(g) || c < 0 || c >= len(g[0]) { return ' ' }
    return g[r][c]
}

func solve(raw string) (string, int) {
    g := parseGrid(raw)
    r, c := 0, strings.IndexByte(string(g[0]), '|')
    dr, dc := 1, 0
    letters := make([]byte, 0, 16)
    steps := 0

    for {
        ch := at(g, r, c)
        if ch == ' ' { break }
        if ch >= 'A' && ch <= 'Z' {
            letters = append(letters, ch)
        } else if ch == '+' {
            if dr != 0 {
                if at(g, r, c-1) != ' ' { dr, dc = 0, -1 } else if at(g, r, c+1) != ' ' { dr, dc = 0, 1 }
            } else {
                if at(g, r-1, c) != ' ' { dr, dc = -1, 0 } else if at(g, r+1, c) != ' ' { dr, dc = 1, 0 }
            }
        }
        r += dr
        c += dc
        steps++
    }

    return string(letters), steps
}

func main() {
    part := flag.Int("part", 0, "part")
    input := flag.String("input", "", "input")
    flag.Parse()
    if *part != 1 && *part != 2 { panic("--part 1|2 required") }

    in := resolveInput(*input)
    if sha256File(in) != expectedSHA { panic("checksum mismatch") }
    p1, p2 := solve(string(must(os.ReadFile(in))))

    t0 := time.Now()
    ans := p1
    if *part == 2 { ans = strconv.Itoa(p2) }
    runtime := float64(time.Since(t0).Nanoseconds()) / 1e6

    expected := expectedPart1
    if *part == 2 { expected = expectedPart2 }
    if ans != expected { panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected)) }

    fmt.Println(ans)
    fmt.Fprintf(os.Stderr, "[go-fancy] day=19 part=%d runtime_ms=%.3f\n", *part, runtime)
}

func must[T any](v T, err error) T { if err != nil { panic(err) }; return v }
