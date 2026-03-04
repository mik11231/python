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

const expectedSHA = "8d4f35b1950c1ca0bd04c13fe9e4a9a15065f902a86a82606973db0b9fe346f7"
const expectedPart1 = "650"
const expectedPart2 = "336"

const FA = int64(16807)
const FB = int64(48271)
const MOD = int64(2147483647)
const MASK = int64(0xFFFF)

func resolveInput(provided string) string {
    if provided != "" { return provided }
    cands := []string{"advent2017/Day15/d15_input.txt", "Day15/d15_input.txt", "../Day15/d15_input.txt", "../../Day15/d15_input.txt"}
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

func parseSeeds(raw string) (int64, int64) {
    vals := []int64{}
    scanner := bufio.NewScanner(strings.NewReader(raw))
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" { continue }
        f := strings.Fields(line)
        v, err := strconv.ParseInt(f[len(f)-1], 10, 64)
        if err != nil { panic(err) }
        vals = append(vals, v)
    }
    if err := scanner.Err(); err != nil { panic(err) }
    return vals[0], vals[1]
}

func solvePart1(a int64, b int64) int {
    cnt := 0
    for i := 0; i < 40000000; i++ {
        a = (a * FA) % MOD
        b = (b * FB) % MOD
        if (a & MASK) == (b & MASK) { cnt++ }
    }
    return cnt
}

func solvePart2(a int64, b int64) int {
    cnt := 0
    for i := 0; i < 5000000; i++ {
        for {
            a = (a * FA) % MOD
            if (a & 3) == 0 { break }
        }
        for {
            b = (b * FB) % MOD
            if (b & 7) == 0 { break }
        }
        if (a & MASK) == (b & MASK) { cnt++ }
    }
    return cnt
}

func main() {
    part := flag.Int("part", 0, "part")
    input := flag.String("input", "", "input")
    flag.Parse()
    if *part != 1 && *part != 2 { panic("--part 1|2 required") }

    in := resolveInput(*input)
    if sha256File(in) != expectedSHA { panic("checksum mismatch") }
    a0, b0 := parseSeeds(string(must(os.ReadFile(in))))

    t0 := time.Now()
    ans := strconv.Itoa(solvePart1(a0, b0))
    if *part == 2 { ans = strconv.Itoa(solvePart2(a0, b0)) }
    expected := expectedPart1
    if *part == 2 { expected = expectedPart2 }
    if ans != expected { panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected)) }

    fmt.Println(ans)
    ms := float64(time.Since(t0).Nanoseconds()) / 1e6
    fmt.Fprintf(os.Stderr, "[go-fancy] day=15 part=%d runtime_ms=%.3f\n", *part, ms)
}

func must[T any](v T, err error) T { if err != nil { panic(err) }; return v }
