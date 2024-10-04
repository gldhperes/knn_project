# K-NN Project
K-NN Project é um projeto baseado no algoritmo de filtragem colaborativa chamado "K-Nearest Neighbors" (K-NN) e em tradução livre "K vizinhos mais próximos".
(EXPLICAR OQUE É K-NN)

## Objetivo
Um algoritimo que preve a nota de um novo aluno no ENEM. A previsão são baseadas nas notas e nas características dos alunos que participaram do exame em anos anteriores.
#### Importante resaltar que para simplificar o projeto e por questões de precificação em servidores, decidi deixar o projeto rodando localmente.

## Modo de criação 
Usando Python juntamente com as bibliotecas scikit-learn para o uso do K-NN e pandas para a a leitura dos dados. Para o frontend, o framework Django, proporcionando uma interface interativa.

## Base de dados pública
Os *Microdados do ENEM* estao disponiveis no site do INEP, pelo link: _https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem_
#### Em especifico usei somente a tabela de 2023.

## Atributos Relevantes:
Os seguintes atributos dos microdados do ENEM serão utilizados para a previsão:
- Notas nas Áreas do Conhecimento:
  - Nota em Matemática e suas Tecnologias (NU_NOTA_MT)
  - Nota em Ciências da Natureza e suas Tecnologias (NU_NOTA_CN)
  - Nota em Linguagens, Códigos e suas Tecnologias (NU_NOTA_LC)
  - Nota em Ciências Humanas e suas Tecnologias (NU_NOTA_CH)
  - Nota da Redação (NU_NOTA_RED)

- Informações Socioeconômicas:
  - Renda Familiar (Q006)
  - Escolaridade da Mãe (Q002)
  - Tipo de Escola (Pública ou Privada) (TP_ESCOLA)
  - Raça/Cor (TP_COR_RACA)
  - Localidade:
  - Estado (SG_UF_RESIDENCIA)
  - Município (CO_MUNICIPIO_RESIDENCIA)

# Preparação dos dados
## Extraindo os dados
Por ter uma base de dados relativamente grande e questoes de performance, foi feito um script (extração_de_dados.py) que, como saida, gere um novo arquivo .csv juntando somente as colunas necessárias para o algoritmo do K-NN agir.

```python
import pandas as pd

# Caminho para o arquivo .csv
arquivo_csv = '../MICRODADOS_ENEM_2023.csv' 

# Carrega os dados do arquivo CSV, especificando o separador como ';'
dados = pd.read_csv(arquivo_csv, encoding='latin1', sep=';')

# Colunas de interesse
colunas_notas = [
    'NU_NOTA_MT',     # Nota em Matemática e suas Tecnologias
    'NU_NOTA_CN',     # Nota em Ciências da Natureza e suas Tecnologias
    'NU_NOTA_LC',     # Nota em Linguagens, Códigos e suas Tecnologias
    'NU_NOTA_CH',     # Nota em Ciências Humanas e suas Tecnologias
    'NU_NOTA_REDACAO' # Nota da Redação (ajustado para o nome correto)
]

colunas_socioeconomicas = [
    'Q006',           # Renda Familiar
    'Q002',           # Escolaridade da Mãe
    'TP_ESCOLA',      # Tipo de Escola (Pública ou Privada)
    'TP_COR_RACA'     # Raça/Cor
]

colunas_localidade = [
    'SG_UF_PROVA',           # Estado
    'CO_MUNICIPIO_PROVA'     # Município
]

# Exibe as colunas agrupadas
print("\nNotas nas Áreas do Conhecimento: \n")
print(dados[colunas_notas])  # Mostra as primeiras linhas das notas

print("Informações Socioeconômicas: \n")
print(dados[colunas_socioeconomicas])  # Mostra as primeiras linhas das informações socioeconômicas

print("Localidade: \n")
print(dados[colunas_localidade])  # Mostra as primeiras linhas da localidade

# Juntando todas as colunas de interesse em um novo DataFrame
dados_combinados = dados[colunas_notas + colunas_socioeconomicas + colunas_localidade]

# Exportando para um novo arquivo CSV
dados_combinados.to_csv('dados_combinados.csv', index=False, encoding='latin1')
```


