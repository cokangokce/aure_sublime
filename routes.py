from flask import Blueprint, request, jsonify
from database import lead_ekle, tum_leadleri_getir
from ai_service import ai_service

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"basari": True, "durum": "Aurae Sublime AI Servisi Aktif"}), 200

@api_bp.route('/sohbet', methods=['POST'])
def sohbet():
    data = request.get_json() or {}
    mesaj = data.get('mesaj', '')
    gecmis = data.get('gecmis', [])
    
    if not mesaj:
        return jsonify({"basari": False, "hata": "Mesaj alani bos birakilamaz."}), 400
    
    cevap = ai_service.yanit_uret(mesaj, gecmis_mesajlar=gecmis)
    return jsonify({"basari": True, "cevap": cevap}), 200

@api_bp.route('/leads', methods=['POST'])
def yeni_lead():
    data = request.get_json() or {}
    isim = data.get('isim')
    telefon = data.get('telefon')
    mesaj = data.get('mesaj', '')

    if not isim or not telefon:
        return jsonify({"basari": False, "hata": "Isim ve telefon zorunludur"}), 400

    lead_ekle(isim, telefon, mesaj)
    return jsonify({"basari": True, "mesaj": "Talebiniz alinmistir. Musteri temsilcimiz en kisa surede donus yapacaktir."}), 201

@api_bp.route('/leads', methods=['GET'])
def lead_listesi():
    leadler = tum_leadleri_getir()
    return jsonify({"basari": True, "data": leadler}), 200