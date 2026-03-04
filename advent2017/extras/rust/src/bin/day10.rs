use sha2::{Digest, Sha256};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "b83c8a7c9fb42d39b4545428717df7858882f3644a62d2770c235c9eb61ace69";
const EXPECTED_PART1: &str = "54675";
const EXPECTED_PART2: &str = "a7af2706aa9a09cf5d848c1e6605dd2a";
const SUFFIX: [usize; 5] = [17, 31, 73, 47, 23];

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() {
        return provided.to_string();
    }
    let cands = ["advent2017/Day10/d10_input.txt", "Day10/d10_input.txt", "../Day10/d10_input.txt", "../../Day10/d10_input.txt"];
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

fn reverse_segment(a: &mut [u8], start: usize, len: usize) {
    let n = a.len();
    for i in 0..(len / 2) {
        let x = (start + i) % n;
        let y = (start + len - 1 - i) % n;
        a.swap(x, y);
    }
}

fn run_round(a: &mut [u8], lengths: &[usize], mut pos: usize, mut skip: usize) -> (usize, usize) {
    let n = a.len();
    for &len in lengths {
        reverse_segment(a, pos, len);
        pos = (pos + len + skip) % n;
        skip += 1;
    }
    (pos, skip)
}

fn solve_part1(raw: &str) -> i64 {
    let lengths = raw
        .trim()
        .split(',')
        .filter(|x| !x.trim().is_empty())
        .map(|x| x.trim().parse::<usize>().expect("int"))
        .collect::<Vec<usize>>();

    let mut ring = (0u8..=255u8).collect::<Vec<u8>>();
    run_round(&mut ring, &lengths, 0, 0);
    (ring[0] as i64) * (ring[1] as i64)
}

fn solve_part2(raw: &str) -> String {
    let mut lengths = raw.trim().bytes().map(|b| b as usize).collect::<Vec<usize>>();
    lengths.extend(SUFFIX);

    let mut ring = (0u8..=255u8).collect::<Vec<u8>>();
    let (mut pos, mut skip) = (0usize, 0usize);
    for _ in 0..64 {
        (pos, skip) = run_round(&mut ring, &lengths, pos, skip);
    }

    let mut dense = [0u8; 16];
    for block in 0..16 {
        let mut x = 0u8;
        for &v in &ring[(block * 16)..((block + 1) * 16)] {
            x ^= v;
        }
        dense[block] = x;
    }
    hex::encode(dense)
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
    let raw = fs::read_to_string(&in_path).expect("read_to_string");

    let t0 = Instant::now();
    let ans = if part == 1 {
        solve_part1(&raw).to_string()
    } else {
        solve_part2(&raw)
    };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected {
        panic!("answer mismatch");
    }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=10 part={} runtime_ms={:.3}", part, ms);
}
