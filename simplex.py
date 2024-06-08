class SimplexSolver:
    def __init__(self, objective_function_data, restrictions_data):
        self.auxiliary_variables_len = len(restrictions_data)
        self.base_labels = ["Aux" + str(label) for label in range(self.auxiliary_variables_len)]
        self.non_base_labels = [label for label in objective_function_data.keys()] + self.base_labels
        self.simplex_matrix = self.build_simplex_matrix_from_data(objective_function_data, restrictions_data);
        self.pivot_col = -1
        self.pivot_row = -1

    def solve(self):
        while min(self.simplex_matrix[0]) < 0:
            self.update_pivot_col();
            self.update_pivot_row();

            # Mudar a base
            tmp = self.non_base_labels[self.pivot_col]
            self.non_base_labels[self.pivot_col] = self.base_labels[self.pivot_row - 1]
            self.base_labels[self.pivot_row - 1] = tmp

            self.update_pivot_line();
            self.update_lines();

    def update_lines(self):
        indexes_to_update = [index for index in range(len(self.simplex_matrix)) if index is not self.pivot_row]
        all_factors = list(map(lambda row: -row[self.pivot_col], self.simplex_matrix))
        factors = [factor for i, factor in enumerate(all_factors) if i in indexes_to_update]

        for i, line_index in enumerate(indexes_to_update):
            for value_index, old_value in enumerate(self.simplex_matrix[line_index]):
                new_value = old_value + factors[i] * self.simplex_matrix[self.pivot_row][value_index]
                self.simplex_matrix[line_index][value_index] = new_value

    def update_pivot_line(self):
        pivot_value = self.simplex_matrix[self.pivot_row][self.pivot_col];
        for i, old_value in enumerate(self.simplex_matrix[self.pivot_row]):
            new_value = old_value / pivot_value
            self.simplex_matrix[self.pivot_row][i] = new_value

    def update_pivot_col(self):
        self.pivot_col = self.simplex_matrix[0].index(min(self.simplex_matrix[0]))

    def update_pivot_row(self):
        smallest_i = -1
        smallest_div = 9999
        for i in range(self.auxiliary_variables_len):
            div = self.simplex_matrix[i + 1][-1] / self.simplex_matrix[i + 1][self.pivot_col]
            if div < smallest_div:
                smallest_i = i + 1
                smallest_div = div

        self.pivot_row = smallest_i

    # Essa função constrói uma matriz 2d contendo as informações necessárias para resolução
    # do problema.
    def build_simplex_matrix_from_data(self, objective_function_data, restrictions_data):
        matrix = []
        objective_line = []

        # Adicionar os coeficientes de lucro
        for value in objective_function_data.values():
            objective_line.append(-value)

        # Adicionar os valores das colunas de variáveis auxiliares
        for _ in range(self.auxiliary_variables_len):
            objective_line.append(0.0)

        # Adicionar o valor do lado direito
        objective_line.append(0.0)

        matrix.append(objective_line)

        # Inserir as linhas de restrições
        for i in range(self.auxiliary_variables_len):
            quantities = [v for v in restrictions_data[i]["quantities"].values()]
            # Variáveis auxiliares e lado direito
            aux = [0.0 for _ in range(self.auxiliary_variables_len + 1)]

            aux[i] = 1.0
            aux[-1] = restrictions_data[i]["max"]

            matrix.append(quantities + aux)

        return matrix
