use sha2::{Digest, Sha256};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "ffefe22d570c7077ac45df89cd8a40c99990e1903f6e68a501d75e53038c80ef";
const EXPECTED_PART1: &str = "1158";
const EXPECTED_PART2: &str = "1132";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() {
        return provided.to_string();
    }
    let cands = [
        "advent2017/Day1/d1_input.txt",
        "Day1/d1_input.txt",
        "../Day1/d1_input.txt",
        "../../Day1/d1_input.txt",
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

fn solve_with_step(raw: &str, step: usize) -> i64 {
    let s = raw.trim().as_bytes();
    if s.is_empty() {
        return 0;
    }
    let mut total: i64 = 0;
    for i in 0..s.len() {
        let j = (i + step) % s.len();
        if s[i] == s[j] {
            total += (s[i] - b'0') as i64;
        }
    }
    total
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
    if part != 1 && part != 2 { panic!("--part 1|2 required") }

    let in_path = resolve_input(&input);
    if sha256_file(&in_path) != EXPECTED_SHA {
        panic!("checksum mismatch");
    }
    let raw = fs::read_to_string(&in_path).expect("read_to_string");

    let t0 = Instant::now();
    let (ans, expected) = if part == 1 {
        (solve_with_step(&raw, 1).to_string(), EXPECTED_PART1)
    } else {
        let n = raw.trim().len();
        (solve_with_step(&raw, n / 2).to_string(), EXPECTED_PART2)
    };

    if ans != expected {
        panic!("answer mismatch");
    }
    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=1 part={} runtime_ms={:.3}", part, ms);
}
