// Architecture Notes:
// - This file is heavily commented for long-term maintainability and reconstruction.
// - Pipeline shape is parse -> model -> compute -> emit.
// - Performance-sensitive sections document data-layout and concurrency tradeoffs.

use sha2::{Digest, Sha256};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "e9c74e01657b99ad1be3cedce52f75bb0e2ac9dfb2efca8714f5f2e0910befa6";
const EXPECTED_PART1: &str = "394829";
const EXPECTED_PART2: &str = "31150702";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() {
        return provided.to_string();
    }
    let cands = ["advent2017/Day5/d5_input.txt", "Day5/d5_input.txt", "../Day5/d5_input.txt", "../../Day5/d5_input.txt"];
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

fn parse_offsets(raw: &str) -> Vec<i32> {
    raw.lines()
        .filter_map(|line| {
            let line = line.trim();
            if line.is_empty() {
                None
            } else {
                Some(line.parse::<i32>().expect("int"))
            }
        })
        .collect::<Vec<i32>>()
}

fn run_program(offsets: &[i32], part: i32) -> i64 {
    let mut a = offsets.to_vec();
    let mut i: i32 = 0;
    let mut steps: i64 = 0;

    while i >= 0 && (i as usize) < a.len() {
        let idx = i as usize;
        let jump = a[idx];
        if part == 1 {
            a[idx] += 1;
        } else if jump >= 3 {
            a[idx] -= 1;
        } else {
            a[idx] += 1;
        }
        i += jump;
        steps += 1;
    }

    steps
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
    let offsets = parse_offsets(&fs::read_to_string(&in_path).expect("read_to_string"));

    let t0 = Instant::now();
    let ans = run_program(&offsets, part).to_string();
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected {
        panic!("answer mismatch");
    }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=5 part={} runtime_ms={:.3}", part, ms);
}
