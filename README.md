# Number Guessing Game

# Overview
Terminal-based Python game where players try to guess a secret number within 10 attempts.

# Features 
- Difficulty Levels: Easy, Medium, and Hard (level determines number of hints)
- Smart Hints: Provided in random order, including even/odd, divisible by 5, prime, and Fibonacci
- Hot/Cold Feedback: Shows if guess is getting closer or farther
- Quit Option: Players can exit anytime by typing q
- Leaderboard: Stores top 5 scores with username, attempts, number guessed, and difficulty

# Installation
1. Make sure you have Python 3 installed
2. Clone the repository: git clone https://github.com/kevinpedregosa/Number-Guessing-Game.git
3. Navigate to the project folder: cd Number-Guessing-Game
4. Run the game: python number_guessing_game.py

# Example Gameplay
NUMBER GUESSING GAME

Choose difficulty (easy / medium / hard): easy

I am thinking of a number between 1 and 100.

You have 10 attempts.

Enter your guess (or 'q' to quit): 67

Close.

You have 9 left.

Enter your guess (or 'q' to quit): 81

Very close. Getting warmer.

Hint: The number is odd.

You have 8 left.

Enter your guess (or 'q' to quit): 85

Very close. Getting warmer.

You have 7 left.

Correct, OJ! You guessed the number in 3 attempts.

Performance: Excellent

LEADERBOARD (Top 5)

username: bill; attempts: 3; difficulty: easy; number: 73

username: OJ; attempts: 3; difficulty: easy; number: 85

username: kped; attempts: 4; difficulty: easy; number: 21

username: bob; attempts: 4; difficulty: easy; number: 91

username: rai; attempts: 6; difficulty: hard; number: 3

# What I learned
- Developed an interactive game utilizing Python functions and loops to add hot/cold feedback, useful hints, and attempt tracking
- Built a top-5 leaderboard system with Python file handling to store, sort, and display player scores
- Managed project versions through Git and GitHub, using branching and merging to maintain code
