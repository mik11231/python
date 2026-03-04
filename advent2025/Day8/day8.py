#!/usr/bin/env python3
"""Advent of Code 2025 - Day 8: Playground"""

from pathlib import Path
import math

class UnionFind:
    """Union-Find (Disjoint Set) data structure for tracking circuits."""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n  # Track size of each circuit
    
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
            # Already in the same circuit
            return False
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
        
        return True
    
    def get_circuit_sizes(self):
        """Get sizes of all circuits (only root nodes)."""
        sizes = []
        for i in range(len(self.parent)):
            if self.parent[i] == i:  # Root node
                sizes.append(self.size[i])
        return sizes

def distance(p1, p2):
    """Calculate 3D Euclidean distance between two points."""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def solve():
    """Solve Day 8 Part 1: Connect 1000 shortest pairs and multiply three largest circuits."""
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
    
    # Connect the 1000 shortest pairs
    print("Connecting 1000 shortest pairs...")
    connections_made = 0
    for dist, i, j in pairs[:1000]:
        if uf.union(i, j):
            connections_made += 1
    
    print(f"Made {connections_made} connections (some pairs were already connected)")
    
    # Get circuit sizes
    circuit_sizes = uf.get_circuit_sizes()
    circuit_sizes.sort(reverse=True)
    
    print(f"Number of circuits: {len(circuit_sizes)}")
    print(f"Three largest circuits: {circuit_sizes[:3]}")
    
    # Multiply the three largest
    result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
    
    return result

if __name__ == "__main__":
    result = solve()
    print(f"\nProduct of three largest circuits: {result}")





