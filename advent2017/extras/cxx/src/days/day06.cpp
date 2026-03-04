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
#include <unordered_set>
#include <vector>

namespace {

const std::string kExpectedSha = "489246369534515a9df814e8824f41c427d6c02ab31d7b5c07cbdc935497f2ba";
const std::string kExpectedPart1 = "12841";
const std::string kExpectedPart2 = "8038";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day6/d6_input.txt", "Day6/d6_input.txt", "../Day6/d6_input.txt", "../../Day6/d6_input.txt"};
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

std::vector<int> parse_banks(const std::string& raw) {
    std::istringstream in(raw);
    std::vector<int> out;
    int v = 0;
    while (in >> v) out.push_back(v);
    return out;
}

std::string key_of(const std::vector<int>& a) {
    std::ostringstream oss;
    for (std::size_t i = 0; i < a.size(); ++i) {
        if (i) oss << ',';
        oss << a[i];
    }
    return oss.str();
}

void redistribute(std::vector<int>& a) {
    std::size_t idx = 0;
    for (std::size_t i = 1; i < a.size(); ++i) {
        if (a[i] > a[idx]) idx = i;
    }
    int blocks = a[idx];
    a[idx] = 0;

    const int n = static_cast<int>(a.size());
    const int q = blocks / n;
    const int r = blocks % n;
    if (q > 0) {
        for (auto& v : a) v += q;
    }
    for (int k = 1; k <= r; ++k) {
        a[(idx + static_cast<std::size_t>(k)) % a.size()]++;
    }
}

long long solve_part1(const std::vector<int>& banks) {
    auto a = banks;
    std::unordered_set<std::string> seen;
    long long steps = 0;
    while (seen.find(key_of(a)) == seen.end()) {
        seen.insert(key_of(a));
        redistribute(a);
        steps++;
    }
    return steps;
}

long long solve_part2(const std::vector<int>& banks) {
    auto a = banks;
    std::unordered_map<std::string, long long> seen;
    long long steps = 0;
    while (seen.find(key_of(a)) == seen.end()) {
        seen[key_of(a)] = steps;
        redistribute(a);
        steps++;
    }
    return steps - seen[key_of(a)];
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
    const auto banks = parse_banks(raw);

    auto t0 = std::chrono::steady_clock::now();
    const std::string ans = std::to_string((part == 1) ? solve_part1(banks) : solve_part2(banks));
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=6 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
