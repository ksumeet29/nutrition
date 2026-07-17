#include <iostream>
#include <iomanip>
#include <cstdlib>
#include "tdee.hpp"
#include "macros.hpp"
#include "utils.hpp"
#include "models.hpp"

int main(int argc, char* argv[]) {
    // Expected arguments: weight_kg height_cm age sex(1/2) bodyfat training_days goal activity_multiplier deficit tdee_method(1/2/3)
    if (argc != 11) {
        std::cerr << "Usage: " << argv[0] << " weight_kg height_cm age sex bodyfat training_days goal activity_multiplier deficit tdee_method\n";
        return 1;
    }

    UserInput u;
    u.weightKg = std::stod(argv[1]);
    u.heightCm = std::stod(argv[2]);
    u.age = std::stoi(argv[3]);
    u.sex = parseSex(std::stoi(argv[4]));
    u.bodyFatPercent = std::stod(argv[5]);
    u.trainingDaysPerWeek = std::stoi(argv[6]);
    u.goal = parseGoal(std::stoi(argv[7]));
    double multiplier = std::stod(argv[8]);
    u.deficitCalories = std::stoi(argv[9]);
    u.tdeeMethod = parseTDEEMethod(std::stoi(argv[10]));

    TDEEOutput base = calculateAllTDEE(u);
    double tdee = calculateTDEE(u, base, multiplier);
    MacroOutput macros = calculateMacros(tdee, u);

    // Output JSON
    std::cout << "{\n";
    std::cout << "  \"mifflin\": " << std::fixed << std::setprecision(2) << base.mifflin << ",\n";
    std::cout << "  \"harris\": " << std::fixed << std::setprecision(2) << base.harris << ",\n";
    std::cout << "  \"katch\": " << std::fixed << std::setprecision(2) << base.katch << ",\n";
    std::cout << "  \"tdee\": " << std::fixed << std::setprecision(0) << tdee << ",\n";
    std::cout << "  \"calories\": " << std::fixed << std::setprecision(0) << macros.calories << ",\n";
    std::cout << "  \"deficit\": " << macros.deficit << ",\n";
    std::cout << "  \"protein\": " << std::fixed << std::setprecision(1) << macros.protein << ",\n";
    std::cout << "  \"fat\": " << std::fixed << std::setprecision(1) << macros.fat << ",\n";
    std::cout << "  \"carbs\": " << std::fixed << std::setprecision(1) << macros.carbs << "\n";
    std::cout << "}\n";

    return 0;
}