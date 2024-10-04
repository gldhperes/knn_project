from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

class KNN:

    def __init__(self, novo_aluno):
        self.dados = pd.read_csv("./knn_app/knn_model/dados_combinados.csv")

        # Colunas de notas para prever
        self.notas = ['NU_NOTA_MT', 'NU_NOTA_CN',
                      'NU_NOTA_LC', 'NU_NOTA_CH', 'NU_NOTA_REDACAO']

        # Colunas de características
        self.caracteristicas = ['Q002', 'Q006', 'TP_ESCOLA',
                                'TP_COR_RACA', 'SG_UF_PROVA', 'CO_MUNICIPIO_PROVA']

        # Separar os dados em características e rótulos
        self.X = self.dados[self.caracteristicas]
        self.y = self.dados[self.notas]

        self.le_dict = {}  # Dicionário para armazenar os LabelEncoders de cada coluna

        for coluna in self.caracteristicas:
            le = LabelEncoder()
            self.X.loc[:, coluna] = le.fit_transform(
                self.X[coluna].astype(str))  # Fit e transform no treino
            # Armazena o LabelEncoder correspondente para cada coluna
            self.le_dict[coluna] = le

        # Preencher valores NaN com 0
        self.X = self.X.fillna(0)
        self.y = self.y.fillna(0)

        # print(self.X)

        # Dividir os dados em conjuntos de treinamento e teste
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42)

        # Criar o modelo KNN Regressor
        n_neighbors = 10
        self.knn = KNeighborsRegressor(n_neighbors=n_neighbors)

        self.knn.fit(self.X_train, self.y_train)

        # Previsão para um novo aluno
        self.novo_aluno = novo_aluno

        # print("novo aluno:", self.novo_aluno)

        for coluna in self.caracteristicas:
            self.novo_aluno[coluna] = self.le_dict[coluna].transform(
                self.novo_aluno[coluna].astype(str))

        # Preencher valores NaN com 0
        self.novo_aluno = self.novo_aluno.fillna(0)

        # print("novo aluno depois do ajuste:", self.novo_aluno)

        # Encontrar os n-alunos mais similares (vizinhos)
        self.distancias, self.indices = self.knn.kneighbors(
            self.novo_aluno, n_neighbors=n_neighbors)

        # Mostrar os n-vizinhos mais próximos
        self.vizinhos_similares = self.X_train.iloc[self.indices[0]]
        self.notas_vizinhos = self.y_train.iloc[self.indices[0]]

        # print("\nAlunos mais similares encontrados:")
        # print(self.vizinhos_similares)
        # print("\nNotas dos alunos mais similares:")
        # print(self.notas_vizinhos)

        # Prever as notas para o novo aluno
        self.notas_preditas = self.knn.predict(self.novo_aluno)

        # Arredondar as notas previstas para 2 casas decimais
        self.notas_preditas = np.round(self.notas_preditas, 2)

        # Função que calcula a melhor recomendação de estudo para o estudante
        self.best_recommendation = self.define_best_recommendation(
            self.notas_preditas[0], self.notas_vizinhos)

        # print(f"\nNotas previstas para o novo aluno: {self.notas_preditas}")
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
