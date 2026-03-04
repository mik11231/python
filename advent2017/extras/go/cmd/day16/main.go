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

const expectedSHA = "6bb64ef97ccf665f21eccff0a7045717f0a03d39ae06aaac5495dd6fff650818"
const expectedPart1 = "kgdchlfniambejop"
const expectedPart2 = "fjpmholcibdgeakn"

func resolveInput(provided string) string {
    if provided != "" { return provided }
    cands := []string{"advent2017/Day16/d16_input.txt", "Day16/d16_input.txt", "../Day16/d16_input.txt", "../../Day16/d16_input.txt"}
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

func parseMoves(raw string) []string {
    parts := strings.Split(strings.TrimSpace(raw), ",")
    out := make([]string, 0, len(parts))
    for _, p := range parts {
        p = strings.TrimSpace(p)
        if p != "" { out = append(out, p) }
    }
    return out
}

func applyOnce(state []byte, moves []string) {
    for _, mv := range moves {
        t := mv[0]
        arg := mv[1:]
        switch t {
        case 's':
            x, _ := strconv.Atoi(arg)
            n := len(state)
            tmp := append([]byte{}, state[n-x:]...)
            tmp = append(tmp, state[:n-x]...)
            copy(state, tmp)
        case 'x':
            ab := strings.Split(arg, "/")
            a, _ := strconv.Atoi(ab[0])
            b, _ := strconv.Atoi(ab[1])
            state[a], state[b] = state[b], state[a]
        case 'p':
            ab := strings.Split(arg, "/")
            a := ab[0][0]
            b := ab[1][0]
            ia, ib := -1, -1
            for i, ch := range state {
                if ch == a { ia = i }
                if ch == b { ib = i }
            }
            state[ia], state[ib] = state[ib], state[ia]
        default:
            panic("bad move")
        }
    }
}

func dance(moves []string, rounds int) string {
    state := []byte("abcdefghijklmnop")
    seen := map[string]int{}

    i := 0
    for i < rounds {
        key := string(state)
        if prev, ok := seen[key]; ok {
            cycle := i - prev
            rem := (rounds - i) % cycle
            for r := 0; r < rem; r++ { applyOnce(state, moves) }
            return string(state)
        }
        seen[key] = i
        applyOnce(state, moves)
        i++
    }
    return string(state)
}

func main() {
    part := flag.Int("part", 0, "part")
    input := flag.String("input", "", "input")
    flag.Parse()
    if *part != 1 && *part != 2 { panic("--part 1|2 required") }

    in := resolveInput(*input)
    if sha256File(in) != expectedSHA { panic("checksum mismatch") }
    moves := parseMoves(string(must(os.ReadFile(in))))

    t0 := time.Now()
    ans := dance(moves, 1)
    if *part == 2 { ans = dance(moves, 1_000_000_000) }
    expected := expectedPart1
    if *part == 2 { expected = expectedPart2 }
    if ans != expected { panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected)) }

    fmt.Println(ans)
    ms := float64(time.Since(t0).Nanoseconds()) / 1e6
    fmt.Fprintf(os.Stderr, "[go-fancy] day=16 part=%d runtime_ms=%.3f\n", *part, ms)
}

func must[T any](v T, err error) T { if err != nil { panic(err) }; return v }
