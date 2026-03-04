use sha2::{Digest, Sha256};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "03a3d955b8799a90f1ff5a39479fde8e618f8ca3282d5b187186f2cf361abd32";
const EXPECTED_PART1: &str = "808";
const EXPECTED_PART2: &str = "47465686";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day17/d17_input.txt", "Day17/d17_input.txt", "../Day17/d17_input.txt", "../../Day17/d17_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn solve_part1(step: usize) -> i64 {
    let mut buf: Vec<i64> = vec![0];
    let mut pos: usize = 0;
    for v in 1..=2017 {
        pos = (pos + step) % buf.len() + 1;
        buf.insert(pos, v as i64);
    }
    buf[(pos + 1) % buf.len()]
}

fn solve_part2(step: usize) -> i64 {
    let mut pos: usize = 0;
    let mut val_after_zero: i64 = 0;
    let mut size: usize = 1;
    for v in 1..=50_000_000usize {
        pos = (pos + step) % size + 1;
        if pos == 1 { val_after_zero = v as i64; }
        size += 1;
    }
    val_after_zero
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
    let step: usize = fs::read_to_string(&in_path).expect("read_to_string").trim().parse().expect("int");

    let t0 = Instant::now();
    let ans = if part == 1 { solve_part1(step).to_string() } else { solve_part2(step).to_string() };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=17 part={} runtime_ms={:.3}", part, ms);
}
