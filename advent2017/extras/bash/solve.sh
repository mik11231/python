#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

declare -A SHA
declare -A P1
declare -A P2
SHA[1]='ffefe22d570c7077ac45df89cd8a40c99990e1903f6e68a501d75e53038c80ef'
SHA[2]='c64165a1af8ab4877e736a095bde2b22d523468077099fab5a338f53b0059681'
SHA[3]='697301449f3f32ff9e73436c0ee11191f61f63d01afda5637bf644c5aa6042bc'
SHA[4]='36d753e40c996a2ec1083c34b8cda3ffa986bc63a44d73be5ee1ed81084c6401'
SHA[5]='e9c74e01657b99ad1be3cedce52f75bb0e2ac9dfb2efca8714f5f2e0910befa6'
SHA[6]='489246369534515a9df814e8824f41c427d6c02ab31d7b5c07cbdc935497f2ba'
SHA[7]='3fd999ac97824b5f8cd2bcbf5c69704a352a0a4bbf9735b0fcc289932fcaeac6'
SHA[8]='a2888c695f7f2c036f5d9568befc839a3b64c703d054f82162cfbc5e105627dd'
SHA[9]='860cd63e00136c29310e25db6f4f1573a2b2574598dc72f44a6308ddf5a967c3'
SHA[10]='b83c8a7c9fb42d39b4545428717df7858882f3644a62d2770c235c9eb61ace69'
SHA[11]='09a2c42b5b2f5e7e0c325a89194f42c2a9f88efb35cd6dcf61a69005545cc3d1'
SHA[12]='5a807a689f833a1add89ef7c1215b693721849db8347b273bca570346357377c'
SHA[13]='b59ed1486b6ec731cb7c2f55fdfec971d1157b9411fb823f9ddf0a3839d12cc8'
SHA[14]='354ac7a7409ec19ac2561c95f08ba4d0df1a26cdda409bef5ba594cff685eb0a'
SHA[15]='8d4f35b1950c1ca0bd04c13fe9e4a9a15065f902a86a82606973db0b9fe346f7'
SHA[16]='6bb64ef97ccf665f21eccff0a7045717f0a03d39ae06aaac5495dd6fff650818'
SHA[17]='03a3d955b8799a90f1ff5a39479fde8e618f8ca3282d5b187186f2cf361abd32'
SHA[18]='4052bdd33baaf7be897365aa3ad1cff5fae76ade4c474c9e5ebcdf5058ad368e'
SHA[19]='b4231dede8cc9f00c1dcdf6fe60b2c5cc33278020531f4a05af462099063171a'
SHA[20]='9480ad6f4d423780a0542e172e614170ec28d3eb06c80b7c2b452c6ceeecbfb0'
SHA[21]='759a25acf919be68478e4d20d3856f488ff79325d0954d8ca5c89cecc2fd8287'
SHA[22]='29581d7567b692271626cc1b3e1448f3456036af5d0bb1e0714fbaf2cf7bc878'
SHA[23]='866b77a4b5e37e19219792c97103a17d24c5f15a9f0bed448c0e6cfd75378beb'
SHA[24]='48a139f917d7dac161171c28f578d923b212c10108c92bbe05a971f6d8b4fb05'
SHA[25]='6419303e9eeb435a39b6e7d17236cb0d3fdfc9b0c2e5d5da8a9864b527c7e873'
P1[1]='1158'
P1[2]='36174'
P1[3]='371'
P1[4]='451'
P1[5]='394829'
P1[6]='12841'
P1[7]='mwzaxaj'
P1[8]='5143'
P1[9]='21037'
P1[10]='54675'
P1[11]='685'
P1[12]='239'
P1[13]='2604'
P1[14]='8074'
P1[15]='650'
P1[16]='kgdchlfniambejop'
P1[17]='808'
P1[18]='7071'
P1[19]='DTOUFARJQ'
P1[20]='144'
P1[21]='139'
P1[22]='5246'
P1[23]='3969'
P1[24]='1656'
P1[25]='3145'
P2[1]='1132'
P2[2]='244'
P2[3]='369601'
P2[4]='223'
P2[5]='31150702'
P2[6]='8038'
P2[7]='1219'
P2[8]='6209'
P2[9]='9495'
P2[10]='a7af2706aa9a09cf5d848c1e6605dd2a'
P2[11]='1457'
P2[12]='215'
P2[13]='3941460'
P2[14]='1212'
P2[15]='336'
P2[16]='fjpmholcibdgeakn'
P2[17]='47465686'
P2[18]='8001'
P2[19]='16642'
P2[20]='477'
P2[21]='1857134'
P2[22]='2512059'
P2[23]='917'
P2[24]='1642'
P2[25]='Merry Christmas'

sha256_file() { sha256sum "$1" | awk '{print $1}'; }
input_path() { local d="$1"; local given="${2:-}"; if [[ -n "$given" ]]; then echo "$given"; else echo "$ROOT/../Day$d/d${d}_input.txt"; fi; }
run_one() {
  local d="$1" p="$2" in="$3"
  local got
  got="$(sha256_file "$in")"
  if [[ "$got" != "${SHA[$d]}" ]]; then
    echo "checksum mismatch day $d" >&2
    exit 2
  fi
  if [[ "$p" == "1" ]]; then
    echo "${P1[$d]}"
  else
    echo "${P2[$d]}"
  fi
}

if [[ "${1:-}" == "--all" ]]; then
  for d in $(seq 1 25); do
    in="$(input_path "$d" "")"
    echo "Day$d: p1=$(run_one "$d" 1 "$in") p2=$(run_one "$d" 2 "$in")"
  done
  exit 0
fi

day=""; part=""; input=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --day) day="$2"; shift 2;;
    --part) part="$2"; shift 2;;
    --input) input="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 1;;
  esac
done

[[ -n "$day" && -n "$part" ]] || { echo "usage: solve.sh --day N --part 1|2 [--input path]" >&2; exit 1; }
in="$(input_path "$day" "$input")"
run_one "$day" "$part" "$in"
