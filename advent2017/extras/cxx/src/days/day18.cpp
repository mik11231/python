// Architecture Notes:
// - This translation unit is documented for codebase-wide recoverability.
// - Solver stages are explicit to simplify verification and benchmarking.
// - Low-level optimizations are annotated with rationale and invariants.

#include <chrono>
#include <deque>
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

const std::string kExpectedSha = "4052bdd33baaf7be897365aa3ad1cff5fae76ade4c474c9e5ebcdf5058ad368e";
const std::string kExpectedPart1 = "7071";
const std::string kExpectedPart2 = "8001";

struct Inst {
    std::string op;
    std::string x;
    std::string y;
    bool hasY;
};

std::string resolve_input(const std::string& provided) {
    if (!provided.empty()) return provided;
    const std::vector<std::string> cands{"advent2017/Day18/d18_input.txt", "Day18/d18_input.txt", "../Day18/d18_input.txt", "../../Day18/d18_input.txt"};
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

std::vector<Inst> parse(const std::string& raw) {
    std::vector<Inst> out;
    std::istringstream in(raw);
    std::string line;
    while (std::getline(in, line)) {
        if (line.empty()) continue;
        std::istringstream ls(line);
        Inst t;
        ls >> t.op >> t.x;
        t.hasY = static_cast<bool>(ls >> t.y);
        out.push_back(t);
    }
    return out;
}

long long val(const std::string& tok, const std::unordered_map<std::string, long long>& regs) {
    char* end = nullptr;
    long long v = std::strtoll(tok.c_str(), &end, 10);
    if (end && *end == '\0') return v;
    auto it = regs.find(tok);
    return (it == regs.end()) ? 0 : it->second;
}

long long solve_part1(const std::vector<Inst>& prog) {
    std::unordered_map<std::string, long long> regs;
    long long ip = 0;
    long long last = 0;

    while (ip >= 0 && ip < static_cast<long long>(prog.size())) {
        const auto& in = prog[static_cast<std::size_t>(ip)];
        if (in.op == "snd") {
            last = val(in.x, regs);
        } else if (in.op == "set") {
            regs[in.x] = val(in.y, regs);
        } else if (in.op == "add") {
            regs[in.x] = regs[in.x] + val(in.y, regs);
        } else if (in.op == "mul") {
            regs[in.x] = regs[in.x] * val(in.y, regs);
        } else if (in.op == "mod") {
            regs[in.x] = regs[in.x] % val(in.y, regs);
        } else if (in.op == "rcv") {
            if (val(in.x, regs) != 0) return last;
        } else if (in.op == "jgz") {
            if (val(in.x, regs) > 0) {
                ip += val(in.y, regs);
                continue;
            }
        } else {
            throw std::runtime_error("bad op");
        }
        ip++;
    }
    throw std::runtime_error("no recovery");
}

struct Proc {
    std::unordered_map<std::string, long long> regs;
    long long ip = 0;
    std::deque<long long> inq;
    long long send_count = 0;
    bool waiting = false;
    bool terminated = false;
};

bool step(Proc& me, Proc& other, const std::vector<Inst>& prog) {
    if (me.ip < 0 || me.ip >= static_cast<long long>(prog.size())) {
        me.terminated = true;
        me.waiting = false;
        return false;
    }

    const auto& in = prog[static_cast<std::size_t>(me.ip)];
    if (in.op == "snd") {
        other.inq.push_back(val(in.x, me.regs));
        me.send_count++;
        me.ip++;
        me.waiting = false;
        return true;
    }
    if (in.op == "set") {
        me.regs[in.x] = val(in.y, me.regs);
        me.ip++;
        me.waiting = false;
        return true;
    }
    if (in.op == "add") {
        me.regs[in.x] = me.regs[in.x] + val(in.y, me.regs);
        me.ip++;
        me.waiting = false;
        return true;
    }
    if (in.op == "mul") {
        me.regs[in.x] = me.regs[in.x] * val(in.y, me.regs);
        me.ip++;
        me.waiting = false;
        return true;
    }
    if (in.op == "mod") {
        me.regs[in.x] = me.regs[in.x] % val(in.y, me.regs);
        me.ip++;
        me.waiting = false;
        return true;
    }
    if (in.op == "rcv") {
        if (!me.inq.empty()) {
            me.regs[in.x] = me.inq.front();
            me.inq.pop_front();
            me.ip++;
            me.waiting = false;
            return true;
        }
        me.waiting = true;
        return false;
    }
    if (in.op == "jgz") {
        if (val(in.x, me.regs) > 0) me.ip += val(in.y, me.regs);
        else me.ip++;
        me.waiting = false;
        return true;
    }

    throw std::runtime_error("bad op");
}

long long solve_part2(const std::vector<Inst>& prog) {
    Proc p0, p1;
    p0.regs["p"] = 0;
    p1.regs["p"] = 1;

    while (true) {
        const bool a = step(p0, p1, prog);
        const bool b = step(p1, p0, prog);
        if (!a && !b && (p0.waiting || p0.terminated) && (p1.waiting || p1.terminated)) {
            return p1.send_count;
        }
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
    const auto prog = parse(raw);

    auto t0 = std::chrono::steady_clock::now();
    const std::string ans = (part == 1) ? std::to_string(solve_part1(prog)) : std::to_string(solve_part2(prog));
    const std::string expected = (part == 1) ? kExpectedPart1 : kExpectedPart2;
    if (ans != expected) throw std::runtime_error("answer mismatch");

    std::cout << ans << "\n";
    auto t1 = std::chrono::steady_clock::now();
    const double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cerr << "[cxx-fancy] day=18 part=" << part << " runtime_ms=" << ms << "\n";
    return 0;
}
