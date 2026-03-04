// Architecture Notes:
// - This translation unit is documented for codebase-wide recoverability.
// - Solver stages are explicit to simplify verification and benchmarking.
// - Low-level optimizations are annotated with rationale and invariants.

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <regex>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <openssl/sha.h>

namespace {
constexpr const char* EXPECTED_SHA = "9480ad6f4d423780a0542e172e614170ec28d3eb06c80b7c2b452c6ceeecbfb0";
constexpr const char* EXPECTED_PART1 = "144";
constexpr const char* EXPECTED_PART2 = "477";

struct V3 {
    int64_t x{}, y{}, z{};
    bool operator==(const V3& o) const { return x == o.x && y == o.y && z == o.z; }
    bool operator<(const V3& o) const {
        if (x != o.x) return x < o.x;
        if (y != o.y) return y < o.y;
        return z < o.z;
    }
};
struct Particle {
    V3 p, v, a;
};
struct V3Hash {
    size_t operator()(const V3& p) const {
        size_t h1 = std::hash<int64_t>{}(p.x);
        size_t h2 = std::hash<int64_t>{}(p.y);
        size_t h3 = std::hash<int64_t>{}(p.z);
        return h1 ^ (h2 << 1) ^ (h3 << 7);
    }
};

int64_t iabs64(int64_t x) { return x < 0 ? -x : x; }
int64_t manhattan(const V3& v) { return iabs64(v.x) + iabs64(v.y) + iabs64(v.z); }

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    std::vector<std::string> cands = {
        "advent2017/Day20/d20_input.txt",
        "Day20/d20_input.txt",
        "../Day20/d20_input.txt",
        "../../Day20/d20_input.txt",
    };
    for (const auto& c : cands) {
        std::ifstream f(c);
        if (f.good()) return c;
    }
    throw std::runtime_error("input not found");
}

std::string sha256_file(const std::string& path) {
    std::ifstream f(path, std::ios::binary);
    if (!f) throw std::runtime_error("read fail");
    std::vector<unsigned char> b((std::istreambuf_iterator<char>(f)), {});
    unsigned char out[SHA256_DIGEST_LENGTH];
    SHA256(b.data(), b.size(), out);
    static const char* HEX = "0123456789abcdef";
    std::string s;
    s.reserve(64);
    for (unsigned char v : out) {
        s.push_back(HEX[v >> 4]);
        s.push_back(HEX[v & 15]);
    }
    return s;
}

std::vector<Particle> parse(const std::string& path) {
    std::ifstream f(path);
    if (!f) throw std::runtime_error("open fail");
    std::regex re(
        R"(p=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>, v=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>, a=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>)");
    std::smatch m;
    std::vector<Particle> out;
    std::string line;
    while (std::getline(f, line)) {
        if (line.empty()) continue;
        if (!std::regex_match(line, m, re)) throw std::runtime_error("bad line");
        std::array<int64_t, 9> n{};
        for (int i = 0; i < 9; ++i) n[i] = std::stoll(m[i + 1].str());
        out.push_back(Particle{
            V3{n[0], n[1], n[2]},
            V3{n[3], n[4], n[5]},
            V3{n[6], n[7], n[8]},
        });
    }
    return out;
}

int solve_part1(const std::vector<Particle>& ps) {
    int best_i = -1;
    int64_t best_a = 0, best_v = 0, best_p = 0;
    for (int i = 0; i < static_cast<int>(ps.size()); ++i) {
        int64_t a = manhattan(ps[i].a);
        int64_t v = manhattan(ps[i].v);
        int64_t p = manhattan(ps[i].p);
        if (best_i < 0 || a < best_a ||
            (a == best_a && (v < best_v || (v == best_v && (p < best_p || (p == best_p && i < best_i)))))) {
            best_i = i;
            best_a = a;
            best_v = v;
            best_p = p;
        }
    }
    return best_i;
}

