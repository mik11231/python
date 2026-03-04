#include <chrono>
#include <cctype>
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

const std::string kExpectedSha = "b4231dede8cc9f00c1dcdf6fe60b2c5cc33278020531f4a05af462099063171a";
const std::string kExpectedPart1 = "DTOUFARJQ";
const std::string kExpectedPart2 = "16642";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day19/d19_input.txt", "Day19/d19_input.txt", "../Day19/d19_input.txt", "../../Day19/d19_input.txt"};
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

std::vector<std::string> parse_grid(const std::string& raw) {
    std::vector<std::string> lines;
    std::istringstream in(raw);
    std::string line;
    std::size_t w = 0;
    while (std::getline(in, line)) {
        lines.push_back(line);
        w = std::max(w, line.size());
    }
    for (auto& l : lines) if (l.size() < w) l += std::string(w - l.size(), ' ');
    return lines;
}

char at(const std::vector<std::string>& g, int r, int c) {
    if (r < 0 || c < 0 || r >= static_cast<int>(g.size()) || c >= static_cast<int>(g[0].size())) return ' ';
    return g[r][c];
}

std::pair<std::string, long long> solve(const std::string& raw) {
    const auto g = parse_grid(raw);
    int r = 0;
    int c = static_cast<int>(g[0].find('|'));
    int dr = 1, dc = 0;
    std::string letters;
    long long steps = 0;

    while (true) {
        const char ch = at(g, r, c);
        if (ch == ' ') break;
        if (ch >= 'A' && ch <= 'Z') letters.push_back(ch);
        else if (ch == '+') {
            if (dr != 0) {
                if (at(g, r, c - 1) != ' ') { dr = 0; dc = -1; }
                else if (at(g, r, c + 1) != ' ') { dr = 0; dc = 1; }
            } else {
                if (at(g, r - 1, c) != ' ') { dr = -1; dc = 0; }
                else if (at(g, r + 1, c) != ' ') { dr = 1; dc = 0; }
            }
        }
        r += dr;
        c += dc;
        steps++;
    }

    return {letters, steps};
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
    const std::string ans = (part == 1) ? p1 : std::to_string(p2);
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=19 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
