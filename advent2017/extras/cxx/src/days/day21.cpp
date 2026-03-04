// Architecture Notes:
// - This translation unit is documented for codebase-wide recoverability.
// - Solver stages are explicit to simplify verification and benchmarking.
// - Low-level optimizations are annotated with rationale and invariants.

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <regex>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
#include <openssl/sha.h>

namespace {
constexpr const char* EXPECTED_SHA = "759a25acf919be68478e4d20d3856f488ff79325d0954d8ca5c89cecc2fd8287";
constexpr const char* EXPECTED_PART1 = "139";
constexpr const char* EXPECTED_PART2 = "1857134";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    std::vector<std::string> cands = {
        "advent2017/Day21/d21_input.txt",
        "Day21/d21_input.txt",
        "../Day21/d21_input.txt",
        "../../Day21/d21_input.txt",
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

std::vector<std::string> rotate(const std::vector<std::string>& p) {
    int n = static_cast<int>(p.size());
    std::vector<std::string> out(n, std::string(n, '.'));
    for (int c = 0; c < n; ++c) {
        for (int r = 0; r < n; ++r) out[c][r] = p[n - 1 - r][c];
    }
    return out;
}

std::vector<std::string> flip(const std::vector<std::string>& p) {
    std::vector<std::string> out = p;
    for (auto& row : out) std::reverse(row.begin(), row.end());
    return out;
}

std::string join_pat(const std::vector<std::string>& p) {
    std::string s;
    for (size_t i = 0; i < p.size(); ++i) {
        if (i) s.push_back('/');
        s += p[i];
    }
    return s;
}

std::string canonical(std::vector<std::string> p) {
    std::vector<std::string> vars;
    vars.reserve(8);
    for (int i = 0; i < 4; ++i) {
        vars.push_back(join_pat(p));
        vars.push_back(join_pat(flip(p)));
        p = rotate(p);
    }
    std::sort(vars.begin(), vars.end());
    return vars[0];
}

std::unordered_map<std::string, std::vector<std::string>> parse_rules(const std::string& path) {
    std::ifstream f(path);
    if (!f) throw std::runtime_error("open fail");
    std::unordered_map<std::string, std::vector<std::string>> rules;
    std::string line;
    while (std::getline(f, line)) {
        if (line.empty()) continue;
        auto pos = line.find(" => ");
        auto lhs = line.substr(0, pos);
        auto rhs = line.substr(pos + 4);
        std::vector<std::string> in, out;
        size_t s = 0, e = 0;
        while ((e = lhs.find('/', s)) != std::string::npos) {
            in.push_back(lhs.substr(s, e - s));
            s = e + 1;
        }
        in.push_back(lhs.substr(s));
        s = 0;
        while ((e = rhs.find('/', s)) != std::string::npos) {
            out.push_back(rhs.substr(s, e - s));
            s = e + 1;
        }
        out.push_back(rhs.substr(s));
        rules[canonical(in)] = out;
    }
    return rules;
}

std::vector<std::string> enhance(const std::vector<std::string>& grid,
                                 const std::unordered_map<std::string, std::vector<std::string>>& rules) {
    int n = static_cast<int>(grid.size());
    int bs = (n % 2 == 0) ? 2 : 3;
    int os = bs + 1;
    int cnt = n / bs;
    int new_n = cnt * os;
    std::vector<std::string> out(new_n, std::string(new_n, '.'));
    for (int br = 0; br < cnt; ++br) {
        for (int bc = 0; bc < cnt; ++bc) {
            std::vector<std::string> sub(bs);
            for (int r = 0; r < bs; ++r) sub[r] = grid[br * bs + r].substr(bc * bs, bs);
            const auto& rep = rules.at(canonical(sub));
            for (int r = 0; r < os; ++r)
                for (int c = 0; c < os; ++c) out[br * os + r][bc * os + c] = rep[r][c];
        }
    }
    return out;
}

int run(const std::unordered_map<std::string, std::vector<std::string>>& rules, int iters) {
    std::vector<std::string> grid = {".#.", "..#", "###"};
    for (int i = 0; i < iters; ++i) grid = enhance(grid, rules);
    int total = 0;
    for (const auto& row : grid)
        for (char ch : row)
            if (ch == '#') ++total;
    return total;
}

std::vector<std::string> split_blocks(const std::vector<std::string>& grid, int bs) {
    int n = static_cast<int>(grid.size());
    int cnt = n / bs;
    std::vector<std::string> out;
    out.reserve(cnt * cnt);
    for (int br = 0; br < cnt; ++br) {
        for (int bc = 0; bc < cnt; ++bc) {
            std::vector<std::string> sub(bs);
            for (int r = 0; r < bs; ++r) sub[r] = grid[br * bs + r].substr(bc * bs, bs);
            out.push_back(join_pat(sub));
        }
    }
    return out;
}

int popcount_key(const std::string& k) {
    return static_cast<int>(std::count(k.begin(), k.end(), '#'));
}

int run_optimized(const std::unordered_map<std::string, std::vector<std::string>>& rules, int iters) {
    if (iters <= 5 || (iters % 3) != 0) return run(rules, iters);

    std::unordered_map<std::string, std::vector<std::string>> memo_expand;
    std::unordered_map<std::string, int> memo_count;

    std::function<std::vector<std::string>(const std::string&)> expand_three_from_3 =
        [&](const std::string& k) -> std::vector<std::string> {
        auto it = memo_expand.find(k);
        if (it != memo_expand.end()) return it->second;
        std::vector<std::string> g;
        size_t s = 0, e = 0;
        while ((e = k.find('/', s)) != std::string::npos) {
            g.push_back(k.substr(s, e - s));
            s = e + 1;
        }
        g.push_back(k.substr(s));
        g = enhance(g, rules);
        g = enhance(g, rules);
        g = enhance(g, rules);
        auto out = split_blocks(g, 3);
        memo_expand[k] = out;
        return out;
    };

    std::function<int(const std::string&, int)> count_cycles =
        [&](const std::string& k, int cycles) -> int {
        std::string mk = std::to_string(cycles) + "|" + k;
        auto it = memo_count.find(mk);
        if (it != memo_count.end()) return it->second;
        int v = 0;
        if (cycles == 0) {
            v = popcount_key(k);
        } else {
            for (const auto& sub : expand_three_from_3(k)) v += count_cycles(sub, cycles - 1);
        }
        memo_count[mk] = v;
        return v;
    };

    return count_cycles(".#./..#/###", iters / 3);
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
    auto rules = parse_rules(input);

    auto t0 = std::chrono::steady_clock::now();
    std::string ans = std::to_string(run_optimized(rules, part == 1 ? 5 : 18));
    std::string expected = part == 1 ? EXPECTED_PART1 : EXPECTED_PART2;
    if (ans != expected) throw std::runtime_error("answer mismatch");
    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=21 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
