// Architecture Notes:
// - This file is heavily commented for long-term maintainability and reconstruction.
// - Pipeline shape is parse -> model -> compute -> emit.
// - Performance-sensitive sections document data-layout and concurrency tradeoffs.

use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "3fd999ac97824b5f8cd2bcbf5c69704a352a0a4bbf9735b0fcc289932fcaeac6";
const EXPECTED_PART1: &str = "mwzaxaj";
const EXPECTED_PART2: &str = "1219";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day7/d7_input.txt", "Day7/d7_input.txt", "../Day7/d7_input.txt", "../../Day7/d7_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn parse_tower(raw: &str) -> (HashMap<String, i32>, HashMap<String, Vec<String>>, HashMap<String, String>) {
    let mut weights: HashMap<String, i32> = HashMap::new();
    let mut children: HashMap<String, Vec<String>> = HashMap::new();
    let mut parent: HashMap<String, String> = HashMap::new();

    for line in raw.lines() {
        let line = line.trim();
        if line.is_empty() { continue; }

        let mut left = line;
        let mut right = "";
        if let Some(pos) = line.find("->") {
            left = line[..pos].trim();
            right = line[(pos + 2)..].trim();
        }

        let parts: Vec<&str> = left.split_whitespace().collect();
        let name = parts[0].to_string();
        let wt: i32 = parts[1].trim_matches(|c| c == '(' || c == ')').parse().expect("int");
        weights.insert(name.clone(), wt);

        let mut kids: Vec<String> = Vec::new();
        if !right.is_empty() {
            for tok in right.split(',') {
                let c = tok.trim().to_string();
                if c.is_empty() { continue; }
                parent.insert(c.clone(), name.clone());
                kids.push(c);
            }
        }
        children.insert(name, kids);
    }

    (weights, children, parent)
}

fn find_root(weights: &HashMap<String, i32>, parent: &HashMap<String, String>) -> String {
    for n in weights.keys() {
        if !parent.contains_key(n) { return n.clone(); }
    }
    panic!("no root");
}

fn solve_part2(weights: &HashMap<String, i32>, children: &HashMap<String, Vec<String>>, root: &str) -> i32 {
    fn total(n: &str, weights: &HashMap<String, i32>, children: &HashMap<String, Vec<String>>, memo: &mut HashMap<String, i32>) -> i32 {
        if let Some(v) = memo.get(n) { return *v; }
        let mut s = *weights.get(n).unwrap();
        if let Some(kids) = children.get(n) {
            for c in kids {
                s += total(c, weights, children, memo);
            }
        }
        memo.insert(n.to_string(), s);
        s
    }

    fn dfs(n: &str, weights: &HashMap<String, i32>, children: &HashMap<String, Vec<String>>, memo: &mut HashMap<String, i32>) -> Option<i32> {
        let kids = children.get(n).unwrap();
        if kids.is_empty() { return None; }

        let mut by_weight: HashMap<i32, Vec<String>> = HashMap::new();
        for c in kids {
            let tw = total(c, weights, children, memo);
            by_weight.entry(tw).or_default().push(c.clone());
        }
        if by_weight.len() <= 1 { return None; }

        let mut bad_total = 0;
        let mut good_total = 0;
        let mut bad_child = String::new();
        for (tw, group) in &by_weight {
            if group.len() == 1 {
                bad_total = *tw;
                bad_child = group[0].clone();
            } else {
                good_total = *tw;
            }
        }

        if let Some(v) = dfs(&bad_child, weights, children, memo) {
            return Some(v);
        }

        Some(weights[&bad_child] + (good_total - bad_total))
    }

    let mut memo: HashMap<String, i32> = HashMap::new();
    dfs(root, weights, children, &mut memo).expect("no imbalance")
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

    let (weights, children, parent) = parse_tower(&raw);
    let root = find_root(&weights, &parent);

    let t0 = Instant::now();
    let ans = if part == 1 { root } else { solve_part2(&weights, &children, &root).to_string() };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=7 part={} runtime_ms={:.3}", part, ms);
}
