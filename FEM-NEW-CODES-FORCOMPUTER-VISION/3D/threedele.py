import numpy as np
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plot_tetrahedral_element(nodes, elements):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for elem in elements:
        tetra_nodes = np.array([nodes[i] for i in elem])
        faces = [
            [tetra_nodes[0], tetra_nodes[1], tetra_nodes[2]],
            [tetra_nodes[0], tetra_nodes[1], tetra_nodes[3]],
            [tetra_nodes[0], tetra_nodes[2], tetra_nodes[3]],
            [tetra_nodes[1], tetra_nodes[2], tetra_nodes[3]]
        ]
        ax.add_collection3d(Poly3DCollection(faces, alpha=0.5, edgecolor='k'))
    
    ax.scatter(*zip(*nodes), color='r', s=50)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

def export_stiffness_matrix(K, filename="stiffness_matrix.csv"):
    """Exports the stiffness matrix to a CSV file."""
    np.savetxt(filename, K, delimiter=",", fmt="%.6f")
    print(f"Stiffness matrix exported to {filename}")

# Example tetrahedral element
nodes = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]  # Four nodes forming a tetrahedron
elements = [(0, 1, 2, 3)]  # Single tetrahedral element

# Example stiffness matrix (Replace with actual computation)
K_example = np.random.rand(12, 12)  # 12x12 matrix for a single tetrahedral element

plot_tetrahedral_element(nodes, elements)
export_stiffness_matrix(K_example)

