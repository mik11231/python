#!/usr/bin/env python3
"""Advent of Code 2022 Day 19 Part 1.

Not Enough Minerals: optimize robot production to maximize geodes in 24 minutes.
Each blueprint defines ore costs for ore/clay/obsidian/geode bots. Uses DFS with
memoization and resource caps to prune the search space.
"""
from functools import lru_cache
from pathlib import Path
import re

def best(bp,minutes):
    """Return max geodes producible for a blueprint in given minutes via DFS."""
    ore_ore,clay_ore,obs_ore,obs_clay,geo_ore,geo_obs=bp
    max_ore=max(ore_ore,clay_ore,obs_ore,geo_ore)

    @lru_cache(None)
    def dfs(t,ore,clay,obs,geode,ro,rc,rb,rg):
        """Recursive DFS for max geodes given time and state."""
        if t==0: return geode
        # cap resources to reduce state space
        ore=min(ore, max_ore*t)
        clay=min(clay, obs_clay*t)
        obs=min(obs, geo_obs*t)

        bestv=geode

        # prioritize geode bot when possible
        built=False
        if ore>=geo_ore and obs>=geo_obs:
            bestv=max(bestv, dfs(t-1, ore-geo_ore+ro, clay+rc, obs-geo_obs+rb, geode+rg, ro,rc,rb,rg+1))
            return bestv

        if ore>=obs_ore and clay>=obs_clay and rb<geo_obs:
            bestv=max(bestv, dfs(t-1, ore-obs_ore+ro, clay-obs_clay+rc, obs+rb, geode+rg, ro,rc,rb+1,rg))
            built=True
        if ore>=clay_ore and rc<obs_clay:
            bestv=max(bestv, dfs(t-1, ore-clay_ore+ro, clay+rc, obs+rb, geode+rg, ro,rc+1,rb,rg))
            built=True
        if ore>=ore_ore and ro<max_ore:
            bestv=max(bestv, dfs(t-1, ore-ore_ore+ro, clay+rc, obs+rb, geode+rg, ro+1,rc,rb,rg))
            built=True
        # wait option
        if not built or True:
            bestv=max(bestv, dfs(t-1, ore+ro, clay+rc, obs+rb, geode+rg, ro,rc,rb,rg))
        return bestv

    return dfs(minutes,0,0,0,0,1,0,0,0)

def solve(s):
    """Parse blueprints and return sum of (quality = id * max geodes) for each."""
    ans=0
    for ln in s.splitlines():
        if not ln: continue
        nums=list(map(int,re.findall(r'\d+',ln)))
        i,oo,co,bo,bc,go,gob=nums
        ans += i*best((oo,co,bo,bc,go,gob),24)
    return ans

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d19_input.txt').read_text()))
