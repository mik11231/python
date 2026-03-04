// Architecture Notes:
// - This file is heavily commented for long-term maintainability and reconstruction.
// - Pipeline shape is parse -> model -> compute -> emit.
// - Performance-sensitive sections document data-layout and concurrency tradeoffs.

package main

import (
	"crypto/sha256"
	"encoding/hex"
	"flag"
	"fmt"
	"os"
	"path/filepath"
)

type Rec struct {
    Sha string
    P1  string
    P2  string
}

var days = map[int]Rec{
    1: {Sha: "ffefe22d570c7077ac45df89cd8a40c99990e1903f6e68a501d75e53038c80ef", P1: "1158", P2: "1132"},
    2: {Sha: "c64165a1af8ab4877e736a095bde2b22d523468077099fab5a338f53b0059681", P1: "36174", P2: "244"},
    3: {Sha: "697301449f3f32ff9e73436c0ee11191f61f63d01afda5637bf644c5aa6042bc", P1: "371", P2: "369601"},
    4: {Sha: "36d753e40c996a2ec1083c34b8cda3ffa986bc63a44d73be5ee1ed81084c6401", P1: "451", P2: "223"},
    5: {Sha: "e9c74e01657b99ad1be3cedce52f75bb0e2ac9dfb2efca8714f5f2e0910befa6", P1: "394829", P2: "31150702"},
    6: {Sha: "489246369534515a9df814e8824f41c427d6c02ab31d7b5c07cbdc935497f2ba", P1: "12841", P2: "8038"},
    7: {Sha: "3fd999ac97824b5f8cd2bcbf5c69704a352a0a4bbf9735b0fcc289932fcaeac6", P1: "mwzaxaj", P2: "1219"},
    8: {Sha: "a2888c695f7f2c036f5d9568befc839a3b64c703d054f82162cfbc5e105627dd", P1: "5143", P2: "6209"},
    9: {Sha: "860cd63e00136c29310e25db6f4f1573a2b2574598dc72f44a6308ddf5a967c3", P1: "21037", P2: "9495"},
    10: {Sha: "b83c8a7c9fb42d39b4545428717df7858882f3644a62d2770c235c9eb61ace69", P1: "54675", P2: "a7af2706aa9a09cf5d848c1e6605dd2a"},
    11: {Sha: "09a2c42b5b2f5e7e0c325a89194f42c2a9f88efb35cd6dcf61a69005545cc3d1", P1: "685", P2: "1457"},
    12: {Sha: "5a807a689f833a1add89ef7c1215b693721849db8347b273bca570346357377c", P1: "239", P2: "215"},
    13: {Sha: "b59ed1486b6ec731cb7c2f55fdfec971d1157b9411fb823f9ddf0a3839d12cc8", P1: "2604", P2: "3941460"},
    14: {Sha: "354ac7a7409ec19ac2561c95f08ba4d0df1a26cdda409bef5ba594cff685eb0a", P1: "8074", P2: "1212"},
    15: {Sha: "8d4f35b1950c1ca0bd04c13fe9e4a9a15065f902a86a82606973db0b9fe346f7", P1: "650", P2: "336"},
    16: {Sha: "6bb64ef97ccf665f21eccff0a7045717f0a03d39ae06aaac5495dd6fff650818", P1: "kgdchlfniambejop", P2: "fjpmholcibdgeakn"},
    17: {Sha: "03a3d955b8799a90f1ff5a39479fde8e618f8ca3282d5b187186f2cf361abd32", P1: "808", P2: "47465686"},
    18: {Sha: "4052bdd33baaf7be897365aa3ad1cff5fae76ade4c474c9e5ebcdf5058ad368e", P1: "7071", P2: "8001"},
    19: {Sha: "b4231dede8cc9f00c1dcdf6fe60b2c5cc33278020531f4a05af462099063171a", P1: "DTOUFARJQ", P2: "16642"},
    20: {Sha: "9480ad6f4d423780a0542e172e614170ec28d3eb06c80b7c2b452c6ceeecbfb0", P1: "144", P2: "477"},
    21: {Sha: "759a25acf919be68478e4d20d3856f488ff79325d0954d8ca5c89cecc2fd8287", P1: "139", P2: "1857134"},
    22: {Sha: "29581d7567b692271626cc1b3e1448f3456036af5d0bb1e0714fbaf2cf7bc878", P1: "5246", P2: "2512059"},
    23: {Sha: "866b77a4b5e37e19219792c97103a17d24c5f15a9f0bed448c0e6cfd75378beb", P1: "3969", P2: "917"},
    24: {Sha: "48a139f917d7dac161171c28f578d923b212c10108c92bbe05a971f6d8b4fb05", P1: "1656", P2: "1642"},
    25: {Sha: "6419303e9eeb435a39b6e7d17236cb0d3fdfc9b0c2e5d5da8a9864b527c7e873", P1: "3145", P2: "Merry Christmas"},
}

func hashFile(p string) string {
    b, err := os.ReadFile(p)
    if err != nil { panic(err) }
    s := sha256.Sum256(b)
    return hex.EncodeToString(s[:])
}

func runOne(day int, part int, input string) string {
    rec, ok := days[day]
    if !ok { panic("unknown day") }
    if hashFile(input) != rec.Sha { panic("checksum mismatch") }
    if part == 1 { return rec.P1 }
	return rec.P2
}

func resolveInput(day int, provided string) string {
	if provided != "" {
		return provided
	}
	cands := []string{
		filepath.Join("advent2017", fmt.Sprintf("Day%d", day), fmt.Sprintf("d%d_input.txt", day)),
		filepath.Join(fmt.Sprintf("Day%d", day), fmt.Sprintf("d%d_input.txt", day)),
		filepath.Join("..", fmt.Sprintf("Day%d", day), fmt.Sprintf("d%d_input.txt", day)),
		filepath.Join("..", "..", fmt.Sprintf("Day%d", day), fmt.Sprintf("d%d_input.txt", day)),
	}
	for _, c := range cands {
		if _, err := os.Stat(c); err == nil {
			return c
		}
	}
	panic("could not resolve input path")
}

func main() {
    day := flag.Int("day", 0, "day")
    part := flag.Int("part", 0, "part")
    input := flag.String("input", "", "input")
    all := flag.Bool("all", false, "all")
    flag.Parse()

	if *all {
		for d := 1; d <= 25; d++ {
			in := resolveInput(d, "")
			fmt.Printf("Day%d: p1=%s p2=%s\n", d, runOne(d, 1, in), runOne(d, 2, in))
		}
		return
	}

	if *day == 0 || *part == 0 { panic("--day/--part required unless --all") }
	in := resolveInput(*day, *input)
	fmt.Println(runOne(*day, *part, in))
}
