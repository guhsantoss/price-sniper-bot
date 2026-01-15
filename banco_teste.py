import sqlite3

# 1. CONECTAR (Ou criar o banco se ele não existir)
# Isso vai criar um arquivo .db na sua pasta
conexao = sqlite3.connect('precos_monitorados.db')
cursor = conexao.cursor()

# 2. CRIAR A TABELA (A "Planilha" do banco)
# Só cria se ela ainda não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        nome TEXT,
        preco REAL,
        loja TEXT
    )
''')

# 3. INSERIR DADOS (Simulando o seu Bot trabalhando)
print("🤖 Salvando preços no banco de dados...")
cursor.execute("INSERT INTO produtos VALUES ('iPhone 15', 4800.00, 'Amazon')")
cursor.execute("INSERT INTO produtos VALUES ('Notebook Gamer', 3500.50, 'Kabum')")
cursor.execute("INSERT INTO produtos VALUES ('Monitor 144hz', 899.90, 'Mercado Livre')")

# Importante: O commit é o botão "Salvar" do banco
conexao.commit() 

# 4. LER OS DADOS (Para ver se funcionou)
print("-" * 40)
print("📋 RELATÓRIO DE PREÇOS SALVOS:")

cursor.execute("SELECT * FROM produtos") # O * significa "TUDO"

for linha in cursor.fetchall():
    print(f"Produto: {linha[0]} | Preço: R$ {linha[1]} | Loja: {linha[2]}")

# 5. Fechar a conexão (Boa prática)
conexao.close()