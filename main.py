from results import print_table, prompt_data
from simplex import SimplexSolver
import json, sys

def main():
    if len(sys.argv) == 3 and sys.argv[1] == "example":
        example_index = int(sys.argv[2])
        with open("example_problems.json") as f:
            problems = json.load(f)
            if example_index >= len(problems):
                print(f"O arquivo de exemplo contém apenas {len(problems)} problemas")
                return
            obj_funct_data = problems[example_index]["obj_funct_data"]
            restrictions_data = problems[example_index]["restrictions_data"]
            deltas = problems[example_index]["deltas"]

    else:
        (obj_funct_data, restrictions_data, deltas) = prompt_data()

    solver = SimplexSolver(obj_funct_data, restrictions_data, deltas)
    solver.solve()
    print_table(solver)

if __name__ == "__main__":
    main()
