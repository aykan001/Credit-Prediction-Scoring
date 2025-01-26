from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import numpy as np
import pandas as pd
import joblib
import os
import re
import firebase_admin
from firebase_admin import auth, credentials, firestore

# Flask uygulamasını başlat
app = Flask(__name__)
app.secret_key = "supersecret"

# Firebase yapılandırması
cred = credentials.Certificate("C:\\Users\\aykan\\Desktop\\Proje\\Flask\\kredinotutahmin-firebase-adminsdk-jbjua-76c8a75603.json")
firebase_admin.initialize_app(cred)

# Firebase Firestore referansı
db = firestore.client()

# Modeli yükle
model = joblib.load('C:\\Users\\aykan\\Desktop\\Proje\\xgboost_model.pkl')  # Model dosyasını burada belirtin


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user_ref = db.collection('users').document(email)
            user_doc = user_ref.get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                if user_data.get('password') == password:
                    session['email'] = email
                    return redirect(url_for('predict'))
                else:
                    flash('Email veya şifre yanlış!', 'danger')
            else:
                flash('Kullanıcı verisi bulunamadı!', 'danger')
        except Exception as e:
            flash(f'Firebase hatası veya başka bir hata: {str(e)}', 'danger')

    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Kullanıcı adı kontrolü: Sadece harf ve rakamlardan oluşmalı, en az bir harf ve rakam içermeli, uzunluğu max 11
        username_pattern = r"^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{1,11}$"
        if not re.match(username_pattern, username):
            flash('Kullanıcı adı yalnızca harf ve rakamlardan oluşmalı, en az bir harf ve rakam içermeli ve 11 karakterden uzun olmamalı!', 'danger')
            return redirect(url_for('register'))

        # E-posta kontrolü: @gmail.com ile bitmeli
        if not email.endswith("@gmail.com"):
            flash('Lütfen geçerli bir e-posta adresi girin! (Örnek: example@gmail.com)', 'danger')
            return redirect(url_for('register'))

        # Kullanıcı adı ve şifre doğrulama
        if password != confirm_password:
            flash('Şifreler uyuşmuyor!', 'danger')
            return redirect(url_for('register'))

        # Firebase'de kullanıcı adı kontrolü
        user_ref = db.collection('users').document(email)
        user_doc = user_ref.get()

        if user_doc.exists:
            flash('Bu e-posta adresi zaten kayıtlı!', 'danger')
        else:
            # Firebase Firestore'a kullanıcı ekle
            user_ref.set({
                'email': email,'password': password})
            flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
            return render_template('login.html')

    return render_template("register.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Kullanıcı giriş kontrolü
    if 'email' not in session:
        flash('Lütfen giriş yapın!', 'danger')
        return redirect(url_for('login'))  # Giriş yapılmadıysa login sayfasına yönlendir

    if request.method == "POST":
        try:
            # Formdan gelen verileri al
            form_data = request.form.to_dict()
            current_month = datetime.now().month

            def create_occupation_map(file_path):
                occupation_map = {}
                # Dosyayı UTF-8 ile açıyoruz
                with open(file_path, 'r', encoding='utf-8') as f:
                    for idx, line in enumerate(f.readlines()):
                        line = line.strip()  # Fazladan satır karakterlerini temizle
                        if line:  # Boş satır kontrolü
                            occupation_map[line] = idx + 1  # Kategoriyi 1, 2, 3 gibi ata
                return occupation_map

            file_path = os.path.join(app.static_folder, 'meslekler.txt')
            occupation_map = create_occupation_map(file_path)

            # Occupation değerini temizlemek için strip
            form_data['Occupation'] = form_data.get('Occupation', '').strip()

            # Verileri işleme
            input_data = {
                'Month': current_month,
                'Age': int(form_data.get('Age', -1)),
                'SSN': int(form_data.get('SSN', -1)),
                'Occupation': occupation_map.get(form_data.get('Occupation', ''), -1),
                'Annual_Income': float(form_data.get('Annual_Income', -1)),
                'Monthly_Inhand_Salary': float(form_data.get('Monthly_Inhand_Salary', -1)),
                'Num_Bank_Accounts': int(form_data.get('Num_Bank_Accounts', -1)),
                'Num_Credit_Card': int(form_data.get('Num_Credit_Card', -1)),
                'Interest_Rate': float(3.11),
                'Num_of_Loan': int(form_data.get('Num_of_Loan', -1)),
                'Delay_from_due_date': int(form_data.get('Delay_from_due_date', -1)),
                'Outstanding_Debt': float(form_data.get('Outstanding_Debt', -1)),
                'Amount_invested_monthly': float(form_data.get('Amount_invested_monthly', -1))
            }

            if -1 in input_data.values():
                return "Eksik veya hatalı kategori girdisi!"
            
            # DataFrame oluştur
            input_df = pd.DataFrame([input_data])

            # Sonuç mesajı
            credit_score_map = {0: 'Poor', 1: 'Standard', 2: 'Good'}
            
            # Model tahminini al
            prediction = model.predict(input_df)
            
            # prediction değerini kontrol et
            if isinstance(prediction, (list, np.ndarray)):  # Eğer liste ya da array ise
                prediction = prediction[0]  # İlk değeri al
            else:
                prediction = int(prediction)  # Eğer tek bir değer dönerse, bunu int'e çevir
            
            # Tahmini sonucu al
            result = credit_score_map.get(prediction, 'Unknown')
            
            # Sonuçları Firestore'a kaydet
            result_data = {
                'email': session['email'],
                'result': result,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'form_data': form_data
            }
            
            db.collection('credit_results').add(result_data)


            # Sonuçları session'a kaydet
            session['prediction_result'] = result
            session['form_data'] = form_data

            return redirect(url_for('conclusion'))

        except Exception as e:
            flash(f"Bir hata oluştu: {e}", "danger")

    return render_template("predict.html")


@app.route('/conclusion', methods=['GET', 'POST'])
def conclusion():
    if 'email' not in session:
        flash('Lütfen giriş yapın!', 'danger')
        return redirect(url_for('login'))

    result = session.pop('prediction_result', 'Bilinmiyor')
    form_data = session.pop('form_data', {})
    tc = form_data.pop('SSN', 'Bilinmiyor')
    monthly_payment = form_data.pop('Monthly_Inhand_Salary', 'Bilinmiyor')

    box_color = 'bg-danger' if result == 'Poor' else 'bg-warning' if result == 'Standard' else 'bg-success'

    return render_template("conclusion.html", result=result, form_data=form_data, tc=tc, monthly_payment=monthly_payment, box_color=box_color)

@app.route('/portfoy', methods=['GET', 'POST'])
def portfoy():
    if 'email' not in session:
        flash('Lütfen giriş yapın!', 'danger')
        return redirect(url_for('login'))

    # Burada portföyle ilgili veriler veya işlemler yapılabilir
    # Örneğin, kullanıcının portföy bilgilerini Firestore'dan çekebilirsiniz.
    # Örnek bir veri çekme işlemi:
    user_portfoy = db.collection('users').document(session['email']).get()

    if user_portfoy.exists:
        portfoy_data = user_portfoy.to_dict()
    else:
        portfoy_data = {}

    return render_template("portfoy.html", portfoy_data=portfoy_data)



@app.route('/past_credit_forecast', methods=['GET', 'POST'])
def past_credit_forecast():
    # Geçmiş sonuçları al
    user_results = db.collection('credit_results').where('email', '==', session['email']).stream()

    results = []
    for result in user_results:
        result_data = result.to_dict()
        result_data['id'] = result.id  # Belge ID'sini kaydediyoruz
        results.append(result_data)

    return render_template('past_credit_forecast.html', results=results)


@app.route('/delete_result/<result_id>', methods=['POST'])
def delete_result(result_id):
    try:
        db.collection('credit_results').document(result_id).delete()
        flash('Sonuç başarıyla silindi!', 'success')
    except Exception as e:
        flash(f"Silme hatası: {str(e)}", 'danger')

    return redirect(url_for('past_credit_forecast'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    flash('Başarıyla çıkış yaptınız!', 'success')
    return render_template('login.html')


if __name__ == "__main__":
    app.run(port=8080, debug=True)