### O arquivo gerado "dados_combinados.csv" foi posta na pasta de caminho "knn_app/knn_model" juntamente com o arquivo "knn.py"

# Implementação do algoritmo e desenvolvimento da interface
### Como o objetivo da documentação é falar sobre o algortimo do trabalho, não entrarei em meritos de como fazer um projeto Django, assim como HTML e CSS.

No caminho "knn_app/knn_model" estará o arquivo "knn.py"

```python
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np


class KNN:

    def __init__(self, novo_aluno):
        # 1) importação da tabela
        self.dados = pd.read_csv("./knn_app/knn_model/dados_combinados.csv")

        # 2)Colunas para prever
        # Colunas de notas para prever
        self.notas = ['NU_NOTA_MT', 'NU_NOTA_CN',
                      'NU_NOTA_LC', 'NU_NOTA_CH', 'NU_NOTA_REDACAO']

        # Colunas de características
        self.caracteristicas = ['Q002', 'Q006', 'TP_ESCOLA',
                                'TP_COR_RACA', 'SG_UF_PROVA', 'CO_MUNICIPIO_PROVA']

        # 2.1) Separar os dados em características e rótulos
        self.X = self.dados[self.caracteristicas]
        self.y = self.dados[self.notas]

        # Dicionário para armazenar os LabelEncoders de cada coluna
        self.le_dict = {}

        for coluna in self.caracteristicas:
            le = LabelEncoder()
            self.X.loc[:, coluna] = le.fit_transform(
                self.X[coluna].astype(str))  # Fit e transform no treino

            # Armazena o LabelEncoder correspondente para cada coluna
            self.le_dict[coluna] = le

        # 3) Preencher valores NaN com 0
        self.X = self.X.fillna(0)
        self.y = self.y.fillna(0)

        # print(self.X)

        # 4) Dividir os dados em conjuntos de treinamento e teste
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42)

        # 5) Criar o modelo KNN Regressor
        n_neighbors = 10
        self.knn = KNeighborsRegressor(n_neighbors=n_neighbors)

        # 5.1) Ajusta o modelo com os dados treinados
        self.knn.fit(self.X_train, self.y_train)

        # 6) Previsão para um novo aluno
        self.novo_aluno = novo_aluno

        # print("novo aluno:", self.novo_aluno)

        for coluna in self.caracteristicas:
            self.novo_aluno[coluna] = self.le_dict[coluna].transform(
                self.novo_aluno[coluna].astype(str))

        # Preencher valores NaN com 0
        self.novo_aluno = self.novo_aluno.fillna(0)

        # print("novo aluno depois do ajuste:", self.novo_aluno)

        # 7) Encontrar os n-alunos mais similares (vizinhos)
        self.distancias, self.indices = self.knn.kneighbors(
            self.novo_aluno, n_neighbors=n_neighbors)

        # 7.1) Mostrar os n-vizinhos mais próximos
        self.vizinhos_similares = self.X_train.iloc[self.indices[0]]
        self.notas_vizinhos = self.y_train.iloc[self.indices[0]]

        # 8) Prever as notas para o novo aluno
        self.notas_preditas = self.knn.predict(self.novo_aluno)

        # 8.1) Arredondar as notas previstas para 2 casas decimais
        self.notas_preditas = np.round(self.notas_preditas, 2)

        # 9) Função que calcula a melhor recomendação de estudo para o estudante
        self.best_recommendation = self.define_best_recommendation(
            self.notas_preditas[0], self.notas_vizinhos)

        # 10) Atribuição dos valores a serem retornados
        self.nota_MT = self.notas_preditas[0][0]
        self.nota_CN = self.notas_preditas[0][1]
        self.nota_LC = self.notas_preditas[0][2]
        self.nota_CH = self.notas_preditas[0][3]
        self.nota_RED = self.notas_preditas[0][4]

        # print(f"\nNotas previstas MT: {self.nota_MT}")


    def define_best_recommendation(self, notas_preditas, notas_vizinhos):
        media_mt = self.get_nota(notas_vizinhos["NU_NOTA_MT"])
        media_cn = self.get_nota(notas_vizinhos["NU_NOTA_CN"])
        media_lc = self.get_nota(notas_vizinhos["NU_NOTA_LC"])
        media_ch = self.get_nota(notas_vizinhos["NU_NOTA_CH"])
        media_red = self.get_nota(notas_vizinhos["NU_NOTA_REDACAO"])

        mt = round(abs(notas_preditas[0] - media_mt), 2)
        cn = round(abs(notas_preditas[1] - media_cn), 2)
        lc = round(abs(notas_preditas[2] - media_lc), 2)
        ch = round(abs(notas_preditas[3] - media_ch), 2)
        red = round(abs(notas_preditas[4] - media_red), 2)

        notas = [mt, cn, lc, ch, red]

        materia = [
            "matematica",
            "ciencias da natureza",
            "linguagens e codigos",
            "ciencias humanas",
            "redação"
        ]

        # print("notas:", notas)

        # Retorna o nome da materia por meio do mesmo indice da nota com maior "desfoque"
        max_nota = materia[notas.index(max(notas))]

        # print("max_notas:", max_notas)
        return max_nota

    def get_nota(self, notas_array):
        for nv in notas_array:
            if nv != 0:
                return nv


```

