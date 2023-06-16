import sidrapy

import numpy as np
import pandas as pd

import datetime as dt

import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px

# Importando a tabela de Variações da Inflação

ipca_raw = sidrapy.get_table(table_code='1737', territorial_level='1',
                             ibge_territorial_code='all', variable='63, 69, 2263, 2264, 2265',
                             period='last%20472')

# Limpando a tabela e manipulando os dados

ipca = (ipca_raw.loc[1:, ['V', 'D2C', 'D3N']].rename(columns={'V': 'value',
                                                              'D2C': 'date',
                                                              'D3N': 'variable'})
        .assign(variable=lambda x: x['variable'].replace({'IPCA - Variação mensal':
                                                              'Variação mensal (%)',
                                                          'IPCA - Variação acumulada no ano':
                                                              'Variação acumulada ano (%)',
                                                          'IPCA - Variação acumulada em 3 meses':
                                                              'Var em 3 meses (%)',
                                                          'IPCA - Variação acumulada em 6 meses':
                                                              'Variação em 6 meses (%)',
                                                          'IPCA - Variação acumulada em 12 meses':
                                                              'Variação em 12 meses (%)'}),
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

# Filtrando a Inflação acumulada em 12 meses

ipca_12 = (
    ipca.pipe(lambda x: x.loc[x.variable == 'Variação em 12 meses (%)'])
)

sns.lineplot(x='date', y='value',
             data=ipca_12).set(title='Inflação acumulada em 12 meses',
                               xlabel='',
                               ylabel='% a.a')

plt.annotate('Fonte: analisemacro.com.br e dados Sidra/IBGE',
             xy=(1.0, -0.5),
             xycoords='axes fraction',
             ha='right',
             va='center',
             fontsize=12)

# Comparando as variações

g = sns.FacetGrid(ipca, col='variable',
                  col_wrap=2,
                  hue='variable',
                  sharey=False,
                  height=4,
                  aspect=2)

g.map_dataframe(sns.lineplot,
                x='date',
                y='value').set(xlabel="",
                               ylabel='%')

plt.annotate('Fonte: analisemacro.com e dados Sidra/IBGE',
             xy=(1.0, -0.015),
             xycoords='axes fraction',
             ha='right',
             va='center',
             fontsize=12)

# Importando as variações dos grupos do IPCA

ipca_gp_raw = sidrapy.get_table(table_code='7060',
                                territorial_level='1',
                                ibge_territorial_code='all',
                                variable='63,66',
                                period='all',
                                classification='315/7170,7445,7486,7558,7625,7660,7712,7766,7786')

# Limpando e manipulando a tabela

ipca_gp = (
    ipca_gp_raw.loc[1:, ['V', 'D2C', 'D3N', 'D4N']].rename(
        columns={'V': 'value',
                 'D2C': 'date',
                 'D3N': 'variable',
                 'D4N': 'groups'}
    ).assign(variable=lambda x: x['variable'].replace({'IPCA - Variação mensal': 'variação',
                                                       'IPCA - Peso mensal': 'peso'}),
             date=lambda x: pd.to_datetime(x['date'],
                                           format="%Y%m"),
             value=lambda x: x['value'].astype(float),
             groups=lambda x: x['groups'].astype(str)).pipe(
        lambda x: x.loc[x.date > '2007-01-01']
    )
)

# Calculando a contribuição de cada grupo para o IPCA

ipca_gp_wide = (
    ipca_gp.pivot_table(index=['date', 'groups'],
                        columns='variable',
                        values='value').reset_index().assign(
        contribuicao=lambda x: (x.peso * x.variação) / 100)
)

plt.show()

# Mostrando as contribuições de cada grupo

plot = px.bar(ipca_gp_wide,
              x='date',
              y='contribuicao',
              color='groups',
              color_discrete_sequence=colors)

fig = px.line(plot)
fig.show()
