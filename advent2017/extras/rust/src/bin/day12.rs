// Architecture Notes:
// - This file is heavily commented for long-term maintainability and reconstruction.
// - Pipeline shape is parse -> model -> compute -> emit.
// - Performance-sensitive sections document data-layout and concurrency tradeoffs.

use sha2::{Digest, Sha256};
use std::collections::{HashMap, HashSet, VecDeque};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "5a807a689f833a1add89ef7c1215b693721849db8347b273bca570346357377c";
const EXPECTED_PART1: &str = "239";
const EXPECTED_PART2: &str = "215";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day12/d12_input.txt", "Day12/d12_input.txt", "../Day12/d12_input.txt", "../../Day12/d12_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn parse_graph(raw: &str) -> HashMap<i32, Vec<i32>> {
    let mut g: HashMap<i32, Vec<i32>> = HashMap::new();
    for line in raw.lines() {
        let line = line.trim();
        if line.is_empty() { continue; }
        let parts = line.split("<->").map(|x| x.trim()).collect::<Vec<&str>>();
        let u: i32 = parts[0].parse().expect("int");
        let nbrs = parts[1]
            .split(',')
            .map(|x| x.trim().parse::<i32>().expect("int"))
            .collect::<Vec<i32>>();
        g.insert(u, nbrs);
    }
    g
}

fn bfs_component(g: &HashMap<i32, Vec<i32>>, start: i32, seen: &mut HashSet<i32>) -> usize {
    let mut q: VecDeque<i32> = VecDeque::new();
    q.push_back(start);
    seen.insert(start);
    let mut count: usize = 0;

    while let Some(u) = q.pop_front() {
        count += 1;
        if let Some(nbrs) = g.get(&u) {
            for v in nbrs {
                if seen.contains(v) { continue; }
                seen.insert(*v);
                q.push_back(*v);
            }
        }
    }

    count
}

fn solve(raw: &str) -> (usize, usize) {
    let g = parse_graph(raw);
    let mut seen: HashSet<i32> = HashSet::new();

    let group0 = bfs_component(&g, 0, &mut seen);
    let mut groups = 1usize;

    for node in g.keys() {
        if seen.contains(node) { continue; }
        bfs_component(&g, *node, &mut seen);
        groups += 1;
    }

    (group0, groups)
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
    let ans = if part == 1 { p1.to_string() } else { p2.to_string() };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=12 part={} runtime_ms={:.3}", part, ms);
}
