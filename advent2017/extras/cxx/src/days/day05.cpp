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

const std::string kExpectedSha = "e9c74e01657b99ad1be3cedce52f75bb0e2ac9dfb2efca8714f5f2e0910befa6";
const std::string kExpectedPart1 = "394829";
const std::string kExpectedPart2 = "31150702";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day5/d5_input.txt", "Day5/d5_input.txt", "../Day5/d5_input.txt", "../../Day5/d5_input.txt"};
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

std::vector<int> parse_offsets(const std::string& raw) {
    std::istringstream in(raw);
    std::vector<int> out;
    int v = 0;
    while (in >> v) out.push_back(v);
    return out;
}

long long run_program(const std::vector<int>& offsets, int part) {
    std::vector<int> a = offsets;
    long long steps = 0;
    int i = 0;
    while (i >= 0 && i < static_cast<int>(a.size())) {
        const int jump = a[static_cast<std::size_t>(i)];
        if (part == 1) {
            a[static_cast<std::size_t>(i)] = jump + 1;
        } else if (jump >= 3) {
            a[static_cast<std::size_t>(i)] = jump - 1;
        } else {
            a[static_cast<std::size_t>(i)] = jump + 1;
        }
        i += jump;
        steps++;
    }
    return steps;
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
    const auto offsets = parse_offsets(raw);

    auto t0 = std::chrono::steady_clock::now();
    const std::string ans = std::to_string(run_program(offsets, part));
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=5 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
