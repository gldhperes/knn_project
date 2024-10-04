from django.shortcuts import render
import pandas as pd
import numpy as np
# Importe sua classe KNN do arquivo onde você a salvou
from .knn_model.knn import KNN
from .knn_model.options_dict import Options


def previsao_view(request):
    form = Options()  # Instanciar o formulário

    if request.method == 'POST':
        # print(request.POST)
        # Coletar os dados do formulário
        novo_aluno = pd.DataFrame({
            'Q002': [request.POST.get('Q002')],
            'Q006': [request.POST.get('Q006')],
            'TP_ESCOLA': [request.POST.get('TP_ESCOLA')],
            'TP_COR_RACA': [request.POST.get('TP_COR_RACA')],
            'SG_UF_PROVA': [request.POST.get('SG_UF_PROVA')],
            'CO_MUNICIPIO_PROVA': [request.POST.get('CO_MUNICIPIO_PROVA')]
        })
        # print(novo_aluno)
        # Instanciar o modelo KNN e fazer as previsões
        _knn = KNN(novo_aluno)

       # Convertendo o DataFrame de vizinhos para uma lista de dicionários
        vizinhos_similares = _knn.vizinhos_similares.to_dict(orient='records')
        notas_vizinhos = _knn.notas_vizinhos.to_dict(orient='records')
        best_recommendation = _knn.best_recommendation

        # Renderizar os resultados na página
        return render(request, 'resultados.html', {
            'form': form,
            'notas_preditas': _knn.notas_preditas[0],
            'vizinhos_similares': vizinhos_similares,
            'notas_vizinhos': notas_vizinhos,
            'nota_MT': _knn.nota_MT,
            'nota_CN': _knn.nota_CN,
            'nota_LC': _knn.nota_LC,
            'nota_CH': _knn.nota_CH,
            'nota_RED': _knn.nota_RED,
            'best_recommendation': best_recommendation,
        })

    return render(request, 'resultados.html', {
        'form': form,
    })
