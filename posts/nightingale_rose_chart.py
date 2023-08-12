import plotly.express as px
import pandas as pd

df = pd.read_excel('Youth unemployment, both sexes.xls')#http://data.un.org/DocumentData.aspx?id=264
df = df[df['Country']=='Russian Federation']
df = df[['Year', 'Youth unemployment rate (%)', 'Adult unemployment rate (%)']]
df = df.melt(id_vars = ['Year'], value_vars = ['Youth unemployment rate (%)', 'Adult unemployment rate (%)'])
df['Year'] = df['Year'].astype('str')
fig = px.bar_polar(df, r="value", theta="Year",
                   color="variable", template="plotly_dark",
                   color_discrete_sequence= px.colors.sequential.Tealgrn_r)
fig.show()