import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np
import joblib

"""
pandas: Veri işleme ve analiz için kullanılır; burada veri setini yüklemek ve sütun manipülasyonu yapmak için kullanılıyor.

train_test_split (scikit-learn): Veri setini eğitim ve test alt kümelerine ayırarak modelin performansını değerlendirmeye yardımcı olur.

GridSearchCV: Hiperparametre optimizasyonu için k-cross doğrulaması kullanarak en iyi model ayarlarını bulur (ancak bu kodda kullanılmamış).

LabelEncoder: Kategorik değişkenleri sayısal değerlere dönüştürür, böylece model eğitimi için kullanılabilir hale gelir.

XGBClassifier (XGBoost): Güçlü bir gradient boosting algoritması olup, sınıflandırma problemleri için optimize edilmiştir ve hızlı/etkili tahminler sağlar.

accuracy_score: Modelin doğru tahmin oranını hesaplayarak performansı değerlendirir.

**matplotlib.pyplot ve numpy: Grafik çizimi ve veri manipülasyonu için kullanılır (bu kodda matplotlib kullanılmamış).

joblib: Eğitimli modeli dosyaya kaydetmek ve daha sonra yeniden yüklemek için kullanılır, böylece yeniden eğitime gerek kalmaz.

"""
data = pd.read_csv('veri.csv')

# Veri setini yükleme
#data = pd.read_csv('veri.csv')

# Gereksiz sütunların çıkarılması
columns_to_drop = ['ID', 'Customer_ID', 'Name','Credit_History_Age','Num_of_Delayed_Payment','Total_EMI_per_month','Changed_Credit_Limit','Num_Credit_Inquiries',
                   'Type_of_Loan','Credit_Utilization_Ratio','Monthly_Balance','Payment_of_Min_Amount','Payment_Behaviour','Credit_Mix' ]
data_cleaned = data.drop(columns=columns_to_drop, axis=1)

# Kategorik verileri sayısallaştırma
#'Payment_of_Min_Amount', 'Payment_Behaviour', çıkarıldı.
categorical_columns = ['Occupation', 'Credit_Score']
label_encoders = {col: LabelEncoder() for col in categorical_columns}
for col in categorical_columns:
    data_cleaned[col] = label_encoders[col].fit_transform(data_cleaned[col])

# Hedef değişken (Credit_Score) ve bağımsız değişkenlerin ayrılması
X = data_cleaned.drop('Credit_Score', axis=1)
y = data_cleaned['Credit_Score']

# Veri setini eğitim ve test olarak ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
# XGBoost modeli oluşturma ve eğitme
model = XGBClassifier(eval_metric='logloss', n_estimators=500, random_state=42)
model.fit(X_train, y_train)

# Modeli dosyaya kaydetme
joblib.dump(model, 'xgboost_model.pkl')
print("Model proje dizinine 'xgboost_model.pkl' olarak kaydedildi.")

# Test seti üzerinde tahmin ve doğruluk oranını hesaplama
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred) * 100
print(accuracy)

print("Tahmin edilen değerler:")
print(y_pred[:10])
print("Gerçek değerler:")
print(y_test[:10].values)