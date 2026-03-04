// Architecture Notes:
// - This file is heavily commented for long-term maintainability and reconstruction.
// - Pipeline shape is parse -> model -> compute -> emit.
// - Performance-sensitive sections document data-layout and concurrency tradeoffs.

use sha2::{Digest, Sha256};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "b59ed1486b6ec731cb7c2f55fdfec971d1157b9411fb823f9ddf0a3839d12cc8";
const EXPECTED_PART1: &str = "2604";
const EXPECTED_PART2: &str = "3941460";

#[derive(Clone, Copy)]
struct Layer {
    depth: i64,
    rng: i64,
    period: i64,
}

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day13/d13_input.txt", "Day13/d13_input.txt", "../Day13/d13_input.txt", "../../Day13/d13_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn parse_layers(raw: &str) -> Vec<Layer> {
    raw.lines()
        .filter_map(|line| {
            let line = line.trim();
            if line.is_empty() { return None; }
            let parts = line.split(':').map(|x| x.trim()).collect::<Vec<&str>>();
            let d = parts[0].parse::<i64>().expect("int");
            let r = parts[1].parse::<i64>().expect("int");
            Some(Layer { depth: d, rng: r, period: 2 * (r - 1) })
        })
        .collect::<Vec<Layer>>()
}

fn solve_part1(layers: &[Layer]) -> i64 {
    layers
        .iter()
        .filter(|l| l.depth % l.period == 0)
        .map(|l| l.depth * l.rng)
        .sum()
}

fn solve_part2(layers: &[Layer]) -> i64 {
    let mut delay: i64 = 0;
    loop {
        let ok = layers.iter().all(|l| (delay + l.depth) % l.period != 0);
        if ok { return delay; }
        delay += 1;
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
    let raw = fs::read_to_string(&in_path).expect("read_to_string");
    let layers = parse_layers(&raw);

    let t0 = Instant::now();
    let ans = if part == 1 { solve_part1(&layers).to_string() } else { solve_part2(&layers).to_string() };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=13 part={} runtime_ms={:.3}", part, ms);
}
