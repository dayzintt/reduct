import pandas as pd

# Caminhos para os arquivos
csv_file = r'C:\Users\d.figueiredo\Desktop\dados(1).csv'
excel_file = r'C:\Users\d.figueiredo\Desktop\VIDAS - MH VIDA (1).xlsx'

# Nome das abas
csv_sheet_name = 'Pagina1'
excel_sheet_name = 'Pagina1'

# Nome das colunas
column_name_csv = 'Nome'  # Ajuste conforme a coluna correta no CSV após limpeza
column_name_excel = 'Nome'

# Ler o arquivo CSV com o delimitador correto
df_csv = pd.read_csv(csv_file, delimiter=';', skipinitialspace=True)

# Limpar colunas e ajustar o nome da coluna no CSV
df_csv.columns = df_csv.columns.str.strip()  # Remover espaços extras nos nomes das colunas
df_csv = df_csv.rename(columns={'codigo;Nome;;;;;;': 'Nome'})  # Ajustar o nome da coluna se necessário

# Ler a planilha Excel
df_excel = pd.read_excel(excel_file, sheet_name=excel_sheet_name)

# Extrair a coluna com os nomes de ambas as fontes
names_csv = df_csv[column_name_csv].dropna().str.strip().str.lower()
names_excel = df_excel[column_name_excel].dropna().str.strip().str.lower()

# Encontrar nomes em comum
common_names = set(names_csv).intersection(names_excel)

# Mostrar os nomes em comum
print(f"Nomes em comum: {common_names}")

# Se você quiser salvar os nomes em comum em um novo arquivo CSV
common_names_df = pd.DataFrame(list(common_names), columns=[column_name_csv])
common_names_df.to_csv(r'C:\Users\d.figueiredo\Desktop\nomes_comum.csv', index=False)

print("Arquivo CSV com nomes em comum gerado com sucesso!")
