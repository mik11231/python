// Architecture Notes:
// - This file is heavily commented for long-term maintainability and reconstruction.
// - Pipeline shape is parse -> model -> compute -> emit.
// - Performance-sensitive sections document data-layout and concurrency tradeoffs.

use sha2::{Digest, Sha256};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "860cd63e00136c29310e25db6f4f1573a2b2574598dc72f44a6308ddf5a967c3";
const EXPECTED_PART1: &str = "21037";
const EXPECTED_PART2: &str = "9495";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day9/d9_input.txt", "Day9/d9_input.txt", "../Day9/d9_input.txt", "../../Day9/d9_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn scan_stream(raw: &str) -> (i64, i64) {
    let s = raw.trim().as_bytes();
    let mut depth: i64 = 0;
    let mut score: i64 = 0;
    let mut garbage: i64 = 0;
    let mut in_garbage = false;
    let mut i = 0usize;

    while i < s.len() {
        let c = s[i];
        if in_garbage {
            if c == b'!' {
                i += 2;
                continue;
            }
            if c == b'>' {
                in_garbage = false;
            } else {
                garbage += 1;
            }
            i += 1;
            continue;
        }

        if c == b'<' {
            in_garbage = true;
        } else if c == b'{' {
            depth += 1;
            score += depth;
        } else if c == b'}' {
            depth -= 1;
        }
        i += 1;
    }

    (score, garbage)
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
    let (p1, p2) = scan_stream(&raw);
    let ans = if part == 1 { p1.to_string() } else { p2.to_string() };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=9 part={} runtime_ms={:.3}", part, ms);
}
