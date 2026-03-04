use sha2::{Digest, Sha256};
use std::collections::{HashMap, HashSet};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "489246369534515a9df814e8824f41c427d6c02ab31d7b5c07cbdc935497f2ba";
const EXPECTED_PART1: &str = "12841";
const EXPECTED_PART2: &str = "8038";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() {
        return provided.to_string();
    }
    let cands = ["advent2017/Day6/d6_input.txt", "Day6/d6_input.txt", "../Day6/d6_input.txt", "../../Day6/d6_input.txt"];
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

fn parse_banks(raw: &str) -> Vec<i32> {
    raw.split_whitespace().map(|x| x.parse::<i32>().expect("int")).collect::<Vec<i32>>()
}

fn redistribute(a: &mut [i32]) {
    let mut idx: usize = 0;
    for i in 1..a.len() {
        if a[i] > a[idx] {
            idx = i;
        }
    }
    let blocks = a[idx];
    a[idx] = 0;

    let n = a.len() as i32;
    let q = blocks / n;
    let r = blocks % n;
    if q > 0 {
        for v in a.iter_mut() {
            *v += q;
        }
    }
    for k in 1..=r {
        let j = ((idx as i32 + k) % n) as usize;
        a[j] += 1;
    }
}

fn solve_part1(banks: &[i32]) -> i64 {
    let mut a = banks.to_vec();
    let mut seen: HashSet<Vec<i32>> = HashSet::new();
    let mut steps: i64 = 0;
    while !seen.contains(&a) {
        seen.insert(a.clone());
        redistribute(&mut a);
        steps += 1;
    }
    steps
}

fn solve_part2(banks: &[i32]) -> i64 {
    let mut a = banks.to_vec();
    let mut seen: HashMap<Vec<i32>, i64> = HashMap::new();
    let mut steps: i64 = 0;
    while !seen.contains_key(&a) {
        seen.insert(a.clone(), steps);
        redistribute(&mut a);
        steps += 1;
    }
    steps - seen[&a]
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
    let banks = parse_banks(&fs::read_to_string(&in_path).expect("read_to_string"));

    let t0 = Instant::now();
    let ans = if part == 1 { solve_part1(&banks) } else { solve_part2(&banks) }.to_string();
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected {
        panic!("answer mismatch");
    }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=6 part={} runtime_ms={:.3}", part, ms);
}
