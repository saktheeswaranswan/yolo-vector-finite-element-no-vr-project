import numpy as np
import csv

class FEMSolver:
    def __init__(self, n_elements=333, bar_length=1000, E=200000, A=25, poisson=0.3, load=1000):
        self.n_elements = n_elements
        self.bar_length = bar_length
        self.E = E
        self.A = A
        self.poisson = poisson
        self.load = load
        self.n_nodes = n_elements + 1
        self.nodes = np.linspace(0, bar_length, self.n_nodes)
        self.global_stiffness = np.zeros((self.n_nodes, self.n_nodes))
        self.full_force = np.zeros(self.n_nodes)
        self.mass_matrix = np.zeros((self.n_nodes, self.n_nodes))
        self.element_stiffness_matrices = []
        self.displacements = None
    
    def assemble_matrices(self):
        for i in range(self.n_elements):
            L = self.nodes[i + 1] - self.nodes[i]
            k = (self.E * self.A) / L
            m = (self.A * L) / 6
            
            k_matrix = np.array([[k, -k], [-k, k]])
            m_matrix = np.array([[2 * m, m], [m, 2 * m]])
            
            self.global_stiffness[i:i+2, i:i+2] += k_matrix
            self.mass_matrix[i:i+2, i:i+2] += m_matrix
            self.element_stiffness_matrices.append(k_matrix)
            
            self.full_force[i] += self.load / 2
            self.full_force[i + 1] += self.load / 2
        
        # Apply tip load of 1000N at the last node
        self.full_force[-1] += 1000
    
    def solve_displacements(self):
        self.displacements = np.linalg.solve(self.global_stiffness, self.full_force)
    
    def export_csv(self, filename, matrix):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for row in matrix:
                writer.writerow(row)
    
    def export_results(self):
        self.export_csv("global_stiffness.csv", self.global_stiffness)
        self.export_csv("mass_matrix.csv", self.mass_matrix)
        self.export_csv("displacements.csv", [self.displacements])
        self.export_csv("force_vector.csv", [self.full_force])
        
        for idx, k_matrix in enumerate(self.element_stiffness_matrices):
            self.export_csv(f"element_stiffness_{idx+1}.csv", k_matrix)
    
    def run(self):
        self.assemble_matrices()
        self.solve_displacements()
        self.export_results()
        print("FEM Analysis Completed. Results exported to CSV files.")

if __name__ == "__main__":
    solver = FEMSolver()
    solver.run()
