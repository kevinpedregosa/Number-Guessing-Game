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

## Documentation

### High‑Level Architecture

- **Core game engine**: Implemented in `number_guessing_game.py` and reused by both the terminal and web versions (hint logic, distance calculations, leaderboard handling).
- **Web backend**: `app.py` exposes HTTP JSON APIs for starting a game, submitting guesses, and fetching the leaderboard, and renders the main HTML page.
- **Web frontend**: `templates/index.html`, `static/app.js`, and `static/style.css` provide the browser UI and communicate with the Flask backend.
- **Persistence**: Scores are stored in a simple text file `leaderboard.txt`, shared between the CLI and web versions.

### Languages & Technologies Used

- **Python 3**
  - Main programming language for the project.
  - Implements game logic (difficulty, hints, hot/cold feedback) and leaderboard management.
- **Flask**
  - Lightweight Python web framework used to build the backend.
  - Renders the main HTML page and provides REST‑style endpoints:
    - `GET /api/leaderboard` to read scores.
    - `POST /api/start-game` to start a new game and initialize session state.
    - `POST /api/guess` to submit guesses and return feedback.
- **Flask Sessions**
  - Used to store per‑user game state on the server (secret number, attempts used, difficulty, hints already given).
  - Allows the game to keep track of progress across multiple HTTP requests from the same browser.
- **HTML**
  - Used in `templates/index.html` to structure the web page (header, setup form, game area, leaderboard table).
  - Integrates with Flask using Jinja templating (`{{ url_for(...) }}`) to link static assets.
- **CSS**
  - Defined in `static/style.css` to provide layout, responsive design, and a modern look (cards, buttons, message styles, leaderboard table).
  - Uses CSS grid for layout and media queries for mobile responsiveness.
- **JavaScript (Vanilla JS)**
  - Located in `static/app.js`.
  - Handles UI interactions: starting a game, submitting guesses, updating messages, and toggling “Play Again”.
  - Uses the Fetch API to call the Flask endpoints, parses JSON responses, and updates DOM elements (status bar, messages, leaderboard).
- **Gunicorn**
  - Production WSGI HTTP server specified in `Procfile` as `gunicorn app:app`.
  - Used by hosting platforms to serve the Flask app in a more robust way than the development server.
- **Text file storage**
  - `leaderboard.txt` stores results in a human‑readable format.
  - Shared between the terminal and web versions so both can show and update the same top 5 scores.

### How the Game Works

- **Terminal Version**
  - Entry point: running `python number_guessing_game.py`.
  - Prompts the player for a username and difficulty.
  - On each attempt, reads input from the terminal, validates it, and:
    - Computes a distance‑based hint (`Very close`, `Close`, `Far`, `Very far`).
    - Provides “Getting warmer/colder” feedback compared to the previous guess.
    - Optionally gives one of four smart hints based on the secret number’s properties.
  - When the game ends (win or attempts exhausted), updates `leaderboard.txt` and prints the leaderboard.

- **Web Version**
  - Entry point: running `python app.py` (development) or `gunicorn app:app` (production).
  - A user opens the browser page, fills in username and difficulty, and the frontend calls `POST /api/start-game`.
  - Flask:
    - Generates a secret number and hint schedule.
    - Stores all game state in the session.
    - Returns basic game info and current leaderboard as JSON.
  - For each guess:
    - The frontend sends `POST /api/guess` with the guess number.
    - The backend validates the guess, updates attempt count and session game state, calculates hints, and checks win/lose conditions.
    - The response includes feedback text, attempts left, any smart hint, and (on game over) performance summary and updated leaderboard.
  - The frontend updates the on‑screen messages, status bar (attempts left, difficulty, username), and the leaderboard table accordingly.

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
