from flask import Blueprint, request, jsonify
from ai_service import ai_service
from database import kayit_ekle, tum_kayitlari_getir

api_bp = Blueprint('api', __name__, url_prefix='/api')

# 1. Sağlık Kontrolü
@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"basari": True, "durum": "Aurae Sublime AI Servisi Aktif"}), 200

# 2. AI Chatbot Endpoint'i (/api/sohbet)
@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    data = request.get_json() or {}
    mesaj = data.get('mesaj', '')
    gecmis = data.get('gecmis', [])
    
    if not mesaj:
        return jsonify({"basari": False, "hata": "Mesaj alanı boş bırakılamaz."}), 400
    
    cevap = ai_service.yanit_uret(mesaj, gecmis_mesajlar=gecmis)
    return jsonify({"basari": True, "cevap": cevap}), 200

# 3. Form Kaydı Ekleme (/api/kayit-ekle)
@api_bp.route('/kayit-ekle', methods=['POST'])
def yeni_kayit():
    data = request.get_json() or {}
    isim = data.get('isim')
    email = data.get('email')
    telefon = data.get('telefon', '')
    deneyim = data.get('deneyim', '')

    if not isim or not email:
        return jsonify({"durum": "hata", "mesaj": "İsim ve Email alanları zorunludur."}), 400

    try:
        kayit_ekle(isim, email, telefon, deneyim)
        return jsonify({"durum": "basarili", "mesaj": "Kayıt veritabanına eklendi"}), 200
    except Exception as e:
        return jsonify({"durum": "hata", "detay": str(e)}), 500

# 4. Yönetim Paneli Repeater Liste (/api/kayitlar)
@api_bp.route('/kayitlar', methods=['GET'])
def kayit_listesi():
    try:
        veriler = tum_kayitlari_getir()
        return jsonify({"durum": "basarili", "veri": veriler}), 200
    except Exception as e:
        return jsonify({"durum": "hata", "detay": str(e)}), 500