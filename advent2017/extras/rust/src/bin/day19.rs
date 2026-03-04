use sha2::{Digest, Sha256};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "b4231dede8cc9f00c1dcdf6fe60b2c5cc33278020531f4a05af462099063171a";
const EXPECTED_PART1: &str = "DTOUFARJQ";
const EXPECTED_PART2: &str = "16642";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day19/d19_input.txt", "Day19/d19_input.txt", "../Day19/d19_input.txt", "../../Day19/d19_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn parse_grid(raw: &str) -> Vec<Vec<u8>> {
    let lines = raw.trim_end_matches('\n').lines().collect::<Vec<&str>>();
    let w = lines.iter().map(|l| l.len()).max().unwrap_or(0);
    lines
        .iter()
        .map(|l| {
            let mut row = vec![b' '; w];
            row[..l.len()].copy_from_slice(l.as_bytes());
            row
        })
        .collect::<Vec<Vec<u8>>>()
}

fn at(g: &[Vec<u8>], r: i32, c: i32) -> u8 {
    if r < 0 || c < 0 || (r as usize) >= g.len() || (c as usize) >= g[0].len() { b' ' }
    else { g[r as usize][c as usize] }
}

fn solve(raw: &str) -> (String, i64) {
    let g = parse_grid(raw);
    let mut r: i32 = 0;
    let mut c: i32 = g[0].iter().position(|&x| x == b'|').unwrap() as i32;
    let mut dr: i32 = 1;
    let mut dc: i32 = 0;
    let mut letters: Vec<u8> = Vec::new();
    let mut steps: i64 = 0;

    loop {
        let ch = at(&g, r, c);
        if ch == b' ' { break; }
        if ch.is_ascii_uppercase() {
            letters.push(ch);
        } else if ch == b'+' {
            if dr != 0 {
                if at(&g, r, c - 1) != b' ' { dr = 0; dc = -1; }
                else if at(&g, r, c + 1) != b' ' { dr = 0; dc = 1; }
            } else {
                if at(&g, r - 1, c) != b' ' { dr = -1; dc = 0; }
                else if at(&g, r + 1, c) != b' ' { dr = 1; dc = 0; }
            }
        }
        r += dr;
        c += dc;
        steps += 1;
    }

    (String::from_utf8(letters).unwrap(), steps)
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
    let ans = if part == 1 { p1 } else { p2.to_string() };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=19 part={} runtime_ms={:.3}", part, ms);
}
