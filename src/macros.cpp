#include "macros.hpp"

MacroOutput calculateMacros(double calories, const UserInput& u) {
    double proteinPerKg;
    double fatPerKg;
    int deficit = (u.goal == Goal::FatLoss) ? u.deficitCalories : 0;

    // Protein logic
    switch (u.goal) {
        case Goal::FatLoss:
            proteinPerKg = 1.4;
            fatPerKg = 0.6;
            break;
        case Goal::MuscleGain:
            proteinPerKg = 2;
            fatPerKg = 0.7;
            break;
        default:
            proteinPerKg = 1.2;
            fatPerKg = 0.7;
    }

    calories = calories - deficit;

    double proteinGrams = proteinPerKg * u.weightKg;
    double fatGrams = fatPerKg * u.weightKg;

    double proteinCalories = proteinGrams * 4;
    double fatCalories = fatGrams * 9;

    double remainingCalories = calories - (proteinCalories + fatCalories);
    double carbsGrams = remainingCalories / 4;

    return {calories, proteinGrams, fatGrams, carbsGrams, deficit};
}