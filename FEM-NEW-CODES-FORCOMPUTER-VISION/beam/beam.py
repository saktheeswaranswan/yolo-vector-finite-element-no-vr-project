import numpy as np
import pandas as pd

def beam_element_stiffness(E, I, L):
    """Generate stiffness matrix for a beam element."""
    k = (E * I / L**3) * np.array([
        [12, 6*L, -12, 6*L],
        [6*L, 4*L**2, -6*L, 2*L**2],
        [-12, -6*L, 12, -6*L],
        [6*L, 2*L**2, -6*L, 4*L**2]
    ])
    return k

def assemble_global_stiffness(n_elements, E, I, L):
    """Assemble global stiffness matrix."""
    dof = 2 * (n_elements + 1)
    K_global = np.zeros((dof, dof))
    
    for i in range(n_elements):
        k = beam_element_stiffness(E, I, L)
        indices = [2*i, 2*i+1, 2*i+2, 2*i+3]
        for a in range(4):
            for b in range(4):
                K_global[indices[a], indices[b]] += k[a, b]
    
    return K_global

def apply_boundary_conditions(K_global):
    """Modify stiffness matrix for simply supported beam."""
    K_mod = K_global.copy()
    K_mod[0, :] = K_mod[:, 0] = 0
    K_mod[-2, :] = K_mod[:, -2] = 0
    K_mod[0, 0] = K_mod[-2, -2] = 1
    return K_mod

def apply_loads(n_nodes, loads):
    """Apply point loads at specific nodes."""
    F = np.zeros(2 * n_nodes)
    for node, force in loads:
        F[2 * node] = force
    return F

def solve_displacements(K_mod, F):
    """Solve for displacements."""
    displacements = np.linalg.solve(K_mod, F)
    return displacements

def compute_reactions(K_global, displacements):
    """Compute reaction forces."""
    reactions = np.dot(K_global, displacements)
    return reactions

def export_to_csv(K_global, K_elements, reactions, displacements, filename_prefix="output"):
    """Export matrices and results to CSV files."""
    pd.DataFrame(K_global).to_csv(f"{filename_prefix}_global_stiffness.csv", index=False, header=False)
    pd.DataFrame(reactions).to_csv(f"{filename_prefix}_reactions.csv", index=False, header=False)
    pd.DataFrame(displacements).to_csv(f"{filename_prefix}_displacements.csv", index=False, header=False)
    for i, k in enumerate(K_elements):
        pd.DataFrame(k).to_csv(f"{filename_prefix}_element_{i+1}_stiffness.csv", index=False, header=False)

def main():
    n_elements = 5  # Number of beam elements
    L = 5.0  # Length of each element
    E = 200e9  # Young's modulus (Pa)
    I = 0.0001  # Moment of inertia (m^4)
    n_nodes = n_elements + 1
    
    # Define point loads as (node_index, force in N)
    loads = [(1, -500), (2, -1000), (3, -1500), (4, -2000), (5, -2500)]
    
    # Assemble matrices
    K_global = assemble_global_stiffness(n_elements, E, I, L)
    K_mod = apply_boundary_conditions(K_global)
    F = apply_loads(n_nodes, loads)
    
    # Solve for displacements and reactions
    displacements = solve_displacements(K_mod, F)
    reactions = compute_reactions(K_global, displacements)
    
    # Export results
    K_elements = [beam_element_stiffness(E, I, L) for _ in range(n_elements)]
    export_to_csv(K_global, K_elements, reactions, displacements)
    
    print("Analysis complete. Results exported to CSV files.")

if __name__ == "__main__":
    main()
