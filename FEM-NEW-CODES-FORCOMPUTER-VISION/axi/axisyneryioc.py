import numpy as np
import matplotlib.pyplot as plt

def input_coordinates():
    """Gets node coordinates for the axisymmetric CST element."""
    nodes = []
    print("Enter the 3 node coordinates as x,y (or x y) format:")
    for i in range(3):
        while True:
            try:
                user_input = input(f"Node {i+1}: ").replace(',', ' ').split()
                x, y = float(user_input[0]), float(user_input[1])
                nodes.append((x, y))
                break
            except (ValueError, IndexError):
                print("Invalid input. Please enter two numbers separated by space or comma.")
    return np.array(nodes)

def compute_stiffness(nodes, E=200e9, nu=0.3, thickness=0.01):
    """Computes the stiffness matrix for the CST element."""
    x1, y1 = nodes[0]
    x2, y2 = nodes[1]
    x3, y3 = nodes[2]
    
    area = 0.5 * abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))
    
    if area == 0:
        raise ValueError("The nodes are collinear, making the element invalid.")
    
    B = np.array([
        [y2 - y3, y3 - y1, y1 - y2],
        [x3 - x2, x1 - x3, x2 - x1],
        [x3 - x2 + y2 - y3, x1 - x3 + y3 - y1, x2 - x1 + y1 - y2]
    ]) / (2 * area)
    
    D = (E / (1 - nu**2)) * np.array([
        [1, nu, 0],
        [nu, 1, 0],
        [0, 0, (1 - nu) / 2]
    ])
    
    stiffness = thickness * area * np.dot(np.dot(B.T, D), B)
    return stiffness

def plot_element(nodes):
    """Plots the CST element."""
    x_vals = np.append(nodes[:, 0], nodes[0, 0])
    y_vals = np.append(nodes[:, 1], nodes[0, 1])
    
    plt.figure()
    plt.fill(x_vals, y_vals, edgecolor='black', fill=False, linewidth=2)
    plt.scatter(nodes[:, 0], nodes[:, 1], color='red', zorder=3)
    
    for i, (x, y) in enumerate(nodes):
        plt.text(x, y, f'  N{i+1}', fontsize=12, verticalalignment='bottom')
    
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Axisymmetric CST Element")
    plt.grid(True, linestyle='--')
    plt.axis("equal")
    plt.show()

# Main Execution
if __name__ == "__main__":
    nodes = input_coordinates()
    stiffness_matrix = compute_stiffness(nodes)
    print("\nStiffness Matrix:")
    print(stiffness_matrix)
    plot_element(nodes)

