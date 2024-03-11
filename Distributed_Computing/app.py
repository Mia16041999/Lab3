from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load your trained models here
model_paths = [
    r'C:\Users\HP\Lab3\Distributed_Computing\model.pkl',  # Add the missing quotation mark and comma
]

# Load models from their respective paths
models = [joblib.load(model_path) for model_path in model_paths]

# Initialize weights for each model
weights = np.ones(len(models)) / len(models)

# Function to make predictions using local models
def make_predictions(features):
    predictions = []
    for model in models:
        prediction = model.predict(features)
        predictions.append(prediction)
    return predictions

# Function to update weights based on prediction accuracy
def update_weights(weights, predictions, consensus):
    # Your implementation to update weights based on prediction accuracy
    pass

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

    # Calculate consensus as a weighted average
    consensus = np.average(predictions, weights=weights)

    # Update weights based on prediction accuracy
    update_weights(weights, external_predictions, consensus)

    # Recalculate the weighted average with updated weights
    aggregated_prediction = np.average(predictions, weights=weights)

    return jsonify({'prediction': aggregated_prediction})

if __name__ == '__main__':
    app.run(host="0.0.0.0")
