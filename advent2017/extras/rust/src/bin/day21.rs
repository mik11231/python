use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "759a25acf919be68478e4d20d3856f488ff79325d0954d8ca5c89cecc2fd8287";
const EXPECTED_PART1: &str = "139";
const EXPECTED_PART2: &str = "1857134";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() {
        return provided.to_string();
    }
    let cands = [
        "advent2017/Day21/d21_input.txt",
        "Day21/d21_input.txt",
        "../Day21/d21_input.txt",
        "../../Day21/d21_input.txt",
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

fn rotate(p: &[String]) -> Vec<String> {
    let n = p.len();
    let mut out = vec![String::new(); n];
    for c in 0..n {
        let mut row = String::with_capacity(n);
        for r in 0..n {
            row.push(p[n - 1 - r].as_bytes()[c] as char);
        }
        out[c] = row;
    }
    out
}

fn flip(p: &[String]) -> Vec<String> {
    p.iter()
        .map(|r| r.chars().rev().collect::<String>())
        .collect::<Vec<String>>()
}

fn canonical(p: &[String]) -> String {
    let mut cur = p.to_vec();
    let mut vars = Vec::with_capacity(8);
    for _ in 0..4 {
        vars.push(cur.join("/"));
        vars.push(flip(&cur).join("/"));
        cur = rotate(&cur);
    }
    vars.sort_unstable();
    vars[0].clone()
}

fn parse_rules(text: &str) -> HashMap<String, Vec<String>> {
    let mut rules = HashMap::new();
    for ln in text.lines() {
        let s = ln.trim();
        if s.is_empty() {
            continue;
        }
        let mut it = s.split(" => ");
        let inp = it
            .next()
            .expect("lhs")
            .split('/')
            .map(|x| x.to_string())
            .collect::<Vec<String>>();
        let out = it
            .next()
            .expect("rhs")
            .split('/')
            .map(|x| x.to_string())
            .collect::<Vec<String>>();
        rules.insert(canonical(&inp), out);
    }
    rules
}

fn enhance(grid: &[String], rules: &HashMap<String, Vec<String>>) -> Vec<String> {
    let n = grid.len();
    let bs = if n % 2 == 0 { 2 } else { 3 };
    let os = bs + 1;
    let cnt = n / bs;
    let new_n = cnt * os;
    let mut out = vec![vec!['.'; new_n]; new_n];
    for br in 0..cnt {
        for bc in 0..cnt {
            let mut sub = Vec::with_capacity(bs);
            for r in 0..bs {
                sub.push(grid[br * bs + r][bc * bs..bc * bs + bs].to_string());
            }
            let rep = rules.get(&canonical(&sub)).expect("rule");
            for r in 0..os {
                for c in 0..os {
                    out[br * os + r][bc * os + c] = rep[r].as_bytes()[c] as char;
                }
            }
        }
    }
    out.into_iter()
        .map(|row| row.into_iter().collect::<String>())
        .collect()
}

fn run_iterative(rules: &HashMap<String, Vec<String>>, iters: usize) -> usize {
    let mut grid = vec![".#.".to_string(), "..#".to_string(), "###".to_string()];
    for _ in 0..iters {
        grid = enhance(&grid, rules);
    }
    grid.iter()
        .map(|r| r.bytes().filter(|&b| b == b'#').count())
        .sum()
}

fn split_blocks(grid: &[String], bs: usize) -> Vec<String> {
    let n = grid.len();
    let cnt = n / bs;
    let mut out = Vec::with_capacity(cnt * cnt);
    for br in 0..cnt {
        for bc in 0..cnt {
            let mut sub = Vec::with_capacity(bs);
            for r in 0..bs {
                sub.push(grid[br * bs + r][bc * bs..bc * bs + bs].to_string());
            }
            out.push(sub.join("/"));
        }
    }
    out
}

fn popcount_key(k: &str) -> usize {
    k.bytes().filter(|&b| b == b'#').count()
}

fn run_optimized(rules: &HashMap<String, Vec<String>>, iters: usize) -> usize {
    if iters <= 5 || iters % 3 != 0 {
        return run_iterative(rules, iters);
    }
    let mut memo_expand: HashMap<String, Vec<String>> = HashMap::new();
    let mut memo_count: HashMap<(String, usize), usize> = HashMap::new();

    fn expand_three_from_3(
        k: &str,
        rules: &HashMap<String, Vec<String>>,
        memo_expand: &mut HashMap<String, Vec<String>>,
    ) -> Vec<String> {
        if let Some(v) = memo_expand.get(k) {
            return v.clone();
        }
        let mut g = k.split('/').map(|s| s.to_string()).collect::<Vec<String>>();
        g = enhance(&g, rules);
        g = enhance(&g, rules);
        g = enhance(&g, rules);
        let out = split_blocks(&g, 3);
        memo_expand.insert(k.to_string(), out.clone());
        out
    }

    fn count_cycles(
        k: &str,
        cycles: usize,
        rules: &HashMap<String, Vec<String>>,
        memo_expand: &mut HashMap<String, Vec<String>>,
        memo_count: &mut HashMap<(String, usize), usize>,
    ) -> usize {
        if let Some(v) = memo_count.get(&(k.to_string(), cycles)) {
            return *v;
        }
        let v = if cycles == 0 {
            popcount_key(k)
        } else {
            expand_three_from_3(k, rules, memo_expand)
                .iter()
                .map(|sub| count_cycles(sub, cycles - 1, rules, memo_expand, memo_count))
                .sum()
        };
        memo_count.insert((k.to_string(), cycles), v);
        v
    }

    count_cycles(
        ".#./..#/###",
        iters / 3,
        rules,
        &mut memo_expand,
        &mut memo_count,
    )
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
    let rules = parse_rules(&fs::read_to_string(&in_path).expect("read_to_string"));

    let t0 = Instant::now();
    let ans = if part == 1 {
        run_optimized(&rules, 5).to_string()
    } else {
        run_optimized(&rules, 18).to_string()
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
    eprintln!("[rust-fancy] day=21 part={} runtime_ms={:.3}", part, ms);
}
