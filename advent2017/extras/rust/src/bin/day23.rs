use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "866b77a4b5e37e19219792c97103a17d24c5f15a9f0bed448c0e6cfd75378beb";
const EXPECTED_PART1: &str = "3969";
const EXPECTED_PART2: &str = "917";

#[derive(Clone)]
struct Ins {
    op: String,
    x: String,
    y: String,
}

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() {
        return provided.to_string();
    }
    let cands = [
        "advent2017/Day23/d23_input.txt",
        "Day23/d23_input.txt",
        "../Day23/d23_input.txt",
        "../../Day23/d23_input.txt",
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

fn parse(text: &str) -> Vec<Ins> {
    text.lines()
        .map(|s| s.trim())
        .filter(|s| !s.is_empty())
        .map(|ln| {
            let p = ln.split_whitespace().collect::<Vec<&str>>();
            Ins {
                op: p[0].to_string(),
                x: p[1].to_string(),
                y: if p.len() > 2 {
                    p[2].to_string()
                } else {
                    "0".to_string()
                },
            }
        })
        .collect()
}

fn val(tok: &str, regs: &HashMap<String, i64>) -> i64 {
    tok.parse::<i64>().unwrap_or_else(|_| *regs.get(tok).unwrap_or(&0))
}

fn solve_part1(prog: &[Ins]) -> i64 {
    let mut regs: HashMap<String, i64> = HashMap::new();
    let mut ip: i64 = 0;
    let mut muls = 0;
    while ip >= 0 && (ip as usize) < prog.len() {
        let inx = &prog[ip as usize];
        match inx.op.as_str() {
            "set" => {
                regs.insert(inx.x.clone(), val(&inx.y, &regs));
            }
            "sub" => {
                let cur = *regs.get(&inx.x).unwrap_or(&0);
                regs.insert(inx.x.clone(), cur - val(&inx.y, &regs));
            }
            "mul" => {
                let cur = *regs.get(&inx.x).unwrap_or(&0);
                regs.insert(inx.x.clone(), cur * val(&inx.y, &regs));
                muls += 1;
            }
            "jnz" => {
                if val(&inx.x, &regs) != 0 {
                    ip += val(&inx.y, &regs);
                    continue;
                }
            }
            _ => panic!("bad op"),
        }
        ip += 1;
    }
    muls
}

fn is_prime(n: i64) -> bool {
    if n < 2 {
        return false;
    }
    if n % 2 == 0 {
        return n == 2;
    }
    let mut d = 3i64;
    while d * d <= n {
        if n % d == 0 {
            return false;
        }
        d += 2;
    }
    true
}

fn solve_part2(prog: &[Ins]) -> i64 {
    let b0: i64 = prog[0].y.parse().expect("int");
    let b = b0 * 100 + 100_000;
    let c = b + 17_000;
    let mut cnt = 0;
    let mut x = b;
    while x <= c {
        if !is_prime(x) {
            cnt += 1;
        }
        x += 17;
    }
    cnt
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
    let prog = parse(&fs::read_to_string(&in_path).expect("read_to_string"));

    let t0 = Instant::now();
    let ans = if part == 1 {
        solve_part1(&prog).to_string()
    } else {
        solve_part2(&prog).to_string()
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
    eprintln!("[rust-fancy] day=23 part={} runtime_ms={:.3}", part, ms);
}
