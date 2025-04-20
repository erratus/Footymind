import json
from sklearn.linear_model import LinearRegression

# Regression model (trained earlier or hardcoded weights)
def get_regression_model():
    model = LinearRegression()
    train_X = [
        [11, 1, 9, 1, 1.51],
        [6, 2, 5, 0, 1.62],
        [14, 0, 3, 2, 1.3],
        [8, 0, 12, 1, 1.7],
        [10, 1, 8, 3, 1.65]
    ]
    train_y = [137, 132, 92, 150, 158]
    model.fit(train_X, train_y)
    return model

# Extrapolate stats to 90 min
def project_stats(current_stats, current_minute):
    factor = 90 / current_minute
    projected = {
        "times_manned": round(current_stats["times_manned"] * factor),
        "goals_scored": round(current_stats["goals_scored"] * factor, 2),
        "passes_done": round(current_stats["passes_done"] * factor),
        "tackles_done": round(current_stats["tackles_done"] * factor),
        "avg_speed": round(current_stats["avg_speed"], 2)  # avg_speed stays same
    }
    return projected

# Predict contribution score
def predict_contribution(model, stats):
    features = [
        stats["times_manned"],
        stats["goals_scored"],
        stats["passes_done"],
        stats["tackles_done"],
        stats["avg_speed"]
    ]
    contribution = round(model.predict([features])[0])
    return contribution

# Final wrapper
def full_match_projection(input_data, current_minute):
    model = get_regression_model()
    output = {}

    for player_name, stats in input_data.items():
        projected = project_stats(stats, current_minute)
        score = predict_contribution(model, projected)
        insight = (
            " High Impact" if score > 140 else
            " Medium Impact" if score > 110 else
            " Low Impact"
        )
        output[player_name] = {
            "projected_stats": projected,
            "predicted_contribution": score,
            "insight": insight
        }

    return output

with open("../phase2.5/player_stats.json", "r") as f:
    data = json.load(f)


result = full_match_projection(data, current_minute=30)
with open("player_contri_output1.json", "w") as f:
    json.dump(result, f, indent=4)
