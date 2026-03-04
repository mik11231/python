// Architecture Notes:
// - This file is heavily commented for long-term maintainability and reconstruction.
// - Pipeline shape is parse -> model -> compute -> emit.
// - Performance-sensitive sections document data-layout and concurrency tradeoffs.

use sha2::{Digest, Sha256};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "09a2c42b5b2f5e7e0c325a89194f42c2a9f88efb35cd6dcf61a69005545cc3d1";
const EXPECTED_PART1: &str = "685";
const EXPECTED_PART2: &str = "1457";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day11/d11_input.txt", "Day11/d11_input.txt", "../Day11/d11_input.txt", "../../Day11/d11_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn cube_distance(x: i64, y: i64, z: i64) -> i64 {
    x.abs().max(y.abs()).max(z.abs())
}

fn solve(raw: &str) -> (i64, i64) {
    let mut x: i64 = 0;
    let mut y: i64 = 0;
    let mut z: i64 = 0;
    let mut best: i64 = 0;

    for step in raw.trim().split(',') {
        let step = step.trim();
        if step.is_empty() { continue; }
        match step {
            "n" => { y += 1; z -= 1; }
            "ne" => { x += 1; z -= 1; }
            "se" => { x += 1; y -= 1; }
            "s" => { y -= 1; z += 1; }
            "sw" => { x -= 1; z += 1; }
            "nw" => { x -= 1; y += 1; }
            _ => panic!("bad step"),
        }
        let d = cube_distance(x, y, z);
        if d > best { best = d; }
    }

    (cube_distance(x, y, z), best)
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
    let (p1, p2) = solve(&raw);
    let ans = if part == 1 { p1.to_string() } else { p2.to_string() };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=11 part={} runtime_ms={:.3}", part, ms);
}
