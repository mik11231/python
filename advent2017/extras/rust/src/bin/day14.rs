use sha2::{Digest, Sha256};
use std::collections::VecDeque;
use std::env;
use std::fs;
use std::path::Path;
use std::sync::mpsc;
use std::thread;
use std::time::Instant;

const EXPECTED_SHA: &str = "354ac7a7409ec19ac2561c95f08ba4d0df1a26cdda409bef5ba594cff685eb0a";
const EXPECTED_PART1: &str = "8074";
const EXPECTED_PART2: &str = "1212";
const SUFFIX: [usize; 5] = [17, 31, 73, 47, 23];

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day14/d14_input.txt", "Day14/d14_input.txt", "../Day14/d14_input.txt", "../../Day14/d14_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn reverse_segment(a: &mut [u8], start: usize, len: usize) {
    let n = a.len();
    for i in 0..(len / 2) {
        let x = (start + i) % n;
        let y = (start + len - 1 - i) % n;
        a.swap(x, y);
    }
}

fn knot_hash_bytes(key: &str) -> [u8; 16] {
    let mut lengths = key.bytes().map(|b| b as usize).collect::<Vec<usize>>();
    lengths.extend(SUFFIX);

    let mut ring = (0u8..=255u8).collect::<Vec<u8>>();
    let (mut pos, mut skip) = (0usize, 0usize);
    for _ in 0..64 {
        for &ln in &lengths {
            reverse_segment(&mut ring, pos, ln);
            pos = (pos + ln + skip) % 256;
            skip += 1;
        }
    }

    let mut dense = [0u8; 16];
    for block in 0..16 {
        let mut x = 0u8;
        for &v in &ring[(block * 16)..((block + 1) * 16)] {
            x ^= v;
        }
        dense[block] = x;
    }
    dense
}

fn build_grid(seed: &str) -> ([[bool; 128]; 128], i64) {
    let mut g = [[false; 128]; 128];
    let mut used: i64 = 0;
    let max_threads = thread::available_parallelism().map(|n| n.get()).unwrap_or(1).min(16).min(128);
    let threads = if max_threads == 0 { 1 } else { max_threads };
    let (tx, rx) = mpsc::channel::<(usize, [bool; 128], i64)>();
    let seed_owned = seed.to_string();
    let mut handles = Vec::with_capacity(threads);

    for t in 0..threads {
        let txc = tx.clone();
        let seedc = seed_owned.clone();
        handles.push(thread::spawn(move || {
            let chunk = 128 / threads;
            let rem = 128 % threads;
            let start = t * chunk + t.min(rem);
            let end = start + chunk + usize::from(t < rem);
            for r in start..end {
                let h = knot_hash_bytes(&format!("{}-{}", seedc, r));
                let mut row = [false; 128];
                let mut row_used: i64 = 0;
                let mut c = 0usize;
                for b in h {
                    row_used += b.count_ones() as i64;
                    for bit in (0..8).rev() {
                        row[c] = ((b >> bit) & 1) == 1;
                        c += 1;
                    }
                }
                txc.send((r, row, row_used)).expect("send row");
            }
        }));
    }
    drop(tx);
    for (r, row, row_used) in rx {
        g[r] = row;
        used += row_used;
    }
    for h in handles {
        h.join().expect("join worker");
    }

    (g, used)
}

fn count_regions(g: &[[bool; 128]; 128]) -> i64 {
    let mut seen = [[false; 128]; 128];
    let mut regions: i64 = 0;

    for i in 0..128 {
        for j in 0..128 {
            if !g[i][j] || seen[i][j] { continue; }
            regions += 1;

            let mut q: VecDeque<(usize, usize)> = VecDeque::new();
            q.push_back((i, j));
            seen[i][j] = true;

            while let Some((x, y)) = q.pop_front() {
                let neigh = [
                    (x.wrapping_add(1), y),
                    (x.wrapping_sub(1), y),
                    (x, y.wrapping_add(1)),
                    (x, y.wrapping_sub(1)),
                ];
                for (nx, ny) in neigh {
                    if nx >= 128 || ny >= 128 { continue; }
                    if !g[nx][ny] || seen[nx][ny] { continue; }
                    seen[nx][ny] = true;
                    q.push_back((nx, ny));
                }
            }
        }
    }

    regions
}

fn solve(seed: &str) -> (i64, i64) {
    let (g, used) = build_grid(seed);
    (used, count_regions(&g))
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
    let seed = fs::read_to_string(&in_path).expect("read_to_string").trim().to_string();

    let t0 = Instant::now();
    let (p1, p2) = solve(&seed);
    let ans = if part == 1 { p1.to_string() } else { p2.to_string() };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=14 part={} runtime_ms={:.3}", part, ms);
}
