# K-NN Project
K-NN Project é um projeto baseado no algoritmo de filtragem colaborativa chamado "K-Nearest Neighbors" (K-NN) e em tradução livre "K vizinhos mais próximos".
(EXPLICAR OQUE É K-NN)

## Objetivo
Um algoritimo que preve a nota de um novo aluno no ENEM. A previsão são baseadas nas notas e nas características dos alunos que participaram do exame em anos anteriores.
#### Importante resaltar que para simplificar o projeto e por questoes de precificação, decidi deixar o projeto rodando localmente, mas, deixei orientações para a quem quiser utilizar.

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

# Preparação para o Projeto
## Extraindo os dados
Por ter uma base de dados relativamente grande e questoes de performance, foi feito um script (extração_de_dados.py) que, como saida, gere um novo arquivo .csv juntando somente as colunas necessárias para o algoritmo do K-NN agir.

```python
import pandas as pd

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



