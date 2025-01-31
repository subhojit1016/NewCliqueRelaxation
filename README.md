# Column Generation with Branch-and-Cut Approach
Column generation iteratively finds feasible solutions by adding new columns (node subsets) based on dual variables.

# Steps:

1. Initial Feasible Solution: Start with singleton sets (each node as its own column).
2. Solve the Restricted Master Problem (RMP): Using Linear Programming (LP) via PuLP, maximizing the number of selected columns.
3. Column Generation Step: Identify new columns to improve the solution.
4. Branch-and-Cut:
  a. If the solution contains fractional values, apply branching (forcing variables to 0 or 1).
  b. Generate valid cutting planes to improve the formulation.
  c. Repeat Until Optimal Solution is Found.
5. Final Results:
   a. The maximum s-stable set size was computed for various graph sizes (n) and probabilities (p).
