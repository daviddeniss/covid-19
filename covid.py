import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o dataset
url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
df = pd.read_csv(url)

# Visualizar as primeiras linhas
print(df.head())

# Informações básicas sobre o dataset
print(df.info())

# Verificar valores faltantes
print(df.isnull().sum())

# Remover colunas desnecessárias
df.drop(['Lat', 'Long'], axis=1, inplace=True)

# Agrupar dados por país e somar apenas colunas numéricas
df = df.groupby('Country/Region').sum(numeric_only=True)

# Resetar o índice para transformar 'Country/Region' em uma coluna
df = df.reset_index()

# Transformar o formato dos dados (colunas para linhas)
df = df.melt(id_vars='Country/Region', var_name='Date', value_name='Confirmed Cases')

# Converter a coluna 'Date' para o tipo datetime
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')

# Verificar o valor máximo de casos confirmados globalmente
max_global_cases = df['Confirmed Cases'].max()
print(f"Valor máximo de casos confirmados globalmente: {max_global_cases}")

# Verificar o valor máximo de casos confirmados por país
max_cases_by_country = df.groupby('Country/Region')['Confirmed Cases'].max().nlargest(10)
print("Valor máximo de casos confirmados por país (Top 10):")
print(max_cases_by_country)

# Função para formatar números em milhares (K) ou milhões (M)
def format_number(number):
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:
        return f"{number / 1_000:.1f}K"
    else:
        return str(number)

# Aplicar formatação aos valores máximos
print("\nValores máximos formatados:")
print(f"Global: {format_number(max_global_cases)}")
print("Por país (Top 10):")
print(max_cases_by_country.apply(format_number))

# Agrupar casos confirmados por data
global_cases = df.groupby('Date')['Confirmed Cases'].sum()

# Plotar o gráfico global
plt.figure(figsize=(12, 6))
global_cases.plot()
plt.title('Casos Confirmados de COVID-19 ao Longo do Tempo (Global)')
plt.xlabel('Data')
plt.ylabel('Casos Confirmados')
plt.grid()

# Adicionar anotação com o valor máximo global
max_global_date = global_cases.idxmax()
max_global_value = global_cases.max()
plt.annotate(f'Máximo: {format_number(max_global_value)}', 
             xy=(max_global_date, max_global_value), 
             xytext=(max_global_date, max_global_value * 0.8),
             arrowprops=dict(facecolor='red', shrink=0.05))

plt.show()

# Plotar o gráfico de barras dos Top 10 países
plt.figure(figsize=(12, 6))
max_cases_by_country.plot(kind='bar', color='red')
plt.title('Top 10 Países com Mais Casos Confirmados de COVID-19')
plt.xlabel('País')
plt.ylabel('Casos Confirmados')
plt.xticks(rotation=45)

# Adicionar anotações com os valores formatados
for i, value in enumerate(max_cases_by_country):
    plt.text(i, value, format_number(value), ha='center', va='bottom')

plt.show()

# Filtrar dados do Brasil
brazil_data = df[df['Country/Region'] == 'Brazil']

# Plotar o gráfico do Brasil
plt.figure(figsize=(12, 6))
plt.plot(brazil_data['Date'], brazil_data['Confirmed Cases'], label='Brasil')
plt.title('Casos Confirmados de COVID-19 no Brasil')
plt.xlabel('Data')
plt.ylabel('Casos Confirmados')
plt.legend()
plt.grid()

# Adicionar anotação com o valor máximo no Brasil
max_brazil_cases = brazil_data['Confirmed Cases'].max()
max_brazil_date = brazil_data.loc[brazil_data['Confirmed Cases'].idxmax(), 'Date']
plt.annotate(f'Máximo: {format_number(max_brazil_cases)}', 
             xy=(max_brazil_date, max_brazil_cases), 
             xytext=(max_brazil_date, max_brazil_cases * 0.8),
             arrowprops=dict(facecolor='red', shrink=0.05))

plt.show()

# Exportar o dataset para um arquivo CSV
df.to_csv('covid_cleaned.csv', index=False)