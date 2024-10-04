from django import forms


class Options(forms.Form):
    opcoes_q002 = [
        ('A', 'Não estudou'),
        ('B', 'Não completou a 4/5 séries'),
        ('C', 'Não completou a 8/9 série'),
        ('D', 'Não completou ensino médio'),
        ('E', 'Não completou faculdade'),
        ('F', 'Não completou pós-graduação'),
        ('G', 'Completou pós'),
        ('H', 'Não sabe'),
    ]

    opcoes_q006 = [
        ('A', 'Nenhuma'),
        ('B', 'Renda mensal de 1320'),
        ('C', 'Renda mensal de 1980'),
        ('D', 'Renda mensal de 2640'),
        ('E', 'Renda mensal de 3300'),
        ('F', 'Renda mensal de 3960'),
        ('G', 'Renda mensal de 5280'),
        ('H', 'Renda mensal de 6600'),
        ('I', 'Renda mensal de 7920'),
        ('J', 'Renda mensal de 9240'),
        ('K', 'Renda mensal de 10560'),
        ('L', 'Renda mensal de 11880'),
        ('M', 'Renda mensal de 13200'),
        ('N', 'Renda mensal de 15840'),
        ('O', 'Renda mensal de 19800'),
        ('P', 'Renda mensal de 26400'),
        ('Q', 'Acima de 26400'),
    ]

    opcoes_tp_escola = [
        (1, 'Não respondeu'),
        (2, 'Pública'),
        (3, 'Privada'),
    ]

    opcoes_tp_cor_raca = [
        (0, 'Não declarado'),
        (1, 'Branca'),
        (2, 'Preta'),
        (3, 'Parda'),
        (4, 'Amarela'),
        (5, 'Indígena'),
        (6, 'Não dispõe da informação'),
    ]

    opcoes_SG_UF_PROVA = [
        ('CE', 'Ceará'),
    ]

    opcoes_CO_MUNICIPIO_PROVA = [
        (2304400, 'Fortaleza'),
    ]

    Q002 = forms.ChoiceField(choices=opcoes_q002, label="Escolaridade da mãe:")
    Q006 = forms.ChoiceField(choices=opcoes_q006, label="Renda familiar mensal:")

    TP_ESCOLA = forms.ChoiceField(choices=opcoes_tp_escola, label="Tipo de escola:")
    TP_COR_RACA = forms.ChoiceField(choices=opcoes_tp_cor_raca, label="Cor/Raça")

    SG_UF_PROVA = forms.ChoiceField(choices=opcoes_SG_UF_PROVA, label="Estado")
    CO_MUNICIPIO_PROVA = forms.ChoiceField(choices=opcoes_CO_MUNICIPIO_PROVA, label="Municipio")
