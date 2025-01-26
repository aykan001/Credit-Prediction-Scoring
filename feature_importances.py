import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Veri setini yükleme
data = pd.read_csv('veri.csv')

# Gereksiz sütunların çıkarılması
columns_to_drop = ['ID', 'Customer_ID', 'Name', 'Credit_History_Age', 'Num_of_Delayed_Payment','Total_EMI_per_month',
                   'Type_of_Loan', 'Credit_Utilization_Ratio', 'Monthly_Balance',
                   'Payment_of_Min_Amount', 'Payment_Behaviour', 'Credit_Mix']
data_cleaned = data.drop(columns=columns_to_drop, axis=1)

# Kategorik verileri sayısallaştırma
categorical_columns = ['Occupation', 'Credit_Score']
label_encoders = {col: LabelEncoder() for col in categorical_columns}

for col in categorical_columns:
    data_cleaned[col] = label_encoders[col].fit_transform(data_cleaned[col])

# Modeli yükleme
model = joblib.load('xgboost_model.pkl')

# Özellikleri ve hedef değişkeni ayırma
X = data_cleaned.drop('Credit_Score', axis=1)

# Modelden özellik önemlerini alma
feature_importance = model.feature_importances_

# Özellikleri ve önemleri Pandas DataFrame'e ekleme
feature_importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importance})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False).reset_index(drop=True)

# Özellik önemlerini yazdırma
print(feature_importance_df)

# Özellik önemlerini görselleştirme
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'], color='dodgerblue')
plt.xlabel("Özelliklerin Önem Dereceleri")
plt.title("XGBoost Model Özellik Önemleri")
plt.grid(True)
plt.show()

