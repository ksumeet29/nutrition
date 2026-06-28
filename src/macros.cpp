#include "macros.hpp"

MacroOutput calculateMacros(double calories, const UserInput& u) {
    double proteinPerKg;
    double fatPerKg;
    int deficit;
    bool isDeficitRequired;
    
    switch(u.deficit) {
        case Deficit::Aggresive:
        deficit = 500;
        break;
        default:
        deficit = 250;
    }

    // Protein logic
    switch (u.goal) {
        case Goal::FatLoss:
            proteinPerKg = 1.4;
            fatPerKg = 0.6;
            isDeficitRequired = 1;
            break;
        case Goal::MuscleGain:
            proteinPerKg = 2;
            fatPerKg = 0.7;
            isDeficitRequired = 0;
            break;
        default:
            proteinPerKg = 1.2;
            fatPerKg = 0.7;
            isDeficitRequired = 0;
    }
    
    calories = calories - deficit*isDeficitRequired;

    double proteinGrams = proteinPerKg * u.weightKg;
    double fatGrams = fatPerKg * u.weightKg;

    double proteinCalories = proteinGrams * 4;
    double fatCalories = fatGrams * 9;

    double remainingCalories = calories - (proteinCalories + fatCalories);
    double carbsGrams = remainingCalories / 4;

    return {calories, proteinGrams, fatGrams, carbsGrams, deficit*isDeficitRequired};
}