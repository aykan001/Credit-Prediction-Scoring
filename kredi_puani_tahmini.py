#Gerekli kütüphanelerin yüklenmesi
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp

#veri okuma işlemi
veri = pd.read_csv("veri.csv")
print(veri) #Verinin hepsi
print(veri.head()) #ilk 5 satır
print(veri.info())  #veri hakkında bilgi
#print(veri.isnull().sum()) #veride boş değer yok

#-----------------------------------GRAFİK OLUŞTURMA VE GÖSTERME-----------------------------------------

# Kredi puanı dağılımını sayma
counts = veri.groupby(['Occupation', 'Credit_Score']).size().reset_index(name='Count')
# Sütun grafiği oluşturma
fig1 = px.bar(counts, 
x='Occupation', 
y='Count', 
color='Credit_Score', 
title='Kredi Puanının Mesleklere Göre Dağılımı',
color_discrete_map={'Poor':'#de1010', 
                    'Standard':'#ff71fb', 
                    'Good':'#5c8cf9'})

fig1.show()

#-----------------------------------------------------------------------------------------------------------
fig = sp.make_subplots(rows=1, cols=2, subplot_titles=('Kredi Puanının Aylık Maaşa Göre Dağılımı',
                                                        'Kredi Puanının Yıllık Gelire Göre Dağılımı'))
#Kutu Grafiği
fig2 = px.box(veri, 
x="Credit_Score", 
y="Monthly_Inhand_Salary",
color = "Credit_Score",
title="Kredi Puanının Aylık Maaşa Göre Dağılımı",
color_discrete_map={'Poor':'#de1010', 
                    'Standard':'#ff71fb', 
                    'Good':'#5c8cf9'})
for trace in fig2.data:
    fig.add_trace(trace, row=1, col=1)

#Kutu Grafiği
fig3 = px.box(veri,
x ='Credit_Score',
y ='Annual_Income',
title='Kredi Puanının Yıllık Gelire Göre Dağılımı',
color = 'Credit_Score',
color_discrete_map={'Poor':'#de1010', 
                    'Standard':'#ff71fb', 
                    'Good':'#5c8cf9'})
for trace in fig3.data:
    fig.add_trace(trace, row=1, col=2)

# Grafiği gösterme
fig.update_layout(title_text="Kredi Puanı Kutu Grafikleri", showlegend=False)
fig.show()

#-------------------------------------------------------------------------------------------------------------
fig_bank = sp.make_subplots(rows=2, cols=2,subplot_titles =('Banka Hesap Sayısına Göre Dağılımı',
                                                            'Kredi Karta Sahip Olma Sayısına Göre Dağılımı',
                                                            'Faiz Oranına Göre Dağılımı',
                                                            'Kredi Borcu Sayısına Göre Dağılımı'
                                                            ))
#Ortalama hesap sayıları alma
ort_bank_account = veri.groupby('Credit_Score')['Num_Bank_Accounts'].mean().reset_index()
#Sütün Grafiği
fig4 = px.bar(ort_bank_account, 
x='Credit_Score',
y='Num_Bank_Accounts', 
title='Banka Hesap Sayısına Göre Dağılımı',
color='Credit_Score',
color_discrete_map={'Poor':'#de1010', 
                    'Standard':'#ff71fb', 
                    'Good':'#5c8cf9'})
for trace in fig4.data:
    fig_bank.add_trace(trace,row=1,col=1)

#Ortalama kredi kart sayıları alma
ort_credit_cart = veri.groupby('Credit_Score')['Num_Credit_Card'].mean().reset_index()
#Sütün Grafiği
fig5= px.bar(ort_credit_cart, 
x='Credit_Score',
y='Num_Credit_Card', 
title='Kredi Karta Sahip Olma Sayısına Göre Dağılımı',
color='Credit_Score',
color_discrete_map={'Poor':'#de1010', 
                    'Standard':'#ff71fb', 
                    'Good':'#5c8cf9'})
for trace in fig5.data:
    fig_bank.add_trace(trace,row=1,col=2)


ort_interest = veri.groupby('Credit_Score')["Interest_Rate"].mean().reset_index()
fig6=px.bar(ort_interest,
x="Credit_Score",
y='Interest_Rate',
title="Faiz Oranına Göre Dağılımı",
color='Credit_Score',
color_discrete_map={'Poor':'#de1010', 
                    'Standard':'#ff71fb', 
                    'Good':'#5c8cf9'})
for trace in fig6.data:
    fig_bank.add_trace(trace,row=2,col=1)


ort_Loan = veri.groupby('Credit_Score')["Num_of_Loan"].mean().reset_index()
fig7=px.bar(ort_Loan,
x="Credit_Score",
y='Num_of_Loan',
title="Kredi Borcu Sayısına Göre Dağılımı",
color='Credit_Score',
color_discrete_map={'Poor':'#de1010', 
                    'Standard':'#ff71fb', 
                    'Good':'#5c8cf9'})
for trace in fig7.data:
    fig_bank.add_trace(trace,row=2,col=2)

fig.update_layout(title_text="Kredi Puanının ; ", showlegend=False)
fig_bank.show()

fig_g = sp.make_subplots(rows=2, cols=2,subplot_titles=('Kredi Ödemelerinde Gecikme Günlerinin Ortalama Sayısına Göre Dağılımı',
                                                    'Kredi Gecikmiş Ödeme Sayısına Göre Dağılımı',
                                                    'Ödenmemiş Kredi Borcuna Göre Dağılımı',
                                                    'Kredi Geçmiş Yaşına Göre Dağılımı'))

fig8 = px.box(veri,
x="Credit_Score",
y="Delay_from_due_date",
title="Kredi Ödemelerinde Gecikme Günlerinin Ortalama Sayısına Göre Dağılımı",
color='Credit_Score',
color_discrete_map={'Poor':'#de1010', 
                    'Standard':'#ff71fb', 
                    'Good':'#5c8cf9'})
for trace in fig8.data:
    fig_g.add_trace(trace, row=1,col=1)

fig9 = px.box(veri,
x="Credit_Score",
y="Num_of_Delayed_Payment",
title="Kredi Gecikmiş Ödeme Sayısına Göre Dağılımı",
color='Credit_Score',
color_discrete_map={'Poor':'#de1010', 
                    'Standard':'#ff71fb', 
                    'Good':'#5c8cf9'})
for trace in fig9.data:
    fig_g.add_trace(trace, row=1,col=2)

fig10 = px.box(veri,
x="Credit_Score",
y="Outstanding_Debt",
title="Ödenmemiş Kredi Borcuna Göre Dağılımı",
color='Credit_Score',
color_discrete_map={'Poor':'#de1010', 
                    'Standard':'#ff71fb', 
                    'Good':'#5c8cf9'})
for trace in fig10.data:
    fig_g.add_trace(trace, row=2,col=1)

fig11 = px.box(veri,
x="Credit_Score",
y="Credit_History_Age",
title="Kredi Geçmiş Yaşına Göre Dağılımı",
color='Credit_Score',
color_discrete_map={'Poor':'#de1010', 
                    'Standard':'#ff71fb', 
                    'Good':'#5c8cf9'})
for trace in fig11.data:
    fig_g.add_trace(trace, row=2,col=2)

fig_g.show()