#include <iostream>

int main() {
    double total = 0;
    double calories;

    std::cout << "Enter calories for each meal (0 to stop):\n";

    while (true) {
        std::cin >> calories;
        if (calories == 0) break;
        total += calories;
    }

    std::cout << "Total daily intake: " << total << " kcal\n";
    return 0;
}