#!/usr/bin/env python3
import subprocess
import json
import os
from flask import Flask, request, jsonify
from pathlib import Path

app = Flask(__name__)

# Get the root directory (where server.py is located)
ROOT_DIR = Path(__file__).parent
BINARY_PATH = ROOT_DIR / "build" / "Release" / "nutrition.exe"

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        # Extract and convert data
        weight_kg = float(data.get('weight_kg', 0))
        height_cm = float(data.get('height_cm', 0))
        age = int(data.get('age', 0))
        sex = int(data.get('sex', 1))  # 1 for male, 2 for female
        bodyfat = float(data.get('bodyfat', 0))
        training_days = int(data.get('training_days', 0))
        goal = int(data.get('goal', 1))  # 1=fat loss, 2=maintenance, 3=muscle gain
        activity_multiplier = float(data.get('activity_multiplier', 1.2))
        deficit = int(data.get('deficit', 1))  # 1=aggressive, 2=moderate
        
        # Build command with all arguments in order
        cmd = [
            str(BINARY_PATH),
            str(weight_kg),
            str(height_cm),
            str(age),
            str(sex),
            str(bodyfat),
            str(training_days),
            str(goal),
            str(activity_multiplier),
            str(deficit)
        ]
        
        # Run the binary
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Parse the JSON output
        output = json.loads(result.stdout)
        
        return jsonify(output)
    
    except FileNotFoundError:
        return jsonify({"error": f"Binary not found at {BINARY_PATH}"}), 500
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Binary execution failed: {e.stderr}"}), 500
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Invalid JSON output from binary: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
