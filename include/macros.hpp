#pragma once
#include "models.hpp"

struct MacroOutput {
    double calories;
    double protein;
    double fat;
    double carbs;
    int deficit;
};

MacroOutput calculateMacros(double calories, const UserInput& u);