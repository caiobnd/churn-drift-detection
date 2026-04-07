from sklearn.linear_model   import LogisticRegression
from pathlib                import Path
from joblib                 import dump
import cleanning

path_data=Path("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
path_model=Path("model/logisticregression.pkl")

df          = cleanning.load_data(path_data)
df_clean    = cleanning.clean_data(df)
df_enconded = cleanning.encoding(df_clean)
X_train, X_test, y_train, y_test = cleanning.split_data(df_enconded)

model =  LogisticRegression(class_weight='balanced', max_iter=2000)
model.fit(X_train,y_train)
dump(model,path_model)


        
    
