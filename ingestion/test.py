import yfinance as yf
import os
from dotenv import load_dotenv

load_dotenv()

def buscar_dados(symbol):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="2y", interval="1d")
        
        if df.empty:
            print(f"Nenhum dado retornado para {symbol}")
            return None
        
        print(f"Conexão 100% - {len(df)} linhas retornadas")
        return df
    
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return None

def transformar_dados(df, symbol):
    if df is None:
        print("Dados inválidos, abortando transformação")
        return None
    
    print(df.head())
    print(df.dtypes)
    return df

dados = buscar_dados("IBM")
transformar_dados(dados, "IBM")