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

const expectedSHA = "4052bdd33baaf7be897365aa3ad1cff5fae76ade4c474c9e5ebcdf5058ad368e"
const expectedPart1 = "7071"
const expectedPart2 = "8001"

type Inst struct {
    op string
    x  string
    y  string
    hasY bool
}

func resolveInput(provided string) string {
    if provided != "" { return provided }
    cands := []string{"advent2017/Day18/d18_input.txt", "Day18/d18_input.txt", "../Day18/d18_input.txt", "../../Day18/d18_input.txt"}
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

func parse(raw string) []Inst {
    out := []Inst{}
    scanner := bufio.NewScanner(strings.NewReader(raw))
    for scanner.Scan() {
        line := strings.TrimSpace(scanner.Text())
        if line == "" { continue }
        p := strings.Fields(line)
        inst := Inst{op: p[0], x: p[1]}
        if len(p) > 2 { inst.y = p[2]; inst.hasY = true }
        out = append(out, inst)
    }
    if err := scanner.Err(); err != nil { panic(err) }
    return out
}

func val(tok string, regs map[string]int64) int64 {
    if v, err := strconv.ParseInt(tok, 10, 64); err == nil { return v }
    return regs[tok]
}

func solvePart1(prog []Inst) int64 {
    regs := map[string]int64{}
    ip := int64(0)
    last := int64(0)

    for ip >= 0 && ip < int64(len(prog)) {
        in := prog[ip]
        switch in.op {
        case "snd":
            last = val(in.x, regs)
        case "set":
            regs[in.x] = val(in.y, regs)
        case "add":
            regs[in.x] = regs[in.x] + val(in.y, regs)
        case "mul":
            regs[in.x] = regs[in.x] * val(in.y, regs)
        case "mod":
            regs[in.x] = regs[in.x] % val(in.y, regs)
        case "rcv":
            if val(in.x, regs) != 0 { return last }
        case "jgz":
            if val(in.x, regs) > 0 {
                ip += val(in.y, regs)
                continue
            }
        default:
            panic("bad op")
        }
        ip++
    }

    panic("no recovery")
}

type Proc struct {
    pid int64
    regs map[string]int64
    ip int64
    inq []int64
    sendCount int64
    waiting bool
    terminated bool
}

func (p *Proc) push(v int64) { p.inq = append(p.inq, v) }
func (p *Proc) pop() (int64, bool) {
    if len(p.inq) == 0 { return 0, false }
    v := p.inq[0]
    p.inq = p.inq[1:]
    return v, true
}

func step(p *Proc, other *Proc, prog []Inst) bool {
    if p.ip < 0 || p.ip >= int64(len(prog)) {
        p.terminated = true
        p.waiting = false
        return false
    }

    in := prog[p.ip]
    switch in.op {
    case "snd":
        other.push(val(in.x, p.regs))
        p.sendCount++
        p.ip++
        p.waiting = false
        return true
    case "set":
        p.regs[in.x] = val(in.y, p.regs)
        p.ip++
        p.waiting = false
        return true
    case "add":
        p.regs[in.x] = p.regs[in.x] + val(in.y, p.regs)
        p.ip++
        p.waiting = false
        return true
    case "mul":
        p.regs[in.x] = p.regs[in.x] * val(in.y, p.regs)
        p.ip++
        p.waiting = false
        return true
    case "mod":
        p.regs[in.x] = p.regs[in.x] % val(in.y, p.regs)
        p.ip++
        p.waiting = false
        return true
    case "rcv":
        if v, ok := p.pop(); ok {
            p.regs[in.x] = v
            p.ip++
            p.waiting = false
            return true
        }
        p.waiting = true
        return false
    case "jgz":
        if val(in.x, p.regs) > 0 {
            p.ip += val(in.y, p.regs)
        } else {
            p.ip++
        }
        p.waiting = false
        return true
    default:
        panic("bad op")
    }
}

func solvePart2(prog []Inst) int64 {
    p0 := &Proc{pid: 0, regs: map[string]int64{"p": 0}}
    p1 := &Proc{pid: 1, regs: map[string]int64{"p": 1}}

    for {
        a := step(p0, p1, prog)
        b := step(p1, p0, prog)
        if !a && !b && (p0.waiting || p0.terminated) && (p1.waiting || p1.terminated) {
            return p1.sendCount
        }
    }
}

func main() {
    part := flag.Int("part", 0, "part")
    input := flag.String("input", "", "input")
    flag.Parse()
    if *part != 1 && *part != 2 { panic("--part 1|2 required") }

    in := resolveInput(*input)
    if sha256File(in) != expectedSHA { panic("checksum mismatch") }
    prog := parse(string(must(os.ReadFile(in))))

    t0 := time.Now()
    ans := strconv.FormatInt(solvePart1(prog), 10)
    if *part == 2 { ans = strconv.FormatInt(solvePart2(prog), 10) }
    expected := expectedPart1
    if *part == 2 { expected = expectedPart2 }
    if ans != expected { panic(fmt.Sprintf("answer mismatch: got %s expected %s", ans, expected)) }

    fmt.Println(ans)
    ms := float64(time.Since(t0).Nanoseconds()) / 1e6
    fmt.Fprintf(os.Stderr, "[go-fancy] day=18 part=%d runtime_ms=%.3f\n", *part, ms)
}

func must[T any](v T, err error) T { if err != nil { panic(err) }; return v }
