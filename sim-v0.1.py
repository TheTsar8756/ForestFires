import argparse
import numpy as np
from matplotlib.colors import ListedColormap
 
"""
Forest fire on a 100x100 lattice.
States: 0=unburnt (green), 1=burning (red), 2=burnt (black).
Start: single burning tree at center.
Usage: python3 Untitled-1.py --p 0.6 --steps 20
"""
import matplotlib.pyplot as plt
 
def simulate_forest_fire_wind(size, p, steps, wind_p):
    # Grid of trees
    grid = np.zeros((size, size), dtype=np.uint8)
    # Unit vector of wind, not implemented yet
    wind = np.zeros((size,size), dtype=(np.float16, np.float16))

    # Set center
    center = size // 2
    grid[center, center] = 1  
    # center burning

    for _ in range(steps):
        new = grid.copy()
        burning = np.argwhere(grid == 1)
        for i, j in burning:
            # For loop across the four vert
            for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):  # 4-neighborhood
                # Add vert to the current position
                ni, nj = i + di, j + dj
                # Check if within bounds
                if 0 <= ni < size and 0 <= nj < size and grid[ni, nj] == 0:
                    # Check probability
                    if np.random.rand() < p:
                        new[ni, nj] = 1
                        # if probability less than chance to be set on fire then set to burnt
            new[i, j] = 2  # burning -> burnt
        grid = new
    return grid

def simulate_forest_fire(size, p, steps):
    # Grid of trees
    grid = np.zeros((size, size), dtype=np.uint8)

    # Set center
    center = size // 2
    grid[center, center] = 1  
    # center burning

    for _ in range(steps):
        new = grid.copy()
        burning = np.argwhere(grid == 1)
        for i, j in burning:
            # For loop across the four vert
            for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):  # 4-neighborhood
                # Add vert to the current position
                ni, nj = i + di, j + dj
                # Check if within bounds
                if 0 <= ni < size and 0 <= nj < size and grid[ni, nj] == 0:
                    # Check probability
                    if np.random.rand() < p:
                        new[ni, nj] = 1
                        # if probability less than chance to be set on fire then set to burnt
            new[i, j] = 2  # burning -> burnt
        grid = new
    return grid
 
def show_grid(grid, p, steps):
    cmap = ListedColormap(['#2ecc71', '#e74c3c', '#2d3436'])  # green, red, black
    plt.figure(figsize=(6,6))
    plt.imshow(grid, cmap=cmap, vmin=0, vmax=2)
    plt.title(f'Forest fire at time {steps} (p={p})')
    plt.axis('off')
    plt.show()
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=100)
    parser.add_argument('--p', type=float, default=0.8, help='transmission probability')
    parser.add_argument('--steps', type=int, default=100, help='time steps to simulate')
    parser.add_argument('--wind_p', type=float, default=1.0, help='percent wind reduces transmission')
    args = parser.parse_args()
 
    final = simulate_forest_fire_wind(args.size, args.p, args.steps, args.wind_p)
    show_grid(final, args.p, args.steps)