#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <openssl/sha.h>

namespace {
constexpr const char* EXPECTED_SHA = "29581d7567b692271626cc1b3e1448f3456036af5d0bb1e0714fbaf2cf7bc878";
constexpr const char* EXPECTED_PART1 = "5246";
constexpr const char* EXPECTED_PART2 = "2512059";

inline uint64_t pack_pos(int r, int c) {
    return (static_cast<uint64_t>(static_cast<uint32_t>(r)) << 32) |
           static_cast<uint32_t>(c);
}

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    std::vector<std::string> cands = {
        "advent2017/Day22/d22_input.txt",
        "Day22/d22_input.txt",
        "../Day22/d22_input.txt",
        "../../Day22/d22_input.txt",
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

std::unordered_set<uint64_t> parse_infected(const std::string& path) {
    std::ifstream f(path);
    if (!f) throw std::runtime_error("open fail");
    std::vector<std::string> lines;
    std::string line;
    while (std::getline(f, line)) {
        if (!line.empty()) lines.push_back(line);
    }
    int n = static_cast<int>(lines.size());
    int off = n / 2;
    std::unordered_set<uint64_t> inf;
    inf.reserve(static_cast<size_t>(n * n));
    for (int r = 0; r < n; ++r) {
        for (int c = 0; c < static_cast<int>(lines[r].size()); ++c) {
            if (lines[r][c] == '#') inf.insert(pack_pos(r - off, c - off));
        }
    }
    return inf;
}

int solve_part1(const std::unordered_set<uint64_t>& inf0) {
    auto inf = inf0;
    inf.reserve(inf0.size() * 4 + 256);
    int r = 0, c = 0, dr = -1, dc = 0;
    int made = 0;
    for (int i = 0; i < 10000; ++i) {
        uint64_t p = pack_pos(r, c);
        if (inf.find(p) != inf.end()) {
            int ndr = dc, ndc = -dr;
            dr = ndr; dc = ndc;
            inf.erase(p);
        } else {
            int ndr = -dc, ndc = dr;
            dr = ndr; dc = ndc;
            inf.insert(p);
            ++made;
        }
        r += dr;
        c += dc;
    }
    return made;
}

int solve_part2(const std::unordered_set<uint64_t>& inf0) {
    // 0 clean, 1 weakened, 2 infected, 3 flagged
    std::unordered_map<uint64_t, uint8_t> state;
    state.reserve(inf0.size() * 16 + 1024);
    for (const auto& p : inf0) state[p] = 2;
    int r = 0, c = 0, dr = -1, dc = 0;
    int made = 0;
    for (int i = 0; i < 10000000; ++i) {
        uint64_t p = pack_pos(r, c);
        uint8_t s = 0;
        auto it = state.find(p);
        if (it != state.end()) s = it->second;
        if (s == 0) {
            int ndr = -dc, ndc = dr;
            dr = ndr; dc = ndc;
            state[p] = 1;
        } else if (s == 1) {
            state[p] = 2;
            ++made;
        } else if (s == 2) {
            int ndr = dc, ndc = -dr;
            dr = ndr; dc = ndc;
            state[p] = 3;
        } else {
            dr = -dr;
            dc = -dc;
            state.erase(p);
        }
        r += dr;
        c += dc;
    }
    return made;
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
    auto inf = parse_infected(input);

    auto t0 = std::chrono::steady_clock::now();
    std::string ans = std::to_string(part == 1 ? solve_part1(inf) : solve_part2(inf));
    std::string expected = part == 1 ? EXPECTED_PART1 : EXPECTED_PART2;
    if (ans != expected) throw std::runtime_error("answer mismatch");
    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=22 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
