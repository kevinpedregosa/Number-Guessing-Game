# Number Guessing Game

# Overview
Terminal-based Python game where players try to guess a secret number within 10 attempts.

# Features 
- Difficulty Levels: Easy, Medium, and Hard with 10 attempts each
- Smart Hints: Provided in random order, including even/odd, divisible by 5, prime, and Fibonacci
- Hot/Cold Feedback: Shows if guess is getting closer or farther
- Leaderboard: Stores top 5 scores with username, attempts, number guessed, and difficulty
- Quit Option: Players can exit anytime by typing q

# Installation
1. Make sure you have Python 3 installed
2. Clone the repository: git clone https://github.com/kevinpedregosa/Number-Guessing-Game.git
3. Navigate to the project folder: cd number-guessing-game
4. Run the game: python number_guessing_game.py

# Example Gameplay
NUMBER GUESSING GAME\n
Enter your username: Alex\n

I am thinking of a number between 1 and 100.\n
You have 10 attempts.\n

Enter your guess (or 'q' to quit): 12\n
Far. Getting warmer.\n
Hint: The number is even.\n
You have 9 left.\n

Enter your guess (or 'q' to quit): 56\n
Close. Getting warmer.\n
You have 8 left.\n

...

Correct, Alex! You guessed the number in 5 attempts.\n
Performance: Excellent\n

LEADERBOARD (Top 5)\n
1. username: Alex; attempts: 5; difficulty: easy; number: 42\n

# What I learned
- Developed an interactive game using Python functions and loops to implement smart hints, hot/cold feedback, and attempt tracking
- Built a top-5 leaderboard system with Python file handling to store, sort, and display player scores efficiently
- Managed code versions through Git and GitHub, using branching and merging to maintain project stability
