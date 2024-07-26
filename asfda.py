import pdfplumber
import csv

# Lista de frases a serem ignoradas
ignore_phrases = [
    "Listagem de Usuários com Produtos",
    "Ordem: Código Do Usuário",
    "Filtros: Data referência: 26/07/2024",
    "Código Usuário Nome Usuário",
    "Inclusão do",
    "Produto",
    "Data",
    "Matrícula",
    "Nascimento",
    "Sexo:",
    "Num Declaração Óbito",
    "Data do Óbito",
    "Nome do Produto",
    "IMPORTANTE:,Os dados e as,totaliza珲es,expressas,neste,relat髍io,podem,diferir,de outros relat髍ios, ainda que, supostamente, devessem ser semelhantes. Eventuais diferen鏰s podem decorrer de: filtros aplicados aos dados, elementos considerados nos c醠culos, prop髎ito e"
]

# Função para verificar se uma linha deve ser ignorada
def should_ignore(line):
    return any(phrase in line for phrase in ignore_phrases)

# Abrir o arquivo PDF
with pdfplumber.open(r'C:\Users\d.figueiredo\Desktop\Listagem_de_Usuários_com_Produtos - 26.07.24.pdf') as pdf:
    all_text = ""
    for page in pdf.pages:
        all_text += page.extract_text()

# Processar o texto extraído
lines = all_text.split('\n')
data = []
error_lines = []  # Lista para armazenar linhas com erros

for line in lines:
    # Ignorar as linhas que contêm qualquer uma das frases a serem ignoradas
    if should_ignore(line):
        continue

    # Supondo que os dados estejam sempre na mesma ordem e formatados da mesma maneira
    parts = line.split()
    
    # Verifica se a linha parece conter dados relevantes
    if len(parts) > 5:
        # Tentar identificar se a linha contém dados esperados
        try:
            # Identificar partes principais do dado
            codigo_usuario = parts[0]
            nome_usuario = ' '.join(parts[1:5])  # Ajuste conforme necessário
            data_inclusao = parts[5]
            data_matricula = parts[6]
            data_nascimento = parts[7]
            sexo = parts[8]
            num_declaracao_obito = parts[9]
            data_obito = parts[10] if len(parts) > 10 else ""
            nome_produto = ' '.join(parts[11:]) if len(parts) > 11 else ""

            data.append([
                codigo_usuario,
                nome_usuario,
                data_inclusao,
                data_matricula,
                data_nascimento,
                sexo,
                num_declaracao_obito,
                data_obito,
                nome_produto
            ])
        except IndexError:
            # Capturar qualquer erro e armazenar a linha para depuração
            error_lines.append([
                'ERRO',  # Identificador de erro
                line,  # Linha com erro
                '', '', '', '', '', '', ''  # Preencher com espaços vazios para outras colunas
            ])

# Escrever os dados e erros para um arquivo CSV
with open(r'C:\Users\d.figueiredo\Desktop\dadosOtro.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['Código Usuário', 'Nome Usuário', 'Data Inclusão', 'Data Matrícula', 'Data Nascimento', 'Sexo', 'Num Declaração Óbito', 'Data do Óbito', 'Nome do Produto'])
    writer.writerows(data)
    
    # Adicionar um separador antes dos erros
    writer.writerow([])
    writer.writerow(['Código Usuário', 'Nome Usuário', 'Data Inclusão', 'Data Matrícula', 'Data Nascimento', 'Sexo', 'Num Declaração Óbito', 'Data do Óbito', 'Nome do Produto'])
    writer.writerows(error_lines)

print("Arquivo CSV gerado com sucesso!")
