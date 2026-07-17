#include "tdee.hpp"

double mifflinStJeor(const UserInput& u) {
    if (u.sex == Sex::Male) {
        return 10 * u.weightKg + 6.25 * u.heightCm - 5 * u.age + 5;
    } else {
        return 10 * u.weightKg + 6.25 * u.heightCm - 5 * u.age - 161;
    }
}

double harrisBenedict(const UserInput& u) {
    if (u.sex == Sex::Male) {
        return 13.397 * u.weightKg + 4.799 * u.heightCm - 5.677 * u.age + 88.362;
    } else {
        return 9.247 * u.weightKg + 3.098 * u.heightCm - 4.330 * u.age + 447.593;
    }
}

double katchMcArdle(const UserInput& u) {
    double leanMass = u.weightKg * (1.0 - u.bodyFatPercent / 100.0);
    return 370 + (21.6 * leanMass);
}

TDEEOutput calculateAllTDEE(const UserInput& u) {
    return {
        mifflinStJeor(u),
        harrisBenedict(u),
        katchMcArdle(u)
    };
}

double applyActivityMultiplier(double bmr, double multiplier) {
    return bmr * multiplier;
}

double calculateTDEE(const UserInput& u, const TDEEOutput& base, double multiplier) {
    switch (u.tdeeMethod) {
        case TDEEMethod::Harris:
            return applyActivityMultiplier(base.harris, multiplier);
        case TDEEMethod::Katch:
            return applyActivityMultiplier(base.katch, multiplier);
        default:
            return applyActivityMultiplier(base.mifflin, multiplier);
    }
}