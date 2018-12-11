// p11.c

// Written by Jakob Ruhe 2018-12-11

// Build with:
// gcc --std=c99 -O2 -Wall p11.c -o p11

#include <stdio.h>
#include <string.h>

#define GridSize 300

typedef int value_t;

value_t calc_power_level(int x, int y, value_t serial)
{
  value_t rack_id = x + 10;
  value_t power_level = rack_id * y;
  power_level += serial;
  power_level *= rack_id;
  value_t h = (power_level / 100) % 10 - 5;
  return h;
}

value_t square(int minx, int miny, int size, value_t serial)
{
  value_t sum = 0;
  for (int y = miny; y < miny + size; y++) {
    for (int x = minx; x < minx + size; x++) {
      sum += calc_power_level(x, y, serial);
    }
  }
  return sum;
}

void solve1(value_t serial)
{
  value_t best_value;
  int best_x = -1, best_y, best_z;
  int z = 3;
  for (int miny = 1; miny < GridSize - z + 1; miny++) {
    for (int minx = 1; minx < GridSize - z + 1; minx++) {
      value_t value = square(minx, miny, z, serial);
      if (best_x == -1 || (value > best_value)) {
        best_value = value;
        best_x = minx;
        best_y = miny;
        best_z = z;
      }
    }
  }
  printf("solve1(%d): %d,%d, power level: %d\n",
      serial, best_x, best_y, best_value);
}

void solve2(value_t serial)
{
  value_t best_value;
  int best_x = -1, best_y, best_z;
  for (int miny = 1; miny < GridSize + 1; miny++) {
    for (int minx = 1; minx < GridSize + 1; minx++) {
      int zmax = miny > minx ? GridSize - miny + 1: GridSize - minx + 1;
      value_t value = calc_power_level(minx, miny, serial);
      for (int z = 1; z <= zmax; z++) {
        if (z >= 2) {
          int x, y;
          y = miny + z - 1;
          for (x = minx; x < minx + z; x++) {
            value += calc_power_level(x, y, serial);
          }
          x = minx + z - 1;
          for (y = miny; y < miny + z; y++) {
            value += calc_power_level(x, y, serial);
          }
        }
        if (best_x == -1 || (value > best_value)) {
          best_value = value;
          best_x = minx;
          best_y = miny;
          best_z = z;
        }
      }
    }
  }
  printf("solve2(%d): %d,%d,%d, power level: %d\n",
      serial, best_x, best_y, best_z, best_value);
}

int main()
{
  solve1(18);
  solve1(42);
  solve1(7672);
  solve2(18);
  solve2(42);
  solve2(7672);
  return 0;
}
