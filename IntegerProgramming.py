import pulp
import networkx as nx
import csv

def create_initial_columns(G, s):
    """ Create initial feasible columns based on simple node inclusion criteria. """
    initial_columns = [{node} for node in G.nodes()]
    return initial_columns

def solve_rmp(G, columns):
    """ Solve the Restricted Master Problem (RMP) using current columns. """
    prob = pulp.LpProblem("Max_s_Stable_Set", pulp.LpMaximize)
    column_vars = pulp.LpVariable.dicts("Column", range(len(columns)), cat='Binary')
    
    # Objective: Maximize the sum of selected columns
    prob += pulp.lpSum(column_vars[i] for i in range(len(columns)))
    
    # Constraint: Each node can only be in one column at most
    for node in G.nodes():
        prob += pulp.lpSum(column_vars[i] for i, col in enumerate(columns) if node in col) <= 1
    
    prob.solve()
    return prob, column_vars

def column_generation(G, s):
    """ Perform column generation to iteratively find and add new columns. """
    columns = create_initial_columns(G, s)
    prob, column_vars = solve_rmp(G, columns)
    
    while True:
        # Placeholder: Solve the pricing problem to find new columns
        new_columns = []  # Assume function to find new columns based on dual values
        if not new_columns:
            break
        columns.extend(new_columns)
        prob, column_vars = solve_rmp(G, columns)

    return columns, column_vars

def branch_and_cut(G, s):
    """ Integrate branch and cut within the column generation framework. """
    columns, column_vars = column_generation(G, s)
    solutions = []

    def branch_on_column(column_index):
        # Create branches based on the fractional values of column variables
        for value in (0, 1):
            prob = pulp.LpProblem("Branch", pulp.LpMaximize)
            column_vars[column_index].setInitialValue(value)
            column_vars[column_index].fixValue()
            prob.solve()
            if prob.status == 1:  # If the problem is still feasible
                solutions.append(prob.objective.value())
                # Further branching and cut generation here

    for i, var in enumerate(column_vars.values()):
        if var.varValue not in (0, 1):
            branch_on_column(i)
            break

    return max(solutions) if solutions else None

# Example usage with a simple graph
nodes = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115, 125, 135, 145, 155, 165, 175, 185, 195, 205]
prob = [0.25, 0.35, 0.45, 0.50, 0.60, 0.70, 0.80, 0.90]

final_val=[]
for i in range(len(nodes)):
    n = nodes[i] 
    val=[]
    for j in range(len(prob)):
        # Number of vertices
        p = prob[j]  # Example probability
        s = 2    # Example s value for s-stable property

# Generate a random graph
        G = nx.erdos_renyi_graph(n, p)
       

# Find the maximum s-stable set using the RDS algorithm
        max_stable_set_size = branch_and_cut(G, s)
        
        val.append(len(max_stable_set_size))
        #print(f"Vertices in the maximum s-stable set: {max_s_stable_set}")
    final_val.append(val)
    
filename = 'BC.csv'

# Open the file in write mode
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write all rows at once
    writer.writerows(final_val)

print(f"Data has been written to {filename}")

G = nx.erdos_renyi_graph(100, 0.5)
s = 2  # Define the s-stability number
max_stable_set_size = branch_and_cut(G, s)
print("Maximum s-stable set size:", max_stable_set_size)

def generate_graph(n, p):
    """Generate a random graph based on the G(n, p) model."""
    return nx.erdos_renyi_graph(n, p)

def plot_graph(G):
    """Plot the graph with nodes labeled and clearly visible."""
    plt.figure(figsize=(12, 8))  # Set the figure size
    pos = nx.spring_layout(G, seed=42)  # For consistent layout between runs
    nx.draw_networkx(G, pos, with_labels=True, node_color='skyblue', node_size=500,
            edge_color='gray', linewidths=1, font_size=15,
            font_color='darkred')
    plt.title("Graph Visualization")
    plt.show()


def is_s_stable(S, G, s):
    """Check if the extended set S' = S + {v} is s-stable."""
    # Adding one vertex v to S and checking the stability
    def check_s_stability(S, v):
        non_neighbors = {u for u in S if not G.has_edge(u, v)}
        if len(non_neighbors) >= s + 1:
            return False
        return True

    # Check every vertex addition to S
    for v in S:
        if not check_s_stability(S, v):
            return False
    return True

def rds_algorithm(G, s):
    """Russian Doll Search to find the maximum s-stable set."""
    def find_max_s_stable(C, P):
        if not C:
            return set(P)
        max_set = set(P)
        for v in list(C):
            if is_s_stable(P + [v], G, s):
                C_new = [u for u in C if u != v and G.has_edge(u, v)]
                candidate_set = find_max_s_stable(C_new, P + [v])
                if len(candidate_set) > len(max_set):
                    max_set = candidate_set
        return max_set

    vertices = list(G.nodes())
    max_s_stable_set = set()
    for i in range(len(vertices)):
        C = [v for v in vertices if v != vertices[i]]
        candidate_set = find_max_s_stable(C, [vertices[i]])
        if len(candidate_set) > len(max_s_stable_set):
            max_s_stable_set = candidate_set
    return max_s_stable_set

# Test the algorithm

nodes = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
prob = [0.25, 0.35, 0.45, 0.50]

final_val=[]
for i in range(len(nodes)):
    n = nodes[i] 
    val=[]
    for j in range(len(prob)):
        # Number of vertices
        p = prob[j]  # Example probability
        s = 2    # Example s value for s-stable property

# Generate a random graph
        G = nx.erdos_renyi_graph(n, p)
        plot_graph(G)

# Find the maximum s-stable set using the RDS algorithm
        max_s_stable_set = rds_algorithm(G, s)
        print(f"Maximum s-stable set size: {len(max_s_stable_set)}")
        val.append(len(max_s_stable_set))
        #print(f"Vertices in the maximum s-stable set: {max_s_stable_set}")
    final_val.append(val)
    
filename = 'A2.csv'

# Open the file in write mode
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    # Write all rows at once
    writer.writerows(final_val)

print(f"Data has been written to {filename}")
