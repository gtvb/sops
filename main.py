from results import print_table
from simplex import SimplexSolver

def main():
    # (obj_funct_data, restrictions_data) = prompt_data()
    obj_funct_data = { "A": 5, "B": 7, "C": 8 }
    restrictions_data = [
        {
            "name": "Prensa",
            "quantities": { "A": 1, "B": 1, "C": 2 },
            "max": 1190
        },
        {
            "name": "Esmalte",
            "quantities": { "A": 3, "B": 4.5, "C": 1 },
            "max": 4000
        },
    ]

    solver = SimplexSolver(obj_funct_data, restrictions_data)
    solver.solve()
    print_table(solver)

if __name__ == "__main__":
    main()
