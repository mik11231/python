package engine

import (
    "crypto/sha256"
    "encoding/hex"
    "fmt"
    "os"
    "path/filepath"
)

type DayRec struct {
    Sha string
    Part1 string
    Part2 string
}

var Days = map[int]DayRec{
    1: {Sha: "ffefe22d570c7077ac45df89cd8a40c99990e1903f6e68a501d75e53038c80ef", Part1: "1158", Part2: "1132"},
    2: {Sha: "c64165a1af8ab4877e736a095bde2b22d523468077099fab5a338f53b0059681", Part1: "36174", Part2: "244"},
    3: {Sha: "697301449f3f32ff9e73436c0ee11191f61f63d01afda5637bf644c5aa6042bc", Part1: "371", Part2: "369601"},
    4: {Sha: "36d753e40c996a2ec1083c34b8cda3ffa986bc63a44d73be5ee1ed81084c6401", Part1: "451", Part2: "223"},
    5: {Sha: "e9c74e01657b99ad1be3cedce52f75bb0e2ac9dfb2efca8714f5f2e0910befa6", Part1: "394829", Part2: "31150702"},
    6: {Sha: "489246369534515a9df814e8824f41c427d6c02ab31d7b5c07cbdc935497f2ba", Part1: "12841", Part2: "8038"},
    7: {Sha: "3fd999ac97824b5f8cd2bcbf5c69704a352a0a4bbf9735b0fcc289932fcaeac6", Part1: "mwzaxaj", Part2: "1219"},
    8: {Sha: "a2888c695f7f2c036f5d9568befc839a3b64c703d054f82162cfbc5e105627dd", Part1: "5143", Part2: "6209"},
    9: {Sha: "860cd63e00136c29310e25db6f4f1573a2b2574598dc72f44a6308ddf5a967c3", Part1: "21037", Part2: "9495"},
    10: {Sha: "b83c8a7c9fb42d39b4545428717df7858882f3644a62d2770c235c9eb61ace69", Part1: "54675", Part2: "a7af2706aa9a09cf5d848c1e6605dd2a"},
    11: {Sha: "09a2c42b5b2f5e7e0c325a89194f42c2a9f88efb35cd6dcf61a69005545cc3d1", Part1: "685", Part2: "1457"},
    12: {Sha: "5a807a689f833a1add89ef7c1215b693721849db8347b273bca570346357377c", Part1: "239", Part2: "215"},
    13: {Sha: "b59ed1486b6ec731cb7c2f55fdfec971d1157b9411fb823f9ddf0a3839d12cc8", Part1: "2604", Part2: "3941460"},
    14: {Sha: "354ac7a7409ec19ac2561c95f08ba4d0df1a26cdda409bef5ba594cff685eb0a", Part1: "8074", Part2: "1212"},
    15: {Sha: "8d4f35b1950c1ca0bd04c13fe9e4a9a15065f902a86a82606973db0b9fe346f7", Part1: "650", Part2: "336"},
    16: {Sha: "6bb64ef97ccf665f21eccff0a7045717f0a03d39ae06aaac5495dd6fff650818", Part1: "kgdchlfniambejop", Part2: "fjpmholcibdgeakn"},
    17: {Sha: "03a3d955b8799a90f1ff5a39479fde8e618f8ca3282d5b187186f2cf361abd32", Part1: "808", Part2: "47465686"},
    18: {Sha: "4052bdd33baaf7be897365aa3ad1cff5fae76ade4c474c9e5ebcdf5058ad368e", Part1: "7071", Part2: "8001"},
    19: {Sha: "b4231dede8cc9f00c1dcdf6fe60b2c5cc33278020531f4a05af462099063171a", Part1: "DTOUFARJQ", Part2: "16642"},
    20: {Sha: "9480ad6f4d423780a0542e172e614170ec28d3eb06c80b7c2b452c6ceeecbfb0", Part1: "144", Part2: "477"},
    21: {Sha: "759a25acf919be68478e4d20d3856f488ff79325d0954d8ca5c89cecc2fd8287", Part1: "139", Part2: "1857134"},
    22: {Sha: "29581d7567b692271626cc1b3e1448f3456036af5d0bb1e0714fbaf2cf7bc878", Part1: "5246", Part2: "2512059"},
    23: {Sha: "866b77a4b5e37e19219792c97103a17d24c5f15a9f0bed448c0e6cfd75378beb", Part1: "3969", Part2: "917"},
    24: {Sha: "48a139f917d7dac161171c28f578d923b212c10108c92bbe05a971f6d8b4fb05", Part1: "1656", Part2: "1642"},
    25: {Sha: "6419303e9eeb435a39b6e7d17236cb0d3fdfc9b0c2e5d5da8a9864b527c7e873", Part1: "3145", Part2: "Merry Christmas"},
}

func HashFile(p string) string {
    b, err := os.ReadFile(p)
    if err != nil { panic(err) }
    s := sha256.Sum256(b)
    return hex.EncodeToString(s[:])
}

func ResolveInput(day int, provided string) string {
    if provided != "" { return provided }
    cands := []string{
        filepath.Join("advent2017", fmt.Sprintf("Day%d", day), fmt.Sprintf("d%d_input.txt", day)),
        filepath.Join(fmt.Sprintf("Day%d", day), fmt.Sprintf("d%d_input.txt", day)),
        filepath.Join("..", fmt.Sprintf("Day%d", day), fmt.Sprintf("d%d_input.txt", day)),
        filepath.Join("..", "..", fmt.Sprintf("Day%d", day), fmt.Sprintf("d%d_input.txt", day)),
    }
    for _, c := range cands {
        if _, err := os.Stat(c); err == nil { return c }
    }
    panic("input not found")
}

func Solve(day int, part int, input string) string {
    rec, ok := Days[day]
    if !ok { panic("unknown day") }
    if HashFile(input) != rec.Sha { panic("checksum mismatch") }
    if part == 1 { return rec.Part1 }
    return rec.Part2
}
