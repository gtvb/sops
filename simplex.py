class SimplexSolver:
    def __init__(self, objective_function_data, restrictions_data, deltas):
        self.restrictions_data = restrictions_data
        self.objective_function_data = objective_function_data

        self.deltas = deltas
        self.deltas_are_viable = True
        self.viability_results = []

        self.auxiliary_variables_len = len(restrictions_data)
        self.base_labels = ["Aux" + str(label) for label in range(self.auxiliary_variables_len)]
        self.non_base_labels = [label for label in objective_function_data.keys()] + self.base_labels

        self.shadow_prices = []
        self.optimal_points = []
        self.profit = 0

        self.simplex_matrix = self.build_simplex_matrix_from_data();

        self.pivot_col = -1
        self.pivot_row = -1

    # Aplica os passos necessários para criar uma tabela simplex.
    # Continua no processo até que os coeficientes da função objetivo 
    # sejam não-negativos.
    def solve(self):
        slice = self.find_obj_func_slice()
        while min(slice) < 0:
            self.update_pivot_col();
            self.update_pivot_row();

            # Mudar a base
            tmp = self.non_base_labels[self.pivot_col]
            self.non_base_labels[self.pivot_col] = self.base_labels[self.pivot_row - 1]
            self.base_labels[self.pivot_row - 1] = tmp

            self.update_pivot_line();
            self.update_lines();

            slice = self.find_obj_func_slice()

        self.find_profit()
        self.find_optimal_points()
        self.find_shadow_prices()

        self.calculate_viability()

    def calculate_viability(self):
        for i in range(1, len(self.simplex_matrix)):
            viability_result = 0

            reversed = self.simplex_matrix[i][::-1]
            coefficients = reversed[1:1+self.auxiliary_variables_len]
            coefficients.reverse()

            for j in range(self.auxiliary_variables_len):
                viability_result += (self.deltas[j] * coefficients[j])
            viability_result += reversed[0]

            self.viability_results.append(viability_result)
            if viability_result >= 0:
                continue

            self.deltas_are_viable = False

    def find_shadow_prices(self):
        reversed = self.simplex_matrix[0][::-1]
        coefficients = reversed[1:1+self.auxiliary_variables_len]
        coefficients.reverse()
        for i in range(len(coefficients)):
            self.shadow_prices.append((self.restrictions_data[i]["name"], coefficients[i]))

    def find_optimal_points(self):
        for i in range(1, len(self.simplex_matrix)):
            if "Aux" in self.base_labels[i - 1]:
                continue
            self.optimal_points.append((self.base_labels[i - 1], self.simplex_matrix[i][-1]))

        # ordenar por ordem alfabética da variável
        self.optimal_points.sort(key=lambda p:p[0])

    def find_profit(self):
        self.profit = self.simplex_matrix[0][-1]

    # Função utilitária para obter os valores da função objetivo
    def find_obj_func_slice(self):
        return self.simplex_matrix[0][:len(self.simplex_matrix[0]) - self.auxiliary_variables_len - 1]

    # Atualiza os valores das outras linhas do quadro baseado 
    # na nova linha de referência.
    def update_lines(self):
        for i in range(len(self.simplex_matrix)):
            if i == self.pivot_row:
                continue

            current_col = self.simplex_matrix[i]
            multiplier = self.simplex_matrix[i][self.pivot_col]
            for j, old_value in enumerate(current_col):
                new_value = old_value - multiplier * self.simplex_matrix[self.pivot_row][j]
                self.simplex_matrix[i][j] = new_value


    # Atualiza a linha do pivô para obter a nova linha de referência
    def update_pivot_line(self):
        pivot_value = self.simplex_matrix[self.pivot_row][self.pivot_col];
        for i, old_value in enumerate(self.simplex_matrix[self.pivot_row]):
            new_value = old_value / pivot_value
            self.simplex_matrix[self.pivot_row][i] = new_value

    def update_pivot_col(self):
        slice = self.find_obj_func_slice()
        self.pivot_col = slice.index(min(slice))

    def update_pivot_row(self):
        min_val, min_index = 999, -1
        for i in range(1, self.auxiliary_variables_len + 1):
            dividend = self.simplex_matrix[i][-1]
            divisor = self.simplex_matrix[i][self.pivot_col]
            if divisor == 0:
                continue

            res = dividend / divisor 

            if res < min_val:
                min_val = res
                min_index = i

        self.pivot_row = min_index

    # Essa função constrói uma matriz 2d contendo as informações necessárias para resolução
    # do problema.
    def build_simplex_matrix_from_data(self):
        matrix = []
        objective_line = []

        # Adicionar os coeficientes de lucro
        for value in self.objective_function_data.values():
            objective_line.append(-value)

        # Adicionar os valores das colunas de variáveis auxiliares
        for _ in range(self.auxiliary_variables_len):
            objective_line.append(0.0)

        # Adicionar o valor do lado direito
        objective_line.append(0.0)

        matrix.append(objective_line)

        # Inserir as linhas de restrições
        for i in range(self.auxiliary_variables_len):
            quantities = [v for v in self.restrictions_data[i]["quantities"].values()]
            # Variáveis auxiliares e lado direito
            aux = [0.0 for _ in range(self.auxiliary_variables_len + 1)]

            aux[i] = 1.0
            aux[-1] = self.restrictions_data[i]["max"]

            matrix.append(quantities + aux)

        return matrix
