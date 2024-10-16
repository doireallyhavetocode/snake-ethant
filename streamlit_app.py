import streamlit as st
import numpy as np
import random
import time
import matplotlib.pyplot as plt

# Game constants
GRID_SIZE = 20
CELL_SIZE = 20

# Initialize game state
def init_game():
    return {
        "snake": [(5, 5), (5, 4), (5, 3)],
        "direction": (0, 1),
        "food": (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)),
        "score": 0,
        "game_over": False
    }

# Draw the game grid
def draw_grid(game_state):
    grid = np.zeros((GRID_SIZE, GRID_SIZE, 3), dtype=int)
    
    for x, y in game_state["snake"]:
        grid[x, y] = [0, 255, 0]  # Snake body (green)
        
    food_x, food_y = game_state["food"]
    grid[food_x, food_y] = [255, 0, 0]  # Food (red)
    
    return grid

# Update the game state
def update_game(game_state):
    if game_state["game_over"]:
        return game_state
    
    snake = game_state["snake"]
    direction = game_state["direction"]
    
    # New head position
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    
    # Check for collisions
    if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or
        new_head[1] < 0 or new_head[1] >= GRID_SIZE or
        new_head in snake):
        game_state["game_over"] = True
        return game_state
    
    # Check for food
    if new_head == game_state["food"]:
        snake.insert(0, new_head)  # Grow snake
        game_state["score"] += 1
        # Generate new food
        while True:
            new_food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            if new_food not in snake:
                game_state["food"] = new_food
                break
    else:
        snake.insert(0, new_head)  # Move snake
        snake.pop()  # Remove the tail
    
    game_state["snake"] = snake
    return game_state

# Streamlit app
def main():
    st.title("Snake Game")
    st.markdown("Use the dropdown to control the snake.")

    game_state = init_game()

    # Game loop
    while not game_state["game_over"]:
        grid = draw_grid(game_state)
        
        # Display the grid using matplotlib
        plt.imshow(grid)
        plt.axis('off')  # Hide axes
        st.pyplot(plt)

        # Get user input for direction
        direction = st.selectbox("Direction", ["Up", "Down", "Left", "Right"], index=1)
        if direction == "Up":
            game_state["direction"] = (-1, 0)
        elif direction == "Down":
            game_state["direction"] = (1, 0)
        elif direction == "Left":
            game_state["direction"] = (0, -1)
        elif direction == "Right":
            game_state["direction"] = (0, 1)

        game_state = update_game(game_state)
        st.text(f"Score: {game_state['score']}")

        time.sleep(0.1)  # Control game speed

    st.text("Game Over! Final Score: " + str(game_state["score"]))

if __name__ == "__main__":
    main()
