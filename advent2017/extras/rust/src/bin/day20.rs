use sha2::{Digest, Sha256};
use std::collections::{HashMap, HashSet};
use std::env;
use std::fs;
use std::path::Path;
use std::time::Instant;

const EXPECTED_SHA: &str = "9480ad6f4d423780a0542e172e614170ec28d3eb06c80b7c2b452c6ceeecbfb0";
const EXPECTED_PART1: &str = "144";
const EXPECTED_PART2: &str = "477";

#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
struct V3 {
    x: i64,
    y: i64,
    z: i64,
}

#[derive(Clone, Copy, Debug)]
struct Particle {
    p: V3,
    v: V3,
    a: V3,
}

fn resolve_input(provided: &str) -> String {
    if !provided.is_empty() {
        return provided.to_string();
    }
    let cands = [
        "advent2017/Day20/d20_input.txt",
        "Day20/d20_input.txt",
        "../Day20/d20_input.txt",
        "../../Day20/d20_input.txt",
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

fn parse(input: &str) -> Vec<Particle> {
    let mut out = Vec::new();
    for ln in input.lines() {
        let s = ln.trim();
        if s.is_empty() {
            continue;
        }
        let nums: Vec<i64> = s
            .split(|c: char| !(c == '-' || c.is_ascii_digit()))
            .filter(|t| !t.is_empty())
            .map(|x| x.parse::<i64>().expect("int"))
            .collect();
        assert!(nums.len() == 9, "bad line: {}", s);
        out.push(Particle {
            p: V3 {
                x: nums[0],
                y: nums[1],
                z: nums[2],
            },
            v: V3 {
                x: nums[3],
                y: nums[4],
                z: nums[5],
            },
            a: V3 {
                x: nums[6],
                y: nums[7],
                z: nums[8],
            },
        });
    }
    out
}

fn manhattan(v: V3) -> i64 {
    v.x.abs() + v.y.abs() + v.z.abs()
}

fn solve_part1(ps: &[Particle]) -> usize {
    ps.iter()
        .enumerate()
        .min_by_key(|(i, p)| (manhattan(p.a), manhattan(p.v), manhattan(p.p), *i))
        .map(|(i, _)| i)
        .expect("non-empty")
}

fn isqrt(n: i128) -> i128 {
    if n <= 0 {
        return 0;
    }
    let mut x = (n as f64).sqrt() as i128;
    while (x + 1) * (x + 1) <= n {
        x += 1;
    }
    while x * x > n {
        x -= 1;
    }
    x
}

fn solve_axis(dp: i64, dv: i64, da: i64) -> (bool, HashSet<i64>) {
    // da*t^2 + (da + 2*dv)*t + 2*dp = 0
    let mut out = HashSet::new();
    if da == 0 && dv == 0 {
        return (dp == 0, out);
    }
    if da == 0 {
        if dv != 0 && (-dp) % dv == 0 {
            let t = (-dp) / dv;
            if t >= 0 {
                out.insert(t);
            }
        }
        return (false, out);
    }
    let b = da as i128 + 2 * dv as i128;
    let c = 2 * dp as i128;
    let a = da as i128;
    let disc = b * b - 4 * a * c;
    if disc < 0 {
        return (false, out);
    }
    let s = isqrt(disc);
    if s * s != disc {
        return (false, out);
    }
    let den = 2 * a;
    for num in [-b + s, -b - s] {
        if den != 0 && num % den == 0 {
            let t = num / den;
            if t >= 0 && t <= i64::MAX as i128 {
                out.insert(t as i64);
            }
        }
    }
    (false, out)
}

fn position_at(p: Particle, t: i64) -> V3 {
    V3 {
        x: p.p.x + p.v.x * t + p.a.x * t * (t + 1) / 2,
        y: p.p.y + p.v.y * t + p.a.y * t * (t + 1) / 2,
        z: p.p.z + p.v.z * t + p.a.z * t * (t + 1) / 2,
    }
}

fn pair_times(a: Particle, b: Particle) -> HashSet<i64> {
    let (ax_any, ax) = solve_axis(a.p.x - b.p.x, a.v.x - b.v.x, a.a.x - b.a.x);
    let (ay_any, ay) = solve_axis(a.p.y - b.p.y, a.v.y - b.v.y, a.a.y - b.a.y);
    let (az_any, az) = solve_axis(a.p.z - b.p.z, a.v.z - b.v.z, a.a.z - b.a.z);
    let mut sets = Vec::new();
    if !ax_any {
        sets.push(ax);
    }
    if !ay_any {
        sets.push(ay);
    }
    if !az_any {
        sets.push(az);
    }
    if sets.is_empty() {
        return HashSet::new();
    }
    let mut it = sets.into_iter();
    let mut cur = it.next().expect("set");
    for s in it {
        cur = cur.intersection(&s).copied().collect();
        if cur.is_empty() {
            break;
        }
    }
    cur
}

fn solve_part2(ps: &[Particle]) -> usize {
    let n = ps.len();
    let mut events: HashMap<i64, Vec<(usize, usize)>> = HashMap::new();
    for i in 0..n {
        for j in (i + 1)..n {
            for t in pair_times(ps[i], ps[j]) {
                events.entry(t).or_default().push((i, j));
            }
        }
    }

    let mut times: Vec<i64> = events.keys().copied().collect();
    times.sort_unstable();
    let mut alive = vec![true; n];
    let mut left = n;

    for t in times {
        let pairs = events.get(&t).expect("events");
        let mut involved: HashSet<usize> = HashSet::new();
        for (i, j) in pairs {
            if alive[*i] && alive[*j] {
                involved.insert(*i);
                involved.insert(*j);
            }
        }
        if involved.len() < 2 {
            continue;
        }
        let mut groups: HashMap<V3, Vec<usize>> = HashMap::new();
        for i in involved {
            groups.entry(position_at(ps[i], t)).or_default().push(i);
        }
        for ids in groups.values() {
            if ids.len() > 1 {
                for i in ids {
                    if alive[*i] {
                        alive[*i] = false;
                        left -= 1;
                    }
                }
            }
        }
    }
    left
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
    let text = fs::read_to_string(&in_path).expect("read_to_string");
    let particles = parse(&text);

    let t0 = Instant::now();
    let ans = if part == 1 {
        solve_part1(&particles).to_string()
    } else {
        solve_part2(&particles).to_string()
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
    eprintln!("[rust-fancy] day=20 part={} runtime_ms={:.3}", part, ms);
}
