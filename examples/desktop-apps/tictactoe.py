import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe Game")
        self.window.geometry("400x500")
        self.window.resizable(False, False)
        self.window.configure(bg="#2c3e50")
        
        # Game state
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.game_mode = "pvp"  # pvp = Player vs Player, pvc = Player vs Computer
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.window,
            text="TIC-TAC-TOE",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title_label.pack(pady=10)
        
        # Game mode selection
        mode_frame = tk.Frame(self.window, bg="#2c3e50")
        mode_frame.pack(pady=10)
        
        self.mode_var = tk.StringVar(value="pvp")
        
        pvp_radio = tk.Radiobutton(
            mode_frame,
            text="Player vs Player",
            variable=self.mode_var,
            value="pvp",
            font=("Arial", 12),
            bg="#2c3e50",
            fg="#ecf0f1",
            selectcolor="#34495e",
            activebackground="#2c3e50",
            activeforeground="#ecf0f1",
            command=self.change_game_mode
        )
        pvp_radio.pack(side=tk.LEFT, padx=10)
        
        pvc_radio = tk.Radiobutton(
            mode_frame,
            text="Player vs Computer",
            variable=self.mode_var,
            value="pvc",
            font=("Arial", 12),
            bg="#2c3e50",
            fg="#ecf0f1",
            selectcolor="#34495e",
            activebackground="#2c3e50",
            activeforeground="#ecf0f1",
            command=self.change_game_mode
        )
        pvc_radio.pack(side=tk.LEFT, padx=10)
        
        # Current player display
        self.player_label = tk.Label(
            self.window,
            text=f"Current Player: {self.current_player}",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="#e74c3c"
        )
        self.player_label.pack(pady=10)
        
        # Game board
        self.board_frame = tk.Frame(self.window, bg="#2c3e50")
        self.board_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(9):
            button = tk.Button(
                self.board_frame,
                text="",
                font=("Arial", 20, "bold"),
                width=5,
                height=2,
                bg="#34495e",
                fg="#ecf0f1",
                activebackground="#95a5a6",
                activeforeground="#2c3e50",
                relief="raised",
                borderwidth=3,
                command=lambda idx=i: self.make_move(idx)
            )
            button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(button)
        
        # Score display
        score_frame = tk.Frame(self.window, bg="#2c3e50")
        score_frame.pack(pady=20)
        
        self.score_label = tk.Label(
            score_frame,
            text=self.get_score_text(),
            font=("Arial", 14),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.score_label.pack()
        
        # Control buttons
        button_frame = tk.Frame(self.window, bg="#2c3e50")
        button_frame.pack(pady=10)
        
        reset_button = tk.Button(
            button_frame,
            text="New Game",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            width=12,
            height=1,
            command=self.reset_game
        )
        reset_button.pack(side=tk.LEFT, padx=5)
        
        reset_scores_button = tk.Button(
            button_frame,
            text="Reset Scores",
            font=("Arial", 12, "bold"),
            bg="#e67e22",
            fg="white",
            activebackground="#d35400",
            activeforeground="white",
            width=12,
            height=1,
            command=self.reset_scores
        )
        reset_scores_button.pack(side=tk.LEFT, padx=5)
        
        quit_button = tk.Button(
            button_frame,
            text="Quit",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white",
            width=12,
            height=1,
            command=self.window.quit
        )
        quit_button.pack(side=tk.LEFT, padx=5)
    
    def change_game_mode(self):
        self.game_mode = self.mode_var.get()
        self.reset_game()
    
    def get_score_text(self):
        if self.game_mode == "pvp":
            return f"Player X: {self.player_score}  |  Player O: {self.computer_score}  |  Ties: {self.ties}"
        else:
            return f"Player: {self.player_score}  |  Computer: {self.computer_score}  |  Ties: {self.ties}"
    
    def make_move(self, index):
        if self.board[index] == "" and not self.game_over:
            self.board[index] = self.current_player
            self.buttons[index].config(
                text=self.current_player,
                fg="#e74c3c" if self.current_player == "X" else "#3498db",
                state="disabled"
            )
            
            if self.check_winner():
                self.game_over = True
                winner = self.current_player
                if winner == "X":
                    self.player_score += 1
                else:
                    self.computer_score += 1
                
                self.score_label.config(text=self.get_score_text())
                
                winner_text = f"Player {winner} wins!" if self.game_mode == "pvp" else (
                    "You win!" if winner == "X" else "Computer wins!"
                )
                messagebox.showinfo("Game Over", winner_text)
                self.disable_all_buttons()
                
            elif self.check_tie():
                self.game_over = True
                self.ties += 1
                self.score_label.config(text=self.get_score_text())
                messagebox.showinfo("Game Over", "It's a tie!")
                
            else:
                self.switch_player()
                
                # Computer move in PvC mode
                if self.game_mode == "pvc" and self.current_player == "O" and not self.game_over:
                    self.window.after(500, self.computer_move)  # Delay for better UX
    
    def computer_move(self):
        if self.game_over:
            return
            
        # Simple AI: Try to win, block player, or random move
        move = self.get_best_move()
        if move is not None:
            self.make_move(move)
    
    def get_best_move(self):
        # First, try to win
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                if self.check_winner():
                    self.board[i] = ""  # Reset for actual move
                    return i
                self.board[i] = ""
        
        # Second, try to block player from winning
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"
                if self.check_winner():
                    self.board[i] = ""  # Reset for actual move
                    return i
                self.board[i] = ""
        
        # Third, take center if available
        if self.board[4] == "":
            return 4
        
        # Fourth, take corners
        corners = [0, 2, 6, 8]
        available_corners = [i for i in corners if self.board[i] == ""]
        if available_corners:
            return random.choice(available_corners)
        
        # Finally, take any available spot
        available_moves = [i for i in range(9) if self.board[i] == ""]
        if available_moves:
            return random.choice(available_moves)
        
        return None
    
    def check_winner(self):
        # Check all winning combinations
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ""):
                # Highlight winning combination
                for i in combo:
                    self.buttons[i].config(bg="#27ae60")
                return True
        return False
    
    def check_tie(self):
        return "" not in self.board
    
    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        color = "#e74c3c" if self.current_player == "X" else "#3498db"
        self.player_label.config(
            text=f"Current Player: {self.current_player}",
            fg=color
        )
    
    def disable_all_buttons(self):
        for button in self.buttons:
            button.config(state="disabled")
    
    def reset_game(self):
        self.current_player = "X"
        self.board = [""] * 9
        self.game_over = False
        
        for button in self.buttons:
            button.config(
                text="",
                state="normal",
                bg="#34495e",
                fg="#ecf0f1"
            )
        
        self.player_label.config(
            text=f"Current Player: {self.current_player}",
            fg="#e74c3c"
        )
    
    def reset_scores(self):
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.score_label.config(text=self.get_score_text())
        self.reset_game()
    
    def run(self):
        self.window.mainloop()

# Create and run the game
if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()