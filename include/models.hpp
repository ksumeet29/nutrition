#pragma once
#include <string>

enum class Sex { Male, Female };

enum class Goal { FatLoss, Maintenance, MuscleGain };

enum class Deficit { Aggresive, Moderate};

struct UserInput {
    double weightKg;
    double heightCm;
    int age;
    Sex sex;
    double bodyFatPercent;
    int trainingDaysPerWeek;
    Goal goal;
    Deficit deficit;
};

struct TDEEOutput {
    double mifflin;
    double harris;
    double katch;
};