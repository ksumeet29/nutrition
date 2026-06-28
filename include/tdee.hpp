#pragma once
#include "models.hpp"

double mifflinStJeor(const UserInput& u);
double harrisBenedict(const UserInput& u);
double katchMcArdle(const UserInput& u);

TDEEOutput calculateAllTDEE(const UserInput& u);

double applyActivityMultiplier(double bmr, double multiplier);