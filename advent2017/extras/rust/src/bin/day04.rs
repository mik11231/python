use sha2::{Digest, Sha256};
use std::collections::HashSet;
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "36d753e40c996a2ec1083c34b8cda3ffa986bc63a44d73be5ee1ed81084c6401";
const EXPECTED_PART1: &str = "451";
const EXPECTED_PART2: &str = "223";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day4/d4_input.txt", "Day4/d4_input.txt", "../Day4/d4_input.txt", "../../Day4/d4_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn parse_lines(raw: &str) -> Vec<Vec<String>> {
    raw.lines()
        .filter_map(|line| {
            let line = line.trim();
            if line.is_empty() { None }
            else { Some(line.split_whitespace().map(|s| s.to_string()).collect::<Vec<String>>()) }
        })
        .collect::<Vec<Vec<String>>>()
}

fn canonical_word(w: &str) -> String {
    let mut c: Vec<char> = w.chars().collect();
    c.sort_unstable();
    c.into_iter().collect::<String>()
}

fn solve_part1(lines: &[Vec<String>]) -> i64 {
    let mut valid = 0;
    for words in lines {
        let mut seen: HashSet<String> = HashSet::new();
        let mut ok = true;
        for w in words {
            if !seen.insert(w.clone()) { ok = false; break; }
        }
        if ok { valid += 1; }
    }
    valid
}

fn solve_part2(lines: &[Vec<String>]) -> i64 {
    let mut valid = 0;
    for words in lines {
        let mut seen: HashSet<String> = HashSet::new();
        let mut ok = true;
        for w in words {
            let c = canonical_word(w);
            if !seen.insert(c) { ok = false; break; }
        }
        if ok { valid += 1; }
    }
    valid
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
    let lines = parse_lines(&fs::read_to_string(&in_path).expect("read_to_string"));

    let t0 = Instant::now();
    let (ans, expected) = if part == 1 {
        (solve_part1(&lines).to_string(), EXPECTED_PART1)
    } else {
        (solve_part2(&lines).to_string(), EXPECTED_PART2)
    };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=4 part={} runtime_ms={:.3}", part, ms);
}
