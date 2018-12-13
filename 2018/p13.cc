// p13.cc

// Written by Jakob Ruhe 2018-12-13

// Build with:
// g++ --std=c++17 -O2 -Wall p13.cc -o p13

#include <algorithm>
#include <iostream>
#include <list>
#include <vector>
#include <sstream>
#include <fstream>
#include <string>
#include <cassert>
#include <iomanip>

using namespace std;

typedef int64_t value_t;

const string test_input1 = R"(/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/
)";

const string test_input2 = R"(/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/
)";

typedef char Direction;
const Direction None = ' ';
const Direction Right = '>';
const Direction Up = '^';
const Direction Left = '<';
const Direction Down = 'v';

struct Point {
  int x;
  int y;
  Point(int x, int y) : x(x), y(y) { }
  bool operator==(const Point& p) { return p.x == x && p.y == y; }
};

ostream& operator<<(ostream& os, const Point& p) {
  os << p.x << "," << p.y;
  return os;
}

struct Cart {
  Point location;
  Direction direction;
  char standing_on;
  int turns;
  bool collided;
  Cart(Point location, Direction direction, char standing_on) :
    location(location), direction(direction), standing_on(standing_on), turns(0), collided(false) { }
};

struct Grid {
  vector<string> rows;
  char get(const Point& p) {
    return rows[p.y][p.x];
  }
  void set(const Point& p, char c) {
    rows[p.y][p.x] = c;
  }
};

struct Game {
  Grid grid;
  vector<Cart> carts;
  int ticks;
  Game() : ticks(0) { }
};

Direction direction_of_cart(char c)
{
  switch (c) {
    case '>':
    return Right;
    case '^':
    return Up;
    case '<':
    return Left;
    case 'v':
    return Down;
    default:
    return None;
  }
}

void get_carts(Grid& grid, vector<Cart>& carts)
{
  for (int y = 0; y < grid.rows.size(); y++) {
    auto& row = grid.rows[y];
    for (int x = 0; x < row.length(); x++) {
      Direction dir = direction_of_cart(row[x]);
      if (dir == None) {
        continue;
      }
      char standing_on;
      switch (dir) {
        case Right:
        case Left:
        standing_on = '-';
        break;
        case Up:
        case Down:
        standing_on = '|';
        break;
        default:
        assert(false);
      }
      Cart cart(Point(x, y), dir, standing_on);
      carts.push_back(cart);
    }
  }
}

Direction turn_left(Direction dir)
{
  switch (dir)
  {
    case Right:
    return Up;
    case Up:
    return Left;
    case Left:
    return Down;
    case Down:
    return Right;
    default:
    assert(false);
  }
}

Direction turn_right(Direction dir)
{
  switch (dir)
  {
    case Right:
    return Down;
    case Up:
    return Right;
    case Left:
    return Up;
    case Down:
    return Left;
    default:
    assert(false);
  }
}

void parse_grid(istream& is, Grid& grid)
{
  string line;
  while (getline(is, line)) {
    grid.rows.push_back(line);
  }
}

bool move_cart(Game& game, Cart& cart)
{
  game.grid.set(cart.location, cart.standing_on);
  switch (cart.direction) {
    case Right:
    cart.location.x++;
    break;
    case Up:
    cart.location.y--;
    break;
    case Left:
    cart.location.x--;
    break;
    case Down:
    cart.location.y++;
    break;
    default:
    assert(false);
  }
  char c = game.grid.get(cart.location);
  Direction dir = direction_of_cart(c);
  if (dir != None) {
    return true;
  }

  switch (c) {
    case '/':
    if (cart.direction == Right) {
      cart.direction = Up;
    }
    else if (cart.direction == Up) {
      cart.direction = Right;
    }
    else if (cart.direction == Left) {
      cart.direction = Down;
    }
    else if (cart.direction == Down) {
      cart.direction = Left;
    }
    else {
      assert(false);
    }
    break;
    case '\\':
    if (cart.direction == Right) {
      cart.direction = Down;
    }
    else if (cart.direction == Up) {
      cart.direction = Left;
    }
    else if (cart.direction == Left) {
      cart.direction = Up;
    }
    else if (cart.direction == Down) {
      cart.direction = Right;
    }
    else {
      assert(false);
    }
    break;
    case '+':
    if (cart.turns % 3 == 0) {
      cart.direction = turn_left(cart.direction);
    }
    else if (cart.turns % 3 == 2) {
      cart.direction = turn_right(cart.direction);
    }
    cart.turns++;
    break;
    case '-':
    break;
    case '|':
    break;
    default:
    cerr << "Not expected character on grid at " << cart.location << ": '" << c << "'" << endl;
    assert(false);
  }

  cart.standing_on = c;
  game.grid.set(cart.location, cart.direction);

  return false;
}

Point solve1(Game game)
{
  get_carts(game.grid, game.carts);
  cout << "Number of carts: " << game.carts.size() << endl;
  while (true) {
    for (auto it = game.carts.begin(); it != game.carts.end(); ++it) {
      if (move_cart(game, *it)) {
        cout << "Tick " << game.ticks << ": Collision at: " << it->location << endl;
        return it->location;
      }
    }
    game.ticks++;
  }
}

auto find_not_collided_cart(Game& game, const Point& p)
{
  for (auto it = game.carts.begin(); it != game.carts.end(); ++it) {
    if (!it->collided && it->location == p) {
      return it;
    }
  }
  assert(false);
}

Point solve2(Game game)
{
  get_carts(game.grid, game.carts);
  cout << "Number of carts: " << game.carts.size() << endl;
  while (game.carts.size() > 1) {
    for (auto it = game.carts.begin(); it != game.carts.end(); ++it) {
      if (!it->collided && move_cart(game, *it)) {
        it->collided = true;
        auto other = find_not_collided_cart(game, it->location);
        game.grid.set(other->location, other->standing_on);
        other->collided = true;
        cout << "Tick " << game.ticks << ": Collision at: " << it->location << endl;
      }
    }
    for (auto it = game.carts.begin(); it != game.carts.end();) {
      if (it->collided) {
        it = game.carts.erase(it);
        cout << "Tick " << game.ticks << ": Removed a cart, carts left: " << game.carts.size() << endl;
      }
      else {
        ++it;
      }
    }
    game.ticks++;
  }
  assert(game.carts.size() == 1);
  cout << "Last cart at: " << game.carts[0].location << " heading " << game.carts[0].direction << endl;
  return game.carts[0].location;
}

void test1()
{
  Game game;
  istringstream is(test_input1);
  parse_grid(is, game.grid);
  assert(solve1(game) == Point(7, 3));
}

void test2()
{
  Game game;
  istringstream is(test_input2);
  parse_grid(is, game.grid);
  assert(solve2(game) == Point(6, 4));
}

int main()
{
  test1();
  test2();

  Game game;
  ifstream is("p13_input.txt");
  parse_grid(is, game.grid);
  solve1(game);
  solve2(game);
  return 0;
}
