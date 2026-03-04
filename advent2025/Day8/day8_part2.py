#!/usr/bin/env python3
"""Advent of Code 2025 - Day 8 Part 2: Playground"""

from pathlib import Path
import math

class UnionFind:
    """Union-Find (Disjoint Set) data structure for tracking circuits."""
    def __init__(self, n):
        """
        Run `__init__` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: self, n.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
    
    def find(self, x):
        """Find the root of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union two elements. Returns True if they were in different circuits."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        
        return True
    
    def num_circuits(self):
        """Count number of separate circuits."""
        count = 0
        for i in range(len(self.parent)):
            if self.parent[i] == i:
                count += 1
        return count

def distance(p1, p2):
    """Calculate 3D Euclidean distance between two points."""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def solve():
    """Solve Day 8 Part 2: Connect until all in one circuit, then multiply X coordinates of last connection."""
    # Read all junction boxes
    boxes = []
    with open(Path(__file__).with_name('d8_input.txt'), 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                coords = [int(x) for x in line.split(',')]
                boxes.append(tuple(coords))
    
    n = len(boxes)
    print(f"Read {n} junction boxes")
    
    # Calculate all pairwise distances
    print("Calculating pairwise distances...")
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(boxes[i], boxes[j])
            pairs.append((dist, i, j))
    
    # Sort by distance
    print(f"Sorting {len(pairs)} pairs...")
    pairs.sort()
    
    # Initialize union-find
    uf = UnionFind(n)
    
    # Connect pairs until all boxes are in one circuit
    print("Connecting pairs until all in one circuit...")
    last_connection = None
    
    for dist, i, j in pairs:
        if uf.union(i, j):
            # This was a new connection
            num_circuits = uf.num_circuits()
            if num_circuits == 1:
                # All boxes are now in one circuit!
                last_connection = (i, j)
                print(f"All boxes connected! Last connection: box {i} <-> box {j}")
                print(f"  Box {i}: {boxes[i]}")
                print(f"  Box {j}: {boxes[j]}")
                break
    
    if last_connection is None:
        print("Error: Could not connect all boxes into one circuit")
        return 0
    
    # Multiply X coordinates of the last connection
    i, j = last_connection
    x1 = boxes[i][0]
    x2 = boxes[j][0]
    result = x1 * x2
    
    print(f"\nX coordinates: {x1} * {x2} = {result}")
    
    return result

if __name__ == "__main__":
    result = solve()
    print(f"\nProduct of X coordinates of last connection: {result}")





