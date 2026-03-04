use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "6bb64ef97ccf665f21eccff0a7045717f0a03d39ae06aaac5495dd6fff650818";
const EXPECTED_PART1: &str = "kgdchlfniambejop";
const EXPECTED_PART2: &str = "fjpmholcibdgeakn";

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() { return provided.to_string(); }
    let cands = ["advent2017/Day16/d16_input.txt", "Day16/d16_input.txt", "../Day16/d16_input.txt", "../../Day16/d16_input.txt"];
    for c in cands { if Path::new(c).exists() { return c.to_string(); } }
    panic!("input not found");
}

fn sha256_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new(); h.update(&b); hex::encode(h.finalize())
}

fn parse_moves(raw: &str) -> Vec<String> {
    raw.trim().split(',').map(|x| x.trim().to_string()).filter(|x| !x.is_empty()).collect()
}

fn apply_once(state: &mut Vec<u8>, moves: &[String]) {
    for mv in moves {
        let t = mv.as_bytes()[0] as char;
        let arg = &mv[1..];
        match t {
            's' => {
                let x: usize = arg.parse().expect("int");
                let n = state.len();
                let mut tmp = state[(n - x)..].to_vec();
                tmp.extend_from_slice(&state[..(n - x)]);
                *state = tmp;
            }
            'x' => {
                let p = arg.split('/').collect::<Vec<&str>>();
                let a: usize = p[0].parse().expect("int");
                let b: usize = p[1].parse().expect("int");
                state.swap(a, b);
            }
            'p' => {
                let p = arg.split('/').collect::<Vec<&str>>();
                let a = p[0].as_bytes()[0];
                let b = p[1].as_bytes()[0];
                let ia = state.iter().position(|&c| c == a).unwrap();
                let ib = state.iter().position(|&c| c == b).unwrap();
                state.swap(ia, ib);
            }
            _ => panic!("bad move"),
        }
    }
}

fn dance(moves: &[String], rounds: usize) -> String {
    let mut state = b"abcdefghijklmnop".to_vec();
    let mut seen: HashMap<String, usize> = HashMap::new();
    let mut i = 0usize;

    while i < rounds {
        let key = String::from_utf8(state.clone()).unwrap();
        if let Some(prev) = seen.get(&key) {
            let cycle = i - prev;
            let rem = (rounds - i) % cycle;
            for _ in 0..rem { apply_once(&mut state, moves); }
            return String::from_utf8(state).unwrap();
        }
        seen.insert(key, i);
        apply_once(&mut state, moves);
        i += 1;
    }

    String::from_utf8(state).unwrap()
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
    let moves = parse_moves(&fs::read_to_string(&in_path).expect("read_to_string"));

    let t0 = Instant::now();
    let ans = if part == 1 { dance(&moves, 1) } else { dance(&moves, 1_000_000_000) };
    let expected = if part == 1 { EXPECTED_PART1 } else { EXPECTED_PART2 };
    if ans != expected { panic!("answer mismatch"); }

    println!("{}", ans);
    let ms = t0.elapsed().as_nanos() as f64 / 1e6;
    eprintln!("[rust-fancy] day=16 part={} runtime_ms={:.3}", part, ms);
}
