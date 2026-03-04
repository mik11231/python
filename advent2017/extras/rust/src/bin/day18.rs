// Architecture Notes:
// - This file is heavily commented for long-term maintainability and reconstruction.
// - Pipeline shape is parse -> model -> compute -> emit.
// - Performance-sensitive sections document data-layout and concurrency tradeoffs.

use sha2::{Digest, Sha256};
use std::collections::VecDeque;
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "4052bdd33baaf7be897365aa3ad1cff5fae76ade4c474c9e5ebcdf5058ad368e";
const EXPECTED_PART1: &str = "7071";
const EXPECTED_PART2: &str = "8001";

#[derive(Clone)]
struct Inst {
    op: String,
    x: String,
    y: Option<String>,
}

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day18/d18_input.txt", "Day18/d18_input.txt", "../Day18/d18_input.txt", "../../Day18/d18_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn parse(raw: &str) -> Vec<Inst> {
    raw.lines()
        .filter_map(|line| {
            let line = line.trim();
            if line.is_empty() { None }
            else {
                let p = line.split_whitespace().collect::<Vec<&str>>();
                Some(Inst {
                    op: p[0].to_string(),
                    x: p[1].to_string(),
                    y: if p.len() > 2 { Some(p[2].to_string()) } else { None },
                })
            }
        })
        .collect::<Vec<Inst>>()
}

fn val(tok: &str, regs: &std::collections::HashMap<String, i64>) -> i64 {
    if let Ok(v) = tok.parse::<i64>() { v } else { *regs.get(tok).unwrap_or(&0) }
}

fn solve_part1(prog: &[Inst]) -> i64 {
    let mut regs: std::collections::HashMap<String, i64> = std::collections::HashMap::new();
    let mut ip: i64 = 0;
    let mut last: i64 = 0;

    while ip >= 0 && (ip as usize) < prog.len() {
        let inx = &prog[ip as usize];
        match inx.op.as_str() {
            "snd" => last = val(&inx.x, &regs),
            "set" => { regs.insert(inx.x.clone(), val(inx.y.as_ref().unwrap(), &regs)); }
            "add" => {
                let cur = *regs.get(&inx.x).unwrap_or(&0);
                regs.insert(inx.x.clone(), cur + val(inx.y.as_ref().unwrap(), &regs));
            }
            "mul" => {
                let cur = *regs.get(&inx.x).unwrap_or(&0);
                regs.insert(inx.x.clone(), cur * val(inx.y.as_ref().unwrap(), &regs));
            }
            "mod" => {
                let cur = *regs.get(&inx.x).unwrap_or(&0);
                regs.insert(inx.x.clone(), cur % val(inx.y.as_ref().unwrap(), &regs));
            }
            "rcv" => { if val(&inx.x, &regs) != 0 { return last; } }
            "jgz" => {
                if val(&inx.x, &regs) > 0 {
                    ip += val(inx.y.as_ref().unwrap(), &regs);
                    continue;
                }
            }
            _ => panic!("bad op"),
        }
        ip += 1;
    }

    panic!("no recovery");
}

struct Proc {
    regs: std::collections::HashMap<String, i64>,
    ip: i64,
    inq: VecDeque<i64>,
    send_count: i64,
    waiting: bool,
    terminated: bool,
}

fn step(me: &mut Proc, other: &mut Proc, prog: &[Inst]) -> bool {
    if me.ip < 0 || (me.ip as usize) >= prog.len() {
        me.terminated = true;
        me.waiting = false;
        return false;
    }

    let inx = &prog[me.ip as usize];
    match inx.op.as_str() {
        "snd" => {
            other.inq.push_back(val(&inx.x, &me.regs));
            me.send_count += 1;
            me.ip += 1;
            me.waiting = false;
            true
        }
        "set" => {
            me.regs.insert(inx.x.clone(), val(inx.y.as_ref().unwrap(), &me.regs));
            me.ip += 1;
            me.waiting = false;
            true
        }
        "add" => {
            let cur = *me.regs.get(&inx.x).unwrap_or(&0);
            me.regs.insert(inx.x.clone(), cur + val(inx.y.as_ref().unwrap(), &me.regs));
            me.ip += 1;
            me.waiting = false;
            true
        }
        "mul" => {
            let cur = *me.regs.get(&inx.x).unwrap_or(&0);
            me.regs.insert(inx.x.clone(), cur * val(inx.y.as_ref().unwrap(), &me.regs));
            me.ip += 1;
            me.waiting = false;
            true
        }
        "mod" => {
            let cur = *me.regs.get(&inx.x).unwrap_or(&0);
            me.regs.insert(inx.x.clone(), cur % val(inx.y.as_ref().unwrap(), &me.regs));
            me.ip += 1;
            me.waiting = false;
            true
        }
        "rcv" => {
            if let Some(v) = me.inq.pop_front() {
                me.regs.insert(inx.x.clone(), v);
                me.ip += 1;
                me.waiting = false;
                true
            } else {
                me.waiting = true;
                false
            }
        }
        "jgz" => {
            if val(&inx.x, &me.regs) > 0 {
                me.ip += val(inx.y.as_ref().unwrap(), &me.regs);
            } else {
                me.ip += 1;
            }
            me.waiting = false;
            true
        }
        _ => panic!("bad op"),
    }
}

fn solve_part2(prog: &[Inst]) -> i64 {
    let mut p0 = Proc {
        regs: std::collections::HashMap::from([("p".to_string(), 0)]),
        ip: 0,
        inq: VecDeque::new(),
        send_count: 0,
        waiting: false,
        terminated: false,
    };
    let mut p1 = Proc {
        regs: std::collections::HashMap::from([("p".to_string(), 1)]),
        ip: 0,
        inq: VecDeque::new(),
        send_count: 0,
        waiting: false,
        terminated: false,
    };

    loop {
        let a = step(&mut p0, &mut p1, prog);
        let b = step(&mut p1, &mut p0, prog);
        if !a && !b && (p0.waiting || p0.terminated) && (p1.waiting || p1.terminated) {
            return p1.send_count;
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut part = 0;
    let mut input = String::new();
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--part" => { part = args[i + 1].parse().unwrap(); i += 2; }
            "--input" => { input = args[i + 1].clone(); i += 2; }
            _ => panic!("unknown arg"),
        }
    }
    if part != 1 && part != 2 { panic!("--part 1|2 required"); }

    let in_path = resolve_input(&input);
    if sha256_file(&in_path) != EXPECTED_SHA { panic!("checksum mismatch"); }
    let prog = parse(&fs::read_to_string(&in_path).expect("read_to_string"));

    let t0 = Instant::now();
    let ans = if part == 1 { solve_part1(&prog).to_string() } else { solve_part2(&prog).to_string() };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=18 part={} runtime_ms={:.3}", part, ms);
}
