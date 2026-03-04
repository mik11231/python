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

const expectedSHA = "c64165a1af8ab4877e736a095bde2b22d523468077099fab5a338f53b0059681"
const expectedPart1 = "36174"
const expectedPart2 = "244"

func resolveInput(provided string) string {
    if provided != "" {
        return provided
    }
    cands := []string{
        "advent2017/Day2/d2_input.txt",
        "Day2/d2_input.txt",
        "../Day2/d2_input.txt",
        "../../Day2/d2_input.txt",
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

func parseRows(raw string) [][]int {
    scanner := bufio.NewScanner(strings.NewReader(raw))
    rows := make([][]int, 0, 64)
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" {
            continue
        }
        fields := strings.Fields(line)
        row := make([]int, 0, len(fields))
        for _, f := range fields {
            v, err := strconv.Atoi(f)
            if err != nil {
                panic(err)
            }
            row = append(row, v)
        }
        rows = append(rows, row)
    }
    if err := scanner.Err(); err != nil {
        panic(err)
    }
    return rows
}

func solvePart1(rows [][]int) int {
    total := 0
    for _, row := range rows {
        if len(row) == 0 {
            continue
        }
        minV, maxV := row[0], row[0]
        for _, v := range row[1:] {
            if v < minV {
                minV = v
            }
            if v > maxV {
                maxV = v
            }
        }
        total += maxV - minV
    }
    return total
}

func solvePart2(rows [][]int) int {
    total := 0
    for _, row := range rows {
        found := false
        for i, a := range row {
            for j, b := range row {
                if i == j {
                    continue
                }
                if b != 0 && a%b == 0 {
                    total += a / b
                    found = true
                    break
                }
            }
            if found {
                break
            }
        }
        if !found {
            panic("no divisible pair found")
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
    raw, err := os.ReadFile(in)
    if err != nil {
        panic(err)
    }

    rows := parseRows(string(raw))

    t0 := time.Now()
    var ans string
    var expected string
    if *part == 1 {
        ans = strconv.Itoa(solvePart1(rows))
        expected = expectedPart1
    } else {
        ans = strconv.Itoa(solvePart2(rows))
        expected = expectedPart2
    }
    if ans != expected {
        panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected))
    }

    fmt.Println(ans)
    ms := float64(time.Since(t0).Nanoseconds()) / 1e6
    fmt.Fprintf(os.Stderr, "[go-fancy] day=2 part=%d runtime_ms=%.3f\n", *part, ms)
}
