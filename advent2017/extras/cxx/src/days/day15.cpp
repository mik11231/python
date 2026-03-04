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

const std::string kExpectedSha = "8d4f35b1950c1ca0bd04c13fe9e4a9a15065f902a86a82606973db0b9fe346f7";
const std::string kExpectedPart1 = "650";
const std::string kExpectedPart2 = "336";

const long long FA = 16807;
const long long FB = 48271;
const long long MOD = 2147483647;
const long long MASK = 0xFFFF;

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day15/d15_input.txt", "Day15/d15_input.txt", "../Day15/d15_input.txt", "../../Day15/d15_input.txt"};
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

std::pair<long long, long long> parse_seeds(const std::string& raw) {
    std::istringstream in(raw);
    std::string line;
    std::vector<long long> vals;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        std::istringstream ls(line);
        std::string tok;
        while (ls >> tok) {}
        vals.push_back(std::stoll(tok));
    }
    return {vals[0], vals[1]};
}

long long solve_part1(long long a, long long b) {
    long long cnt = 0;
    for (int i = 0; i < 40000000; ++i) {
        a = (a * FA) % MOD;
        b = (b * FB) % MOD;
        if ((a & MASK) == (b & MASK)) cnt++;
    }
    return cnt;
}

long long solve_part2(long long a, long long b) {
    long long cnt = 0;
    for (int i = 0; i < 5000000; ++i) {
        do { a = (a * FA) % MOD; } while ((a & 3) != 0);
        do { b = (b * FB) % MOD; } while ((b & 7) != 0);
        if ((a & MASK) == (b & MASK)) cnt++;
    }
    return cnt;
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
    const auto [a0, b0] = parse_seeds(raw);

    auto t0 = std::chrono::steady_clock::now();
    const std::string ans = (part == 1) ? std::to_string(solve_part1(a0, b0)) : std::to_string(solve_part2(a0, b0));
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=15 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
