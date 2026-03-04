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

const expectedSHA = "860cd63e00136c29310e25db6f4f1573a2b2574598dc72f44a6308ddf5a967c3"
const expectedPart1 = "21037"
const expectedPart2 = "9495"

func resolveInput(provided string) string {
    if provided != "" { return provided }
    cands := []string{"advent2017/Day9/d9_input.txt", "Day9/d9_input.txt", "../Day9/d9_input.txt", "../../Day9/d9_input.txt"}
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

func scanStream(raw string) (int, int) {
    s := strings.TrimSpace(raw)
    depth := 0
    score := 0
    garbage := 0
    inGarbage := false

    for i := 0; i < len(s); i++ {
        c := s[i]
        if inGarbage {
            if c == '!' {
                i++
                continue
            }
            if c == '>' {
                inGarbage = false
            } else {
                garbage++
            }
            continue
        }

        if c == '<' {
            inGarbage = true
        } else if c == '{' {
            depth++
            score += depth
        } else if c == '}' {
            depth--
        }
    }

    return score, garbage
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
    p1, p2 := scanStream(string(raw))
    ans := strconv.Itoa(p1)
    if *part == 2 { ans = strconv.Itoa(p2) }
    expected := expectedPart1
    if *part == 2 { expected = expectedPart2 }
    if ans != expected { panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected)) }

    fmt.Println(ans)
    ms := float64(time.Since(t0).Nanoseconds()) / 1e6
    fmt.Fprintf(os.Stderr, "[go-fancy] day=9 part=%d runtime_ms=%.3f\n", *part, ms)
}
