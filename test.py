import pandas as pd
import joblib

# Modeli yükleme
model_path = ("C:\\Users\\senar\\OneDrive\\Masaüstü\\Ders\\bilgisayar müh geliş\\New\\Proje\\Proje\\xgboost_model.pkl")  # Model dosyanızın yolu
model = joblib.load(model_path)

# Gereksiz sütunların çıkarılması
columns_to_drop = [
    'ID', 'Customer_ID', 'Name', 'Credit_History_Age', 'Num_of_Delayed_Payment',
    'Total_EMI_per_month', 'Changed_Credit_Limit', 'Num_Credit_Inquiries',
    'Type_of_Loan', 'Credit_Utilization_Ratio', 'Monthly_Balance',
    'Payment_of_Min_Amount', 'Payment_Behaviour', 'Credit_Mix'
]

# Örnek test verisi (kolonları modeli eğitirken kullandığınız veri yapısına uygun hale getirin)
test_data = pd.DataFrame([{
    'Month': 1,
    'Age': 35,
    'SSN': 987654321,
    'Occupation': 2,
    'Annual_Income': 100000,
    'Monthly_Inhand_Salary': 8000,
    'Num_Bank_Accounts': 3,
    'Num_Credit_Card': 2,
    'Interest_Rate': 2.5,
    'Num_of_Loan': 1,
    'Delay_from_due_date': 0,
    'Outstanding_Debt': 2000,
    'Amount_invested_monthly': 1500,
    'ID': '789XYZ',
    'Customer_ID': '123ABC',
    'Name': 'Good User',
    'Credit_History_Age': 10,
    'Num_of_Delayed_Payment': 0,
    'Total_EMI_per_month': 500,
    'Changed_Credit_Limit': 1,
    'Num_Credit_Inquiries': 2,
    'Type_of_Loan': 'Home Loan',
    'Credit_Utilization_Ratio': 0.2,
    'Monthly_Balance': 5000,
    'Payment_of_Min_Amount': 'No',
    'Payment_Behaviour': 'Regular',
    'Credit_Mix': 'Excellent'
}])

# Gereksiz sütunları çıkarma
test_data_cleaned = test_data.drop(columns=columns_to_drop, errors='ignore')

# Model tahmini
prediction = model.predict(test_data_cleaned)

# Tahmin sonucunu yazdırma
print(f"Tahmin sonucu: {prediction}")
