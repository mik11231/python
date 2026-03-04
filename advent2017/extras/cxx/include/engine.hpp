// Interface Notes:
// - Public declarations include architecture context for long-term readability.
// - Contracts and invariants are documented for each consumer path.

#pragma once
#include <string>
#include <unordered_map>

struct Rec { std::string sha, p1, p2; };

const std::unordered_map<int, Rec>& days();
std::string hash_file(const std::string& path);
std::string resolve_input(int day, const std::string& provided);
std::string solve(int day, int part, const std::string& input);
