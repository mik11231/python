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

const expectedSHA = "3fd999ac97824b5f8cd2bcbf5c69704a352a0a4bbf9735b0fcc289932fcaeac6"
const expectedPart1 = "mwzaxaj"
const expectedPart2 = "1219"

func resolveInput(provided string) string {
    if provided != "" { return provided }
    cands := []string{"advent2017/Day7/d7_input.txt", "Day7/d7_input.txt", "../Day7/d7_input.txt", "../../Day7/d7_input.txt"}
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

func parseTower(raw string) (map[string]int, map[string][]string, map[string]string) {
    weights := map[string]int{}
    children := map[string][]string{}
    parent := map[string]string{}

    scanner := bufio.NewScanner(strings.NewReader(raw))
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" { continue }

        left := line
        right := ""
        if strings.Contains(line, "->") {
            parts := strings.SplitN(line, "->", 2)
            left = strings.TrimSpace(parts[0])
            right = strings.TrimSpace(parts[1])
        }

        fields := strings.Fields(left)
        name := fields[0]
        wt, err := strconv.Atoi(strings.Trim(fields[1], "()"))
        if err != nil { panic(err) }
        weights[name] = wt

        kids := []string{}
        if right != "" {
            for _, tok := range strings.Split(right, ",") {
                c := strings.TrimSpace(tok)
                if c == "" { continue }
                kids = append(kids, c)
                parent[c] = name
            }
        }
        children[name] = kids
    }
    if err := scanner.Err(); err != nil { panic(err) }
    return weights, children, parent
}

func findRoot(weights map[string]int, parent map[string]string) string {
    for n := range weights {
        if _, ok := parent[n]; !ok {
            return n
        }
    }
    panic("no root")
}

func solvePart2(weights map[string]int, children map[string][]string, root string) int {
    memo := map[string]int{}
    var total func(string) int
    total = func(n string) int {
        if v, ok := memo[n]; ok { return v }
        s := weights[n]
        for _, c := range children[n] { s += total(c) }
        memo[n] = s
        return s
    }

    var dfs func(string) (int, bool)
    dfs = func(n string) (int, bool) {
        kids := children[n]
        if len(kids) == 0 { return 0, false }

        byWeight := map[int][]string{}
        for _, c := range kids {
            tw := total(c)
            byWeight[tw] = append(byWeight[tw], c)
        }
        if len(byWeight) <= 1 { return 0, false }

        badTotal, goodTotal := 0, 0
        badChild := ""
        for tw, nodes := range byWeight {
            if len(nodes) == 1 {
                badTotal = tw
                badChild = nodes[0]
            } else {
                goodTotal = tw
            }
        }

        if deeper, ok := dfs(badChild); ok {
            return deeper, true
        }
        return weights[badChild] + (goodTotal - badTotal), true
    }

    out, ok := dfs(root)
    if !ok { panic("no imbalance") }
    return out
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

    weights, children, parent := parseTower(string(raw))
    root := findRoot(weights, parent)

    t0 := time.Now()
    ans := ""
    if *part == 1 {
        ans = root
    } else {
        ans = strconv.Itoa(solvePart2(weights, children, root))
    }
    expected := expectedPart1
    if *part == 2 { expected = expectedPart2 }
    if ans != expected { panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected)) }

    fmt.Println(ans)
    ms := float64(time.Since(t0).Nanoseconds()) / 1e6
    fmt.Fprintf(os.Stderr, "[go-fancy] day=7 part=%d runtime_ms=%.3f\n", *part, ms)
}
