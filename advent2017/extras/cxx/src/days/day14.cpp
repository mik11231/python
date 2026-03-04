// Architecture Notes:
// - This translation unit is documented for codebase-wide recoverability.
// - Solver stages are explicit to simplify verification and benchmarking.
// - Low-level optimizations are annotated with rationale and invariants.

#include <array>
#include <chrono>
#include <cctype>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <openssl/sha.h>
#include <queue>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

namespace {

const std::string kExpectedSha = "354ac7a7409ec19ac2561c95f08ba4d0df1a26cdda409bef5ba594cff685eb0a";
const std::string kExpectedPart1 = "8074";
const std::string kExpectedPart2 = "1212";
const int kSuffix[5] = {17, 31, 73, 47, 23};

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day14/d14_input.txt", "Day14/d14_input.txt", "../Day14/d14_input.txt", "../../Day14/d14_input.txt"};
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

void reverse_segment(std::array<int, 256>& ring, int start, int len) {
    for (int i = 0; i < len / 2; ++i) {
        const int x = (start + i) & 255;
        const int y = (start + len - 1 - i) & 255;
        std::swap(ring[x], ring[y]);
    }
}

std::array<unsigned char, 16> knot_hash_bytes(const std::string& key) {
    std::vector<int> lengths;
    lengths.reserve(key.size() + 5);
    for (unsigned char c : key) lengths.push_back(static_cast<int>(c));
    for (int v : kSuffix) lengths.push_back(v);

    std::array<int, 256> ring{};
    for (int i = 0; i < 256; ++i) ring[i] = i;

    int pos = 0, skip = 0;
    for (int round = 0; round < 64; ++round) {
        for (int len : lengths) {
            reverse_segment(ring, pos, len);
            pos = (pos + len + skip) & 255;
            skip++;
        }
    }

    std::array<unsigned char, 16> out{};
    for (int b = 0; b < 16; ++b) {
        int x = 0;
        for (int i = 0; i < 16; ++i) x ^= ring[b * 16 + i];
        out[b] = static_cast<unsigned char>(x);
    }
    return out;
}

std::pair<int, int> solve(const std::string& seed) {
    bool g[128][128]{};
    std::array<int, 128> used_rows{};
    unsigned t = std::thread::hardware_concurrency();
    if (t == 0) t = 1;
    if (t > 16) t = 16;
    if (t > 128) t = 128;
    std::vector<std::thread> workers;
    workers.reserve(t);
    for (unsigned ti = 0; ti < t; ++ti) {
        workers.emplace_back([&, ti]() {
            const int chunk = 128 / static_cast<int>(t);
            const int rem = 128 % static_cast<int>(t);
            const int start = static_cast<int>(ti) * chunk + std::min(static_cast<int>(ti), rem);
            const int end = start + chunk + (static_cast<int>(ti) < rem ? 1 : 0);
            for (int r = start; r < end; ++r) {
                auto h = knot_hash_bytes(seed + "-" + std::to_string(r));
                int c = 0;
                int row_used = 0;
                for (unsigned char b : h) {
                    row_used += __builtin_popcount(static_cast<unsigned int>(b));
                    for (int bit = 7; bit >= 0; --bit) {
                        g[r][c++] = ((b >> bit) & 1U) != 0;
                    }
                }
                used_rows[r] = row_used;
            }
        });
    }
    for (auto& th : workers) th.join();
    int used = 0;
    for (int u : used_rows) used += u;

    bool seen[128][128]{};
    int regions = 0;
    const int dx[4] = {1, -1, 0, 0};
    const int dy[4] = {0, 0, 1, -1};

    for (int i = 0; i < 128; ++i) {
        for (int j = 0; j < 128; ++j) {
            if (!g[i][j] || seen[i][j]) continue;
            regions++;
            std::queue<std::pair<int, int>> q;
            q.push({i, j});
            seen[i][j] = true;
            while (!q.empty()) {
                auto [x, y] = q.front();
                q.pop();
                for (int k = 0; k < 4; ++k) {
                    const int nx = x + dx[k];
                    const int ny = y + dy[k];
                    if (nx < 0 || nx >= 128 || ny < 0 || ny >= 128) continue;
                    if (!g[nx][ny] || seen[nx][ny]) continue;
                    seen[nx][ny] = true;
                    q.push({nx, ny});
                }
            }
        }
    }

    return {used, regions};
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
    const std::string seed = trim_ws(raw);

    auto t0 = std::chrono::steady_clock::now();
    const auto [p1, p2] = solve(seed);
    const std::string ans = (part == 1) ? std::to_string(p1) : std::to_string(p2);
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=14 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
