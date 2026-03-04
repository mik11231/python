use sha2::{Digest, Sha256};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "c64165a1af8ab4877e736a095bde2b22d523468077099fab5a338f53b0059681";
const EXPECTED_PART1: &str = "36174";
const EXPECTED_PART2: &str = "244";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() {
        return provided.to_string();
    }
    let cands = [
        "advent2017/Day2/d2_input.txt",
        "Day2/d2_input.txt",
        "../Day2/d2_input.txt",
        "../../Day2/d2_input.txt",
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

fn parse_rows(raw: &str) -> Vec<Vec<i64>> {
    raw.lines()
        .filter_map(|line| {
            let line = line.trim();
            if line.is_empty() {
                None
            } else {
                Some(
                    line.split_whitespace()
                        .map(|x| x.parse::<i64>().expect("int"))
                        .collect::<Vec<i64>>(),
                )
            }
        })
        .collect::<Vec<Vec<i64>>>()
}

fn solve_part1(rows: &[Vec<i64>]) -> i64 {
    rows.iter()
        .map(|row| row.iter().max().unwrap() - row.iter().min().unwrap())
        .sum()
}

fn solve_part2(rows: &[Vec<i64>]) -> i64 {
    let mut total: i64 = 0;
    for row in rows {
        let mut found = false;
        for (i, a) in row.iter().enumerate() {
            for (j, b) in row.iter().enumerate() {
                if i == j {
                    continue;
                }
                if *b != 0 && a % b == 0 {
                    total += a / b;
                    found = true;
                    break;
                }
            }
            if found {
                break;
            }
        }
        if !found {
            panic!("no divisible pair found");
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
        panic!("--part 1|2 required")
    }

    let in_path = resolve_input(&input);
    if sha256_file(&in_path) != EXPECTED_SHA {
        panic!("checksum mismatch");
    }
    let raw = fs::read_to_string(&in_path).expect("read_to_string");
    let rows = parse_rows(&raw);

    let t0 = Instant::now();
    let (ans, expected) = if part == 1 {
        (solve_part1(&rows).to_string(), EXPECTED_PART1)
    } else {
        (solve_part2(&rows).to_string(), EXPECTED_PART2)
    };

    if ans != expected {
        panic!("answer mismatch");
    }
    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=2 part={} runtime_ms={:.3}", part, ms);
}
