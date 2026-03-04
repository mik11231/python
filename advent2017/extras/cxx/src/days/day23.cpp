// Architecture Notes:
// - This translation unit is documented for codebase-wide recoverability.
// - Solver stages are explicit to simplify verification and benchmarking.
// - Low-level optimizations are annotated with rationale and invariants.

#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <array>
#include <vector>
#include <openssl/sha.h>

namespace {
constexpr const char* EXPECTED_SHA = "866b77a4b5e37e19219792c97103a17d24c5f15a9f0bed448c0e6cfd75378beb";
constexpr const char* EXPECTED_PART1 = "3969";
constexpr const char* EXPECTED_PART2 = "917";

struct Arg {
    bool imm;
    int64_t v;
};

enum Op : uint8_t { OP_SET = 0, OP_SUB = 1, OP_MUL = 2, OP_JNZ = 3 };

struct Ins {
    Op op;
    Arg x;
    Arg y;
};

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    std::vector<std::string> cands = {
        "advent2017/Day23/d23_input.txt",
        "Day23/d23_input.txt",
        "../Day23/d23_input.txt",
        "../../Day23/d23_input.txt",
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

Arg parse_arg(const std::string& s) {
    if (!s.empty() && ((s[0] >= '0' && s[0] <= '9') || s[0] == '-')) {
        return {true, std::stoll(s)};
    }
    return {false, static_cast<int64_t>(s[0] - 'a')};
}

std::vector<Ins> parse(const std::string& path) {
    std::ifstream f(path);
    if (!f) throw std::runtime_error("open fail");
    std::vector<Ins> p;
    std::string op, x, y;
    while (f >> op >> x) {
        f >> y;
        Op opc = OP_SET;
        if (op == "set") {
            opc = OP_SET;
        } else if (op == "sub") {
            opc = OP_SUB;
        } else if (op == "mul") {
            opc = OP_MUL;
        } else if (op == "jnz") {
            opc = OP_JNZ;
        } else {
            throw std::runtime_error("bad op");
        }
        p.push_back({opc, parse_arg(x), parse_arg(y)});
    }
    return p;
}

inline int64_t val(const Arg& a, const std::array<int64_t, 26>& regs) {
    return a.imm ? a.v : regs[static_cast<size_t>(a.v)];
}

int solve_part1(const std::vector<Ins>& prog) {
    std::array<int64_t, 26> regs{};
    int64_t ip = 0;
    int muls = 0;
    while (ip >= 0 && ip < static_cast<int64_t>(prog.size())) {
        const auto& in = prog[static_cast<size_t>(ip)];
        if (in.op == OP_SET) {
            regs[static_cast<size_t>(in.x.v)] = val(in.y, regs);
        } else if (in.op == OP_SUB) {
            regs[static_cast<size_t>(in.x.v)] -= val(in.y, regs);
        } else if (in.op == OP_MUL) {
            regs[static_cast<size_t>(in.x.v)] *= val(in.y, regs);
            ++muls;
        } else {
            if (val(in.x, regs) != 0) {
                ip += val(in.y, regs);
                continue;
            }
        }
        ++ip;
    }
    return muls;
}

bool is_prime(int64_t n) {
    if (n < 2) return false;
    if (n % 2 == 0) return n == 2;
    int64_t lim = static_cast<int64_t>(std::sqrt(static_cast<double>(n)));
    for (int64_t d = 3; d <= lim; d += 2)
        if (n % d == 0) return false;
    return true;
}

int solve_part2(const std::vector<Ins>& prog) {
    int64_t b0 = prog[0].y.v;
    int64_t b = b0 * 100 + 100000;
    int64_t c = b + 17000;
    int cnt = 0;
    for (int64_t x = b; x <= c; x += 17)
        if (!is_prime(x)) ++cnt;
    return cnt;
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
    auto prog = parse(input);

    auto t0 = std::chrono::steady_clock::now();
    std::string ans = std::to_string(part == 1 ? solve_part1(prog) : solve_part2(prog));
    std::string expected = part == 1 ? EXPECTED_PART1 : EXPECTED_PART2;
    if (ans != expected) throw std::runtime_error("answer mismatch");
    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=23 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
