#include <algorithm>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <openssl/sha.h>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

const std::string kExpectedSha = "36d753e40c996a2ec1083c34b8cda3ffa986bc63a44d73be5ee1ed81084c6401";
const std::string kExpectedPart1 = "451";
const std::string kExpectedPart2 = "223";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day4/d4_input.txt", "Day4/d4_input.txt", "../Day4/d4_input.txt", "../../Day4/d4_input.txt"};
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

std::vector<std::vector<std::string>> parse_lines(const std::string& raw) {
    std::vector<std::vector<std::string>> out;
    std::istringstream in(raw);
    std::string line;
    while (std::getline(in, line)) {
        std::istringstream ls(line);
        std::vector<std::string> words;
        std::string w;
        while (ls >> w) words.push_back(w);
        if (!words.empty()) out.push_back(std::move(words));
    }
    return out;
}

std::string canonical_word(std::string w) {
    std::sort(w.begin(), w.end());
    return w;
}

int solve_part1(const std::vector<std::vector<std::string>>& lines) {
    int valid = 0;
    for (const auto& words : lines) {
        std::set<std::string> seen(words.begin(), words.end());
        valid += static_cast<int>(seen.size() == words.size());
    }
    return valid;
}

int solve_part2(const std::vector<std::vector<std::string>>& lines) {
    int valid = 0;
    for (const auto& words : lines) {
        std::set<std::string> seen;
        bool ok = true;
        for (const auto& w : words) {
            std::string c = canonical_word(w);
            if (!seen.insert(c).second) { ok = false; break; }
        }
        valid += static_cast<int>(ok);
    }
    return valid;
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
    const auto lines = parse_lines(raw);

    auto t0 = std::chrono::steady_clock::now();
    std::string ans;
    std::string expected;
    if (part == 1) { ans = std::to_string(solve_part1(lines)); expected = kExpectedPart1; }
    if (part == 2) { ans = std::to_string(solve_part2(lines)); expected = kExpectedPart2; }
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=4 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
