#!/usr/bin/env python3
"""Advent of Code 2022 Day 19 Part 2.

Same blueprint optimization but 32 minutes and only first 3 blueprints.
Returns the product of max geodes for each of those three blueprints.
"""
from functools import lru_cache
from pathlib import Path
import re

def best(bp,minutes):
    """Return max geodes for a blueprint in given minutes via DFS."""
    ore_ore,clay_ore,obs_ore,obs_clay,geo_ore,geo_obs=bp
    max_ore=max(ore_ore,clay_ore,obs_ore,geo_ore)

    @lru_cache(None)
    def dfs(t,ore,clay,obs,geode,ro,rc,rb,rg):
        """Recursive DFS for max geodes given time and state."""
        if t==0: return geode
        ore=min(ore, max_ore*t)
        clay=min(clay, obs_clay*t)
        obs=min(obs, geo_obs*t)

        if ore>=geo_ore and obs>=geo_obs:
            return dfs(t-1, ore-geo_ore+ro, clay+rc, obs-geo_obs+rb, geode+rg, ro,rc,rb,rg+1)

        bestv=dfs(t-1, ore+ro, clay+rc, obs+rb, geode+rg, ro,rc,rb,rg)
        if ore>=obs_ore and clay>=obs_clay and rb<geo_obs:
            bestv=max(bestv, dfs(t-1, ore-obs_ore+ro, clay-obs_clay+rc, obs+rb, geode+rg, ro,rc,rb+1,rg))
        if ore>=clay_ore and rc<obs_clay:
            bestv=max(bestv, dfs(t-1, ore-clay_ore+ro, clay+rc, obs+rb, geode+rg, ro,rc+1,rb,rg))
        if ore>=ore_ore and ro<max_ore:
            bestv=max(bestv, dfs(t-1, ore-ore_ore+ro, clay+rc, obs+rb, geode+rg, ro+1,rc,rb,rg))
        return bestv

    return dfs(minutes,0,0,0,0,1,0,0,0)

def solve(s):
    """Parse first 3 blueprints and return product of their max geodes at 32 min."""
    bps=[]
    for ln in s.splitlines()[:3]:
        if not ln: continue
        _,oo,co,bo,bc,go,gob=map(int,re.findall(r'\d+',ln))
        bps.append((oo,co,bo,bc,go,gob))
    ans=1
    for bp in bps: ans*=best(bp,32)
    return ans

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d19_input.txt').read_text()))
