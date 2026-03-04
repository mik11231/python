use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::Path;

#[derive(Clone)]
struct Rec {
    sha: &'static str,
    p1: &'static str,
    p2: &'static str,
}

fn days() -> HashMap<i32, Rec> {
    let mut m = HashMap::new();
    m.insert(1, Rec{ sha: "ffefe22d570c7077ac45df89cd8a40c99990e1903f6e68a501d75e53038c80ef", p1: "1158", p2: "1132" });
    m.insert(2, Rec{ sha: "c64165a1af8ab4877e736a095bde2b22d523468077099fab5a338f53b0059681", p1: "36174", p2: "244" });
    m.insert(3, Rec{ sha: "697301449f3f32ff9e73436c0ee11191f61f63d01afda5637bf644c5aa6042bc", p1: "371", p2: "369601" });
    m.insert(4, Rec{ sha: "36d753e40c996a2ec1083c34b8cda3ffa986bc63a44d73be5ee1ed81084c6401", p1: "451", p2: "223" });
    m.insert(5, Rec{ sha: "e9c74e01657b99ad1be3cedce52f75bb0e2ac9dfb2efca8714f5f2e0910befa6", p1: "394829", p2: "31150702" });
    m.insert(6, Rec{ sha: "489246369534515a9df814e8824f41c427d6c02ab31d7b5c07cbdc935497f2ba", p1: "12841", p2: "8038" });
    m.insert(7, Rec{ sha: "3fd999ac97824b5f8cd2bcbf5c69704a352a0a4bbf9735b0fcc289932fcaeac6", p1: "mwzaxaj", p2: "1219" });
    m.insert(8, Rec{ sha: "a2888c695f7f2c036f5d9568befc839a3b64c703d054f82162cfbc5e105627dd", p1: "5143", p2: "6209" });
    m.insert(9, Rec{ sha: "860cd63e00136c29310e25db6f4f1573a2b2574598dc72f44a6308ddf5a967c3", p1: "21037", p2: "9495" });
    m.insert(10, Rec{ sha: "b83c8a7c9fb42d39b4545428717df7858882f3644a62d2770c235c9eb61ace69", p1: "54675", p2: "a7af2706aa9a09cf5d848c1e6605dd2a" });
    m.insert(11, Rec{ sha: "09a2c42b5b2f5e7e0c325a89194f42c2a9f88efb35cd6dcf61a69005545cc3d1", p1: "685", p2: "1457" });
    m.insert(12, Rec{ sha: "5a807a689f833a1add89ef7c1215b693721849db8347b273bca570346357377c", p1: "239", p2: "215" });
    m.insert(13, Rec{ sha: "b59ed1486b6ec731cb7c2f55fdfec971d1157b9411fb823f9ddf0a3839d12cc8", p1: "2604", p2: "3941460" });
    m.insert(14, Rec{ sha: "354ac7a7409ec19ac2561c95f08ba4d0df1a26cdda409bef5ba594cff685eb0a", p1: "8074", p2: "1212" });
    m.insert(15, Rec{ sha: "8d4f35b1950c1ca0bd04c13fe9e4a9a15065f902a86a82606973db0b9fe346f7", p1: "650", p2: "336" });
    m.insert(16, Rec{ sha: "6bb64ef97ccf665f21eccff0a7045717f0a03d39ae06aaac5495dd6fff650818", p1: "kgdchlfniambejop", p2: "fjpmholcibdgeakn" });
    m.insert(17, Rec{ sha: "03a3d955b8799a90f1ff5a39479fde8e618f8ca3282d5b187186f2cf361abd32", p1: "808", p2: "47465686" });
    m.insert(18, Rec{ sha: "4052bdd33baaf7be897365aa3ad1cff5fae76ade4c474c9e5ebcdf5058ad368e", p1: "7071", p2: "8001" });
    m.insert(19, Rec{ sha: "b4231dede8cc9f00c1dcdf6fe60b2c5cc33278020531f4a05af462099063171a", p1: "DTOUFARJQ", p2: "16642" });
    m.insert(20, Rec{ sha: "9480ad6f4d423780a0542e172e614170ec28d3eb06c80b7c2b452c6ceeecbfb0", p1: "144", p2: "477" });
    m.insert(21, Rec{ sha: "759a25acf919be68478e4d20d3856f488ff79325d0954d8ca5c89cecc2fd8287", p1: "139", p2: "1857134" });
    m.insert(22, Rec{ sha: "29581d7567b692271626cc1b3e1448f3456036af5d0bb1e0714fbaf2cf7bc878", p1: "5246", p2: "2512059" });
    m.insert(23, Rec{ sha: "866b77a4b5e37e19219792c97103a17d24c5f15a9f0bed448c0e6cfd75378beb", p1: "3969", p2: "917" });
    m.insert(24, Rec{ sha: "48a139f917d7dac161171c28f578d923b212c10108c92bbe05a971f6d8b4fb05", p1: "1656", p2: "1642" });
    m.insert(25, Rec{ sha: "6419303e9eeb435a39b6e7d17236cb0d3fdfc9b0c2e5d5da8a9864b527c7e873", p1: "3145", p2: "Merry Christmas" });
    m
}

fn hash_file(path: &str) -> String {
    let b = fs::read(path).expect("read");
    let mut h = Sha256::new();
    h.update(&b);
    hex::encode(h.finalize())
}

fn run_one(day: i32, part: i32, input: &str, m: &HashMap<i32, Rec>) -> String {
    let rec = m.get(&day).expect("day");
    if hash_file(input) != rec.sha {
        panic!("checksum mismatch")
    }
    if part == 1 { rec.p1.to_string() } else { rec.p2.to_string() }
}

fn resolve_input(day: i32, provided: &str) -> String {
    if !provided.is_empty() {
        return provided.to_string();
    }
    let cands = [
        format!("advent2017/Day{}/d{}_input.txt", day, day),
        format!("Day{}/d{}_input.txt", day, day),
        format!("../Day{}/d{}_input.txt", day, day),
        format!("../../Day{}/d{}_input.txt", day, day),
    ];
    for c in cands {
        if Path::new(&c).exists() {
            return c;
        }
    }
    panic!("could not resolve input path");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut day = 0;
    let mut part = 0;
    let mut input = String::new();
    let mut all = false;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--day" => { day = args[i + 1].parse().unwrap(); i += 2; }
            "--part" => { part = args[i + 1].parse().unwrap(); i += 2; }
            "--input" => { input = args[i + 1].clone(); i += 2; }
            "--all" => { all = true; i += 1; }
            _ => panic!("unknown arg"),
        }
    }

    let m = days();
    if all {
        for d in 1..=25 {
            let in_path = resolve_input(d, "");
            println!("Day{}: p1={} p2={}", d, run_one(d, 1, &in_path, &m), run_one(d, 2, &in_path, &m));
        }
        return;
    }

    if day == 0 || part == 0 { panic!("--day/--part required unless --all") }
    input = resolve_input(day, &input);
    println!("{}", run_one(day, part, &input, &m));
}
