import tkinter as tk
import random

class Snake:
    def __init__(self, canvas, canvas_width, canvas_height):
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.snake_size = 20
        self.snake_body = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.snake_parts = []
        self.create_snake()
    
    def create_snake(self):
        for x, y in self.snake_body:
            part = self.canvas.create_rectangle(x, y, x + self.snake_size, y + self.snake_size, 
                                              fill="green", outline="black")
            self.snake_parts.append(part)
    
    def move(self):
        head_x, head_y = self.snake_body[0]
        
        if self.direction == "Right":
            new_head = (head_x + self.snake_size, head_y)
        elif self.direction == "Left":
            new_head = (head_x - self.snake_size, head_y)
        elif self.direction == "Up":
            new_head = (head_x, head_y - self.snake_size)
        elif self.direction == "Down":
            new_head = (head_x, head_y + self.snake_size)
        
        self.snake_body.insert(0, new_head)
        
        self.canvas.delete(self.snake_parts[-1])
        self.snake_parts.pop()
        
        head_part = self.canvas.create_rectangle(new_head[0], new_head[1], 
                                               new_head[0] + self.snake_size, 
                                               new_head[1] + self.snake_size,
                                               fill="green", outline="black")
        self.snake_parts.insert(0, head_part)
        
        self.snake_body.pop()
    
    def grow(self):
        tail_x, tail_y = self.snake_body[-1]
        self.snake_body.append((tail_x, tail_y))
        tail_part = self.canvas.create_rectangle(tail_x, tail_y, 
                                               tail_x + self.snake_size, 
                                               tail_y + self.snake_size,
                                               fill="green", outline="black")
        self.snake_parts.append(tail_part)
    
    def change_direction(self, new_direction):
        opposite = {"Right": "Left", "Left": "Right", "Up": "Down", "Down": "Up"}
        if new_direction != opposite[self.direction]:
            self.direction = new_direction
    
    def check_collision(self):
        head_x, head_y = self.snake_body[0]
        
        if (head_x < 0 or head_x >= self.canvas_width or 
            head_y < 0 or head_y >= self.canvas_height):
            return True
        
        for segment in self.snake_body[1:]:
            if (head_x, head_y) == segment:
                return True
        
        return False

class Food:
    def __init__(self, canvas, canvas_width, canvas_height, snake_size):
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.snake_size = snake_size
        self.food_item = None
        self.create_food()
    
    def create_food(self):
        if self.food_item:
            self.canvas.delete(self.food_item)
        
        x = random.randint(0, (self.canvas_width // self.snake_size) - 1) * self.snake_size
        y = random.randint(0, (self.canvas_height // self.snake_size) - 1) * self.snake_size
        
        self.food_item = self.canvas.create_rectangle(x, y, x + self.snake_size, y + self.snake_size,
                                                     fill="red", outline="black")
        self.position = (x, y)
    
    def get_position(self):
        return self.position

class SnakeGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Snake Game")
        self.root.resizable(False, False)
        
        self.canvas_width = 600
        self.canvas_height = 600
        self.snake_size = 20
        
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()
        
        self.score = 0
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.pack()
        
        self.snake = Snake(self.canvas, self.canvas_width, self.canvas_height)
        self.food = Food(self.canvas, self.canvas_width, self.canvas_height, self.snake_size)
        
        self.game_running = True
        
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.focus_set()
        
        self.game_loop()
    
    def on_key_press(self, event):
        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            self.snake.change_direction(key)
        elif key == "r" and not self.game_running:
            self.restart_game()
    
    def check_food_collision(self):
        head_x, head_y = self.snake.snake_body[0]
        food_x, food_y = self.food.get_position()
        
        if head_x == food_x and head_y == food_y:
            return True
        return False
    
    def game_loop(self):
        if self.game_running:
            self.snake.move()
            
            if self.check_food_collision():
                self.snake.grow()
                self.food.create_food()
                self.score += 10
                self.score_label.config(text=f"Score: {self.score}")
            
            if self.snake.check_collision():
                self.game_over()
                return
            
            self.root.after(150, self.game_loop)
    
    def game_over(self):
        self.game_running = False
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
                               text="GAME OVER", fill="white", font=("Arial", 24))
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 40,
                               text="Press 'r' to restart", fill="white", font=("Arial", 16))
    
    def restart_game(self):
        self.canvas.delete("all")
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")
        self.snake = Snake(self.canvas, self.canvas_width, self.canvas_height)
        self.food = Food(self.canvas, self.canvas_width, self.canvas_height, self.snake_size)
        self.game_running = True
        self.game_loop()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()