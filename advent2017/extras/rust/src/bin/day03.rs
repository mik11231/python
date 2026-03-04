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

const EXPECTED_SHA: &str = "697301449f3f32ff9e73436c0ee11191f61f63d01afda5637bf644c5aa6042bc";
const EXPECTED_PART1: &str = "371";
const EXPECTED_PART2: &str = "369601";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day3/d3_input.txt", "Day3/d3_input.txt", "../Day3/d3_input.txt", "../../Day3/d3_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new();
    h.update(&b);
    hex::encode(h.finalize())
}

fn solve_part1(n: i64) -> i64 {
    if n == 1 { return 0; }
    let mut layer: i64 = 0;
    while (2 * layer + 1) * (2 * layer + 1) < n { layer += 1; }
    let side = 2 * layer;
    let maxv = (2 * layer + 1) * (2 * layer + 1);
    let mut best = i64::MAX;
    for i in 0..4 {
        let mid = maxv - layer - side * i;
        let d = (n - mid).abs();
        if d < best { best = d; }
    }
    layer + best
}

fn solve_part2(target: i64) -> i64 {
    let nei = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)];
    let mut grid: HashMap<(i32,i32), i64> = HashMap::new();
    grid.insert((0,0), 1);
    let (mut x, mut y, mut step) = (0i32, 0i32, 1i32);

    let sum_nei = |x0: i32, y0: i32, g: &HashMap<(i32,i32), i64>| -> i64 {
        nei.iter().map(|(dx,dy)| g.get(&(x0 + dx, y0 + dy)).copied().unwrap_or(0)).sum()
    };

    loop {
        for _ in 0..step { x += 1; let v = sum_nei(x,y,&grid); if v > target { return v; } grid.insert((x,y), v); }
        for _ in 0..step { y += 1; let v = sum_nei(x,y,&grid); if v > target { return v; } grid.insert((x,y), v); }
        step += 1;
        for _ in 0..step { x -= 1; let v = sum_nei(x,y,&grid); if v > target { return v; } grid.insert((x,y), v); }
        for _ in 0..step { y -= 1; let v = sum_nei(x,y,&grid); if v > target { return v; } grid.insert((x,y), v); }
        step += 1;
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
    let n: i64 = fs::read_to_string(&in_path).expect("read_to_string").trim().parse().expect("int");

    let t0 = Instant::now();
    let (ans, expected) = if part == 1 {
        (solve_part1(n).to_string(), EXPECTED_PART1)
    } else {
        (solve_part2(n).to_string(), EXPECTED_PART2)
    };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=3 part={} runtime_ms={:.3}", part, ms);
}
