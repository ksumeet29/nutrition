#pragma once
#include <string>

enum class Sex { Male, Female };

enum class Goal { FatLoss, Maintenance, MuscleGain };

enum class TDEEMethod { Mifflin, Harris, Katch };

struct UserInput {
    double weightKg;
    double heightCm;
    int age;
    Sex sex;
    double bodyFatPercent;
    int trainingDaysPerWeek;
    Goal goal;
    int deficitCalories;
    TDEEMethod tdeeMethod;
};

struct TDEEOutput {
    double mifflin;
    double harris;
    double katch;
};