std::pair<bool, std::set<int64_t>> solve_axis(int64_t dp, int64_t dv, int64_t da) {
    std::set<int64_t> out;
    if (da == 0 && dv == 0) return {dp == 0, out};
    if (da == 0) {
        if (dv != 0 && (-dp) % dv == 0) {
            int64_t t = (-dp) / dv;
            if (t >= 0) out.insert(t);
        }
        return {false, out};
    }
    __int128 b = static_cast<__int128>(da) + 2 * static_cast<__int128>(dv);
    __int128 c = 2 * static_cast<__int128>(dp);
    __int128 a = static_cast<__int128>(da);
    __int128 disc = b * b - 4 * a * c;
    if (disc < 0) return {false, out};
    long double ds = std::sqrt(static_cast<long double>(disc));
    __int128 s = static_cast<__int128>(ds);
    while ((s + 1) * (s + 1) <= disc) ++s;
    while (s * s > disc) --s;
    if (s * s != disc) return {false, out};
    __int128 den = 2 * a;
    for (__int128 num : { -b + s, -b - s }) {
        if (den != 0 && num % den == 0) {
            __int128 t = num / den;
            if (t >= 0 && t <= std::numeric_limits<int64_t>::max()) out.insert(static_cast<int64_t>(t));
        }
    }
    return {false, out};
}

std::set<int64_t> intersect_set(const std::set<int64_t>& a, const std::set<int64_t>& b) {
    std::set<int64_t> out;
    std::set_intersection(a.begin(), a.end(), b.begin(), b.end(), std::inserter(out, out.begin()));
    return out;
}

V3 pos_at(const Particle& p, int64_t t) {
    return V3{
        p.p.x + p.v.x * t + p.a.x * t * (t + 1) / 2,
        p.p.y + p.v.y * t + p.a.y * t * (t + 1) / 2,
        p.p.z + p.v.z * t + p.a.z * t * (t + 1) / 2,
    };
}

std::set<int64_t> pair_times(const Particle& a, const Particle& b) {
    auto [ax_any, ax] = solve_axis(a.p.x - b.p.x, a.v.x - b.v.x, a.a.x - b.a.x);
    auto [ay_any, ay] = solve_axis(a.p.y - b.p.y, a.v.y - b.v.y, a.a.y - b.a.y);
    auto [az_any, az] = solve_axis(a.p.z - b.p.z, a.v.z - b.v.z, a.a.z - b.a.z);
    std::vector<std::set<int64_t>> concrete;
    if (!ax_any) concrete.push_back(std::move(ax));
    if (!ay_any) concrete.push_back(std::move(ay));
    if (!az_any) concrete.push_back(std::move(az));
    if (concrete.empty()) return {};
    std::set<int64_t> cur = concrete[0];
    for (size_t i = 1; i < concrete.size(); ++i) {
        cur = intersect_set(cur, concrete[i]);
        if (cur.empty()) break;
    }
    return cur;
}

int solve_part2(const std::vector<Particle>& ps) {
    using Pair = std::pair<int, int>;
    std::map<int64_t, std::vector<Pair>> events;
    int n = static_cast<int>(ps.size());
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            auto ts = pair_times(ps[i], ps[j]);
            for (int64_t t : ts) events[t].push_back({i, j});
        }
    }
    std::vector<char> alive(n, 1);
    int left = n;
    for (const auto& [t, pairs] : events) {
        std::unordered_set<int> involved;
        for (const auto& [i, j] : pairs) {
            if (alive[i] && alive[j]) {
                involved.insert(i);
                involved.insert(j);
            }
        }
        if (involved.size() < 2) continue;
        std::unordered_map<V3, std::vector<int>, V3Hash> groups;
        for (int i : involved) groups[pos_at(ps[i], t)].push_back(i);
        for (const auto& kv : groups) {
            if (kv.second.size() > 1) {
                for (int i : kv.second) {
                    if (alive[i]) {
                        alive[i] = 0;
                        --left;
                    }
                }
            }
        }
    }
    return left;
}
}  // namespace

int main(int argc, char** argv) {
    int part = 0;
    std::string input;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "--part")
            part = std::stoi(argv[++i]);
        else if (a == "--input")
            input = argv[++i];
        else
            throw std::runtime_error("unknown arg");
    }
    if (part != 1 && part != 2) throw std::runtime_error("--part 1|2 required");
    input = resolve_input(input);
    if (sha256_file(input) != EXPECTED_SHA) throw std::runtime_error("checksum mismatch");
    auto particles = parse(input);

    auto t0 = std::chrono::steady_clock::now();
    std::string ans = part == 1 ? std::to_string(solve_part1(particles)) : std::to_string(solve_part2(particles));
    std::string expected = part == 1 ? EXPECTED_PART1 : EXPECTED_PART2;
    if (ans != expected) throw std::runtime_error("answer mismatch");
    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=20 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
