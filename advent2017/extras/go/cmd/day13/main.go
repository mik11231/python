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

const expectedSHA = "b59ed1486b6ec731cb7c2f55fdfec971d1157b9411fb823f9ddf0a3839d12cc8"
const expectedPart1 = "2604"
const expectedPart2 = "3941460"

type layer struct {
    depth  int
    rng    int
    period int
}

func resolveInput(provided string) string {
    if provided != "" {
        return provided
    }
    cands := []string{"advent2017/Day13/d13_input.txt", "Day13/d13_input.txt", "../Day13/d13_input.txt", "../../Day13/d13_input.txt"}
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

func parseLayers(raw string) []layer {
    out := make([]layer, 0, 64)
    scanner := bufio.NewScanner(strings.NewReader(raw))
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" {
            continue
        }
        parts := strings.Split(line, ":")
        d, err := strconv.Atoi(strings.TrimSpace(parts[0]))
        if err != nil {
            panic(err)
        }
        r, err := strconv.Atoi(strings.TrimSpace(parts[1]))
        if err != nil {
            panic(err)
        }
        out = append(out, layer{depth: d, rng: r, period: 2 * (r - 1)})
    }
    if err := scanner.Err(); err != nil {
        panic(err)
    }
    return out
}

func solvePart1(layers []layer) int {
    severity := 0
    for _, l := range layers {
        if l.depth%l.period == 0 {
            severity += l.depth * l.rng
        }
    }
    return severity
}

func solvePart2(layers []layer) int {
    delay := 0
    for {
        ok := true
        for _, l := range layers {
            if (delay+l.depth)%l.period == 0 {
                ok = false
                break
            }
        }
        if ok {
            return delay
        }
        delay++
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
    layers := parseLayers(string(raw))

    t0 := time.Now()
    ans := strconv.Itoa(solvePart1(layers))
    if *part == 2 {
        ans = strconv.Itoa(solvePart2(layers))
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
    fmt.Fprintf(os.Stderr, "[go-fancy] day=13 part=%d runtime_ms=%.3f\n", *part, ms)
}
