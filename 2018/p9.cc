// p9.cc

// Written by Jakob Ruhe 2018-12-09

// Build with:
// g++ --std=c++17 -O2 -Wall p9.cc -o p9

#include <algorithm>
#include <iostream>
#include <list>
#include <vector>

using namespace std;

typedef uint64_t marble_t;
typedef uint64_t score_t;

class Deck {
  std::list<marble_t> marbles;
  std::list<marble_t>::iterator current;

public:
  Deck();
  void change_clockwise(int steps);
  void change_counter_clockwise(int steps);
  void insert(marble_t marble);
  marble_t remove();
  void print(ostream& os);
};

class Game {
  std::vector<score_t> player_scores;
  marble_t current_marble;
  Deck deck;

  int current_player();
  void next();

public:
  Game(int num_players);
  score_t highest_score();
  void play(marble_t until, bool print);
  void print_state();
};

Deck::Deck() : marbles({0}), current(marbles.begin())
{

}

void Deck::change_clockwise(int steps)
{
  while (steps--) {
    ++this->current;
    if (this->current == this->marbles.end()) {
      this->current = this->marbles.begin();
    }
  }
}

void Deck::change_counter_clockwise(int steps)
{
  while (steps--) {
    if (this->current == this->marbles.begin()) {
      this->current = this->marbles.end();
    }
    --this->current;
  }
}

void Deck::insert(marble_t marble)
{
  this->current = this->marbles.insert(this->current, marble);
}

marble_t Deck::remove()
{
  marble_t removed = *this->current;
  this->current = this->marbles.erase(this->current);
  return removed;
}

void Deck::print(ostream& os)
{
  for (auto it = this->marbles.begin(); it != this->marbles.end(); ++it) {
    if (it == current) {
      os << "(" << *it << ") ";
    }
    else {
      os << *it << " ";
    }
  }
}

Game::Game(int num_players) :
  player_scores(num_players, 0), current_marble(0)
{

}

score_t Game::highest_score()
{
  score_t highest = 0;
  for (auto it = this->player_scores.begin(); it != this->player_scores.end(); ++it) {
    if (*it > highest) {
      highest = *it;
    }
  }
  return highest;
}

void Game::play(marble_t until, bool print)
{
  while (this->current_marble < until) {
    this->next();
    if (print) {
      this->print_state();
    }
  }
}

int Game::current_player()
{
  return (this->current_marble - 1) % this->player_scores.size();
}

void Game::print_state()
{
  cout << "[" << current_player() << "]";
  deck.print(cout);
  cout << endl;
}

void Game::next()
{
  this->current_marble++;
  auto player = this->current_player();
  if (this->current_marble % 23 == 0) {
    this->player_scores[player] += this->current_marble;
    this->deck.change_counter_clockwise(7);
    marble_t removed = this->deck.remove();
    this->player_scores[player] += removed;
  }
  else {
    this->deck.change_clockwise(2);
    this->deck.insert(this->current_marble);
  }
}

score_t solve(int num_players, marble_t last_marble, bool print)
{
  Game game(num_players);
  game.play(last_marble, print);
  return game.highest_score();
}

int main()
{
  auto res = solve(9, 25, true);
  cout << "1: " << res << endl;
  cout << solve(10, 1618, false) << endl;
  cout << solve(13, 7999, false) << endl;
  cout << solve(17, 1104, false) << endl;
  cout << solve(21, 6111, false) << endl;
  cout << solve(30, 5807, false) << endl;
  cout << "Answer to subproblem 1 is: " << solve(423, 71944, false) << endl;
  cout << "Answer to subproblem 2 is: " << solve(423, 7194400, false) << endl;
  return 0;
}
