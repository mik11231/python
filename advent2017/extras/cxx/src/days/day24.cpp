#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
#include <openssl/sha.h>

namespace {
constexpr const char* EXPECTED_SHA = "48a139f917d7dac161171c28f578d923b212c10108c92bbe05a971f6d8b4fb05";
constexpr const char* EXPECTED_PART1 = "1656";
constexpr const char* EXPECTED_PART2 = "1642";

struct Comp {
    int a, b;
};
struct Ret {
    int s, l, ls;
};

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    std::vector<std::string> cands = {
        "advent2017/Day24/d24_input.txt",
        "Day24/d24_input.txt",
        "../Day24/d24_input.txt",
        "../../Day24/d24_input.txt",
    };
    for (const auto& c : cands) {
        std::ifstream f(c);
        if (f.good()) return c;
    }
    throw std::runtime_error("input not found");
}

std::string sha256_file(const std::string& path) {
    std::ifstream f(path, std::ios::binary);
    if (!f) throw std::runtime_error("read fail");
    std::vector<unsigned char> b((std::istreambuf_iterator<char>(f)), {});
    unsigned char out[SHA256_DIGEST_LENGTH];
    SHA256(b.data(), b.size(), out);
    static const char* HEX = "0123456789abcdef";
    std::string s;
    s.reserve(64);
    for (unsigned char v : out) {
        s.push_back(HEX[v >> 4]);
        s.push_back(HEX[v & 15]);
    }
    return s;
}

void parse(const std::string& path, std::vector<Comp>& comps, std::unordered_map<int, std::vector<int>>& by) {
    std::ifstream f(path);
    if (!f) throw std::runtime_error("open fail");
    std::string line;
    while (std::getline(f, line)) {
        if (line.empty()) continue;
        auto slash = line.find('/');
        int a = std::stoi(line.substr(0, slash));
        int b = std::stoi(line.substr(slash + 1));
        int i = static_cast<int>(comps.size());
        comps.push_back(Comp{a, b});
        by[a].push_back(i);
        if (b != a) by[b].push_back(i);
    }
}

Ret dfs(int port, const std::vector<Comp>& comps, const std::unordered_map<int, std::vector<int>>& by,
        std::vector<char>& used) {
    Ret best{0, 0, 0};
    auto it = by.find(port);
    if (it == by.end()) return best;
    for (int i : it->second) {
        if (used[i]) continue;
        const auto& c = comps[i];
        int nxt = (c.a == port) ? c.b : c.a;
        int seg = c.a + c.b;
        used[i] = 1;
        Ret ch = dfs(nxt, comps, by, used);
        used[i] = 0;

        if (seg + ch.s > best.s) best.s = seg + ch.s;
        int cl = 1 + ch.l;
        int cls = seg + ch.ls;
        if (cl > best.l || (cl == best.l && cls > best.ls)) {
            best.l = cl;
            best.ls = cls;
        }
    }
    return best;
}
}  // namespace

int main(int argc, char** argv) {
    int part = 0;
    std::string input;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "--part")
            part = std::stoi(argv[++i]);
        else if (a == "--input")
            input = argv[++i];
        else
            throw std::runtime_error("unknown arg");
    }
    if (part != 1 && part != 2) throw std::runtime_error("--part 1|2 required");
    input = resolve_input(input);
    if (sha256_file(input) != EXPECTED_SHA) throw std::runtime_error("checksum mismatch");

    std::vector<Comp> comps;
    std::unordered_map<int, std::vector<int>> by;
    parse(input, comps, by);
    std::vector<char> used(comps.size(), 0);

    auto t0 = std::chrono::steady_clock::now();
    Ret r = dfs(0, comps, by, used);
    std::string ans = std::to_string(part == 1 ? r.s : r.ls);
    std::string expected = part == 1 ? EXPECTED_PART1 : EXPECTED_PART2;
    if (ans != expected) throw std::runtime_error("answer mismatch");
    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=24 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
