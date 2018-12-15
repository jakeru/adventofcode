// p14.cc

// Written by Jakob Ruhe 2018-12-15

// Build with:
// g++ --std=c++17 -O2 -Wall p14.cc -o p14

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

typedef unsigned char score_t;
typedef size_t pos_t;

struct State {
    vector<pos_t> current_recipes;
    vector<score_t> recipes;

    State(vector<score_t> init) : recipes(init) {
        current_recipes.push_back(0);
        current_recipes.push_back(1);
    }

    void next();
    void add_recipes();
    void pick_new_recipes();
};

vector<score_t> scores_from_string(const string& str)
{
    vector<score_t> scores;
    for (auto it = str.begin(); it != str.end(); ++it) {
        scores.push_back(*it - '0');
    }
    return scores;
}

string to_string(const vector<score_t>& scores, size_t start, size_t num)
{
    string str;
    for (size_t i = start; i < start + num; i++) {
        str.push_back(scores[i] + '0');
    }
    return str;
}

void State::add_recipes()
{
    score_t sum = 0;
    for (auto&& r: current_recipes) {
        sum += recipes[r];
    }
    assert(sum < 100);
    if (sum >= 10) {
        recipes.push_back(sum / 10);
    }
    recipes.push_back(sum % 10);
}

void State::pick_new_recipes()
{
    for (auto&& r: current_recipes) {
        r = (r + 1 + recipes[r]) % recipes.size();
    }
}

void State::next()
{
    add_recipes();
    pick_new_recipes();
}

string solve1(const string& init, pos_t skill_improves_after)
{
    const size_t num_recipes_more = 10;
    State state(scores_from_string(init));
    while (state.recipes.size() < skill_improves_after + num_recipes_more) {
        state.next();
    }
    return to_string(state.recipes, skill_improves_after, num_recipes_more);
}

bool match(const vector<score_t>& needle, const vector<score_t>& haystack, size_t pos)
{
    for (size_t i = 0; i < needle.size(); i++) {
        if (needle[i] != haystack[pos+i]) {
            return false;
        }
    }
    return true;
}

ssize_t find_seq(const vector<score_t>& needle, const vector<score_t>& haystack)
{
    if (haystack.size() < needle.size()) {
        return -1;
    }
    // Do not bother searching already seen part of the haystack.
    size_t start = haystack.size() - needle.size() < 2 ? 0 : haystack.size() - needle.size() - 2;
    for (size_t i = start; i < haystack.size() - needle.size(); i++) {
        if (match(needle, haystack, i)) {
            return i;
        }
    }
    return -1;
}

size_t solve2(const string& init, const string& score_sequence_str)
{
    State state(scores_from_string(init));
    vector<score_t> score_sequence = scores_from_string(score_sequence_str);
    while (true) {
        ssize_t p = find_seq(score_sequence, state.recipes);
        if (p >= 0) {
            return p;
        }
        state.next();
        if (state.recipes.size() % 1000 < 2) {
            cout << state.recipes.size() << endl;
        }
    }
}

void test1()
{
    assert(solve1("37", 9) == "5158916779");
    assert(solve1("37", 5) == "0124515891");
    assert(solve1("37", 18) == "9251071085");
    assert(solve1("37", 2018) == "5941429882");
}

void test2()
{
    assert(solve2("37", "51589") == 9);
    assert(solve2("37", "01245") == 5);
    assert(solve2("37", "92510") == 18);
    assert(solve2("37", "59414") == 2018);
}

int main()
{
    test1();
    test2();
    string p1 = solve1("37", 633601);
    cout << "The answer to subproblem 1 is: " << p1 << endl;
    size_t p2 = solve2("37", "633601");
    cout << "The answer to subproblem 2 is: " << p2<< endl;
    return 0;
}
