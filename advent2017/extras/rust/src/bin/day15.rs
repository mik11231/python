use sha2::{Digest, Sha256};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "8d4f35b1950c1ca0bd04c13fe9e4a9a15065f902a86a82606973db0b9fe346f7";
const EXPECTED_PART1: &str = "650";
const EXPECTED_PART2: &str = "336";

const FA: i64 = 16807;
const FB: i64 = 48271;
const MOD: i64 = 2147483647;
const MASK: i64 = 0xFFFF;

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day15/d15_input.txt", "Day15/d15_input.txt", "../Day15/d15_input.txt", "../../Day15/d15_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn parse_seeds(raw: &str) -> (i64, i64) {
    let vals = raw
        .lines()
        .filter_map(|line| {
            let line = line.trim();
            if line.is_empty() { None }
            else {
                let parts = line.split_whitespace().collect::<Vec<&str>>();
                Some(parts[parts.len() - 1].parse::<i64>().expect("int"))
            }
        })
        .collect::<Vec<i64>>();
    (vals[0], vals[1])
}

fn solve_part1(mut a: i64, mut b: i64) -> i64 {
    let mut cnt = 0;
    for _ in 0..40_000_000 {
        a = (a * FA) % MOD;
        b = (b * FB) % MOD;
        if (a & MASK) == (b & MASK) { cnt += 1; }
    }
    cnt
}

fn solve_part2(mut a: i64, mut b: i64) -> i64 {
    let mut cnt = 0;
    for _ in 0..5_000_000 {
        loop {
            a = (a * FA) % MOD;
            if (a & 3) == 0 { break; }
        }
        loop {
            b = (b * FB) % MOD;
            if (b & 7) == 0 { break; }
        }
        if (a & MASK) == (b & MASK) { cnt += 1; }
    }
    cnt
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
    let (a0, b0) = parse_seeds(&fs::read_to_string(&in_path).expect("read_to_string"));

    let t0 = Instant::now();
    let ans = if part == 1 { solve_part1(a0, b0).to_string() } else { solve_part2(a0, b0).to_string() };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=15 part={} runtime_ms={:.3}", part, ms);
}
