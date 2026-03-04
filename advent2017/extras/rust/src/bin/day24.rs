// Architecture Notes:
// - This file is heavily commented for long-term maintainability and reconstruction.
// - Pipeline shape is parse -> model -> compute -> emit.
// - Performance-sensitive sections document data-layout and concurrency tradeoffs.

use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "48a139f917d7dac161171c28f578d923b212c10108c92bbe05a971f6d8b4fb05";
const EXPECTED_PART1: &str = "1656";
const EXPECTED_PART2: &str = "1642";

#[derive(Clone, Copy)]
struct Comp {
    a: i32,
    b: i32,
}

#[derive(Clone, Copy)]
struct Ret {
    s: i32,
    l: i32,
    ls: i32,
}

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() {
        return provided.to_string();
    }
    let cands = [
        "advent2017/Day24/d24_input.txt",
        "Day24/d24_input.txt",
        "../Day24/d24_input.txt",
        "../../Day24/d24_input.txt",
    ];
    for c in cands {
        if Path::new(c).exists() {
            return c.to_string();
        }
    }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new();
    h.update(&b);
    hex::encode(h.finalize())
}

fn parse(text: &str) -> (Vec<Comp>, HashMap<i32, Vec<usize>>) {
    let mut comps = Vec::new();
    let mut by: HashMap<i32, Vec<usize>> = HashMap::new();
    for ln in text.lines() {
        let s = ln.trim();
        if s.is_empty() {
            continue;
        }
        let p = s.split('/').collect::<Vec<&str>>();
        let a: i32 = p[0].parse().expect("int");
        let b: i32 = p[1].parse().expect("int");
        let i = comps.len();
        comps.push(Comp { a, b });
        by.entry(a).or_default().push(i);
        if b != a {
            by.entry(b).or_default().push(i);
        }
    }
    (comps, by)
}

fn solve(comps: &[Comp], by: &HashMap<i32, Vec<usize>>) -> (i32, i32) {
    let mut used = vec![false; comps.len()];
    fn dfs(port: i32, comps: &[Comp], by: &HashMap<i32, Vec<usize>>, used: &mut [bool]) -> Ret {
        let mut best = Ret { s: 0, l: 0, ls: 0 };
        if let Some(cands) = by.get(&port) {
            for &i in cands {
                if used[i] {
                    continue;
                }
                let c = comps[i];
                let nxt = if c.a == port { c.b } else { c.a };
                let seg = c.a + c.b;
                used[i] = true;
                let ch = dfs(nxt, comps, by, used);
                used[i] = false;

                if seg + ch.s > best.s {
                    best.s = seg + ch.s;
                }
                let cl = 1 + ch.l;
                let cls = seg + ch.ls;
                if cl > best.l || (cl == best.l && cls > best.ls) {
                    best.l = cl;
                    best.ls = cls;
                }
            }
        }
        best
    }
    let r = dfs(0, comps, by, &mut used);
    (r.s, r.ls)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut part = 0;
    let mut input = String::new();
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--part" => {
                part = args[i + 1].parse().unwrap();
                i += 2;
            }
            "--input" => {
                input = args[i + 1].clone();
                i += 2;
            }
            _ => panic!("unknown arg"),
        }
    }
    if part != 1 && part != 2 {
        panic!("--part 1|2 required");
    }
    let in_path = resolve_input(&input);
    if sha256_file(&in_path) != EXPECTED_SHA {
        panic!("checksum mismatch");
    }
    let (comps, by) = parse(&fs::read_to_string(&in_path).expect("read_to_string"));

    let t0 = Instant::now();
    let (p1, p2) = solve(&comps, &by);
    let ans = if part == 1 {
        p1.to_string()
    } else {
        p2.to_string()
    };
    let expected = if part == 1 {
        EXPECTED_PART1
    } else {
        EXPECTED_PART2
    };
    if ans != expected {
        panic!("answer mismatch");
    }
    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=24 part={} runtime_ms={:.3}", part, ms);
}
