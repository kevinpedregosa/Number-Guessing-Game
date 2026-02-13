import random
import math


def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def get_difficulty():
    """Ask the user to select a difficulty level."""
    while True:
        choice = input("Choose difficulty (easy / medium / hard): ").lower()
        if choice == "easy":
            return 100, 10
        if choice == "medium":
            return 500, 9
        if choice == "hard":
            return 1000, 8
        print("Invalid choice. Please try again.")


def provide_hints(secret, guess, attempt):
    """Provide distance-based and smart hints."""
    diff = abs(secret - guess)

    # Distance hints
    if diff <= 10:
        print("Very close.")
    elif diff <= 50:
        print("Close.")
    elif diff <= 100:
        print("Far.")
    else:
        print("Very far.")

    # Smart hints at specific attempts
    if attempt == 3:
        print("Hint: The number is even." if secret % 2 == 0 else "Hint: The number is odd.")
    elif attempt == 5:
        print("Hint: The number is divisible by 5." if secret % 5 == 0 else "Hint: The number is not divisible by 5.")
    elif attempt == 6:
        print("Hint: The number is prime." if is_prime(secret) else "Hint: The number is not prime.")


def play_game():
    """Run a single game session."""
    max_number, max_attempts = get_difficulty()
    secret = random.randint(1, max_number)
    last_diff = None

    print(f"\nI am thinking of a number between 1 and {max_number}.")
    print(f"You have {max_attempts} attempts.\n")

    for attempt in range(1, max_attempts + 1):
        # Input validation loop
        while True:
            try:
                guess = int(input("Enter your guess: "))
                if 1 <= guess <= max_number:
                    break
                else:
                    print(f"Guess must be between 1 and {max_number}.")
            except ValueError:
                print("Please enter a valid number.")

        diff = abs(secret - guess)

        # Hot / cold feedback
        if last_diff is not None:
            if diff < last_diff:
                print("Getting warmer.")
            else:
                print("Getting colder.")

        last_diff = diff

        if guess == secret:
            print(f"\nCorrect! You guessed the number in {attempt} attempts.")
            if attempt <= 5:
                print("Performance: Excellent")
            elif attempt <= 8:
                print("Performance: Good")
            else:
                print("Performance: Fair")
            return

        provide_hints(secret, guess, attempt)
        print(f"Attempts left: {max_attempts - attempt}\n")

    print(f"\nGame over. The number was {secret}.")


def main():
    """Main loop for replaying the game."""
    while True:
        print("\nNUMBER GUESSING GAME")
        play_game()
        again = input("\nPlay again? (yes/no): ").lower()
        if again != "yes":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
