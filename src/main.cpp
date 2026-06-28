#include <iostream>
#include "tdee.hpp"
#include "macros.hpp"
#include "utils.hpp"
#include "models.hpp"

int main() {
    UserInput u;

    int sexInput, goalInput, deficitInput;

    std::cout << "Enter your body weight in kg: ";
    std::cin >> u.weightKg;

    std::cout << "Enter your height in cms: ";
    std::cin >> u.heightCm;

    std::cout << "Age: ";
    std::cin >> u.age;

    std::cout << "Sex (1 = Male, 2 = Female): ";
    std::cin >> sexInput;
    u.sex = parseSex(sexInput);

    std::cout << "Estimated Body Fat %: ";
    std::cin >> u.bodyFatPercent;

    std::cout << "Training days/week: ";
    std::cin >> u.trainingDaysPerWeek;

    std::cout << "Goal (1 = Fat Loss, 2 = Maintenance, 3 = Muscle Gain): ";
    std::cin >> goalInput;
    u.goal = parseGoal(goalInput);

    TDEEOutput base = calculateAllTDEE(u);

    std::cout << "\nBase BMR Estimates:\n";
    std::cout << "Mifflin: " << base.mifflin << "\n";
    std::cout << "Harris: " << base.harris << "\n";
    std::cout << "Katch: " << base.katch << "\n";

    double multiplier;
        std::cout << "\nActivity Multiplier Guide:\n";
    std::cout << "  1.2   - Sedentary, desk job, little exercise\n";
    std::cout << "  1.375 - Lightly active, light exercise 1-3 days/week\n";
    std::cout << "  1.55  - Moderately active, training 3-5 days/week\n";
    std::cout << "  1.725 - Very active, hard training 4-6 days/week\n";
    std::cout << "  1.9   - Extremely active, hard daily training/physical job\n";
    std::cout << "\nEnter activity multiplier: ";
    std::cin >> multiplier;

    double tdee = applyActivityMultiplier(base.mifflin, multiplier);

    std::cout << "\nTDEE (Mifflin-based): " << tdee << " kcal\n";

    std::cout << "\nEnter your deficit goals (1 = Aggresive, 2 = Moderate)\n";
    std::cin >>deficitInput;
    u.deficit = parseDeficit(deficitInput);

    MacroOutput macros = calculateMacros(tdee, u);

    std::cout << "\n--- MACROS ---\n";
    std::cout << "Calories Intake required: " << macros.calories << "kcals \n";
    std::cout << "Calorie Deficit: " << macros.deficit << " kcals \n";
    std::cout << "Protein: " << macros.protein << " grams \n";
    std::cout << "Fat: " << macros.fat << " grams \n";
    std::cout << "Carbs: " << macros.carbs << " grams \n";

    return 0;
}