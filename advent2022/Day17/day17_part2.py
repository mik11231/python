#!/usr/bin/env python3
"""Advent of Code 2022 Day 17 Part 2.

Same pyroclastic flow but for 1 trillion rocks. Uses cycle detection: when the
same (shape index, jet index, skyline profile) repeats, extrapolate the
remaining height from the cycle period and height gain.
"""
from pathlib import Path

SHAPES=[
    [(0,0),(1,0),(2,0),(3,0)],
    [(1,0),(0,1),(1,1),(2,1),(1,2)],
    [(0,0),(1,0),(2,0),(2,1),(2,2)],
    [(0,0),(0,1),(0,2),(0,3)],
    [(0,0),(1,0),(0,1),(1,1)],
]

def solve(s,target=1_000_000_000_000):
    """Simulate rocks with cycle detection to handle 1 trillion rocks."""
    jets=s.strip()
    occ={(x,0) for x in range(7)}
    top=0; ji=0; i=0
    seen={}
    added=0

    def profile(top):
        """Return relative skyline (heights from top) for cycle detection."""
        out=[]
        for x in range(7):
            y=top
            while y>0 and (x,y) not in occ and top-y<80: y-=1
            out.append(top-y)
        return tuple(out)

    while i<target:
        sh=SHAPES[i%5]
        x,y=2,top+4
        while True:
            d=jets[ji%len(jets)]; ji=(ji+1)%len(jets)
            nx=x+(-1 if d=='<' else 1)
            if all(0<=nx+sx<7 and (nx+sx,y+sy) not in occ for sx,sy in sh): x=nx
            if all((x+sx,y+sy-1) not in occ for sx,sy in sh): y-=1
            else:
                for sx,sy in sh: occ.add((x+sx,y+sy)); top=max(top,y+sy)
                break
        i+=1

        key=(i%5,ji,profile(top))
        if key in seen and i<target:
            pi,ptop=seen[key]
            clen=i-pi; cheight=top-ptop
            rem=target-i
            k=rem//clen
            if k:
                i += k*clen
                added += k*cheight
        else:
            seen[key]=(i,top)

        # trim old rows
        min_keep=top-120
        occ={p for p in occ if p[1]>=min_keep or p[1]==0}

    return top+added

if __name__=='__main__':
    print(solve(Path(__file__).with_name('d17_input.txt').read_text()))
