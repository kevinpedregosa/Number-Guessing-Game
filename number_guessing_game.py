import random
import math

LEADERBOARD_FILE = "leaderboard.txt"


# --- Hint helper functions --- #
def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def is_fibonacci(n):
    """Check if a number is in the Fibonacci sequence."""
    if n < 0:
        return False
    a, b = 0, 1
    while a <= n:
        if a == n:
            return True
        a, b = b, a + b
    return False


def is_even(n):
    """Check if a number is even."""
    return n % 2 == 0


def divisible_by_five(n):
    """Check if a number is divisible by 5."""
    return n % 5 == 0


# --- Game setup --- #
def get_difficulty():
    """Ask the user to select a difficulty level."""
    while True:
        choice = input("Choose difficulty (easy / medium / hard): ").lower()
        if choice == "easy":
            return 100, 10, "easy"
        if choice == "medium":
            return 100, 10, "medium"
        if choice == "hard":
            return 100, 10, "hard"
        print("Invalid choice. Please try again.")


def generate_distance_hint(secret, guess):
    """Return a distance-based hint."""
    diff = abs(secret - guess)
    if diff <= 10:
        return "Very close."
    if diff <= 25:
        return "Close."
    if diff <= 100:
        return "Far."
    return "Very far."


def generate_smart_hints(secret):
    """
    Return a dictionary of all 4 possible smart hints.
    Keys: 'even', 'div5', 'prime', 'fib'
    """
    return {
        'even': "Hint: The number is even." if is_even(secret) else "Hint: The number is odd.",
        'div5': "Hint: The number is divisible by 5."
        if divisible_by_five(secret)
        else "Hint: The number is not divisible by 5.",
        'prime': "Hint: The number is prime."
        if is_prime(secret)
        else "Hint: The number is not prime.",
        'fib': "Hint: The number is in the Fibonacci sequence."
        if is_fibonacci(secret)
        else "Hint: The number is not in the Fibonacci sequence."
    }


def get_player_guess(max_number):
    """Get a valid guess or allow quitting with 'q'."""
    while True:
        user_input = input("Enter your guess (or 'q' to quit): ").lower()
        if user_input == "q":
            return None
        try:
            guess = int(user_input)
            if 1 <= guess <= max_number:
                return guess
            print(f"Guess must be between 1 and {max_number}.")
        except ValueError:
            print("Please enter a valid number or 'q' to quit.")


def save_score(username, attempts, number_guessed, difficulty):
    """Save score to leaderboard with labeled fields and keep top 5."""
    scores = []

    # Load existing scores
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(";")
                try:
                    user = parts[0].split(":")[1].strip()
                    att = int(parts[1].split(":")[1].strip())
                    diff = parts[2].split(":")[1].strip()
                    num = parts[3].split(":")[1].strip()
                    scores.append((user, att, num, diff))
                except (IndexError, ValueError):
                    continue
    except FileNotFoundError:
        pass

    # Add new score
    scores.append((username, attempts, number_guessed, difficulty))

    # Sort by attempts ascending
    scores.sort(key=lambda x: x[1])

    # Keep only top 5
    scores = scores[:5]

    # Save back to file
    with open(LEADERBOARD_FILE, "w") as file:
        for user, att, num, diff in scores:
            file.write(
                f"username: {user}; attempts: {att}; difficulty: {diff}; number: {num}\n"
            )


def display_leaderboard():
    """Display top 5 scores with labeled fields."""
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            print("\nLEADERBOARD (Top 5)")
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("\nNo leaderboard data yet.")


def play_game(username):
    """Run one game session."""
    max_number, max_attempts, difficulty = get_difficulty()
    secret = random.randint(1, max_number)
    last_diff = None
    triggered_hints = set()

    # Prepare smart hints
    all_hints = generate_smart_hints(secret)

    # Determine hint schedule based on difficulty
    if difficulty == "easy":
        hint_schedule = {2, 4, 6, 8}
    elif difficulty == "medium":
        # Random 3 hints at attempts 3,6,9
        hint_schedule = {3, 6, 9}
    else:  # hard
        # Random 2 hints at attempts 4,8
        hint_schedule = {4, 8}

    # Map attempts to randomly chosen hints
    hint_attempt_mapping = {}
    keys = list(all_hints.keys())
    if difficulty == "easy":
        for idx, att in enumerate(sorted(hint_schedule)):
            hint_attempt_mapping[att] = keys[idx]
    else:
        selected_keys = random.sample(keys, len(hint_schedule))
        for att, key in zip(sorted(hint_schedule), selected_keys):
            hint_attempt_mapping[att] = key

    print(f"\nI am thinking of a number between 1 and {max_number}.")
    print(f"You have {max_attempts} attempts.\n")

    for attempt in range(1, max_attempts + 1):
        guess = get_player_guess(max_number)
        if guess is None:
            print("\nYou quit the game.")
            return

        diff = abs(secret - guess)
        distance_hint = generate_distance_hint(secret, guess)

        # Hot/cold feedback
        temp_feedback = ""
        if last_diff is not None:
            temp_feedback = "Getting warmer." if diff < last_diff else "Getting colder."
        last_diff = diff

        # Print distance + hot/cold
        print(f"{distance_hint} {temp_feedback}".strip())

        # Smart hint if scheduled for this attempt
        if attempt in hint_attempt_mapping:
            key = hint_attempt_mapping[attempt]
            if key not in triggered_hints:
                print(all_hints[key])
                triggered_hints.add(key)

        # Print attempts left
        print(f"You have {max_attempts - attempt} left.\n")

        # Check win
        if guess == secret:
            print(f"\nCorrect, {username}! You guessed the number in {attempt} attempts.")
            if attempt <= max_attempts - 2:
                print("Performance: Excellent")
            elif attempt == max_attempts - 1:
                print("Performance: Good")
            else:
                print("Performance: Fair")

            save_score(username, attempt, secret, difficulty)
            display_leaderboard()
            return

    # If not guessed
    print(f"\nGame over. The number was {secret}.")


def main():
    """Main loop to start the game."""
    print("\nNUMBER GUESSING GAME")
    username = input("Enter your username: ").strip()
    if not username:
        username = "Player"

    while True:
        play_game(username)
        again = input("\nPlay again? (yes/no): ").lower()
        if again != "yes":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
