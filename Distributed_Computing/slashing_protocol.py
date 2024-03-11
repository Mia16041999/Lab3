import json

# File path to the model balances JSON database
DATABASE_FILE = "model_balances.json"

# Initialize the database if it doesn't exist
def initialize_database():
    try:
        with open(DATABASE_FILE, "r") as file:
            pass  # File exists, no need to initialize
    except FileNotFoundError:
        with open(DATABASE_FILE, "w") as file:
            json.dump({}, file)  # Initialize with an empty dictionary

# Register a model with an initial deposit
def register_model(model_address, initial_deposit):
    with open(DATABASE_FILE, "r+") as file:
        data = json.load(file)
        data[model_address] = initial_deposit
        file.seek(0)
        json.dump(data, file)

# Slash a model's deposit by a given amount
def slash_model(model_address, penalty_amount):
    with open(DATABASE_FILE, "r+") as file:
        data = json.load(file)
        if model_address in data:
            data[model_address] -= penalty_amount
            if data[model_address] < 0:
                data[model_address] = 0  # Ensure balance doesn't go negative
            file.seek(0)
            json.dump(data, file)
            return True  # Slashing successful
        else:
            return False  # Model not found in the database

# Example usage:
if __name__ == "__main__":
    # Initialize the database (only needed once)
    initialize_database()
    
    # Example of registering a model with an initial deposit
    register_model("model1", 1000)
    
    # Example of slashing a model's deposit by a certain amount
    model_address_to_slash = "model1"
    slashing_penalty = 200
    if slash_model(model_address_to_slash, slashing_penalty):
        print(f"Model {model_address_to_slash} slashed by {slashing_penalty} euros.")
    else:
        print(f"Model {model_address_to_slash} not found.")
