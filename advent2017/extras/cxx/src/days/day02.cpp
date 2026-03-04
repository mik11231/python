#include <algorithm>
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

const std::string kExpectedSha = "c64165a1af8ab4877e736a095bde2b22d523468077099fab5a338f53b0059681";
const std::string kExpectedPart1 = "36174";
const std::string kExpectedPart2 = "244";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{
        "advent2017/Day2/d2_input.txt",
        "Day2/d2_input.txt",
        "../Day2/d2_input.txt",
        "../../Day2/d2_input.txt",
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
    for (auto b : out) oss << std::setw(2) << static_cast<int>(b);
    return oss.str();
}

std::vector<std::vector<int>> parse_rows(const std::string& raw) {
    std::vector<std::vector<int>> rows;
    std::istringstream in(raw);
    std::string line;
    while (std::getline(in, line)) {
        bool all_ws = true;
        for (char c : line) {
            if (!std::isspace(static_cast<unsigned char>(c))) {
                all_ws = false;
                break;
            }
        }
        if (all_ws) continue;

        std::istringstream ls(line);
        std::vector<int> row;
        int v = 0;
        while (ls >> v) row.push_back(v);
        if (!row.empty()) rows.push_back(std::move(row));
    }
    return rows;
}

int solve_part1(const std::vector<std::vector<int>>& rows) {
    int total = 0;
    for (const auto& row : rows) {
        auto mm = std::minmax_element(row.begin(), row.end());
        total += (*mm.second - *mm.first);
    }
    return total;
}

int solve_part2(const std::vector<std::vector<int>>& rows) {
    int total = 0;
    for (const auto& row : rows) {
        bool found = false;
        for (std::size_t i = 0; i < row.size() && !found; ++i) {
            for (std::size_t j = 0; j < row.size(); ++j) {
                if (i == j) continue;
                const int a = row[i];
                const int b = row[j];
                if (b != 0 && a % b == 0) {
                    total += a / b;
                    found = true;
                    break;
                }
            }
        }
        if (!found) throw std::runtime_error("no divisible pair found");
    }
    return total;
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
    const auto rows = parse_rows(raw);

    auto t0 = std::chrono::steady_clock::now();
    std::string ans;
    std::string expected;
    if (part == 1) {
        ans = std::to_string(solve_part1(rows));
        expected = kExpectedPart1;
    } else {
        ans = std::to_string(solve_part2(rows));
        expected = kExpectedPart2;
    }
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=2 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
