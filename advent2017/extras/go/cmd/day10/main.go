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

const expectedSHA = "b83c8a7c9fb42d39b4545428717df7858882f3644a62d2770c235c9eb61ace69"
const expectedPart1 = "54675"
const expectedPart2 = "a7af2706aa9a09cf5d848c1e6605dd2a"

var suffix = []int{17, 31, 73, 47, 23}

func resolveInput(provided string) string {
    if provided != "" {
        return provided
    }
    cands := []string{"advent2017/Day10/d10_input.txt", "Day10/d10_input.txt", "../Day10/d10_input.txt", "../../Day10/d10_input.txt"}
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

func reverseSegment(a []int, start int, length int) {
    n := len(a)
    for i := 0; i < length/2; i++ {
        x := (start + i) % n
        y := (start + length - 1 - i) % n
        a[x], a[y] = a[y], a[x]
    }
}

func runRound(a []int, lengths []int, pos int, skip int) (int, int) {
    n := len(a)
    for _, length := range lengths {
        reverseSegment(a, pos, length)
        pos = (pos + length + skip) % n
        skip++
    }
    return pos, skip
}

func solvePart1(raw string) int {
    parts := strings.Split(strings.TrimSpace(raw), ",")
    lengths := make([]int, 0, len(parts))
    for _, p := range parts {
        p = strings.TrimSpace(p)
        if p == "" {
            continue
        }
        v, err := strconv.Atoi(p)
        if err != nil {
            panic(err)
        }
        lengths = append(lengths, v)
    }

    ring := make([]int, 256)
    for i := range ring {
        ring[i] = i
    }
    runRound(ring, lengths, 0, 0)
    return ring[0] * ring[1]
}

func solvePart2(raw string) string {
    s := strings.TrimSpace(raw)
    lengths := make([]int, 0, len(s)+len(suffix))
    for _, b := range []byte(s) {
        lengths = append(lengths, int(b))
    }
    lengths = append(lengths, suffix...)

    ring := make([]int, 256)
    for i := range ring {
        ring[i] = i
    }

    pos, skip := 0, 0
    for i := 0; i < 64; i++ {
        pos, skip = runRound(ring, lengths, pos, skip)
    }

    dense := make([]byte, 16)
    for block := 0; block < 16; block++ {
        x := 0
        for i := 0; i < 16; i++ {
            x ^= ring[block*16+i]
        }
        dense[block] = byte(x)
    }
    return hex.EncodeToString(dense)
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
    ans := strconv.Itoa(solvePart1(string(raw)))
    if *part == 2 {
        ans = solvePart2(string(raw))
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
    fmt.Fprintf(os.Stderr, "[go-fancy] day=10 part=%d runtime_ms=%.3f\n", *part, ms)
}
