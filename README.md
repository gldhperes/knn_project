## K-NN Project
K-NN Project é um projeto baseado no algoritmo de filtragem colaborativa chamado "K-Nearest Neighbors" (K-NN) e em tradução livre "K vizinhos mais próximos".
Construi o algoritimo usando Python juntamente com as bibliotecas scikit-learn para o uso do K-NN e pandas para a a leitura dos dados. Para o frontend, implementei o framework Django, proporcionando uma interface interativa.

#### Importante resaltar que para simplificar o projeto e por questoes de precificação, decidi deixar o projeto rodando local, mas para os interessados, deixarei orientações para a utilização.

## Objetivo
Prever a nota de um novo aluno no ENEM. A previsão será baseada nas notas e nas características dos alunos que participaram do exame em anos anteriores.

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

 Informações Socioeconômicas:
o Renda Familiar (Q006)
o Escolaridade da Mãe (Q002)
o Tipo de Escola (Pública ou Privada) (TP_ESCOLA)
o Raça/Cor (TP_COR_RACA)
 Localidade:
o Estado (SG_UF_RESIDENCIA)
o Município (CO_MUNICIPIO_RESIDENCIA)
