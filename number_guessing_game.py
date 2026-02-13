import random
import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def get_difficulty():
    while True:
        choice = input("Choose difficulty (easy / medium / hard): ").lower()
        if choice == "easy":
            return 100, 10
        elif choice == "medium":
            return 500, 9
        elif choice == "hard":
            return 1000, 8
        else:
            print("Invalid choice. Try again.")


def play_game():
    max_number, max_attempts = get_difficulty()
    secret = random.randint(1, max_number)

    print(f"\nI am thinking of a number between 1 and {max_number}.")
    print(f"You have {max_attempts} attempts.\n")

    attempts = 0
    last_diff = None

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
            if guess < 1 or guess > max_number:
                print("Out of range.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        attempts += 1
        diff = abs(guess - secret)

        if guess == secret:
            print(f"\nCorrect. You guessed the number in {attempts} tries.")

            if attempts <= 5:
                print("Performance: Excellent")
            elif attempts <= 8:
                print("Performance: Good")
            else:
                print("Performance: Fair")
            return

        # Hot / Cold feedback
        if last_diff is not None:
            if diff < last_diff:
                print("Getting warmer.")
            else:
                print("Getting colder.")

        # Distance hints
        if diff <= 10:
            print("Very close.")
        elif diff <= 50:
            print("Close.")
        elif diff <= 100:
            print("Far.")
        else:
            print("Very far.")

        # Smart hints
        if attempts == 3:
            print("Hint: The number is even." if secret % 2 == 0 else "Hint: The number is odd.")
        elif attempts == 5:
            print("Hint: The number is divisible by 5." if secret % 5 == 0 else "Hint: Not divisible by 5.")
        elif attempts == 6:
            print("Hint: The number is prime." if is_prime(secret) else "Hint: The number is not prime.")

        last_diff = diff
        print(f"Attempts left: {max_attempts - attempts}\n")

    print(f"\nGame over. The number was {secret}.")


# Main loop
while True:
    print("\nRANDOM NUMBER GUESSING GAME")
    play_game()

    again = input("\nPlay again? (yes/no): ").lower()
    if again != "yes":
        print("Thanks for playing.")
        break
