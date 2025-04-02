import numpy as np
import csv
import matplotlib.pyplot as plt
import re

def parse_input(prompt):
    """Handles various input formats and extracts two float values."""
    while True:
        user_input = input(prompt).strip()
        user_input = re.split(r'[,\s]+', user_input)  # Split by space or comma
        if len(user_input) == 2:
            try:
                return float(user_input[0]), float(user_input[1])
            except ValueError:
                pass
        print("Invalid input. Please enter two numbers separated by space or comma.")

def compute_stiffness(x, thickness, E, nu):
    """Computes the stiffness matrix for a single CST element."""
    
    C = (E / (1 - nu**2)) * np.array([
        [1, nu, 0],
        [nu, 1, 0],
        [0, 0, (1 - nu) / 2]
    ])

    x1, y1 = x[0]
    x2, y2 = x[1]
    x3, y3 = x[2]

    A = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

    B = (1 / (2 * A)) * np.array([
        [y2 - y3, 0, y3 - y1, 0, y1 - y2, 0],
        [0, x3 - x2, 0, x1 - x3, 0, x2 - x1],
        [x3 - x2, y2 - y3, x1 - x3, y3 - y1, x2 - x1, y1 - y2]
    ])

    K = thickness * A * np.dot(np.dot(B.T, C), B)
    return K

def save_stiffness_matrix(K, filename="stiffness_matrix.csv"):
    """Saves the stiffness matrix to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Stiffness Matrix"])
        for row in K:
            writer.writerow(row)
    print(f"Stiffness matrix saved to {filename}")

def plot_triangle(x):
    """Plots the CST element in a simple ASCII line diagram."""
    x1, y1 = x[0]
    x2, y2 = x[1]
    x3, y3 = x[2]

    plt.figure()
    plt.plot([x1, x2], [y1, y2], 'bo-')
    plt.plot([x2, x3], [y2, y3], 'bo-')
    plt.plot([x3, x1], [y3, y1], 'bo-')
    plt.scatter(*zip(*x), color='red', zorder=3)
    
    for i, (xi, yi) in enumerate(x, 1):
        plt.text(xi, yi, f"  {i}", fontsize=12, verticalalignment='bottom')

    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("CST Triangle Element")
    plt.grid(True)
    plt.axis("equal")
    plt.show()

# === User Input from Terminal ===
print("Enter coordinates of the three nodes (x y) separated by space or comma:")

x1, y1 = parse_input("Node 1: ")
x2, y2 = parse_input("Node 2: ")
x3, y3 = parse_input("Node 3: ")

x = np.array([[x1, y1], [x2, y2], [x3, y3]])

thickness = float(input("Enter thickness: "))
E = float(input("Enter Young's modulus (E): "))
nu = float(input("Enter Poisson's ratio (ν): "))

# === Compute Stiffness Matrix ===
K = compute_stiffness(x, thickness, E, nu)

# === Save and Plot ===
save_stiffness_matrix(K)
plot_triangle(x)

