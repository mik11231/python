// Architecture Notes:
// - This translation unit is documented for codebase-wide recoverability.
// - Solver stages are explicit to simplify verification and benchmarking.
// - Low-level optimizations are annotated with rationale and invariants.

#include <chrono>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <openssl/sha.h>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

const std::string kExpectedSha = "3fd999ac97824b5f8cd2bcbf5c69704a352a0a4bbf9735b0fcc289932fcaeac6";
const std::string kExpectedPart1 = "mwzaxaj";
const std::string kExpectedPart2 = "1219";

struct Tower {
    std::unordered_map<std::string, int> weights;
    std::unordered_map<std::string, std::vector<std::string>> children;
    std::unordered_map<std::string, std::string> parent;
};

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day7/d7_input.txt", "Day7/d7_input.txt", "../Day7/d7_input.txt", "../../Day7/d7_input.txt"};
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

Tower parse_tower(const std::string& raw) {
    Tower t;
    std::istringstream in(raw);
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;

        std::string left = line;
        std::string right;
        const auto pos = line.find("->");
        if (pos != std::string::npos) {
            left = line.substr(0, pos);
            right = line.substr(pos + 2);
        }

        std::istringstream ls(left);
        std::string name, wt_s;
        ls >> name >> wt_s;
        const int wt = std::stoi(wt_s.substr(1, wt_s.size() - 2));
        t.weights[name] = wt;

        std::vector<std::string> kids;
        if (!right.empty()) {
            std::istringstream rs(right);
            std::string tok;
            while (std::getline(rs, tok, ',')) {
                while (!tok.empty() && tok.front() == ' ') tok.erase(tok.begin());
                while (!tok.empty() && tok.back() == ' ') tok.pop_back();
                if (tok.empty()) continue;
                kids.push_back(tok);
                t.parent[tok] = name;
            }
        }
        t.children[name] = std::move(kids);
    }
    return t;
}

std::string find_root(const Tower& t) {
    for (const auto& kv : t.weights) {
        if (t.parent.find(kv.first) == t.parent.end()) return kv.first;
    }
    throw std::runtime_error("no root");
}

int solve_part2(const Tower& t, const std::string& root) {
    std::unordered_map<std::string, int> memo;

    std::function<int(const std::string&)> total = [&](const std::string& n) {
        const auto it = memo.find(n);
        if (it != memo.end()) return it->second;
        int s = t.weights.at(n);
        for (const auto& c : t.children.at(n)) s += total(c);
        memo[n] = s;
        return s;
    };

    std::function<int(const std::string&, bool&)> dfs = [&](const std::string& n, bool& ok) {
        const auto& kids = t.children.at(n);
        if (kids.empty()) {
            ok = false;
            return 0;
        }

        std::unordered_map<int, std::vector<std::string>> by;
        for (const auto& c : kids) by[total(c)].push_back(c);
        if (by.size() <= 1) {
            ok = false;
            return 0;
        }

        int bad_total = 0, good_total = 0;
        std::string bad_child;
        for (const auto& kv : by) {
            if (kv.second.size() == 1) {
                bad_total = kv.first;
                bad_child = kv.second[0];
            } else {
                good_total = kv.first;
            }
        }

        bool deep_ok = false;
        const int deep = dfs(bad_child, deep_ok);
        if (deep_ok) {
            ok = true;
            return deep;
        }

        ok = true;
        return t.weights.at(bad_child) + (good_total - bad_total);
    };

    bool ok = false;
    const int out = dfs(root, ok);
    if (!ok) throw std::runtime_error("no imbalance");
    return out;
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

    const Tower t = parse_tower(raw);
    const std::string root = find_root(t);

    auto t0 = std::chrono::steady_clock::now();
    const std::string ans = (part == 1) ? root : std::to_string(solve_part2(t, root));
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=7 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
