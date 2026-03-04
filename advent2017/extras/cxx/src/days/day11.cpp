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

const std::string kExpectedSha = "09a2c42b5b2f5e7e0c325a89194f42c2a9f88efb35cd6dcf61a69005545cc3d1";
const std::string kExpectedPart1 = "685";
const std::string kExpectedPart2 = "1457";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day11/d11_input.txt", "Day11/d11_input.txt", "../Day11/d11_input.txt", "../../Day11/d11_input.txt"};
    for (const auto& c : cands) if (std::filesystem::exists(c)) return c;
    throw std::runtime_error("input not found");
}

std::string read_all(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    if (!in) throw std::runtime_error("failed to read input");
    return std::string((std::istreambuf_iterator<char>(in)), {});
}

std::string trim_ws(const std::string& s) {
    std::size_t b = 0;
    while (b < s.size() && std::isspace(static_cast<unsigned char>(s[b]))) b++;
    std::size_t e = s.size();
    while (e > b && std::isspace(static_cast<unsigned char>(s[e - 1]))) e--;
    return s.substr(b, e - b);
}

std::string sha256_hex(const std::string& data) {
    unsigned char out[SHA256_DIGEST_LENGTH];
    SHA256(reinterpret_cast<const unsigned char*>(data.data()), data.size(), out);
    std::ostringstream oss;
    oss << std::hex << std::setfill('0');
    for (auto b : out) oss << std::setw(2) << static_cast<int>(b);
    return oss.str();
}

long long cube_distance(long long x, long long y, long long z) {
    x = std::llabs(x);
    y = std::llabs(y);
    z = std::llabs(z);
    return std::max(x, std::max(y, z));
}

std::pair<long long, long long> solve(const std::string& raw) {
    const std::string s = trim_ws(raw);
    std::istringstream in(s);
    std::string step;
    long long x = 0, y = 0, z = 0;
    long long best = 0;

    while (std::getline(in, step, ',')) {
        if (step == "n") {
            y += 1; z -= 1;
        } else if (step == "ne") {
            x += 1; z -= 1;
        } else if (step == "se") {
            x += 1; y -= 1;
        } else if (step == "s") {
            y -= 1; z += 1;
        } else if (step == "sw") {
            x -= 1; z += 1;
        } else if (step == "nw") {
            x -= 1; y += 1;
        } else if (!step.empty()) {
            throw std::runtime_error("bad step");
        }
        best = std::max(best, cube_distance(x, y, z));
    }

    return {cube_distance(x, y, z), best};
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
    std::cerr << "[cxx-fancy] day=11 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