Explicação:
- 1. Inicialização e Importação dos Dados
O algoritmo começa carregando um arquivo CSV com dados de alunos, incluindo suas características e notas. As colunas de características são, por exemplo, o tipo de escola, a raça, e o estado de prova. As notas a serem previstas são de disciplinas como matemática, ciências, linguagens e redação.
- 2. Pré-processamento
Separação de Características e Rótulos: As colunas de características (self.caracteristicas) são usadas para prever as notas, enquanto as colunas de notas (self.notas) são os valores que se quer prever.
LabelEncoder: Para as colunas de características, que são categóricas, o LabelEncoder transforma os valores categóricos (por exemplo, tipos de escola) em números, pois o algoritmo KNN não funciona diretamente com strings.
Preenchimento de Valores Faltantes: Qualquer valor NaN (faltante) é substituído por 0, para evitar problemas na modelagem.
- 3. Divisão dos Dados
Os dados são divididos em dois conjuntos: um de treino (self.X_train, self.y_train) e outro de teste (self.X_test, self.y_test), com 80% dos dados para treino e 20% para teste. Isso permite avaliar a performance do modelo em dados que ele não viu antes.
- 4. Treinamento do Modelo K-NN
Um modelo de regressão KNN é criado com 10 vizinhos mais próximos (n_neighbors = 10), que será responsável por prever as notas com base nos vizinhos mais similares do novo aluno. O modelo é treinado com os dados de treino.
- 5. Previsão para Novo Aluno
O novo aluno é passado como um parâmetro (novo_aluno), contendo as características nas mesmas colunas do conjunto de dados.
Essas características são também transformadas usando os mesmos LabelEncoders para garantir a compatibilidade.
O modelo encontra os 10 alunos mais próximos (vizinhos) no conjunto de treino e usa esses vizinhos para prever as notas do novo aluno.
- 6. Cálculo das Notas Previstas
As notas do novo aluno são previstas usando os vizinhos mais próximos, e elas são arredondadas para duas casas decimais.
- 7. Recomendação de Estudo
A função define_best_recommendation calcula a diferença entre as notas previstas do novo aluno e a média das notas dos vizinhos para cada disciplina.
A disciplina com a maior diferença é identificada, e o algoritmo sugere que o aluno precisa focar mais naquela matéria. Isso é feito para ajudar o aluno a saber onde ele precisa melhorar.
- 8. Retorno das Notas
As notas previstas para cada disciplina (Matemática, Ciências da Natureza, Linguagens e Códigos, Ciências Humanas e Redação) são armazenadas em variáveis (self.nota_MT, self.nota_CN, etc.) e podem ser acessadas fora da classe.

