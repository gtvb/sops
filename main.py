from results import print_table, prompt_data
from simplex import SimplexSolver

def main():
    # (obj_funct_data, restrictions_data, deltas) = prompt_data()
    obj_funct_data = { "E": 80, "M": 70, "A": 100, "P": 16 }
    restrictions_data = [
        {
            "name": "X1",
            "quantities": { "E": 1, "M": 1, "A": 1, "P": 4 },
            "max": 250
        },
        {
            "name": "X2",
            "quantities": { "E": 0, "M": 1, "A": 1, "P": 2 },
            "max": 600
        },
        {
            "name": "X3",
            "quantities": { "E": 3, "M": 2, "A": 4, "P": 0 },
            "max": 500
        },
    ]
    deltas = [250.0, 0.0, 0.0]

    solver = SimplexSolver(obj_funct_data, restrictions_data, deltas)
    solver.solve()
    print_table(solver)

if __name__ == "__main__":
    main()
