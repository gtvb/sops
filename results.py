from rich.table import Table
from rich.console import Console

from simplex import SimplexSolver

console = Console()

def prompt_data():
    console.clear()
    console.rule("Solucionador de PPL's por Simplex!")
    console.print("""
    Olá! Para resolver os [b]Problemas[/b] de [b]Programação Linear[/b], \
    basta fornecer as informações necessárias, sendo elas:
        - Coeficientes de Lucro/Custo e nome de cada variável do problema.
        - Restrições, com os recursos utilizados por cada variável e sua quantidade máxima (e o seu nome também).
        - Variações de restrições

    Aproveite!
    """)

    console.rule("Função Objetivo")
    num_vars = int(console.input("Quantas [b]variáveis de decisão[/b] nesse problema? "))

    obj_funct_data = {}
    for i in range(num_vars):
        if i == 0:
            var_name = console.input("[b]Nome da variável [u](ex: 'Motos')[/u]:[/b] ")
        else:
            var_name = console.input("[b]Nome da variável:[/b] ")
        factor = float(console.input("[b]Lucro/Custo por unidade:[/b] "))
        
        obj_funct_data[var_name] = factor
        console.print()

    console.print(obj_funct_data)

    console.rule("Restrições")
    num_restrictions = int(console.input("Quantas [b]restrições[/b] para esse problema? "))

    restrictions_data = []
    for i in range(num_restrictions):
        res_name = console.input("[b]Nome da restrição:[/b] ")
        quantities = {}
        for key in obj_funct_data.keys():
            factor = float(console.input(f"[b]> Quantidade utilizada da variável '{key}':[/b] "))
            quantities[key] = float(factor)
        
        max = float(console.input("[b]Quantidade máxima desse recurso:[/b] "))
        restrictions_data.append({ "name": res_name, "quantities": quantities, "max": max })

        console.print()

    console.print(restrictions_data)

    console.rule("Variações")
    deltas = []
    for r in restrictions_data:
        delta = float(console.input(f"[bold]> Variação no estoque de '{r['name']}' (Adicione '-' para remoção do estoque, e '+' para adição:[/bold] "))
        deltas.append(delta)
    console.print(deltas)
        
    console.rule("Resultados")
    console.input("[b]Para mostrar o resultado, digite qualquer coisa[/b] ")

    return (obj_funct_data, restrictions_data, deltas)


def print_table(simplex_obj: SimplexSolver):
    console.clear()
    table = Table(title=None, show_lines=True)

    table.add_column("VB", justify="center", style="cyan")
    for label in simplex_obj.non_base_labels:
        table.add_column(label, justify="center")
    table.add_column("LD", justify="center", style="green")

    row = []
    row.append("Z")
    for val in simplex_obj.simplex_matrix[0]:
        row.append(str(round(val, 3)))
    table.add_row(*row)

    for i in range(simplex_obj.auxiliary_variables_len):
        row = []
        row.append(simplex_obj.base_labels[i])
        for val in simplex_obj.simplex_matrix[i + 1]:
            row.append(str(round(val, 3)))
        table.add_row(*row)

    console.rule("Tabela Final")
    console.print(table)

    console.rule("Resultados")
    console.print(f"[b]Lucro:[/b] {simplex_obj.profit}")

    console.print("[b]Pontos ótimos:[/b]")
    for (name, value) in simplex_obj.optimal_points:
        console.print(f"[b]> {name}:[/b] {value}")

    console.print("[b]Preços-Sombra:[/b]")
    for (name, value) in simplex_obj.shadow_prices:
        console.print(f"[b]> {name}:[/b] {value}")
        
    console.rule("Análise de Viabilidade")
    v_table = Table(title=None, show_lines=True)

    v_table.add_column("Restrição", justify="center", style="cyan")
    v_table.add_column("Resultado", justify="center", style="white")
    for i in range(simplex_obj.auxiliary_variables_len):
        row = []
        row.append(simplex_obj.restrictions_data[i]["name"])
        row.append(str(round(simplex_obj.viability_results[i])))
        v_table.add_row(*row)

    console.print(v_table)
    console.print(f"[b]É viável:[/b] {simplex_obj.deltas_are_viable}")
    console.rule()
