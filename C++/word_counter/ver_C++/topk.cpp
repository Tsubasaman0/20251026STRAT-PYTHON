// topk.cpp
#include <iostream>
#include <fstream>
#include <unordered_map>
#include <vector>
#include <algorithm>
#include <chrono>

int main() {
    using namespace std;
    auto start = chrono::high_resolution_clock::now();

    ifstream file("../words_data/words.txt");
    unordered_map<string, size_t> counts;
    string word;

    while (getline(file, word)) {
        counts[word]++;
    }

    vector<pair<string, size_t>> vec(counts.begin(), counts.end());

    partial_sort(vec.begin(), vec.begin() + 10, vec.end(),
        [](const auto& a, const auto& b) {
            return a.second > b.second;
        });
    
        auto end = chrono::high_resolution_clock::now();
        chrono::duration<double> elapsed = end - start;

        cout << "Top10:\n";
        for (int i = 0; i < 10; ++i) {
            cout << vec[i].first << " : " << vec[i].second << "\n";
        }

        cout << "Time: " << elapsed.count() << " sec\n";
}