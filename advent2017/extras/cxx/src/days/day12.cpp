// Architecture Notes:
// - This translation unit is documented for codebase-wide recoverability.
// - Solver stages are explicit to simplify verification and benchmarking.
// - Low-level optimizations are annotated with rationale and invariants.

#include <chrono>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <openssl/sha.h>
#include <queue>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace {

const std::string kExpectedSha = "5a807a689f833a1add89ef7c1215b693721849db8347b273bca570346357377c";
const std::string kExpectedPart1 = "239";
const std::string kExpectedPart2 = "215";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day12/d12_input.txt", "Day12/d12_input.txt", "../Day12/d12_input.txt", "../../Day12/d12_input.txt"};
    for (const auto& c : cands) if (std::filesystem::exists(c)) return c;
    throw std::runtime_error("input not found");
}

std::string read_all(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    if (!in) throw std::runtime_error("failed to read input");
    return std::string((std::istreambuf_iterator<char>(in)), {});
}

std::string sha256_hex(const std::string& data) {
    unsigned char out[SHA256_DIGEST_LENGTH];
    SHA256(reinterpret_cast<const unsigned char*>(data.data()), data.size(), out);
    std::ostringstream oss;
    oss << std::hex << std::setfill('0');
    for (auto b : out) oss << std::setw(2) << static_cast<int>(b);
    return oss.str();
}

using Graph = std::unordered_map<int, std::vector<int>>;

Graph parse_graph(const std::string& raw) {
    Graph g;
    std::istringstream in(raw);
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;

        const auto pos = line.find("<->");
        if (pos == std::string::npos) throw std::runtime_error("bad input line");

        const int u = std::stoi(line.substr(0, pos));
        std::string rhs = line.substr(pos + 3);

        std::vector<int> nbrs;
        std::istringstream rs(rhs);
        std::string tok;
        while (std::getline(rs, tok, ',')) {
            while (!tok.empty() && tok.front() == ' ') tok.erase(tok.begin());
            while (!tok.empty() && tok.back() == ' ') tok.pop_back();
            if (!tok.empty()) nbrs.push_back(std::stoi(tok));
        }
        g[u] = std::move(nbrs);
    }
    return g;
}

std::size_t bfs_component(const Graph& g, int start, std::unordered_set<int>& seen) {
    std::queue<int> q;
    q.push(start);
    seen.insert(start);
    std::size_t count = 0;

    while (!q.empty()) {
        const int u = q.front();
        q.pop();
        count++;

        auto it = g.find(u);
        if (it == g.end()) continue;
        for (int v : it->second) {
            if (seen.find(v) != seen.end()) continue;
            seen.insert(v);
            q.push(v);
        }
    }

    return count;
}

std::pair<std::size_t, std::size_t> solve(const std::string& raw) {
    const Graph g = parse_graph(raw);
    std::unordered_set<int> seen;

    const std::size_t group0 = bfs_component(g, 0, seen);
    std::size_t groups = 1;

    for (const auto& kv : g) {
        if (seen.find(kv.first) != seen.end()) continue;
        bfs_component(g, kv.first, seen);
        groups++;
    }

    return {group0, groups};
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

    auto t0 = std::chrono::steady_clock::now();
    const auto [p1, p2] = solve(raw);
    const std::string ans = (part == 1) ? std::to_string(p1) : std::to_string(p2);
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=12 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
