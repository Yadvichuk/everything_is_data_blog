import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pytrends.request import TrendReq
import warnings
warnings.filterwarnings('ignore')


def get_interest_over_time(kw, time, size = 1, cat = 0, geo = '', normalize = True):
    def chunk_gen(l, n):
        for i in range(0, len(l), n):
            yield l[i : i + n]
    chunks = chunk_gen(kw, size)
    df = pd.DataFrame(columns=['date'])
    pytrends = TrendReq(tz=360, backoff_factor=0.2)
    for chunk in chunks:
        pytrends.build_payload(chunk, cat=cat, geo=geo, timeframe=time)
        df_chunk = pytrends.interest_over_time()
        df_chunk.drop('isPartial', axis=1, inplace=True)
        df = pd.merge(df, df_chunk, how='right', on='date')
    df.iloc[:,1:] = df.iloc[:,1:] * (100 / df.iloc[:,1:].max())
    df = df.melt(id_vars=['date'], var_name='Keyword', value_name='Interest')
    return df


def draw_ridgeplot(df, aspect=15, height=0.55, 
                   palette=sns.diverging_palette(220, 0, as_cmap=False),
                   hspace=-0.35, reflinewidth=2, plotlinewidth=1.5,
                   font='monospace', indent=70):
    def label(x, color, label):
        ax = plt.gca()
        ax.text(
            0,
            0.35,
            label,
            fontsize=11,
            font = 'monospace',
            fontweight='bold',
            color=color,
            ha='left',
            va='center',
            transform=ax.transAxes,
        )

    sns.set_theme(style='white', rc={'axes.facecolor': (0, 0, 0, 0)})
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['xtick.color'] = (0.8, 0.8, 0.8)
    plt.rcParams['font.family'] = [font]  
    plt.rcParams['figure.facecolor'] = (0.1,0.1,0.1)#(0.16, 0.16, 0.16)
    plt.rcParams['text.color'] = 'white'

    g = sns.FacetGrid(
        df,
        row='Keyword',
        hue='Keyword',
        aspect=aspect,
        height=height,
        palette=palette,
    )
    g.map(label, 'date')
    g.map(plt.plot, 'date', 'Interest', color='white', linewidth=plotlinewidth)
    g.map(plt.fill_between, 'date', 'Interest', alpha=0.7)
    g.refline(y=0, linewidth=reflinewidth, linestyle='-', color=None, clip_on=False)
    g.figure.subplots_adjust(hspace=hspace)
    g.set_titles('')
    g.set(xlim=[df['date'].min() - datetime.timedelta(days=indent),
            df['date'].max(),],
        xticks=[datetime.datetime(df.date.min().year, i, 12) for i in range(1, 13)],
        xticklabels=[datetime.date(2000, _ , 1).strftime('%B').upper()[:3] for _ in range(1,13)])
    g.despine(bottom=True, left=True)
    
    plt.suptitle(f'Год в поиске: {df.date.min().year} ', fontsize=24, alpha = .8) 
    plt.savefig('2022_searches.png',dpi = 300)
    plt.show()

year = 2022
pytrend = TrendReq(hl='ru-RU', tz=360) 
kw = pytrend.top_charts(year, hl='ru-RU', tz=300, geo='GLOBAL')['title'].to_list()#['Wordle', 'Ukraine', 'Indian Premier League', 'iPhone 14', 'Queen Elizabeth',  'World Cup']
time.sleep(1)
draw_ridgeplot(get_interest_over_time(kw, f'{year}-01-01 {year+1}-01-01'))