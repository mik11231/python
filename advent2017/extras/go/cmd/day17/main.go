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

const expectedSHA = "03a3d955b8799a90f1ff5a39479fde8e618f8ca3282d5b187186f2cf361abd32"
const expectedPart1 = "808"
const expectedPart2 = "47465686"

func resolveInput(provided string) string {
    if provided != "" { return provided }
    cands := []string{"advent2017/Day17/d17_input.txt", "Day17/d17_input.txt", "../Day17/d17_input.txt", "../../Day17/d17_input.txt"}
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

func solvePart1(step int) int {
    buf := []int{0}
    pos := 0
    for v := 1; v <= 2017; v++ {
        pos = (pos+step)%len(buf) + 1
        buf = append(buf, 0)
        copy(buf[pos+1:], buf[pos:])
        buf[pos] = v
    }
    return buf[(pos+1)%len(buf)]
}

func solvePart2(step int) int {
    pos := 0
    valAfterZero := 0
    size := 1
    for v := 1; v <= 50000000; v++ {
        pos = (pos+step)%size + 1
        if pos == 1 { valAfterZero = v }
        size++
    }
    return valAfterZero
}

func main() {
    part := flag.Int("part", 0, "part")
    input := flag.String("input", "", "input")
    flag.Parse()
    if *part != 1 && *part != 2 { panic("--part 1|2 required") }

    in := resolveInput(*input)
    if sha256File(in) != expectedSHA { panic("checksum mismatch") }
    step, err := strconv.Atoi(strings.TrimSpace(string(must(os.ReadFile(in)))))
    if err != nil { panic(err) }

    t0 := time.Now()
    ans := strconv.Itoa(solvePart1(step))
    if *part == 2 { ans = strconv.Itoa(solvePart2(step)) }
    expected := expectedPart1
    if *part == 2 { expected = expectedPart2 }
    if ans != expected { panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected)) }

    fmt.Println(ans)
    ms := float64(time.Since(t0).Nanoseconds()) / 1e6
    fmt.Fprintf(os.Stderr, "[go-fancy] day=17 part=%d runtime_ms=%.3f\n", *part, ms)
}

func must[T any](v T, err error) T { if err != nil { panic(err) }; return v }
