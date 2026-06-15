# Bibliotecas necessárias
import os
import yfinance as yf
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Credenciais
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

# Ações que vamos ingerir
SYMBOLS = ["IBM", "AAPL", "MSFT", "GOOGL", "AMZN"]

def buscar_dados(symbol):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="2y", interval="1d")
        
        if df.empty:
            print(f"Nenhum dado retornado para {symbol}")
            return None
        
        print(f"[{symbol}] {len(df)} linhas retornadas")
        return df
    
    except Exception as e:
        print(f"Erro ao buscar {symbol}: {e}")
        return None

def transformar_dados(df, symbol):
    if df is None:
        return None
    
    df = df.reset_index()
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    df["symbol"] = symbol
    df["date"] = df["date"].dt.date
    df = df[["symbol", "date", "open", "high", "low", "close", "volume"]]
    
    return df

def conectar_banco():
    try:
        conexao = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT
        )
        print("Banco conectado")
        return conexao
    except psycopg2.Error as e:
        print(f"Erro na conexão: {e}")
        return None

def criar_tabela(conexao):
    sql = """
    CREATE TABLE IF NOT EXISTS raw_stock_prices (
        symbol      VARCHAR(10),
        date        DATE,
        open        FLOAT,
        high        FLOAT,
        low         FLOAT,
        close       FLOAT,
        volume      BIGINT,
        PRIMARY KEY (symbol, date)
    );
    """
    cursor = conexao.cursor()
    cursor.execute(sql)
    conexao.commit()
    cursor.close()
    print("Tabela criada/verificada")

def inserir_dados(conexao, df):
    cursor = conexao.cursor()
    inseridos = 0
    
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO raw_stock_prices (symbol, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol, date) DO NOTHING
        """, (row["symbol"], row["date"], row["open"], row["high"], row["low"], row["close"], row["volume"]))
        inseridos += 1
    
    conexao.commit()
    cursor.close()
    print(f"{inseridos} linhas inseridas")

# Execução
conexao = conectar_banco()

if conexao:
    criar_tabela(conexao)
    
    for symbol in SYMBOLS:
        df = buscar_dados(symbol)
        df = transformar_dados(df, symbol)
        
        if df is not None:
            inserir_dados(conexao, df)
    
    conexao.close()
    print("Concluído")