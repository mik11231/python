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

const std::string kExpectedSha = "860cd63e00136c29310e25db6f4f1573a2b2574598dc72f44a6308ddf5a967c3";
const std::string kExpectedPart1 = "21037";
const std::string kExpectedPart2 = "9495";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day9/d9_input.txt", "Day9/d9_input.txt", "../Day9/d9_input.txt", "../../Day9/d9_input.txt"};
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

std::string trim_ws(const std::string& s) {
    std::size_t b = 0;
    while (b < s.size() && std::isspace(static_cast<unsigned char>(s[b]))) b++;
    std::size_t e = s.size();
    while (e > b && std::isspace(static_cast<unsigned char>(s[e - 1]))) e--;
    return s.substr(b, e - b);
}

std::pair<long long, long long> scan_stream(const std::string& raw) {
    const std::string s = trim_ws(raw);
    long long depth = 0;
    long long score = 0;
    long long garbage = 0;
    bool in_garbage = false;

    for (std::size_t i = 0; i < s.size(); ++i) {
        const char c = s[i];
        if (in_garbage) {
            if (c == '!') {
                i++;
                continue;
            }
            if (c == '>') {
                in_garbage = false;
            } else {
                garbage++;
            }
            continue;
        }

        if (c == '<') {
            in_garbage = true;
        } else if (c == '{') {
            depth++;
            score += depth;
        } else if (c == '}') {
            depth--;
        }
    }

    return {score, garbage};
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
    const auto [p1, p2] = scan_stream(raw);
    const std::string ans = (part == 1) ? std::to_string(p1) : std::to_string(p2);
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=9 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
