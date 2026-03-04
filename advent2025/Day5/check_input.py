#!/usr/bin/env python3
"""Check the structure of the input file"""

with open('Day5/d5_input.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

ranges = []
ids = []

for line in lines:
    if '-' in line:
        ranges.append(line)
    else:
        ids.append(line)

print(f'Total lines: {len(lines)}')
print(f'Ranges: {len(ranges)}')
print(f'IDs: {len(ids)}')
print(f'\nFirst range: {ranges[0]}')
print(f'Last range: {ranges[-1]}')
print(f'\nFirst ID: {ids[0]}')
print(f'Last ID: {ids[-1]}')






