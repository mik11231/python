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
#include <vector>

namespace {

const std::string kExpectedSha = "03a3d955b8799a90f1ff5a39479fde8e618f8ca3282d5b187186f2cf361abd32";
const std::string kExpectedPart1 = "808";
const std::string kExpectedPart2 = "47465686";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day17/d17_input.txt", "Day17/d17_input.txt", "../Day17/d17_input.txt", "../../Day17/d17_input.txt"};
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

long long solve_part1(int step) {
    std::vector<int> buf{0};
    int pos = 0;
    for (int v = 1; v <= 2017; ++v) {
        pos = (pos + step) % static_cast<int>(buf.size()) + 1;
        buf.insert(buf.begin() + pos, v);
    }
    return buf[(pos + 1) % static_cast<int>(buf.size())];
}

long long solve_part2(int step) {
    int pos = 0;
    int val_after_zero = 0;
    int size = 1;
    for (int v = 1; v <= 50000000; ++v) {
        pos = (pos + step) % size + 1;
        if (pos == 1) val_after_zero = v;
        size++;
    }
    return val_after_zero;
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
    const int step = std::stoi(raw);

    auto t0 = std::chrono::steady_clock::now();
    const std::string ans = (part == 1) ? std::to_string(solve_part1(step)) : std::to_string(solve_part2(step));
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=17 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
