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

const expectedSHA = "a2888c695f7f2c036f5d9568befc839a3b64c703d054f82162cfbc5e105627dd"
const expectedPart1 = "5143"
const expectedPart2 = "6209"

func resolveInput(provided string) string {
    if provided != "" { return provided }
    cands := []string{"advent2017/Day8/d8_input.txt", "Day8/d8_input.txt", "../Day8/d8_input.txt", "../../Day8/d8_input.txt"}
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

func check(a int, op string, b int) bool {
    switch op {
    case "<": return a < b
    case "<=": return a <= b
    case ">": return a > b
    case ">=": return a >= b
    case "==": return a == b
    case "!=": return a != b
    default: panic("bad op")
    }
}

func runProgram(raw string) (int, int) {
    reg := map[string]int{}
    best := 0

    scanner := bufio.NewScanner(strings.NewReader(raw))
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" { continue }
        f := strings.Fields(line)
        r, op, vS, cr, cmp, cvS := f[0], f[1], f[2], f[4], f[5], f[6]
        v, _ := strconv.Atoi(vS)
        cv, _ := strconv.Atoi(cvS)

        if check(reg[cr], cmp, cv) {
            if op == "inc" { reg[r] += v } else { reg[r] -= v }
            if reg[r] > best { best = reg[r] }
        }
    }
    if err := scanner.Err(); err != nil { panic(err) }

    maxv := 0
    first := true
    for _, v := range reg {
        if first || v > maxv { maxv = v; first = false }
    }
    return maxv, best
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

    t0 := time.Now()
    p1, p2 := runProgram(string(raw))
    ans := strconv.Itoa(p1)
    if *part == 2 { ans = strconv.Itoa(p2) }
    expected := expectedPart1
    if *part == 2 { expected = expectedPart2 }
    if ans != expected { panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected)) }

    fmt.Println(ans)
    ms := float64(time.Since(t0).Nanoseconds()) / 1e6
    fmt.Fprintf(os.Stderr, "[go-fancy] day=8 part=%d runtime_ms=%.3f\n", *part, ms)
}
