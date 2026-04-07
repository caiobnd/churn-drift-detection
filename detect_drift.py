from evidently.presets  import DataDriftPreset
from evidently          import Report, Dataset, DataDefinition
from pathlib            import Path
import pandas   as pd
import numpy    as np

path_reference = Path("data/reference/WA_Fn-UseC_-Telco-Customer-Churn.csv")
path_current   = Path("data/current/drift_critico.csv")
path_report    = Path("reports/relatorio.html")

path_report.parent.mkdir(parents=True, exist_ok=True)

df_reference = pd.read_csv(path_reference)
df_current   = pd.read_csv(path_current)

df_reference['TotalCharges'] = pd.to_numeric(df_reference['TotalCharges'], errors='coerce').fillna(0)
df_current['TotalCharges']   = pd.to_numeric(df_current['TotalCharges'], errors='coerce').fillna(0)

data_definition = DataDefinition(
    numerical_columns=['tenure', 'MonthlyCharges', 'TotalCharges'],
    categorical_columns=['gender', 'Contract', 'PaymentMethod']
)

reference_dataset = Dataset.from_pandas(df_reference, data_definition=data_definition)
current_dataset   = Dataset.from_pandas(df_current, data_definition=data_definition)

report = Report(metrics=[DataDriftPreset()])

snapshot = report.run(
    reference_data=reference_dataset,
    current_data=current_dataset
)

snapshot.save_html(str(path_report))
