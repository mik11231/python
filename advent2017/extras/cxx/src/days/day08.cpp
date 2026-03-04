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
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

namespace {

const std::string kExpectedSha = "a2888c695f7f2c036f5d9568befc839a3b64c703d054f82162cfbc5e105627dd";
const std::string kExpectedPart1 = "5143";
const std::string kExpectedPart2 = "6209";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day8/d8_input.txt", "Day8/d8_input.txt", "../Day8/d8_input.txt", "../../Day8/d8_input.txt"};
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

bool check(long long a, const std::string& op, long long b) {
    if (op == "<") return a < b;
    if (op == "<=") return a <= b;
    if (op == ">") return a > b;
    if (op == ">=") return a >= b;
    if (op == "==") return a == b;
    if (op == "!=") return a != b;
    throw std::runtime_error("bad operator");
}

std::pair<long long, long long> run_program(const std::string& raw) {
    std::unordered_map<std::string, long long> reg;
    long long peak = 0;

    std::istringstream in(raw);
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        std::istringstream ls(line);
        std::string r, op, iftok, cr, cmp;
        long long v = 0, cv = 0;
        ls >> r >> op >> v >> iftok >> cr >> cmp >> cv;
        const long long crv = reg[cr];
        if (check(crv, cmp, cv)) {
            if (op == "inc") reg[r] += v;
            else reg[r] -= v;
            if (reg[r] > peak) peak = reg[r];
        }
    }

    long long maxv = 0;
    for (const auto& kv : reg) if (kv.second > maxv) maxv = kv.second;
    return {maxv, peak};
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
    const auto [p1, p2] = run_program(raw);
    const std::string ans = (part == 1) ? std::to_string(p1) : std::to_string(p2);
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=8 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
