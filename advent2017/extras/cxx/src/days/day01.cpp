#include <filesystem>
#include <fstream>
#include <chrono>
#include <cctype>
#include <iomanip>
#include <iostream>
#include <openssl/sha.h>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

const std::string kExpectedSha = "ffefe22d570c7077ac45df89cd8a40c99990e1903f6e68a501d75e53038c80ef";
const std::string kExpectedPart1 = "1158";
const std::string kExpectedPart2 = "1132";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{
        "advent2017/Day1/d1_input.txt",
        "Day1/d1_input.txt",
        "../Day1/d1_input.txt",
        "../../Day1/d1_input.txt",
    };
    for (const auto& c : cands) {
        if (std::filesystem::exists(c)) return c;
    }
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
    for (auto b : out) {
        oss << std::setw(2) << static_cast<int>(b);
    }
    return oss.str();
}

std::string trim_ws(std::string s) {
    while (!s.empty() && std::isspace(static_cast<unsigned char>(s.back()))) s.pop_back();
    std::size_t i = 0;
    while (i < s.size() && std::isspace(static_cast<unsigned char>(s[i]))) ++i;
    return s.substr(i);
}

int solve_with_step(const std::string& raw, int step) {
    const std::string s = trim_ws(raw);
    if (s.empty()) return 0;
    int sum = 0;
    const int n = static_cast<int>(s.size());
    for (int i = 0; i < n; ++i) {
        const int j = (i + step) % n;
        if (s[i] == s[j]) {
            sum += (s[i] - '0');
        }
    }
    return sum;
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
    std::string ans;
    std::string expected;
    if (part == 1) {
        ans = std::to_string(solve_with_step(raw, 1));
        expected = kExpectedPart1;
    } else {
        const int n = static_cast<int>(trim_ws(raw).size());
        ans = std::to_string(solve_with_step(raw, n / 2));
        expected = kExpectedPart2;
    }
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=1 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
