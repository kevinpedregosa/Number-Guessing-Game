import random
from flask import Flask, jsonify, render_template, request, session

from number_guessing_game import (
    LEADERBOARD_FILE,
    generate_distance_hint,
    generate_smart_hints,
    save_score,
)


app = Flask(__name__)

# NOTE: For a real deployment, load this from an environment variable.
app.secret_key = "change-this-secret-key"


def parse_leaderboard():
    """Parse leaderboard file into a list of dicts."""
    entries = []
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(";")
                if len(parts) < 4:
                    continue
                try:
                    user = parts[0].split(":")[1].strip()
                    attempts = int(parts[1].split(":")[1].strip())
                    difficulty = parts[2].split(":")[1].strip()
                    number = parts[3].split(":")[1].strip()
                    entries.append(
                        {
                            "username": user,
                            "attempts": attempts,
                            "difficulty": difficulty,
                            "number": number,
                        }
                    )
                except (IndexError, ValueError):
                    continue
    except FileNotFoundError:
        pass
    return entries


def build_hint_schedule(difficulty, all_hints):
    """Return mapping of attempt number -> smart hint key."""
    keys = list(all_hints.keys())

    if difficulty == "easy":
        hint_schedule = [2, 4, 6, 8]
        mapping = {att: keys[idx] for idx, att in enumerate(hint_schedule)}
    elif difficulty == "medium":
        hint_schedule = [3, 6, 9]
        selected_keys = random.sample(keys, len(hint_schedule))
        mapping = {att: key for att, key in zip(hint_schedule, selected_keys)}
    else:  # hard
        hint_schedule = [4, 8]
        selected_keys = random.sample(keys, len(hint_schedule))
        mapping = {att: key for att, key in zip(hint_schedule, selected_keys)}

    return mapping


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/leaderboard")
def api_leaderboard():
    return jsonify({"leaderboard": parse_leaderboard()})


@app.route("/api/start-game", methods=["POST"])
def api_start_game():
    data = request.get_json(silent=True) or request.form

    username = (data.get("username") or "Player").strip()
    difficulty = (data.get("difficulty") or "easy").lower()
    if difficulty not in {"easy", "medium", "hard"}:
        difficulty = "easy"

    max_number = 100
    max_attempts = 10

    secret = random.randint(1, max_number)
    all_hints = generate_smart_hints(secret)
    hint_mapping = build_hint_schedule(difficulty, all_hints)

    # Persist game state in the session
    session["game"] = {
        "username": username,
        "difficulty": difficulty,
        "max_number": max_number,
        "max_attempts": max_attempts,
        "secret": secret,
        "attempt": 0,
        "last_diff": None,
        "triggered_hints": [],
        "hint_attempt_mapping": {str(k): v for k, v in hint_mapping.items()},
        "all_hints": all_hints,
    }

    return jsonify(
        {
            "status": "ok",
            "username": username,
            "difficulty": difficulty,
            "max_number": max_number,
            "max_attempts": max_attempts,
            "leaderboard": parse_leaderboard(),
        }
    )


@app.route("/api/guess", methods=["POST"])
def api_guess():
    game = session.get("game")
    if not game:
        return jsonify({"error": "No active game. Start a new game first."}), 400

    data = request.get_json(silent=True) or request.form
    raw_guess = data.get("guess")
    try:
        guess = int(raw_guess)
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid guess. Please send a number."}), 400

    if guess < 1 or guess > game["max_number"]:
        return (
            jsonify(
                {
                    "error": f"Guess must be between 1 and {game['max_number']}.",
                    "max_number": game["max_number"],
                }
            ),
            400,
        )

    secret = game["secret"]
    game["attempt"] += 1
    attempt = game["attempt"]

    diff = abs(secret - guess)
    distance_hint = generate_distance_hint(secret, guess)

    temp_feedback = ""
    if game["last_diff"] is not None:
        temp_feedback = (
            "Getting warmer." if diff < game["last_diff"] else "Getting colder."
        )
    game["last_diff"] = diff

    # Smart hints logic
    smart_hint = None
    triggered = set(game["triggered_hints"])
    mapping = game["hint_attempt_mapping"]
    all_hints = game["all_hints"]

    key = mapping.get(str(attempt))
    if key and key not in triggered:
        smart_hint = all_hints[key]
        triggered.add(key)

    game["triggered_hints"] = list(triggered)

    attempts_left = game["max_attempts"] - attempt

    response = {
        "distance_hint": distance_hint,
        "temp_feedback": temp_feedback,
        "attempt": attempt,
        "attempts_left": max(attempts_left, 0),
        "smart_hint": smart_hint,
        "correct": False,
        "game_over": False,
    }

    # Win condition
    if guess == secret:
        response["correct"] = True
        response["game_over"] = True

        if attempt <= game["max_attempts"] - 2:
            performance = "Excellent"
        elif attempt == game["max_attempts"] - 1:
            performance = "Good"
        else:
            performance = "Fair"

        response["performance"] = performance

        # Save score on win, like the CLI version
        save_score(game["username"], attempt, secret, game["difficulty"])
        response["leaderboard"] = parse_leaderboard()

        session.pop("game", None)
        return jsonify(response)

    # Lose condition (out of attempts)
    if attempt >= game["max_attempts"]:
        response["game_over"] = True
        response["secret"] = secret
        response["leaderboard"] = parse_leaderboard()
        session.pop("game", None)
        return jsonify(response)

    # Persist updated game state
    session["game"] = game
    return jsonify(response)


if __name__ == "__main__":
    # Local development entrypoint.
    # Uses port 5050 by default, or the PORT env var if set.
    import os

    port = int(os.environ.get("PORT", 5050))
    app.run(debug=True, host="0.0.0.0", port=port)

