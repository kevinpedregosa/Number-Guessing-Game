# Number Guessing Game

## Game Description
A number guessing game with both:
- **Terminal version** (classic CLI experience)
- **Full‑stack web version** built with **Flask** (Python) and simple HTML/CSS/JS.

## Game Features 
- **3 Different Difficulty Levels**: Easy, Medium, and Hard (determines number of hints)
- **4 Different Hot/Cold Feedback Responses**: Shows if guess is getting closer or farther based on the absolute difference between guess and secret number
- **4 Different Smart Hints**: including even/odd, divisible by 5, prime, and fibonacci; provided in random order
- **Attempt Tracking**: Reports number of attempts remaining, and hints are given after specific number of guesses (determined by difficulty level)
- **Quit Option (CLI)**: Players can exit anytime by typing `q`
- **Leaderboard**: Stores and displays top 5 scores with username, attempts, number guessed, and difficulty (shared between CLI and web versions)

---

## Play Online

Once deployed, the web version will be available at a public URL.  
Update this section with your live link, for example:

- **Live site**: `[Play the web version here](https://your-deployed-url.example.com)`

You can get a URL like this by:
- Hosting the app on a platform that supports Python/Flask (for example Render, Railway, Fly.io, or Heroku‑style platforms that use the `Procfile`).
- Connecting your GitHub repository to that platform.
- Copying the deployed URL into the bullet above.

---

## Running Locally (Web Version)

1. **Clone the repo**
   ```bash
   git clone https://github.com/kevinpedregosa/Number-Guessing-Game.git
   cd Number-Guessing-Game
   ```
2. **Create and activate a virtual environment (recommended)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Flask web server**
   ```bash
   python app.py
   ```
   By default the app runs on port `5050`.  
   Open your browser and go to:
   ```text
   http://localhost:5050
   ```

To run the app on a different port, set the `PORT` environment variable before running:
```bash
export PORT=8000
python app.py
```
and open `http://localhost:8000`.

---

## Running Locally (Terminal Version)

1. Make sure you have **Python 3** installed.
2. Clone the repository:
   ```bash
   git clone https://github.com/kevinpedregosa/Number-Guessing-Game.git
   cd Number-Guessing-Game
   ```
3. Run the terminal game:
   ```bash
   python number_guessing_game.py
   ```

---

## Gameplay Example (Terminal)
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
