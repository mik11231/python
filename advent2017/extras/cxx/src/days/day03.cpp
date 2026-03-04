// Architecture Notes:
// - This translation unit is documented for codebase-wide recoverability.
// - Solver stages are explicit to simplify verification and benchmarking.
// - Low-level optimizations are annotated with rationale and invariants.

#include <chrono>
#include <cctype>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <openssl/sha.h>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

const std::string kExpectedSha = "697301449f3f32ff9e73436c0ee11191f61f63d01afda5637bf644c5aa6042bc";
const std::string kExpectedPart1 = "371";
const std::string kExpectedPart2 = "369601";

struct PairHash {
    std::size_t operator()(const std::pair<int, int>& p) const noexcept {
        return (static_cast<std::size_t>(static_cast<unsigned int>(p.first)) << 32) ^
               static_cast<std::size_t>(static_cast<unsigned int>(p.second));
    }
};

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{
        "advent2017/Day3/d3_input.txt", "Day3/d3_input.txt", "../Day3/d3_input.txt", "../../Day3/d3_input.txt",
    };
    for (const auto& c : cands) if (std::filesystem::exists(c)) return c;
    throw std::runtime_error("input not found");
}

std::string read_all(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    if (!in) throw std::runtime_error("failed to read input");
    return std::string((std::istreambuf_iterator<char>(in)), {});
}

std::string trim_ws(std::string s) {
    while (!s.empty() && std::isspace(static_cast<unsigned char>(s.back()))) s.pop_back();
    std::size_t i = 0;
    while (i < s.size() && std::isspace(static_cast<unsigned char>(s[i]))) ++i;
    return s.substr(i);
}

std::string sha256_hex(const std::string& data) {
    unsigned char out[SHA256_DIGEST_LENGTH];
    SHA256(reinterpret_cast<const unsigned char*>(data.data()), data.size(), out);
    std::ostringstream oss;
    oss << std::hex << std::setfill('0');
    for (auto b : out) oss << std::setw(2) << static_cast<int>(b);
    return oss.str();
}

int iabs(int v) { return v < 0 ? -v : v; }

int solve_part1(int n) {
    if (n == 1) return 0;
    int layer = 0;
    while ((2 * layer + 1) * (2 * layer + 1) < n) layer++;
    const int side = 2 * layer;
    const int maxv = (2 * layer + 1) * (2 * layer + 1);
    int best = std::numeric_limits<int>::max();
    for (int i = 0; i < 4; ++i) {
        const int mid = maxv - layer - side * i;
        const int d = iabs(n - mid);
        if (d < best) best = d;
    }
    return layer + best;
}

int solve_part2(int target) {
    static const int nei[8][2] = {{-1,-1},{-1,0},{-1,1},{0,-1},{0,1},{1,-1},{1,0},{1,1}};
    std::unordered_map<std::pair<int, int>, int, PairHash> grid;
    grid[{0, 0}] = 1;
    int x = 0, y = 0, step = 1;

    auto sum_nei = [&](int cx, int cy) {
        int s = 0;
        for (const auto& d : nei) {
            auto it = grid.find({cx + d[0], cy + d[1]});
            if (it != grid.end()) s += it->second;
        }
        return s;
    };

    while (true) {
        for (int i = 0; i < step; ++i) { x++; int v = sum_nei(x,y); if (v > target) return v; grid[{x,y}] = v; }
        for (int i = 0; i < step; ++i) { y++; int v = sum_nei(x,y); if (v > target) return v; grid[{x,y}] = v; }
        step++;
        for (int i = 0; i < step; ++i) { x--; int v = sum_nei(x,y); if (v > target) return v; grid[{x,y}] = v; }
        for (int i = 0; i < step; ++i) { y--; int v = sum_nei(x,y); if (v > target) return v; grid[{x,y}] = v; }
        step++;
    }
}

}  // namespace

int main(int argc, char** argv) {
    int part = 0;
    std::string input;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "--part") part = std::stoi(argv[++i]);
        else if (a == "--input") input = argv[++i];
        else throw std::runtime_error("unknown arg");
    }
    if (part != 1 && part != 2) throw std::runtime_error("--part 1|2 required");

    input = resolve_input(input);
    const std::string raw = read_all(input);
    if (sha256_hex(raw) != kExpectedSha) throw std::runtime_error("checksum mismatch");
    const int n = std::stoi(trim_ws(raw));

    auto t0 = std::chrono::steady_clock::now();
    std::string ans;
    std::string expected;
    if (part == 1) {
        ans = std::to_string(solve_part1(n));
        expected = kExpectedPart1;
    } else {
        ans = std::to_string(solve_part2(n));
        expected = kExpectedPart2;
    }
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=3 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
