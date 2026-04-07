# Churn Drift Detection

Monitoramento de Data Drift em modelos de Machine Learning — detecta mudanças na distribuição dos dados de produção usando Evidently AI e gera relatórios visuais automáticos.

---

## Visão Geral

Modelos de ML degradam em produção sem avisar. O motivo mais comum é o **data drift** — os dados de produção mudam e o modelo, treinado com dados antigos, começa a errar mais sem que ninguém perceba.

Este projeto simula esse cenário real:

1. Treina um modelo com dados de referência (dataset Telco)
2. Simula 10 cenários de drift com diferentes intensidades
3. Usa o **Evidently AI** para comparar as distribuições e detectar o drift
4. Gera relatórios HTML visuais automáticos para cada cenário

---

## Cenários de Drift Simulados

O drift foi simulado na feature `tenure` (tempo de contrato em meses) — uma das features mais preditivas para churn.

| Cenário | Média (μ) | Desvio (σ) | Drift Score |
|---|---|---|---|
| referencia | 32.4 | 24.6 | — |
| drift_minimo | 30.0 | 24.6 | baixo |
| drift_leve | 26.0 | 24.6 | leve |
| drift_moderado | 20.0 | 24.6 | moderado |
| drift_forte | 8.0 | 5.0 | forte |
| **drift_critico** | **2.0** | **1.0** | **1.236 ✅ Detectado** |
| retencao_alta | 40.0 | 24.6 | invertido |
| base_antiga | 50.0 | 24.6 | invertido |
| baixo_ruido | 32.4 | 5.0 | volatilidade |
| volatilidade | 32.4 | 45.0 | dispersão |

**Resultado no cenário `drift_critico`:** Drift detectado em 1 de 7 colunas (14.3%) — exatamente a feature modificada. Wasserstein distance normalizada: **1.236**.

---

## Estrutura do Projeto

```
churn-drift-detection/
├── data/
│   ├── reference/     ← dataset original (Telco)
│   └── current/       ← datasets simulados por cenário
├── reports/
│   └── .gitkeep       ← relatórios HTML gerados
├── model/
│   └── .gitkeep
├── cleaning.py
├── constants.py
├── generate_data.py   ← simula os cenários de drift
├── train.py           ← treina o modelo de referência
├── detect_drift.py    ← compara datasets e gera relatório HTML
├── requirements.txt
└── README.md
```

---

## Como Executar

### 1. Clone o repositório

```bash
git clone https://github.com/caiobnd/churn-drift-detection.git
cd churn-drift-detection
```

### 2. Configure o ambiente

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 3. Baixe o dataset

Baixe o [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) e coloque o CSV em `data/reference/`.

### 4. Gere os cenários de drift

```bash
python generate_data.py
```

Isso gera 10 CSVs em `data/current/`, um para cada cenário.

### 5. Treine o modelo de referência

```bash
python train.py
```

### 6. Gere o relatório de drift

```bash
python detect_drift.py
```

O relatório HTML será salvo em `reports/`. Abra no navegador para visualizar.

---

## Exemplo de Resultado

Cenário `drift_critico` — `tenure` com média reduzida de 32 para 2 meses:

- **Drift detectado:** tenure ✅
- **Teste estatístico:** Wasserstein distance (normed)
- **Drift Score:** 1.236
- **Colunas afetadas:** 1 de 7 (14.3%)

O gráfico gerado mostra claramente a separação entre a distribuição de referência (verde) e a distribuição atual (vermelho).

---

## Tecnologias Utilizadas

- **Python 3.12**
- **Evidently AI** — drift detection e geração de relatórios
- **scikit-learn** — modelo de referência (Logistic Regression)
- **pandas** — manipulação de dados
- **numpy** — simulação de distribuições estatísticas
- **joblib** — serialização do modelo

---

## Próximos Passos

- [ ] Testar drift em múltiplas features simultaneamente
- [ ] Adicionar alertas automáticos quando drift score ultrapassar threshold
- [ ] Integrar com MLflow para rastrear histórico de drift
- [ ] Adicionar CI/CD com GitHub Actions