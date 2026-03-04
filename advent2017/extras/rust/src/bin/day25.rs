// Architecture Notes:
// - This file is heavily commented for long-term maintainability and reconstruction.
// - Pipeline shape is parse -> model -> compute -> emit.
// - Performance-sensitive sections document data-layout and concurrency tradeoffs.

use sha2::{Digest, Sha256};
use std::collections::HashSet;
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "6419303e9eeb435a39b6e7d17236cb0d3fdfc9b0c2e5d5da8a9864b527c7e873";
const EXPECTED_PART1: &str = "3145";
const EXPECTED_PART2: &str = "Merry Christmas";

#[derive(Clone, Copy)]
struct Rule {
    write: i32,
    mov: i32,
    next: u8,
}

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() {
        return provided.to_string();
    }
    let cands = [
        "advent2017/Day25/d25_input.txt",
        "Day25/d25_input.txt",
        "../Day25/d25_input.txt",
        "../../Day25/d25_input.txt",
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

fn solve_part1(text: &str) -> i32 {
    let lines: Vec<&str> = text.lines().collect();
    let start = lines[0]
        .split_whitespace()
        .nth(3)
        .expect("start")
        .trim_end_matches('.')
        .as_bytes()[0];
    let steps: usize = lines[1]
        .split_whitespace()
        .nth(5)
        .expect("steps")
        .parse()
        .expect("int");
    let mut trans = [[Rule { write: 0, mov: 0, next: b'A' }; 2]; 26];
    let mut i = 2usize;
    while i < lines.len() {
        if lines[i].trim().is_empty() {
            i += 1;
            continue;
        }
        // Block layout is fixed to 10 lines.
        let st = lines[i]
            .split_whitespace()
            .nth(2)
            .expect("state")
            .trim_end_matches(':')
            .as_bytes()[0];
        let w0: i32 = lines[i + 2]
            .split_whitespace()
            .last()
            .expect("w0")
            .trim_end_matches('.')
            .parse()
            .expect("int");
        let m0 = if lines[i + 3].contains("right") { 1 } else { -1 };
        let n0 = lines[i + 4]
            .split_whitespace()
            .last()
            .expect("n0")
            .trim_end_matches('.')
            .as_bytes()[0];
        let w1: i32 = lines[i + 6]
            .split_whitespace()
            .last()
            .expect("w1")
            .trim_end_matches('.')
            .parse()
            .expect("int");
        let m1 = if lines[i + 7].contains("right") { 1 } else { -1 };
        let n1 = lines[i + 8]
            .split_whitespace()
            .last()
            .expect("n1")
            .trim_end_matches('.')
            .as_bytes()[0];
        trans[(st - b'A') as usize][0] = Rule { write: w0, mov: m0, next: n0 };
        trans[(st - b'A') as usize][1] = Rule { write: w1, mov: m1, next: n1 };
        i += 10;
    }

    let mut tape: HashSet<i64> = HashSet::new();
    let mut cur: i64 = 0;
    let mut st = start;
    for _ in 0..steps {
        let v = if tape.contains(&cur) { 1 } else { 0 };
        let r = trans[(st - b'A') as usize][v];
        if r.write == 1 {
            tape.insert(cur);
        } else {
            tape.remove(&cur);
        }
        cur += r.mov as i64;
        st = r.next;
    }
    tape.len() as i32
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
    let text = fs::read_to_string(&in_path).expect("read_to_string");

    let t0 = Instant::now();
    let ans = if part == 1 {
        solve_part1(&text).to_string()
    } else {
        EXPECTED_PART2.to_string()
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
    eprintln!("[rust-fancy] day=25 part={} runtime_ms={:.3}", part, ms);
}
