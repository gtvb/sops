## Solucionador de problemas por Simplex

Esse programa oferece uma interface de simples uso para a solução de problemas de Programação Linear.
Utiliza apenas uma dependência para mostrar os resultados no terminal ([rich](https://github.com/Textualize/rich)). 
Todo o resto é implementado com os recursos nativos da linguagem.

### Como executar

Para testar localmente, siga os seguintes passos:

- Clone o repositório: `git clone https://github.com/gtvb/sops.git`
- Acesse a pasta em seu ambiente: `cd <DIRETÓRIO>`

Eu indico a criação de um ambiente virtual para manter os projetos Python isolados.

- Para criar e ativar um ambiente virtual: 
```bash
python -m venv .venv # Cria um ambiente com o nome '.venv'

# Para ativar no Windows
.venv\Scripts\activate

# Para ativar no Mac e Linux
source .venv/bin/activate
```

Com o ambiente ativado, instale a dependência: `pip install -r requirements.txt`.

### Como utilizar

Se quiser inserir seus próprios dados dos começo, basta executar `python main.py`.
O arquivo `example_problems.json` contém dois exemplos simples que ajudam a visualizar 
os resultados sem precisar inserir todos os dados do zero. Para utilizá-lo, basta 
executar: `python main.py example <n>`, onde n é o índice do exemplo (como existem
apenas 2 exemplos, os índices são 0 e 1).

### Exemplo de resultado
Executando: `python main.py example 0`:

![Exemplo 0](/assets/example_0.png "Exemplo 0")

Executando: `python main.py example 1`:

![Exemplo 1](/assets/example_1.png "Exemplo 1")
