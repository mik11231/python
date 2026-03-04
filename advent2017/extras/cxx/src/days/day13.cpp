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

const std::string kExpectedSha = "b59ed1486b6ec731cb7c2f55fdfec971d1157b9411fb823f9ddf0a3839d12cc8";
const std::string kExpectedPart1 = "2604";
const std::string kExpectedPart2 = "3941460";

struct Layer {
    long long depth;
    long long rng;
    long long period;
};

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day13/d13_input.txt", "Day13/d13_input.txt", "../Day13/d13_input.txt", "../../Day13/d13_input.txt"};
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

std::vector<Layer> parse_layers(const std::string& raw) {
    std::vector<Layer> out;
    std::istringstream in(raw);
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        const auto pos = line.find(':');
        if (pos == std::string::npos) throw std::runtime_error("bad line");
        const long long d = std::stoll(line.substr(0, pos));
        const long long r = std::stoll(line.substr(pos + 1));
        out.push_back(Layer{d, r, 2 * (r - 1)});
    }
    return out;
}

long long solve_part1(const std::vector<Layer>& layers) {
    long long severity = 0;
    for (const auto& l : layers) {
        if (l.depth % l.period == 0) severity += l.depth * l.rng;
    }
    return severity;
}

long long solve_part2(const std::vector<Layer>& layers) {
    long long delay = 0;
    while (true) {
        bool ok = true;
        for (const auto& l : layers) {
            if ((delay + l.depth) % l.period == 0) {
                ok = false;
                break;
            }
        }
        if (ok) return delay;
        delay++;
    }
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
    const auto layers = parse_layers(raw);

    auto t0 = std::chrono::steady_clock::now();
    const std::string ans = (part == 1) ? std::to_string(solve_part1(layers)) : std::to_string(solve_part2(layers));
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=13 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
