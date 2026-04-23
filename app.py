import iyzipay
import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

config = {
    'api_key': 'API_ANAHTARI_BURAYA',
    'secret_key': 'GIZLI_ANAHTAR_BURAYA',
    'base_url': 'https://sandbox-api.iyzipay.com' 
}

@app.route('/odeme-formu-al', methods=['POST'])
def get_payment_form():
    data = request.get_json(silent=True) or {}
    try:
        raw_price = float(data.get('price', 100.0))
    except (ValueError, TypeError):
        raw_price = 100.0
    
    sepet_tutari = str(raw_price)

    request_data = {
        'locale': 'tr',
        'conversationId': '123456789',
        'price': sepet_tutari,
        'paidPrice': sepet_tutari,
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        'callbackUrl': 'http://127.0.0.1:5000/odeme-sonuc',
        'buyer': {
            'id': 'BY789',
            'name': 'MusteriAd',
            'surname': 'MusteriSoyad',
            'email': 'email@ornek.com',
            'identityNumber': '11111111111',
            'registrationAddress': 'Musteri Kayit Adresi',
            'city': 'Sehir',
            'country': 'Turkey'
        },
        'shippingAddress': {
            'contactName': 'Teslimat Ad Soyad',
            'city': 'Sehir',
            'country': 'Turkey',
            'address': 'Teslimat Adresi'
        },
        'billingAddress': {
            'contactName': 'Fatura Ad Soyad',
            'city': 'Sehir',
            'country': 'Turkey',
            'address': 'Fatura Adresi'
        },
        'basketItems': [
            {
                'id': 'BI101',
                'name': 'Shopypet Siparis',
                'category1': 'Evcil Hayvan Urunleri',
                'itemType': 'PHYSICAL',
                'price': sepet_tutari
            }
        ]
    }
    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request_data, config)
    return jsonify(json.loads(checkout_form_initialize.read().decode('utf-8')))

@app.route('/odeme-sonuc', methods=['POST'])
def payment_result():
    token = request.form.get('token')
    result_data = {'locale': 'tr', 'conversationId': '123456789', 'token': token}
    checkout_form = iyzipay.CheckoutForm().retrieve(result_data, config)
    result = json.loads(checkout_form.read().decode('utf-8'))
    if result.get('paymentStatus') == 'SUCCESS':
        return """
        <div style="font-family:-apple-system,sans-serif; text-align:center; margin-top:100px;">
            <h1 style="color:#00c853; font-size:48px;">✓</h1>
            <h2>Ödeme Başarıyla Tamamlandı!</h2>
            <p>Shopypet siparişiniz yola çıkmak için hazırlanıyor.</p>
        </div>
        """
    return f"<h1 style='color:red;'>Ödeme Başarısız: {result.get('errorMessage')}</h1>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)