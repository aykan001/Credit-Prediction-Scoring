import pandas as pd
import plotly.express as px

# Veri okuma işlemi
veri = pd.read_csv("veri.csv")

# Kredi puanı dağılımını sayma
counts = veri.groupby(['Occupation', 'Credit_Score']).size().reset_index(name='Count')

# 1. Grafik: Kredi Puanının Mesleklere Göre Dağılımı
fig1 = px.bar(counts, 
              x='Occupation', 
              y='Count', 
              color='Credit_Score', 
              title='Kredi Puanının Mesleklere Göre Dağılımı',
              color_discrete_map={'Poor':'#de1010', 
                                  'Standard':'#ff71fb', 
                                  'Good':'#5c8cf9'})
fig1.write_html("C:/Users/senar/OneDrive/Masaüstü/Ders/bilgisayar müh geliş/Proje_new/Proje (2)/Proje/Flask/static/fig/fig1.html")

# 2. Grafik: Kredi Puanının Aylık Maaşa Göre Dağılımı
fig2 = px.box(veri, 
              x="Credit_Score", 
              y="Monthly_Inhand_Salary",
              color="Credit_Score",
              title="Kredi Puanının Aylık Maaşa Göre Dağılımı",
              color_discrete_map={'Poor':'#de1010', 
                                  'Standard':'#ff71fb', 
                                  'Good':'#5c8cf9'})
fig2.write_html("C:/Users/senar/OneDrive/Masaüstü/Ders/bilgisayar müh geliş/Proje_new/Proje (2)/Proje/Flask/static/fig/fig2.html")

# 3. Grafik: Kredi Puanının Yıllık Gelire Göre Dağılımı
fig3 = px.box(veri,
              x='Credit_Score',
              y='Annual_Income',
              title='Kredi Puanının Yıllık Gelire Göre Dağılımı',
              color='Credit_Score',
              color_discrete_map={'Poor':'#de1010', 
                                  'Standard':'#ff71fb', 
                                  'Good':'#5c8cf9'})
fig3.write_html("C:/Users/senar/OneDrive/Masaüstü/Ders/bilgisayar müh geliş/Proje_new/Proje (2)/Proje/Flask/static/fig/fig3.html")

ort_bank_account = veri.groupby('Credit_Score')['Num_Bank_Accounts'].mean().reset_index()
# 4. Grafik: Kredi Puanına Göre Banka Hesap Sayısı Dağılımı
fig4 = px.bar(ort_bank_account, 
              x="Credit_Score", 
              y="Num_Bank_Accounts", 
              title="Banka Hesap Sayısına Göre Dağılımı",
              color='Credit_Score',
              color_discrete_map={'Poor':'#de1010', 
                                  'Standard':'#ff71fb', 
                                  'Good':'#5c8cf9'})
fig4.write_html("C:/Users/senar/OneDrive/Masaüstü/Ders/bilgisayar müh geliş/Proje_new/Proje (2)/Proje/Flask/static/fig/fig4.html")

# 5. Grafik: Kredi Puanına Göre Kredi Kartı Sayısı Dağılımı
ort_credit_cart = veri.groupby('Credit_Score')['Num_Credit_Card'].mean().reset_index()
fig5 = px.bar(ort_credit_cart, 
              x="Credit_Score", 
              y="Num_Credit_Card", 
              title="Kredi Karta Sahip Olma Sayısına Göre Dağılımı",
              color='Credit_Score',
              color_discrete_map={'Poor':'#de1010', 
                                  'Standard':'#ff71fb', 
                                  'Good':'#5c8cf9'})
fig5.write_html("C:/Users/senar/OneDrive/Masaüstü/Ders/bilgisayar müh geliş/Proje_new/Proje (2)/Proje/Flask/static/fig/fig5.html")

# 6. Grafik: Faiz Oranına Göre Dağılımı
ort_interest = veri.groupby('Credit_Score')["Interest_Rate"].mean().reset_index()
fig6 = px.bar(ort_interest, 
              x="Credit_Score", 
              y="Interest_Rate", 
              title="Faiz Oranına Göre Dağılımı",
              color='Credit_Score',
              color_discrete_map={'Poor':'#de1010', 
                                  'Standard':'#ff71fb', 
                                  'Good':'#5c8cf9'})
fig6.write_html("C:/Users/senar/OneDrive/Masaüstü/Ders/bilgisayar müh geliş/Proje_new/Proje (2)/Proje/Flask/static/fig/fig6.html")

# 7. Grafik: Kredi Borcu Sayısına Göre Dağılımı
ort_Loan = veri.groupby('Credit_Score')["Num_of_Loan"].mean().reset_index()
fig7 = px.bar(ort_Loan, 
              x="Credit_Score", 
              y="Num_of_Loan", 
              title="Kredi Borcu Sayısına Göre Dağılımı",
              color='Credit_Score',
              color_discrete_map={'Poor':'#de1010', 
                                  'Standard':'#ff71fb', 
                                  'Good':'#5c8cf9'})
fig7.write_html("C:/Users/senar/OneDrive/Masaüstü/Ders/bilgisayar müh geliş/Proje_new/Proje (2)/Proje/Flask/static/fig/fig7.html")

# 8. Grafik: Kredi Gecikmiş Ödeme Sayısına Göre Dağılımı
fig8 = px.box(veri, 
              x="Credit_Score", 
              y="Num_of_Delayed_Payment", 
              title="Kredi Gecikmiş Ödeme Sayısına Göre Dağılımı",
              color='Credit_Score',
              color_discrete_map={'Poor':'#de1010', 
                                  'Standard':'#ff71fb', 
                                  'Good':'#5c8cf9'})
fig8.write_html("C:/Users/senar/OneDrive/Masaüstü/Ders/bilgisayar müh geliş/Proje_new/Proje (2)/Proje/Flask/static/fig/fig8.html")

# 9. Grafik: Ödenmemiş Kredi Borcuna Göre Dağılımı
fig9 = px.box(veri, 
              x="Credit_Score", 
              y="Outstanding_Debt", 
              title="Ödenmemiş Kredi Borcuna Göre Dağılımı",
              color='Credit_Score',
              color_discrete_map={'Poor':'#de1010', 
                                  'Standard':'#ff71fb', 
                                  'Good':'#5c8cf9'})
fig9.write_html("C:/Users/senar/OneDrive/Masaüstü/Ders/bilgisayar müh geliş/Proje_new/Proje (2)/Proje/Flask/static/fig/fig9.html")
