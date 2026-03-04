// Architecture Notes:
// - This translation unit is documented for codebase-wide recoverability.
// - Solver stages are explicit to simplify verification and benchmarking.
// - Low-level optimizations are annotated with rationale and invariants.

#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <regex>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>
#include <openssl/sha.h>

namespace {
constexpr const char* EXPECTED_SHA = "6419303e9eeb435a39b6e7d17236cb0d3fdfc9b0c2e5d5da8a9864b527c7e873";
constexpr const char* EXPECTED_PART1 = "3145";
constexpr const char* EXPECTED_PART2 = "Merry Christmas";

struct Rule {
    int write;
    int move;
    char next;
};

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    std::vector<std::string> cands = {
        "advent2017/Day25/d25_input.txt",
        "Day25/d25_input.txt",
        "../Day25/d25_input.txt",
        "../../Day25/d25_input.txt",
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

int solve_part1(const std::string& text) {
    std::smatch m;
    std::regex start_re(R"(Begin in state ([A-Z])\.)");
    std::regex steps_re(R"(Perform a diagnostic checksum after (\d+) steps\.)");
    if (!std::regex_search(text, m, start_re)) throw std::runtime_error("bad header");
    char start = m[1].str()[0];
    if (!std::regex_search(text, m, steps_re)) throw std::runtime_error("bad header");
    int steps = std::stoi(m[1].str());

    std::regex blk_re(
        R"(In state ([A-Z]):\s+If the current value is 0:\s+- Write the value ([01])\.\s+- Move one slot to the (right|left)\.\s+- Continue with state ([A-Z])\.\s+If the current value is 1:\s+- Write the value ([01])\.\s+- Move one slot to the (right|left)\.\s+- Continue with state ([A-Z])\.)");
    std::sregex_iterator it(text.begin(), text.end(), blk_re), end;
    Rule trans[26][2]{};
    for (; it != end; ++it) {
        auto c = *it;
        char st = c[1].str()[0];
        trans[st - 'A'][0] = Rule{
            std::stoi(c[2].str()),
            c[3].str() == "right" ? 1 : -1,
            c[4].str()[0],
        };
        trans[st - 'A'][1] = Rule{
            std::stoi(c[5].str()),
            c[6].str() == "right" ? 1 : -1,
            c[7].str()[0],
        };
    }

    std::unordered_set<int64_t> tape;
    int64_t cur = 0;
    char st = start;
    for (int i = 0; i < steps; ++i) {
        int v = tape.find(cur) == tape.end() ? 0 : 1;
        const Rule& r = trans[st - 'A'][v];
        if (r.write == 1)
            tape.insert(cur);
        else
            tape.erase(cur);
        cur += r.move;
        st = r.next;
    }
    return static_cast<int>(tape.size());
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
    std::ifstream f(input);
    if (!f) throw std::runtime_error("open fail");
    std::string text((std::istreambuf_iterator<char>(f)), {});

    auto t0 = std::chrono::steady_clock::now();
    std::string ans = part == 1 ? std::to_string(solve_part1(text)) : std::string(EXPECTED_PART2);
    std::string expected = part == 1 ? EXPECTED_PART1 : EXPECTED_PART2;
    if (ans != expected) throw std::runtime_error("answer mismatch");
    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=25 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
