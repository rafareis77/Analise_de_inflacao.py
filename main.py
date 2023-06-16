import sidrapy

import numpy as np
import pandas as pd

import datetime as dt

import seaborn as sns
from matplotlib import pyplot as plt

#  Importando a tabela de Variações da Inflação

ipca_raw = sidrapy.get_table(table_code='1737', territorial_level='1',
                             ibge_territorial_code='all', variable='63, 69, 2263, 2264, 2265',
                             period='last%20472')

# Limpando a tabela e manipulando os dados

ipca = (ipca_raw.loc[1:, ['V', 'D2C', 'D3N']].rename(columns={'V': 'value',
                                                              'D2C': 'date',
                                                              'D3N': 'variable'})
        .assign(variable=lambda x: x['variable'].replace({'IPCA - Variação mensal':
                                                              'Var. mensal (%)',
                                                          'IPCA - Variação acumulada no ano':
                                                              'Var. acumulada ano (%)',
                                                          'IPCA - Variação acumulada em 3 meses':
                                                              'Var. MM3M (%)',
                                                          'IPCA - Variação acumulada em 6 meses':
                                                              'Var. MM6M (%)',
                                                          'IPCA - Variação acumulada em 12 meses':
                                                              'Var. MM12M (%)'}),
                date=lambda x:
                pd.to_datetime(x['date'],
                               format="%Y%m"),
                value=lambda x: x['value'].astype(float))
        .pipe(lambda x: x.loc[x.date > '2007-01-01']))

# Escolhendo as cores do gráfico

colors = ['#282f6b', '#b22200', '#eace3f',
          '#224f20', '#b35c1e', '#419391',
          '#839c56', '#3b89bc']

theme = {'figure.figsize': (15, 10)}
sns.set_theme(rc=theme, palette=colors)

#  Filtrando a Inflação acumulada em 12 meses

ipca_12 = (
    ipca.pipe(lambda x: x.loc[x.variable == 'Var. MM12M (%)'])
)

sns.lineplot(x='date', y='value',
             data=ipca_12).set(title='Inflação acumulada em 12 meses',
                               xlabel='',
                               ylabel='% a.a')

plt.annotate('Fonte: analisemacro.com.br e dados Sidra/IBGE',
             xy=(1.0, -0.08),
             xycoords='axes fraction',
             ha='right',
             va='center',
             fontsize=12)
plt.show()
