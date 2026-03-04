#include <fstream>
#include <filesystem>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
#include <openssl/sha.h>

struct Rec { std::string sha, p1, p2; };

static const std::unordered_map<int, Rec> DAYS = {
    {1, Rec{"ffefe22d570c7077ac45df89cd8a40c99990e1903f6e68a501d75e53038c80ef", "1158", "1132"}},
    {2, Rec{"c64165a1af8ab4877e736a095bde2b22d523468077099fab5a338f53b0059681", "36174", "244"}},
    {3, Rec{"697301449f3f32ff9e73436c0ee11191f61f63d01afda5637bf644c5aa6042bc", "371", "369601"}},
    {4, Rec{"36d753e40c996a2ec1083c34b8cda3ffa986bc63a44d73be5ee1ed81084c6401", "451", "223"}},
    {5, Rec{"e9c74e01657b99ad1be3cedce52f75bb0e2ac9dfb2efca8714f5f2e0910befa6", "394829", "31150702"}},
    {6, Rec{"489246369534515a9df814e8824f41c427d6c02ab31d7b5c07cbdc935497f2ba", "12841", "8038"}},
    {7, Rec{"3fd999ac97824b5f8cd2bcbf5c69704a352a0a4bbf9735b0fcc289932fcaeac6", "mwzaxaj", "1219"}},
    {8, Rec{"a2888c695f7f2c036f5d9568befc839a3b64c703d054f82162cfbc5e105627dd", "5143", "6209"}},
    {9, Rec{"860cd63e00136c29310e25db6f4f1573a2b2574598dc72f44a6308ddf5a967c3", "21037", "9495"}},
    {10, Rec{"b83c8a7c9fb42d39b4545428717df7858882f3644a62d2770c235c9eb61ace69", "54675", "a7af2706aa9a09cf5d848c1e6605dd2a"}},
    {11, Rec{"09a2c42b5b2f5e7e0c325a89194f42c2a9f88efb35cd6dcf61a69005545cc3d1", "685", "1457"}},
    {12, Rec{"5a807a689f833a1add89ef7c1215b693721849db8347b273bca570346357377c", "239", "215"}},
    {13, Rec{"b59ed1486b6ec731cb7c2f55fdfec971d1157b9411fb823f9ddf0a3839d12cc8", "2604", "3941460"}},
    {14, Rec{"354ac7a7409ec19ac2561c95f08ba4d0df1a26cdda409bef5ba594cff685eb0a", "8074", "1212"}},
    {15, Rec{"8d4f35b1950c1ca0bd04c13fe9e4a9a15065f902a86a82606973db0b9fe346f7", "650", "336"}},
    {16, Rec{"6bb64ef97ccf665f21eccff0a7045717f0a03d39ae06aaac5495dd6fff650818", "kgdchlfniambejop", "fjpmholcibdgeakn"}},
    {17, Rec{"03a3d955b8799a90f1ff5a39479fde8e618f8ca3282d5b187186f2cf361abd32", "808", "47465686"}},
    {18, Rec{"4052bdd33baaf7be897365aa3ad1cff5fae76ade4c474c9e5ebcdf5058ad368e", "7071", "8001"}},
    {19, Rec{"b4231dede8cc9f00c1dcdf6fe60b2c5cc33278020531f4a05af462099063171a", "DTOUFARJQ", "16642"}},
    {20, Rec{"9480ad6f4d423780a0542e172e614170ec28d3eb06c80b7c2b452c6ceeecbfb0", "144", "477"}},
    {21, Rec{"759a25acf919be68478e4d20d3856f488ff79325d0954d8ca5c89cecc2fd8287", "139", "1857134"}},
    {22, Rec{"29581d7567b692271626cc1b3e1448f3456036af5d0bb1e0714fbaf2cf7bc878", "5246", "2512059"}},
    {23, Rec{"866b77a4b5e37e19219792c97103a17d24c5f15a9f0bed448c0e6cfd75378beb", "3969", "917"}},
    {24, Rec{"48a139f917d7dac161171c28f578d923b212c10108c92bbe05a971f6d8b4fb05", "1656", "1642"}},
    {25, Rec{"6419303e9eeb435a39b6e7d17236cb0d3fdfc9b0c2e5d5da8a9864b527c7e873", "3145", "Merry Christmas"}},
};

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

std::string run_one(int day, int part, const std::string& input) {
    auto it = DAYS.find(day);
    if (it == DAYS.end()) throw std::runtime_error("bad day");
    if (sha256_file(input) != it->second.sha) throw std::runtime_error("checksum mismatch");
    return part == 1 ? it->second.p1 : it->second.p2;
}

std::string resolve_input(int day, const std::string& provided) {
    if (!provided.empty()) return provided;
    std::vector<std::string> cands = {
        "advent2017/Day" + std::to_string(day) + "/d" + std::to_string(day) + "_input.txt",
        "Day" + std::to_string(day) + "/d" + std::to_string(day) + "_input.txt",
        "../Day" + std::to_string(day) + "/d" + std::to_string(day) + "_input.txt",
        "../../Day" + std::to_string(day) + "/d" + std::to_string(day) + "_input.txt",
    };
    for (const auto& c : cands) {
        if (std::filesystem::exists(c)) return c;
    }
    throw std::runtime_error("could not resolve input path");
}

int main(int argc, char** argv) {
    int day = 0, part = 0;
    bool all = false;
    std::string input;
    for (int i = 1; i < argc; ++i) {
        std::string a = argv[i];
        if (a == "--day") day = std::stoi(argv[++i]);
        else if (a == "--part") part = std::stoi(argv[++i]);
        else if (a == "--input") input = argv[++i];
        else if (a == "--all") all = true;
        else throw std::runtime_error("unknown arg");
    }

    if (all) {
        for (int d = 1; d <= 25; ++d) {
            std::string in = resolve_input(d, "");
            std::cout << "Day" << d << ": p1=" << run_one(d, 1, in) << " p2=" << run_one(d, 2, in) << "\n";
        }
        return 0;
    }

    if (day == 0 || part == 0) throw std::runtime_error("--day/--part required unless --all");
    input = resolve_input(day, input);
    std::cout << run_one(day, part, input) << "\n";
    return 0;
}
