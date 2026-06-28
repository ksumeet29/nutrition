#include "utils.hpp"

Sex parseSex(int input) {
    return (input == 1) ? Sex::Male : Sex::Female;
}

Goal parseGoal(int input) {
    switch (input) {
        case 1: return Goal::FatLoss;
        case 3: return Goal::MuscleGain;
        default: return Goal::Maintenance;
    }
}

Deficit parseDeficit(int input) {
    return (input == 1) ? Deficit::Aggresive : Deficit::Moderate;
}