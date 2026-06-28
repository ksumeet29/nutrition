#!/usr/bin/env python3
import argparse
import subprocess
import os
import shutil
import pandas as pd
from datetime import datetime, timedelta

def load_bodyweight(filepath):
    df = pd.read_excel(filepath)

    # Auto-detect date and weight columns
    date_cols = [c for c in df.columns if 'date' in c.lower()]
    weight_cols = [c for c in df.columns if any(k in c.lower() for k in ['weight', 'bw', 'kg'])]

    if not date_cols or not weight_cols:
        # Fallback: assume first col = date, second = weight
        df.columns = ['Date', 'Weight'] + list(df.columns[2:])
        date_col, weight_col = 'Date', 'Weight'
    else:
        date_col, weight_col = date_cols[0], weight_cols[0]

    df[date_col] = pd.to_datetime(df[date_col])
    df = df.dropna(subset=[date_col, weight_col]).sort_values(date_col).reset_index(drop=True)
    return df, date_col, weight_col

def get_weight_stats(filepath):
    df, date_col, weight_col = load_bodyweight(filepath)

    latest = df.iloc[-1]
    current_weight = float(latest[weight_col])
    current_date = latest[date_col]

    one_month_ago = current_date - timedelta(days=30)
    past_df = df[df[date_col] <= one_month_ago]

    if past_df.empty:
        past_record = df.iloc[0]
    else:
        past_record = past_df.iloc[-1]

    past_weight = float(past_record[weight_col])
    past_date = past_record[date_col]

    return current_weight, past_weight, current_date, past_date

def main():
    parser = argparse.ArgumentParser(description="Run the nutrition calculator")
    parser.add_argument("--weight", type=float, default=None, help="Override body weight in kg (default: latest from BW.xlsx)")
    parser.add_argument("--height", type=float, default=178, help="Height in cm (default: 178)")
    parser.add_argument("--age", type=int, default=27, help="Age (default: 27)")
    parser.add_argument("--sex", type=int, default=1, help="1=Male, 2=Female (default: 1)")
    parser.add_argument("--bodyfat", type=float, default=40, help="Body fat %% (default: 40)")
    parser.add_argument("--trainingdays", type=int, default=0, help="Training days/week (default: 0)")
    parser.add_argument("--goal", type=int, default=1, help="1=Fat Loss, 2=Maintenance, 3=Muscle Gain (default: 1)")
    parser.add_argument("--mul", type=float, default=1.2, help="Activity multiplier (default: 1.2)")
    parser.add_argument("--deficit", type=int, default=1, help="1=Aggressive, 2=Moderate (default: 1)")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.abspath(__file__))
    bw_file = os.path.join(project_root, "BW.xlsx")
    build_dir = os.path.join(project_root, "build")

    # Load weight from Excel
    current_weight, past_weight, current_date, past_date = get_weight_stats(bw_file)
    weight_change = current_weight - past_weight

    if args.weight is not None:
        weight = args.weight
        print(f"\nManually provided weight: {weight} kg")
    else:
        weight = current_weight
        print(f"\nLatest weight from BW.xlsx: {weight} kg (recorded: {current_date.date()})")

    # Print monthly weight change
    days_diff = (current_date - past_date).days
    if weight_change < 0:
        print(f"Lost {abs(weight_change):.2f} kg in the last {days_diff} days ({past_date.date()} → {current_date.date()})")
    elif weight_change > 0:
        print(f"Gained {weight_change:.2f} kg in the last {days_diff} days ({past_date.date()} → {current_date.date()})")
    else:
        print(f"No weight change over the last {days_diff} days")

    os.makedirs(build_dir, exist_ok=True)
    subprocess.run(["cmake", ".."], cwd=build_dir, check=True)
    subprocess.run(["make"], cwd=build_dir, check=True)

    input_data = "\n".join([
        str(weight),
        str(args.height),
        str(args.age),
        str(args.sex),
        str(args.bodyfat),
        str(args.trainingdays),
        str(args.goal),
        str(args.mul),
        str(args.deficit),
    ]) + "\n"

    result = subprocess.run(
        [os.path.join(build_dir, "nutrition")],
        input=input_data,
        text=True,
        capture_output=True,
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

    shutil.rmtree(build_dir)

if __name__ == "__main__":
    main()