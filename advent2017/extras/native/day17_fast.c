#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int solve_part1(int step) {
    int buf[2018];
    int size = 1;
    int pos = 0;
    buf[0] = 0;
    for (int v = 1; v <= 2017; ++v) {
        pos = ((pos + step) % size) + 1;
        memmove(&buf[pos + 1], &buf[pos], (size - pos) * sizeof(int));
        buf[pos] = v;
        ++size;
    }
    return buf[(pos + 1) % size];
}

static int solve_part2(int step) {
    int pos = 0;
    int after0 = 0;
    int size = 1;
    for (int v = 1; v <= 50000000; ++v) {
        pos = ((pos + step) % size) + 1;
        if (pos == 1) after0 = v;
        ++size;
    }
    return after0;
}

int main(int argc, char** argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s <part> <step>\n", argv[0]);
        return 2;
    }
    int part = atoi(argv[1]);
    int step = atoi(argv[2]);
    if (part == 1) {
        printf("%d\n", solve_part1(step));
        return 0;
    }
    if (part == 2) {
        printf("%d\n", solve_part2(step));
        return 0;
    }
    return 3;
}
