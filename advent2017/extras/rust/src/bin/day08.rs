use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "a2888c695f7f2c036f5d9568befc839a3b64c703d054f82162cfbc5e105627dd";
const EXPECTED_PART1: &str = "5143";
const EXPECTED_PART2: &str = "6209";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day8/d8_input.txt", "Day8/d8_input.txt", "../Day8/d8_input.txt", "../../Day8/d8_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn check(a: i64, op: &str, b: i64) -> bool {
    match op {
        "<" => a < b,
        "<=" => a <= b,
        ">" => a > b,
        ">=" => a >= b,
        "==" => a == b,
        "!=" => a != b,
        _ => panic!("bad op"),
    }
}

fn run_program(raw: &str) -> (i64, i64) {
    let mut reg: HashMap<String, i64> = HashMap::new();
    let mut best: i64 = 0;

    for line in raw.lines() {
        let line = line.trim();
        if line.is_empty() { continue; }
        let f = line.split_whitespace().collect::<Vec<&str>>();
        let r = f[0].to_string();
        let op = f[1];
        let v: i64 = f[2].parse().expect("int");
        let cr = f[4].to_string();
        let cmp = f[5];
        let cv: i64 = f[6].parse().expect("int");

        let crv = *reg.get(&cr).unwrap_or(&0);
        if check(crv, cmp, cv) {
            let rv = *reg.get(&r).unwrap_or(&0);
            let nv = if op == "inc" { rv + v } else { rv - v };
            reg.insert(r, nv);
            if nv > best { best = nv; }
        }
    }

    let mut maxv = 0;
    for v in reg.values() {
        if *v > maxv { maxv = *v; }
    }
    (maxv, best)
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
    let raw = fs::read_to_string(&in_path).expect("read_to_string");

    let t0 = Instant::now();
    let (p1, p2) = run_program(&raw);
    let ans = if part == 1 { p1.to_string() } else { p2.to_string() };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=8 part={} runtime_ms={:.3}", part, ms);
}
