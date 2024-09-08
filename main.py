import tkinter as tk
from tkinter import filedialog, messagebox
import random
 
 
def display_word(word, guessed_letters):
   """Display the word with unguessed letters as underscores."""
   return " ".join([letter if letter in guessed_letters else '_' for letter in word])
 
 
def process_guess(event):
   """Process user input guess and update game state."""
   global word, guessed_letters, attempts, word_label, attempts_label, message_label
 
 
   guess = guess_entry.get().lower()
   guess_entry.delete(0, tk.END)
 
 
   if len(guess) != 1 or not guess.isalpha():
       message_label.config(text="Please enter a valid letter.")
       return
 
 
   if guess in guessed_letters:
       message_label.config(text=f"You already guessed '{guess}'.")
   elif guess in word:
       guessed_letters.add(guess)
       message_label.config(text=f"Good job! '{guess}' is in the word.")
   else:
       attempts -= 1
       message_label.config(text=f"Sorry, '{guess}' is not in the word.")
 
 
   update_game_state()
 
 
def show_hint():
   """Reveal a random letter from the word as a hint."""
   global word, guessed_letters, attempts, message_label
 
 
   available_letters = [letter for letter in word if letter not in guessed_letters]
   if available_letters:
       hint_letter = random.choice(available_letters)
       guessed_letters.add(hint_letter)
       attempts -= 1
       message_label.config(text=f"Hint: The letter '{hint_letter}' has been revealed!")
       update_game_state()
   else:
       message_label.config(text="No more letters to reveal.")
 
 
def update_game_state():
   """Update the game display and check for win/loss conditions."""
   global word, guessed_letters, attempts, word_label, attempts_label, message_label, guess_entry, hint_button, restart_button
 
 
   word_label.config(text=display_word(word, guessed_letters))
   attempts_label.config(text=f"Attempts left: {attempts}")
 
 
   if all(letter in guessed_letters for letter in word):
       message_label.config(text=f"Congratulations! You've guessed the word '{word}'.")
       end_game()
   elif attempts == 0:
       word_label.config(text=word)
       message_label.config(text=f"Game Over! The word was '{word}'.")
       end_game()
 
 
def end_game():
   """Disable input and show restart button when the game ends."""
   guess_entry.config(state=tk.DISABLED)
   hint_button.config(state=tk.DISABLED)
   restart_button.config(state=tk.NORMAL)
 
 
def restart_game():
   """Restart the game with a new random word."""
   global word, guessed_letters, attempts, word_list
 
 
   word = random.choice(word_list)
   guessed_letters = set()
   attempts = 6
   word_label.config(text=display_word(word, guessed_letters))
   attempts_label.config(text=f"Attempts left: {attempts}")
   message_label.config(text="")
   guess_entry.config(state=tk.NORMAL)
   hint_button.config(state=tk.NORMAL)
   restart_button.config(state=tk.DISABLED)
 
 
def upload_word_list():
   """Allow user to upload a custom word list."""
   global word_list, word
 
 
   file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
   if file_path:
       try:
           with open(file_path, 'r') as file:
               words = file.read().splitlines()
           if words:
               word_list = words
               restart_game()  # Start a new game with the uploaded word list
               messagebox.showinfo("Word List Uploaded", "A new word list has been successfully uploaded.")
           else:
               messagebox.showerror("Error", "The file is empty.")
       except Exception as e:
           messagebox.showerror("Error", f"Failed to load the file: {e}")
   else:
       messagebox.showwarning("No File Selected", "Please select a valid text file.")
 
 
 
 
# Initialize game variables
word_list = [
   'python', 'hangman', 'programming', 'developer', 'algorithm', 'function',
   'variable', 'software', 'debugging', 'network', 'database', 'compiler'
]
word = random.choice(word_list)
guessed_letters = set()
attempts = 6
 
 
# Create GUI
root = tk.Tk()
root.title("Word Guesser Game - The Pycodes")
root.geometry("400x500")
 
 
word_label = tk.Label(root, text=display_word(word, guessed_letters), font=('Helvetica', 20))
word_label.pack(pady=20)
 
 
attempts_label = tk.Label(root, text=f"Attempts left: {attempts}", font=('Helvetica', 14))
attempts_label.pack(pady=10)
 
 
guess_entry = tk.Entry(root, font=('Helvetica', 16), width=3)
guess_entry.pack(pady=10)
guess_entry.bind("<Return>", process_guess)
 
 
message_label = tk.Label(root, text="", font=('Helvetica', 14))
message_label.pack(pady=10)
 
 
hint_button = tk.Button(root, text="Show Hint", command=show_hint)
hint_button.pack(pady=5)
 
 
upload_button = tk.Button(root, text="Upload Word List", command=upload_word_list)
upload_button.pack(pady=5)
 
 
restart_button = tk.Button(root, text="Restart", command=restart_game, state=tk.DISABLED)
restart_button.pack(pady=20)
 
 
root.mainloop()
