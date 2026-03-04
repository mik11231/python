use sha2::{Digest, Sha256};
use std::collections::{HashMap, HashSet};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "29581d7567b692271626cc1b3e1448f3456036af5d0bb1e0714fbaf2cf7bc878";
const EXPECTED_PART1: &str = "5246";
const EXPECTED_PART2: &str = "2512059";

#[inline(always)]
fn pack_pos(r: i32, c: i32) -> u64 {
    ((r as u32 as u64) << 32) | (c as u32 as u64)
}

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() {
        return provided.to_string();
    }
    let cands = [
        "advent2017/Day22/d22_input.txt",
        "Day22/d22_input.txt",
        "../Day22/d22_input.txt",
        "../../Day22/d22_input.txt",
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

fn parse(text: &str) -> HashSet<u64> {
    let lines: Vec<&str> = text.lines().map(|s| s.trim()).filter(|s| !s.is_empty()).collect();
    let n = lines.len() as i32;
    let off = n / 2;
    let mut inf = HashSet::new();
    for (r, row) in lines.iter().enumerate() {
        for (c, ch) in row.bytes().enumerate() {
            if ch == b'#' {
                inf.insert(pack_pos(r as i32 - off, c as i32 - off));
            }
        }
    }
    inf
}

fn solve_part1(inf0: &HashSet<u64>) -> i32 {
    let mut inf = inf0.clone();
    let (mut r, mut c) = (0i32, 0i32);
    let (mut dr, mut dc) = (-1i32, 0i32);
    let mut made = 0;
    for _ in 0..10_000 {
        let p = pack_pos(r, c);
        if inf.contains(&p) {
            (dr, dc) = (dc, -dr);
            inf.remove(&p);
        } else {
            (dr, dc) = (-dc, dr);
            inf.insert(p);
            made += 1;
        }
        r += dr;
        c += dc;
    }
    made
}

fn solve_part2(inf0: &HashSet<u64>) -> i32 {
    // 0 clean, 1 weakened, 2 infected, 3 flagged
    let mut state: HashMap<u64, u8> = HashMap::with_capacity(inf0.len() * 16 + 1024);
    for &p in inf0 {
        state.insert(p, 2);
    }
    let (mut r, mut c) = (0i32, 0i32);
    let (mut dr, mut dc) = (-1i32, 0i32);
    let mut made = 0;
    for _ in 0..10_000_000 {
        let p = pack_pos(r, c);
        let s = *state.get(&p).unwrap_or(&0);
        match s {
            0 => {
                (dr, dc) = (-dc, dr);
                state.insert(p, 1);
            }
            1 => {
                state.insert(p, 2);
                made += 1;
            }
            2 => {
                (dr, dc) = (dc, -dr);
                state.insert(p, 3);
            }
            _ => {
                (dr, dc) = (-dr, -dc);
                state.remove(&p);
            }
        }
        r += dr;
        c += dc;
    }
    made
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
    let inf = parse(&fs::read_to_string(&in_path).expect("read_to_string"));

    let t0 = Instant::now();
    let ans = if part == 1 {
        solve_part1(&inf).to_string()
    } else {
        solve_part2(&inf).to_string()
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
    eprintln!("[rust-fancy] day=22 part={} runtime_ms={:.3}", part, ms);
}
