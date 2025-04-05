import random
import time
import os
import json
from datetime import datetime

class HangmanGame:
    """
    A comprehensive Hangman game with multiple features:
    - Different difficulty levels
    - Word categories
    - Score tracking
    - ASCII art animations
    - Hint system
    - Player profiles
    - Basic statistics
    """
    
    def __init__(self):
        """Initialize the Hangman game with default settings."""
        # Game configuration
        self.max_incorrect_guesses = 6  # Number of attempts before game over
        self.current_incorrect_guesses = 0  # Current number of incorrect guesses
        self.guessed_letters = []  # Letters already guessed
        self.word_to_guess = ""  # The word player needs to guess
        self.word_display = []  # Word display with revealed letters and underscores
        self.game_over = False  # Flag to track if the game is over
        self.game_won = False  # Flag to track if the player won
        self.current_player = "Guest"  # Default player name
        self.score = 0  # Player's score for the current game
        self.difficulty = "medium"  # Default difficulty level
        self.category = "random"  # Default word category
        self.game_start_time = None  # Track when the game started
        self.game_end_time = None  # Track when the game ended
        self.hints_used = 0  # Track how many hints were used
        
        # Word categories with words of varying difficulties
        self.word_categories = {
            "animals": {
                "easy": ["dog", "cat", "fish", "bird", "frog", "duck", "cow", "pig", "fox", "wolf"],
                "medium": ["dolphin", "elephant", "penguin", "kangaroo", "leopard", "giraffe", "zebra", "monkey", "turtle", "rabbit"],
                "hard": ["platypus", "rhinoceros", "hippopotamus", "chameleon", "crocodile", "chimpanzee", "porcupine", "orangutan", "anaconda", "tarantula"]
            },
            "countries": {
                "easy": ["spain", "japan", "italy", "egypt", "india", "china", "peru", "chile", "cuba", "mali"],
                "medium": ["australia", "germany", "canada", "mexico", "brazil", "turkey", "russia", "sweden", "ireland", "morocco"],
                "hard": ["kazakhstan", "zimbabwe", "uruguay", "switzerland", "philippines", "madagascar", "mongolia", "nicaragua", "azerbaijan", "bangladesh"]
            },
            "technology": {
                "easy": ["mouse", "phone", "code", "game", "data", "wifi", "chip", "blog", "site", "byte"],
                "medium": ["keyboard", "internet", "software", "hardware", "database", "network", "website", "computer", "algorithm", "password"],
                "hard": ["cryptography", "blockchain", "javascript", "middleware", "kubernetes", "recursion", "virtualization", "microservice", "authentication", "algorithm"]
            },
            "space": {
                "easy": ["star", "moon", "mars", "sun", "sky", "earth", "space", "comet", "orbit", "venus"],
                "medium": ["galaxy", "jupiter", "neptune", "planet", "asteroid", "meteor", "saturn", "gravity", "cosmos", "telescope"],
                "hard": ["constellation", "supernova", "spacecraft", "atmosphere", "nebulosity", "satellite", "observatory", "interstellar", "gravitational", "astrophysics"]
            },
            "food": {
                "easy": ["cake", "rice", "fish", "meat", "milk", "corn", "egg", "soup", "taco", "pie"],
                "medium": ["chicken", "burger", "spaghetti", "sandwich", "chocolate", "pancake", "lasagna", "burrito", "waffle", "cupcake"],
                "hard": ["quesadilla", "croissant", "asparagus", "blueberry", "carbonara", "guacamole", "cheesecake", "stroganoff", "bruschetta", "frittata"]
            }
        }
        
        # Player profiles storage
        self.player_profiles = {}
        self.load_player_profiles()
        
        # ASCII art for hangman stages
        self.hangman_stages = [
            # 0 incorrect guesses
            """
              +---+
              |   |
                  |
                  |
                  |
                  |
            =========
            """,
            # 1 incorrect guess
            """
              +---+
              |   |
              O   |
                  |
                  |
                  |
            =========
            """,
            # 2 incorrect guesses
            """
              +---+
              |   |
              O   |
              |   |
                  |
                  |
            =========
            """,
            # 3 incorrect guesses
            """
              +---+
              |   |
              O   |
             /|   |
                  |
                  |
            =========
            """,
            # 4 incorrect guesses
            """
              +---+
              |   |
              O   |
             /|\\  |
                  |
                  |
            =========
            """,
            # 5 incorrect guesses
            """
              +---+
              |   |
              O   |
             /|\\  |
             /    |
                  |
            =========
            """,
            # 6 incorrect guesses (game over)
            """
              +---+
              |   |
              O   |
             /|\\  |
             / \\  |
                  |
            =========
            """
        ]
        
        # ASCII art for game title
        self.title_art = """
        ██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
        ██║  ██║██╔══██╗████╗  ██║██╔════╝ ████╗ ████║██╔══██╗████╗  ██║
        ███████║███████║██╔██╗ ██║██║  ███╗██╔████╔██║███████║██╔██╗ ██║
        ██╔══██║██╔══██║██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║
        ██║  ██║██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║
        ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
        """
        
        # ASCII art for win/lose messages
        self.win_art = """
         __   __  _______  __   __    _     _  ___   __    _  __   __
        |  | |  ||       ||  | |  |  | | _ | ||   | |  |  | ||  | |  |
        |  |_|  ||   _   ||  | |  |  | || || ||   | |   |_| ||  |_|  |
        |       ||  | |  ||  |_|  |  |       ||   | |       ||       |
        |_     _||  |_|  ||       |  |       ||   | |  _    ||       |
          |   |  |       ||       |  |   _   ||   | | | |   ||   _   |
          |___|  |_______||_______|  |__| |__||___| |_|  |__||__| |__|
        """
        
        self.lose_art = """
         __   __  _______  __   __    ___      _______  _______  _______    __
        |  | |  ||       ||  | |  |  |   |    |       ||       ||       |  |  |
        |  |_|  ||   _   ||  | |  |  |   |    |   _   ||  _____||_     _|  |  |
        |       ||  | |  ||  |_|  |  |   |    |  | |  || |_____   |   |    |  |
        |_     _||  |_|  ||       |  |   |___ |  |_|  ||_____  |  |   |    |__|
          |   |  |       ||       |  |       ||       | _____| |  |   |     __
          |___|  |_______||_______|  |_______||_______||_______|  |___|    |__|
        """

    def clear_screen(self):
        """Clear the console screen (works on Windows, macOS, and Linux)."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def load_player_profiles(self):
        """Load player profiles from a JSON file if it exists."""
        try:
            with open("hangman_profiles.json", "r") as file:
                self.player_profiles = json.load(file)
            print("Player profiles loaded successfully!")
        except FileNotFoundError:
            # If the file doesn't exist, create an empty dictionary
            self.player_profiles = {}
            print("No player profiles found. Starting fresh!")
        except json.JSONDecodeError:
            # If the file is corrupted
            self.player_profiles = {}
            print("Player profile file corrupted. Starting fresh!")
    
    def save_player_profiles(self):
        """Save player profiles to a JSON file."""
        try:
            with open("hangman_profiles.json", "w") as file:
                json.dump(self.player_profiles, file, indent=4)
            print("Player profiles saved successfully!")
        except Exception as e:
            print(f"Failed to save player profiles: {e}")
    
    def create_player_profile(self, name):
        """Create a new player profile or load an existing one."""
        if name in self.player_profiles:
            print(f"Welcome back, {name}!")
        else:
            self.player_profiles[name] = {
                "games_played": 0,
                "games_won": 0,
                "games_lost": 0,
                "best_score": 0,
                "total_score": 0,
                "favorite_category": "",
                "last_played": "",
                "highest_streak": 0,
                "current_streak": 0
            }
            print(f"New player profile created for {name}!")
        
        self.current_player = name
    
    def update_player_stats(self, won):
        """Update player statistics after a game."""
        if self.current_player in self.player_profiles:
            profile = self.player_profiles[self.current_player]
            profile["games_played"] += 1
            profile["last_played"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if won:
                profile["games_won"] += 1
                profile["current_streak"] += 1
                if profile["current_streak"] > profile["highest_streak"]:
                    profile["highest_streak"] = profile["current_streak"]
            else:
                profile["games_lost"] += 1
                profile["current_streak"] = 0
            
            profile["total_score"] += self.score
            if self.score > profile["best_score"]:
                profile["best_score"] = self.score
            
            # Update favorite category based on most played
            if "category_counts" not in profile:
                profile["category_counts"] = {}
            
            if self.category not in profile["category_counts"]:
                profile["category_counts"][self.category] = 1
            else:
                profile["category_counts"][self.category] += 1
            
            # Find the most played category
            favorite = max(profile["category_counts"].items(), key=lambda x: x[1])
            profile["favorite_category"] = favorite[0]
            
            self.save_player_profiles()
    
    def display_player_stats(self):
        """Display player statistics."""
        if self.current_player not in self.player_profiles:
            print("No player profile found. Create a profile first!")
            return
        
        profile = self.player_profiles[self.current_player]
        self.clear_screen()
        print(f"\n{'=' * 40}")
        print(f"  Player Stats: {self.current_player}")
        print(f"{'=' * 40}")
        print(f"  Games Played: {profile['games_played']}")
        print(f"  Games Won: {profile['games_won']}")
        print(f"  Games Lost: {profile['games_lost']}")
        win_rate = 0 if profile['games_played'] == 0 else (profile['games_won'] / profile['games_played']) * 100
        print(f"  Win Rate: {win_rate:.1f}%")
        print(f"  Best Score: {profile['best_score']}")
        print(f"  Total Score: {profile['total_score']}")
        print(f"  Current Streak: {profile['current_streak']}")
        print(f"  Highest Streak: {profile['highest_streak']}")
        
        if "favorite_category" in profile and profile["favorite_category"]:
            print(f"  Favorite Category: {profile['favorite_category'].capitalize()}")
        
        if "last_played" in profile and profile["last_played"]:
            print(f"  Last Played: {profile['last_played']}")
        
        print(f"{'=' * 40}")
        input("\nPress Enter to continue...")
    
    def choose_random_word(self):
        """Choose a random word based on the current category and difficulty."""
        # Get words from the selected category or from all categories if 'random'
        if self.category == "random":
            # If random category, pick a random category first
            category_name = random.choice(list(self.word_categories.keys()))
            words = self.word_categories[category_name][self.difficulty]
        else:
            words = self.word_categories[self.category][self.difficulty]
        
        # Return a random word from the list
        return random.choice(words)
    
    def initialize_word_display(self):
        """Initialize the word display with underscores for each letter."""
        self.word_display = ["_" for _ in self.word_to_guess]
    
    def display_game(self):
        """Display the current state of the game."""
        self.clear_screen()
        
        # Display title
        print(self.title_art)
        
        # Display game information
        print(f"\nPlayer: {self.current_player} | Difficulty: {self.difficulty.capitalize()} | Category: {self.category.capitalize()}")
        print(f"Score: {self.score} | Hints Used: {self.hints_used}")
        
        # Display hangman ASCII art
        print(self.hangman_stages[self.current_incorrect_guesses])
        
        # Display word with guessed letters
        print("\nWord: " + " ".join(self.word_display))
        
        # Display guessed letters
        print("\nGuessed letters: " + ", ".join(sorted(self.guessed_letters)) if self.guessed_letters else "\nGuessed letters: None")
        
        # Display remaining attempts
        remaining = self.max_incorrect_guesses - self.current_incorrect_guesses
        print(f"\nRemaining attempts: {remaining}")
    
    def update_word_display(self, letter):
        """Update the word display with the correctly guessed letter."""
        for i in range(len(self.word_to_guess)):
            if self.word_to_guess[i] == letter:
                self.word_display[i] = letter
    
    def is_word_guessed(self):
        """Check if the word has been completely guessed."""
        return "_" not in self.word_display
    
    def process_guess(self, guess):
        """Process a player's guess."""
        # Check if the guess is a single letter
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            time.sleep(1)
            return
        
        # Convert to lowercase
        guess = guess.lower()
        
        # Check if the letter has already been guessed
        if guess in self.guessed_letters:
            print("You already guessed that letter!")
            time.sleep(1)
            return
        
        # Add the letter to guessed letters
        self.guessed_letters.append(guess)
        
        # Check if the guess is correct
        if guess in self.word_to_guess:
            print("Good guess!")
            self.update_word_display(guess)
            # Calculate score for correct guess based on difficulty
            difficulty_multiplier = {"easy": 1, "medium": 2, "hard": 3}
            self.score += 10 * difficulty_multiplier[self.difficulty]
        else:
            print("Incorrect guess!")
            self.current_incorrect_guesses += 1
        
        # Check if the game is over
        if self.is_word_guessed():
            self.game_won = True
            self.game_over = True
            self.game_end_time = time.time()
            # Bonus points for winning based on difficulty and remaining attempts
            time_bonus = max(0, int(300 - (self.game_end_time - self.game_start_time)))
            difficulty_multiplier = {"easy": 1, "medium": 2, "hard": 3}
            remaining_attempts = self.max_incorrect_guesses - self.current_incorrect_guesses
            win_bonus = 50 * difficulty_multiplier[self.difficulty] * (remaining_attempts + 1)
            self.score += win_bonus + time_bonus
            # Penalty for using hints
            self.score -= self.hints_used * 25
            self.score = max(0, self.score)  # Ensure score doesn't go negative
        elif self.current_incorrect_guesses >= self.max_incorrect_guesses:
            self.game_over = True
            self.game_end_time = time.time()
        
        time.sleep(0.5)  # Brief pause for feedback
    
    def provide_hint(self):
        """Provide a hint to the player at the cost of score reduction."""
        if "_" not in self.word_display:
            print("You've already guessed the word! No hint needed.")
            time.sleep(1)
            return
        
        # Find all hidden letters
        hidden_indices = [i for i, char in enumerate(self.word_display) if char == "_"]
        
        if not hidden_indices:
            print("No more hints available.")
            time.sleep(1)
            return
        
        # Choose a random hidden letter to reveal
        hint_index = random.choice(hidden_indices)
        hint_letter = self.word_to_guess[hint_index]
        
        # Check if the letter has already been guessed
        if hint_letter in self.guessed_letters:
            print("Let me find another hint...")
            time.sleep(1)
            self.provide_hint()  # Try again with another letter
            return
        
        # Update the display and guessed letters
        self.guessed_letters.append(hint_letter)
        self.update_word_display(hint_letter)
        
        # Increment hints used counter and reduce score
        self.hints_used += 1
        self.score = max(0, self.score - 25)  # Reduce score but don't go below 0
        
        print(f"Hint: The letter '{hint_letter}' is in the word!")
        time.sleep(1.5)
    
    def show_game_over(self):
        """Display the game over screen."""
        self.clear_screen()
        
        if self.game_won:
            print(self.win_art)
            print(f"\nCongratulations, {self.current_player}! You guessed the word: {self.word_to_guess}")
            print(f"Your score: {self.score}")
            
            # Calculate time taken
            time_taken = int(self.game_end_time - self.game_start_time)
            minutes = time_taken // 60
            seconds = time_taken % 60
            print(f"Time taken: {minutes} minutes and {seconds} seconds")
        else:
            print(self.lose_art)
            print(f"\nSorry, {self.current_player}! You've run out of attempts.")
            print(f"The word was: {self.word_to_guess}")
            print(f"Your score: {self.score}")
        
        self.update_player_stats(self.game_won)
        
        print("\nDo you want to:")
        print("1. Play again")
        print("2. View your statistics")
        print("3. Exit")
        
        while True:
            choice = input("\nEnter your choice (1-3): ")
            if choice == "1":
                return True  # Play again
            elif choice == "2":
                self.display_player_stats()
                return self.show_game_over()  # Show this menu again after displaying stats
            elif choice == "3":
                return False  # Exit
            else:
                print("Invalid choice. Please try again.")
    
    def show_main_menu(self):
        """Display the main menu of the game."""
        self.clear_screen()
        print(self.title_art)
        print("\nWelcome to Hangman!")
        print("\nMain Menu:")
        print("1. Start a new game")
        print("2. Select difficulty")
        print("3. Select category")
        print("4. Player profile")
        print("5. View statistics")
        print("6. How to play")
        print("7. Exit")
        
        while True:
            choice = input("\nEnter your choice (1-7): ")
            
            if choice == "1":
                self.start_game()
                break
            elif choice == "2":
                self.select_difficulty()
                return self.show_main_menu()
            elif choice == "3":
                self.select_category()
                return self.show_main_menu()
            elif choice == "4":
                self.manage_profile()
                return self.show_main_menu()
            elif choice == "5":
                self.display_player_stats()
                return self.show_main_menu()
            elif choice == "6":
                self.show_instructions()
                return self.show_main_menu()
            elif choice == "7":
                self.clear_screen()
                print("\nThank you for playing Hangman! Goodbye.")
                return False
            else:
                print("Invalid choice. Please try again.")
    
    def select_difficulty(self):
        """Allow the player to select a difficulty level."""
        self.clear_screen()
        print("\nSelect Difficulty:")
        print("1. Easy (Simple words)")
        print("2. Medium (Moderate words)")
        print("3. Hard (Challenging words)")
        print("4. Back to main menu")
        
        while True:
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                self.difficulty = "easy"
                print("Difficulty set to Easy")
                time.sleep(1)
                break
            elif choice == "2":
                self.difficulty = "medium"
                print("Difficulty set to Medium")
                time.sleep(1)
                break
            elif choice == "3":
                self.difficulty = "hard"
                print("Difficulty set to Hard")
                time.sleep(1)
                break
            elif choice == "4":
                return
            else:
                print("Invalid choice. Please try again.")
    
    def select_category(self):
        """Allow the player to select a word category."""
        self.clear_screen()
        print("\nSelect Word Category:")
        
        # Display available categories
        categories = list(self.word_categories.keys())
        categories.append("random")  # Add random option
        
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category.capitalize()}")
        
        print(f"{len(categories) + 1}. Back to main menu")
        
        while True:
            choice = input(f"\nEnter your choice (1-{len(categories) + 1}): ")
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(categories):
                    self.category = categories[choice_num - 1]
                    print(f"Category set to {self.category.capitalize()}")
                    time.sleep(1)
                    break
                elif choice_num == len(categories) + 1:
                    return
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
    
    def manage_profile(self):
        """Manage player profiles."""
        self.clear_screen()
        print("\nPlayer Profile Management:")
        print("1. Create/Select a profile")
        print("2. View all profiles")
        print("3. Delete a profile")
        print("4. Back to main menu")
        
        while True:
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                name = input("\nEnter your name: ").strip()
                if name:
                    self.create_player_profile(name)
                    time.sleep(1)
                break
            elif choice == "2":
                self.clear_screen()
                print("\nAvailable Profiles:")
                
                if not self.player_profiles:
                    print("No profiles found.")
                else:
                    for i, name in enumerate(self.player_profiles.keys(), 1):
                        print(f"{i}. {name}")
                
                input("\nPress Enter to continue...")
                return self.manage_profile()
            elif choice == "3":
                self.delete_profile()
                return self.manage_profile()
            elif choice == "4":
                return
            else:
                print("Invalid choice. Please try again.")
    
    def delete_profile(self):
        """Delete a player profile."""
        self.clear_screen()
        print("\nDelete Profile:")
        
        if not self.player_profiles:
            print("No profiles found.")
            time.sleep(1)
            return
        
        profiles = list(self.player_profiles.keys())
        for i, name in enumerate(profiles, 1):
            print(f"{i}. {name}")
        
        print(f"{len(profiles) + 1}. Cancel")
        
        while True:
            choice = input(f"\nSelect a profile to delete (1-{len(profiles) + 1}): ")
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(profiles):
                    profile_name = profiles[choice_num - 1]
                    
                    # Confirm deletion
                    confirm = input(f"Are you sure you want to delete the profile for {profile_name}? (y/n): ")
                    if confirm.lower() == 'y':
                        del self.player_profiles[profile_name]
                        self.save_player_profiles()
                        print(f"Profile for {profile_name} deleted.")
                        
                        # If the current player's profile was deleted, reset to Guest
                        if self.current_player == profile_name:
                            self.current_player = "Guest"
                    break
                elif choice_num == len(profiles) + 1:
                    return
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
        
        time.sleep(1)
    
    def show_instructions(self):
        """Display game instructions."""
        self.clear_screen()
        print("\n=== How to Play Hangman ===")
        print("\n1. The computer will choose a random word based on your selected category and difficulty.")
        print("2. You need to guess the word letter by letter.")
        print("3. For each incorrect guess, a part of the hangman is drawn.")
        print("4. You have 6 incorrect guesses before the game is over.")
        print("5. You can use hints to reveal a letter, but it will reduce your score.")
        print("\nScoring System:")
        print("- Correct guess: 10-30 points (based on difficulty)")
        print("- Winning bonus: Based on difficulty, remaining attempts, and time taken")
        print("- Hint penalty: -25 points per hint")
        print("\nDifficulty Levels:")
        print("- Easy: Simple words")
        print("- Medium: Moderate words")
        print("- Hard: Challenging words")
        print("\nCategories:")
        print("- Animals, Countries, Technology, Space, Food")
        print("- Random: Words from any category")
        
        input("\nPress Enter to continue...")
    
    def start_game(self):
        """Initialize and start a new game."""
        # Reset game state
        self.current_incorrect_guesses = 0
        self.guessed_letters = []
        self.game_over = False
        self.game_won = False
        self.score = 0
        self.hints_used = 0
        
        # Select a word to guess
        self.word_to_guess = self.choose_random_word()
        
        # Initialize word display
        self.initialize_word_display()
        
        # Start the game loop
        self.game_start_time = time.time()
        while not self.game_over:
            # Display the current game state
            self.display_game()
            
            # Get player input
            print("\nOptions:")
            print("1. Guess a letter")
            print("2. Use a hint")
            print("3. Return to main menu")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == "1":
                guess = input("Enter a letter: ")
                self.process_guess(guess)
            elif choice == "2":
                self.provide_hint()
            elif choice == "3":
                confirm = input("Are you sure you want to exit the game? (y/n): ")
                if confirm.lower() == 'y':
                    return self.show_main_menu()
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)
            
            # Check if the game is over
            if self.game_over:
                play_again = self.show_game_over()
                if play_again:
                    return self.start_game()
                else:
                    return self.show_main_menu()
    
    def run(self):
        """Run the Hangman game."""
        continue_game = True
        while continue_game:
            continue_game = self.show_main_menu()


def main():
    """Main function to run the Hangman game."""
    # Create and run the game
    game = HangmanGame()
    game.run()


if __name__ == "__main__":
    main()
