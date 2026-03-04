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

const std::string kExpectedSha = "b83c8a7c9fb42d39b4545428717df7858882f3644a62d2770c235c9eb61ace69";
const std::string kExpectedPart1 = "54675";
const std::string kExpectedPart2 = "a7af2706aa9a09cf5d848c1e6605dd2a";
const int kSuffix[5] = {17, 31, 73, 47, 23};

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day10/d10_input.txt", "Day10/d10_input.txt", "../Day10/d10_input.txt", "../../Day10/d10_input.txt"};
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

void reverse_segment(std::vector<int>& a, int start, int len) {
    const int n = static_cast<int>(a.size());
    for (int i = 0; i < len / 2; ++i) {
        const int x = (start + i) % n;
        const int y = (start + len - 1 - i) % n;
        std::swap(a[x], a[y]);
    }
}

std::pair<int, int> run_round(std::vector<int>& a, const std::vector<int>& lengths, int pos, int skip) {
    const int n = static_cast<int>(a.size());
    for (int len : lengths) {
        reverse_segment(a, pos, len);
        pos = (pos + len + skip) % n;
        skip++;
    }
    return {pos, skip};
}

int solve_part1(const std::string& raw) {
    std::vector<int> lengths;
    std::istringstream in(trim_ws(raw));
    std::string tok;
    while (std::getline(in, tok, ',')) {
        if (tok.empty()) continue;
        lengths.push_back(std::stoi(tok));
    }

    std::vector<int> ring(256);
    for (int i = 0; i < 256; ++i) ring[i] = i;
    run_round(ring, lengths, 0, 0);
    return ring[0] * ring[1];
}

std::string solve_part2(const std::string& raw) {
    const std::string s = trim_ws(raw);
    std::vector<int> lengths;
    lengths.reserve(s.size() + 5);
    for (unsigned char c : s) lengths.push_back(static_cast<int>(c));
    for (int v : kSuffix) lengths.push_back(v);

    std::vector<int> ring(256);
    for (int i = 0; i < 256; ++i) ring[i] = i;

    int pos = 0, skip = 0;
    for (int i = 0; i < 64; ++i) {
        auto st = run_round(ring, lengths, pos, skip);
        pos = st.first;
        skip = st.second;
    }

    std::ostringstream out;
    out << std::hex << std::setfill('0');
    for (int block = 0; block < 16; ++block) {
        int x = 0;
        for (int i = 0; i < 16; ++i) x ^= ring[block * 16 + i];
        out << std::setw(2) << x;
    }
    return out.str();
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
    const std::string ans = (part == 1) ? std::to_string(solve_part1(raw)) : solve_part2(raw);
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=10 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
