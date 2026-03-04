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
#include <vector>

namespace {

const std::string kExpectedSha = "6bb64ef97ccf665f21eccff0a7045717f0a03d39ae06aaac5495dd6fff650818";
const std::string kExpectedPart1 = "kgdchlfniambejop";
const std::string kExpectedPart2 = "fjpmholcibdgeakn";

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day16/d16_input.txt", "Day16/d16_input.txt", "../Day16/d16_input.txt", "../../Day16/d16_input.txt"};
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

std::vector<std::string> parse_moves(const std::string& raw) {
    std::vector<std::string> out;
    std::stringstream ss(raw);
    std::string tok;
    while (std::getline(ss, tok, ',')) {
        if (!tok.empty() && tok.back() == '\n') tok.pop_back();
        if (!tok.empty()) out.push_back(tok);
    }
    return out;
}

void apply_once(std::string& state, const std::vector<std::string>& moves) {
    for (const auto& mv : moves) {
        const char t = mv[0];
        const std::string arg = mv.substr(1);
        if (t == 's') {
            const int x = std::stoi(arg);
            state = state.substr(state.size() - x) + state.substr(0, state.size() - x);
        } else if (t == 'x') {
            const auto pos = arg.find('/');
            const int a = std::stoi(arg.substr(0, pos));
            const int b = std::stoi(arg.substr(pos + 1));
            std::swap(state[a], state[b]);
        } else if (t == 'p') {
            const char a = arg[0];
            const char b = arg[2];
            const std::size_t ia = state.find(a);
            const std::size_t ib = state.find(b);
            std::swap(state[ia], state[ib]);
        } else {
            throw std::runtime_error("bad move");
        }
    }
}

std::string dance(const std::vector<std::string>& moves, long long rounds) {
    std::string state = "abcdefghijklmnop";
    std::unordered_map<std::string, long long> seen;

    long long i = 0;
    while (i < rounds) {
        auto it = seen.find(state);
        if (it != seen.end()) {
            const long long cycle = i - it->second;
            const long long rem = (rounds - i) % cycle;
            for (long long r = 0; r < rem; ++r) apply_once(state, moves);
            return state;
        }
        seen[state] = i;
        apply_once(state, moves);
        i++;
    }
    return state;
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
    const auto moves = parse_moves(raw);

    auto t0 = std::chrono::steady_clock::now();
    const std::string ans = (part == 1) ? dance(moves, 1) : dance(moves, 1000000000LL);
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=16 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
