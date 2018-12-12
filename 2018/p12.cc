// p12.cc

// Written by Jakob Ruhe 2018-12-12

// Build with:
// g++ --std=c++17 -O2 -Wall p12.cc -o p12

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

const string test_input = R"(initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
)";

class State {
public:
  string pots;
  State(const string& pots = "") : pots(pots) { }
};

class Rule {
public:
  string pattern;
  char result;
  Rule(const string& pattern, char result) : pattern(pattern), result(result) { }
};

typedef vector<Rule> Rules;

State state_from_string(const string& str)
{
  istringstream is(str);
  string w1, w2, w3;
  is >> w1 >> w2 >> w3;
  State state(w3);
  return state;
}

Rule rule_from_string(const string& str)
{
  istringstream is(str);
  string w1, w2, w3;
  is >> w1 >> w2 >> w3;
  assert(w3.size() == 1);
  assert(w3[0] == '#' || w3[0] == '.');
  assert(w1.size() == 5);
  Rule rule(w1, w3[0]);
  return rule;
}

void parse(istream& is, State& state, Rules& rules)
{
  string line;
  getline(is, line);
  state = state_from_string(line);
  getline(is, line);
  while (getline(is, line)) {
    rules.push_back(rule_from_string(line));
  }
}

bool match(const string& pots, size_t pos, const string& pattern)
{
  for (size_t i = 0; i < pattern.length(); i++) {
    if (pots[i + pos] != pattern[i]) {
      return false;
    }
  }
  return true;
}

char find_rule(const string& pots, size_t pos, const Rules& rules)
{
  for (auto it = rules.begin(); it != rules.end(); ++it) {
    if (match(pots, pos, it->pattern)) {
      return it->result;
    }
  }
  return '.';
}

void next(State& state, const Rules& rules)
{
  State prev_state(state);
  const size_t margin = 2;
  for (size_t i = 0; i < state.pots.size() - margin * 2; i++) {
    state.pots[i + margin] = find_rule(prev_state.pots, i, rules);
  }
}

value_t calc_sum(const State& state, value_t offset)
{
  value_t sum = 0;
  value_t pot = -offset;
  for (auto it = state.pots.begin(); it != state.pots.end(); ++it) {
    if (*it == '#') {
      sum += pot;
    }
    pot++;
  }
  return sum;
}

int left_adjust(string& str, int margin)
{
  size_t first = str.find('#');
  assert(first != string::npos);
  if (first > margin) {
    int num_erased = first - margin;
    str.erase(0, num_erased);
    return -num_erased;
  }
  else if (first < margin) {
    int num_added = margin - first;
    for (int i = 0; i < num_added; i++) {
      str.insert(0, ".");
    }
    return num_added;
  }
  return 0;
}

void right_adjust(string& str, int margin)
{
  size_t last = str.rfind('#');
  assert(last != string::npos);
  str.resize(last + 1);
  for (int i = 0; i < margin; i++) {
    str.append(".");
  }
}

value_t solve(istream& is, value_t generations, bool print)
{
  State state;
  Rules rules;
  parse(is, state, rules);

  if (print) {
    for (auto it = rules.begin(); it != rules.end(); ++it) {
      cout << it->pattern << " => " << it->result << endl;
    }
  }

  assert(find_rule(".....", 0, rules) == '.');

  const int margin = 5;
  value_t offset = left_adjust(state.pots, margin);
  value_t prev_offset = offset;
  right_adjust(state.pots, margin);

  State prev_state(state);
  size_t generation;
  for (generation = 0; generation < generations; generation++) {
    if (print) {
      cout << setw(2) << generation << ": " << state.pots << " (" << offset << ")" << endl;
    }
    next(state, rules);
    offset += left_adjust(state.pots, margin);
    right_adjust(state.pots, margin);

    if (state.pots == prev_state.pots) {
      cout << "No need to conintue, the pattern is repeating itself after generation " << generation << endl;
      break;
    }
    prev_state = state;
    prev_offset = offset;
  }

  cout << setw(2) << generation << ": " << state.pots << " (" << offset << ")" << endl;

  value_t sum = calc_sum(state, offset);
  cout << "Sum at generation " << generation << ": " << sum << endl;

  if (generation < generations) {
    value_t generations_left = generations - generation - 1;
    value_t offset_diff = offset - prev_offset;
    value_t offset_at_last_generation = offset + generations_left * offset_diff;
    sum = calc_sum(state, offset_at_last_generation);
    cout << "Sum at generation " << generations << ": " << sum << endl;
  }

  return sum;
}

void test()
{
  assert(match("##.##.", 0, "##.##"));
  assert(match(".##.##.", 1, "##.##"));

  if (true) {
    string str = ".....#";
    assert(left_adjust(str, 5) == 0);
    assert(str == ".....#");
  }
  if (true) {
    string str = "......#";
    assert(left_adjust(str, 5) == -1);
    assert(str == ".....#");
  }
  if (true) {
    string str = "....#";
    assert(left_adjust(str, 5) == 1);
    assert(str == ".....#");
  }

  if (true) {
    string str = "#.....";
    right_adjust(str, 5);
    assert(str == "#.....");
  }
  if (true) {
    string str = "#......";
    right_adjust(str, 5);
    assert(str == "#.....");
  }
  if (true) {
    string str = "#....";
    right_adjust(str, 5);
    assert(str == "#.....");
  }

  istringstream is(test_input);
  assert(solve(is, 20, true) == 325);
}

int main()
{
  test();
  if (true) {
    ifstream is("p12_input.txt");
    value_t p1 = solve(is, 20, true);
    cout << "P1: The sum of the pots containing plants is " << p1 << endl;
  }
  if (true) {
    ifstream is("p12_input.txt");
    value_t iterations = 50000000000LL;
    value_t p2 = solve(is, iterations , false);
    cout << "P2: The sum of the pots containing plants after "
      << iterations << " iterations is: "<< p2 << endl;
  }
  return 0;
}
