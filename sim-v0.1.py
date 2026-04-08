import argparse
import numpy as np
import math
import collections
from matplotlib.colors import ListedColormap
from matplotlib.widgets import Button
 
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
    # Vector of wind, not implemented yet
    wind = np.zeros((size,size), dtype=[('i', np.float16), ('j', np.float16)])

    # Set center
    center = size // 2
    grid[center, center] = 1  
    # center burning

    total_burning = []

    for _ in range(steps):
        new = grid.copy()
        burning = np.argwhere(grid == 1)

        # Get amount of burning every step
        total_burning.append(len(burning))

        for i, j in burning:
            # reference to the vector of wind at the point
            w_x, w_y = calc_wind(wind_p, wind, i, j)

            # For loop across the four vert
            for di, dj in ((1,0),(-1,0),(0,1),(0,-1)):  # 4-neighborhood
                # Add vert to the current position
                ni, nj = i + di, j + dj
                # Check if within bounds
                if 0 <= ni < size and 0 <= nj < size and grid[ni, nj] == 0:
                    # Check probability
                    # Would be way better to use the cosine of the dot product?
                    calc_p = p

                    if(w_x != 0.0):
                        if(di == 1):
                                calc_p += w_x
                        if(di == -1):
                                calc_p -= w_x
                        if(dj == 1):
                                calc_p += w_y
                        if(dj == -1):
                                calc_p -= w_y

                    if np.random.rand() < calc_p:
                        new[ni, nj] = 1
                        # if probability less than chance to be set on fire then set to burnt
            new[i, j] = 2  # burning -> burnt
        grid = new
    return grid, total_burning

def calc_wind(wind_p, wind, i, j):
    wind_ref = (0, -1)
    w_x = wind_p * wind_ref[0]
    w_y = wind_p * wind_ref[1]
    return w_x,w_y

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

# Runs simulation and sets new map on plot. Also takes in one variable because the button passes one in.
def show_map(val):
    print("Refreshing map")
    cmap = ListedColormap(['#2ecc71', '#e74c3c', '#2d3436'])
    grid, total_burning = simulate_forest_fire_wind(args.size, args.p, args.steps, args.wind_p)
    grid_ax.imshow(grid, cmap=cmap, vmin=0, vmax=2, origin = "lower")

def simulate_total(val):
    print("Simulating 100 times and saving")

    list_total = []

    for i in range(args.steps):
        grid, total_burning = simulate_forest_fire_wind(args.size, args.p, args.steps, args.wind_p)
        list_total.append(len(np.argwhere(grid == 2)))

    np.savetxt("total.csv", list_total, 
              delimiter = ",")
    
def simulate_total_burning(val):
    print("Simulating 100 times and saving")

    list_burning = []

    for i in range(100):
        grid, total_burning = simulate_forest_fire_wind(args.size, args.p, args.steps, args.wind_p)
        list_burning.append(total_burning)

    np.savetxt(f"total_burning-{args.p}.csv", list_burning, 
              delimiter = ",")

 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=100)
    parser.add_argument('--p', type=float, default=0.5, help='transmission probability')
    parser.add_argument('--steps', type=int, default=100, help='time steps to simulate')
    parser.add_argument('--wind_p', type=float, default=0.1, help='percent wind adds or reduces transmission probability')
    args = parser.parse_args()

    # Setup plot

    # Setup two plots so that buttons and grid are seperate
    fig_ax, grid_ax = plt.subplots()
    # grid_ax.set_figure(figsize=(6,6))

    grid_ax.set_title(f'Forest fire at time {args.steps} (p={args.p})')
    grid_ax.axis('off')
    
    # Run initial simulation
    show_map(0)
    # Set position for button
    bref_axes = fig_ax.add_axes([0.6, 0.05, 0.1, 0.075])
    bsim_axes = fig_ax.add_axes([0.71, 0.05, 0.1, 0.075])
    bcount_axes = fig_ax.add_axes([0.82, 0.05, 0.1, 0.075])

    brefresh = Button(bref_axes, 'New',color="gray")
    bsim = Button(bsim_axes, 'Sim',color="gray")
    bcount = Button(bcount_axes, 'Count',color="gray")

    brefresh.on_clicked(show_map)
    bsim.on_clicked(simulate_total)
    bcount.on_clicked(simulate_total_burning)

    plt.show()