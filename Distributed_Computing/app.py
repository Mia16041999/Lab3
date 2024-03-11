from flask import Flask, request, jsonify
import joblib
import numpy as np
import json

app = Flask(__name__)

# Load your trained models here
model_paths = [
    r'C:\Users\HP\Lab3\Distributed_Computing\model.pkl',  # Add the missing quotation mark and comma
]

# Load models from their respective paths
models = [joblib.load(model_path) for model_path in model_paths]

# Initialize weights for each model
weights = np.ones(len(models)) / len(models)

# Initialize model balances
model_balances = {model_path: 1000 for model_path in model_paths}  # Initial deposit of 1000 euros for each model

# Function to make predictions using local models
def make_predictions(features):
    predictions = []
    for model in models:
        prediction = model.predict(features)
        predictions.append(prediction)
    return predictions

# Function to update weights based on prediction accuracy and slashing penalties
def update_weights(weights, predictions, consensus, penalties):
    # Update weights based on prediction accuracy
    for i, model_prediction in enumerate(predictions):
        if model_prediction == consensus:
            weights[i] += 0.01  # Example: Increase weight for accurate predictions
        else:
            weights[i] -= 0.01  # Example: Decrease weight for inaccurate predictions
    
    # Apply slashing penalties
    for model_path, penalty in penalties.items():
        model_balances[model_path] -= penalty  # Deduct penalty from model's balance
        if model_balances[model_path] <= 0:
            # Reset model's weight and balance if balance becomes zero or negative
            weights[model_paths.index(model_path)] = 1 / len(models)  # Reset weight
            model_balances[model_path] = 1000  # Reset balance to initial deposit

# Route for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = data['features']

    # Perform prediction using the loaded models
    local_predictions = [model.predict([features])[0] for model in models]

    # Make predictions using local models
    external_predictions = make_predictions(features)
    predictions = [local_prediction for local_prediction in local_predictions]

    # Calculate consensus as the most common prediction
    consensus = max(set(predictions), key=predictions.count)

    # Calculate penalties based on model performance (e.g., consistently inaccurate predictions)
    penalties = {model_paths[i]: 50 for i, prediction in enumerate(predictions) if prediction != consensus}

    # Update weights based on prediction accuracy and apply slashing penalties
    update_weights(weights, external_predictions, consensus, penalties)

    # Recalculate the weighted average with updated weights
    aggregated_prediction = np.average(predictions, weights=weights)

    return jsonify({'prediction': aggregated_prediction})

if __name__ == '__main__':
    app.run(host="0.0.0.0")
