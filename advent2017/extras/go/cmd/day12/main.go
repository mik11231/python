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

const expectedSHA = "5a807a689f833a1add89ef7c1215b693721849db8347b273bca570346357377c"
const expectedPart1 = "239"
const expectedPart2 = "215"

func resolveInput(provided string) string {
    if provided != "" {
        return provided
    }
    cands := []string{"advent2017/Day12/d12_input.txt", "Day12/d12_input.txt", "../Day12/d12_input.txt", "../../Day12/d12_input.txt"}
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

func parseGraph(raw string) map[int][]int {
    g := map[int][]int{}
    scanner := bufio.NewScanner(strings.NewReader(raw))
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" {
            continue
        }
        parts := strings.Split(line, "<->")
        u, err := strconv.Atoi(strings.TrimSpace(parts[0]))
        if err != nil {
            panic(err)
        }
        nbrs := []int{}
        for _, tok := range strings.Split(parts[1], ",") {
            v, err := strconv.Atoi(strings.TrimSpace(tok))
            if err != nil {
                panic(err)
            }
            nbrs = append(nbrs, v)
        }
        g[u] = nbrs
    }
    if err := scanner.Err(); err != nil {
        panic(err)
    }
    return g
}

func bfsComponent(g map[int][]int, start int, seen map[int]bool) []int {
    q := []int{start}
    seen[start] = true
    comp := []int{start}

    for len(q) > 0 {
        u := q[0]
        q = q[1:]
        for _, v := range g[u] {
            if seen[v] {
                continue
            }
            seen[v] = true
            comp = append(comp, v)
            q = append(q, v)
        }
    }
    return comp
}

func solve(raw string) (int, int) {
    g := parseGraph(raw)
    seen := map[int]bool{}

    group0 := bfsComponent(g, 0, seen)
    groups := 1
    for node := range g {
        if seen[node] {
            continue
        }
        bfsComponent(g, node, seen)
        groups++
    }

    return len(group0), groups
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
    p1, p2 := solve(string(raw))
    ans := strconv.Itoa(p1)
    if *part == 2 {
        ans = strconv.Itoa(p2)
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
    fmt.Fprintf(os.Stderr, "[go-fancy] day=12 part=%d runtime_ms=%.3f\n", *part, ms)
}
