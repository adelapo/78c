# Snake Game using Tkinter Canvas -- an intro to Python and Raspberry Pi
# Andrew DeLapo

import tkinter as tk  # Popular GUI library for Python
import random  # Generate random numbers

# Holds our game
root = tk.Tk()

# Title of the window
root.wm_title("Snake Game")

canvas_width = 800
canvas_height = 600

# Drawing surface
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")

# Put the canvas in the root window
canvas.pack(fill="both", expand=True)


# Helper function draws rectangles on the canvas
def draw_rect(x, y, color):
    square_size = 20
    canvas.create_rectangle(x * square_size, y * square_size, (x + 1) * square_size, (y + 1) * square_size,
                            fill=color, outline=color)


# Apple object
class Apple:
    def __init__(self, position):
        self.position = position

    def respawn(self):
        self.position[0] = random.randint(0, 39)
        self.position[1] = random.randint(0, 29)

    def draw(self):
        draw_rect(self.position[0], self.position[1], "red")


# Snake object
class Snake:
    def __init__(self, start_body):
        self.body = start_body
        self.direction = "right"
        self.growth = 0
        self.score = 0

    def move(self):
        dx = 0
        dy = 0
        if self.direction == "left":
            dx = -1
        elif self.direction == "right":
            dx = 1
        elif self.direction == "up":
            dy = -1
        elif self.direction == "down":
            dy = 1

        old_head = self.body[-1]
        new_head = [old_head[0] + dx, old_head[1] + dy]
        self.body.append(new_head)
        if self.growth > 0:
            self.growth = self.growth - 1
        else:
            self.body = self.body[1:]

    def draw(self):
        for segment in self.body:
            draw_rect(segment[0], segment[1], "green")

    def contains(self, position):
        for segment in self.body:
            if segment[0] == position[0] and segment[1] == position[1]:
                return True
        return False

    def is_self_colliding(self):
        head = self.body[-1]
        for segment in self.body[:-1]:
            if segment[0] == head[0] and segment[1] == head[1]:
                return True
        return False

    def grow(self):
        self.growth = self.growth + 1


# Create game objects
snake = Snake([[0, 0], [1, 0], [2, 0], [3, 0]])
apple = Apple([0, 0])
apple.respawn()

# Keycodes for arrow keys
LEFT_ARROW = 113  # 37 for PCs
UP_ARROW = 111  # 38 for PCs
RIGHT_ARROW = 114  # 39 for PCs
DOWN_ARROW = 116  # 40 for PCs


# Runs when arrow keys are pressed; changes direction of snake
def arrow_key_press(event):
    if event.keycode == LEFT_ARROW:
        snake.direction = "left"
    elif event.keycode == RIGHT_ARROW:
        snake.direction = "right"
    elif event.keycode == UP_ARROW:
        snake.direction = "up"
    elif event.keycode == DOWN_ARROW:
        snake.direction = "down"


# Run arrow_key_press when arrow keys are pressed
root.bind("<Left>", arrow_key_press)
root.bind("<Right>", arrow_key_press)
root.bind("<Up>", arrow_key_press)
root.bind("<Down>", arrow_key_press)


# The game over screen
def game_over():
    canvas.create_text((canvas_width / 2, canvas_height / 2 - 100), text="GAME OVER", font="Arial 32 bold",
                       fill="white", anchor="center")
    canvas.create_text((canvas_width / 2, canvas_height / 2 + 100), text="Score: " + str(snake.score),
                       font="Arial 32 bold", fill="white", anchor="center")


# This gameloop function runs over and over
def gameloop():
    # Clear the screen
    canvas.delete("all")

    snake.move()
    snake.draw()

    apple.draw()

    # Is the snake eating the apple?
    if snake.contains(apple.position):
        apple.respawn()
        snake.grow()
        snake.score = snake.score + 1

    # Is the snake hitting itself?
    if not snake.is_self_colliding():
        canvas.after(50, gameloop)
    else:
        game_over()

# Start the gameloop
gameloop()

# When game starts, make sure window is in focus
root.after(100, root.focus)

# Start the game
root.mainloop()
