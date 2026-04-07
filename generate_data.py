import pandas   as pd
import numpy    as np
from   pathlib    import Path

path_df     = Path("data/reference/WA_Fn-UseC_-Telco-Customer-Churn.csv")
path_csv    = Path("data/current")
df          = pd.read_csv(path_df)
df_current  = df.copy()

std_tenure  = df['tenure'].std()
mean_tenure = df['tenure'].mean()

# Simula drift: reduz a média de tenure para 8 (novos clientes) com desvio 5 para criar um sinal estatístico evidente.
df_current['tenure'] = np.abs(np.random.normal(loc=8,scale=5,size=len(df_current)).round().astype(int))

'''Usando cálculo baseado na Distância Estatística em relação ao Desvio Padrão original. 
Esses são os valores que vou usar para média '''
cenarios = [
    {"nome": "referencia", "mu": 32.4, "sigma": 24.6},      
    {"nome": "drift_minimo", "mu": 30.0, "sigma": 24.6},    
    {"nome": "drift_leve", "mu": 26.0, "sigma": 24.6},     
    {"nome": "drift_moderado", "mu": 20.0, "sigma": 24.6},  
    {"nome": "drift_forte", "mu": 8.0, "sigma": 5.0},      
    {"nome": "drift_critico", "mu": 2.0, "sigma": 1.0},   
    {"nome": "retencao_alta", "mu": 40.0, "sigma": 24.6},   
    {"nome": "base_antiga", "mu": 50.0, "sigma": 24.6},    
    {"nome": "baixo_ruido", "mu": 32.4, "sigma": 5.0},      
    {"nome": "volatilidade", "mu": 32.4, "sigma": 45.0}    
]

for itens in cenarios:
    df_current = df.copy()
    df_current['tenure'] = np.abs(np.random.normal(loc=itens['mu'],scale=itens['sigma'],size=len(df_current)).round().astype(int))
    path_current         = path_csv/f"{itens['nome']}.csv"
    df_current.to_csv(path_current,index=False)