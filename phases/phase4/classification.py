from collections import Counter
import json
def classify_playstyle(p):
    t = p["tackles_done"]
    m = p["times_manned"]
    p_done = p["passes_done"]
    g = p["goals_scored"]
    s = p["avg_speed"]
    
    c = m * 10 + g * 50 + p_done * 10 + t * 2 + (20 if s > 1.5 else 0)
    p["contribution_score"] = c
    
    if t > 5 and m > 10 and s <= 1.5:
        return "Aggressive Defender"
    elif p_done > 10 and g >= 1 and s >= 1.5:
        return "Creative Midfielder"
    elif m > 12 and c < 40 and p_done < 5 and g == 0 and t < 2:
        return "Passive Midfielder"
    elif g >= 2 and p_done < 5 and t < 2:
        return "Striker/Finisher"
    elif t > 3 and p_done > 8 and g >= 1 and s > 1.5 and m > 5:
        return "Box-to-Box"
    elif 5 <= p_done <= 10 and s >= 1.6 and g <= 1 and t <= 3:
        return "Supportive Winger"
    elif t > 6 and s < 1.3 and p_done < 4 and g == 0:
        return "Anchor Defender"
    else:
        return "Unclassified"

# 🔹 Step 2: Classify Team Strategy
def classify_team_strategy(player_dict):  # changed param name for clarity
    players = []

    for name, data in player_dict.items():
        data["name"] = name
        data["playstyle"] = classify_playstyle(data)
        players.append(data)

    style_count = Counter(p["playstyle"] for p in players)
    avg_team_speed = sum(p['avg_speed'] for p in players) / len(players)
    mvp = max(players, key=lambda x: x['contribution_score'])

    # Team strategy logic (unchanged)
    if style_count["Creative Midfielder"] >= 2 and style_count["Striker/Finisher"] >= 1:
        strategy = "Strategy 1: Play through center with short passes, isolate striker for scoring"
    elif style_count["Supportive Winger"] >= 2 and style_count["Box-to-Box"] >= 1:
        strategy = "Strategy 2: Use wide counter-attacks, quick switches of play"
    elif style_count["Aggressive Defender"] >= 2 and style_count["Anchor Defender"] >= 1:
        strategy = "Strategy 3: Defensive block, absorb pressure, low-risk buildup"
    elif style_count["Passive Midfielder"] >= 3 and style_count["Striker/Finisher"] == 0:
        strategy = "Strategy 4: Minimize risk, focus on set pieces or long shots"
    elif mvp["contribution_score"] > 100:
        strategy = "Strategy 13: Play around MVP, keep them free of marking"
    elif avg_team_speed > 1.6:
        strategy = "Strategy 12: Constant pressing, transition-heavy football"
    elif style_count["Box-to-Box"] >= 1 and style_count["Anchor Defender"] >= 1 and style_count["Creative Midfielder"] >= 1:
        strategy = "Strategy 11: Rotate midfield roles, staggered pressing"
    elif all(style_count[style] >= 1 for style in ["Creative Midfielder", "Box-to-Box", "Supportive Winger", "Aggressive Defender"]):
        strategy = "Strategy 8: Maintain flexible structure, adapt strategy live"
    else:
        strategy = "No dominant strategy match – fallback: Balanced approach"

    return {
        "Player_Styles": {p['name']: p['playstyle'] for p in players},
        "Playstyle_Counts": dict(style_count),
        "Avg_Team_Speed": round(avg_team_speed, 2),
        "MVP": {
            "name": mvp['name'],
            "contribution_score": mvp['contribution_score'],
            "playstyle": mvp['playstyle']
        },
        "Recommended_Strategy": strategy
    }

if __name__ == "__main__":
    with open("../phase2.5/player_stats1.json", "r") as f:
        data = json.load(f)
    print(data)
    result = classify_team_strategy(data)
    with open("player_class_impact_output1.json", "w") as f:
        json.dump(result, f, indent=4)
