from simplex import SimplexSolver


obj ={ "a": 5.0, "b": 7.0, "c": 8.0 }
rest = [ 
    { 
      "name": "Resource 1",
      "quantities": { "a": 1.0, "b": 1.0, "c": 2.0 },
      "max": 1190.0
    },
    { 
      "name": "Resource 2",
      "quantities": { "a": 3.0, "b": 4.5, "c": 1.0 },
      "max": 4000.0
    }
]

simplex = SimplexSolver(obj, rest)
simplex.solve()
