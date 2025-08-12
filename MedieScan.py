from pythainlp.tokenize import word_tokenize
import torch
# ...existing code...
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

 # ข้อมูลโรคและอาการ (local AI logic)
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ข้อมูลโรคและอาการ (local AI logic)
diseases = [
    {"name": "ไข้หวัดธรรมดา", "symptoms": ["ไอ", "จาม", "คัดจมูก", "น้ำมูก", "เจ็บคอ", "มีไข้ต่ำ"], "medications": ["พาราเซตามอล", "ยาแก้ไอ", "ยาลดน้ำมูก"]},
    {"name": "ไข้หวัดใหญ่", "symptoms": ["ไข้สูง", "ปวดหัว", "ปวดกล้ามเนื้อ", "ไอ", "หนาวสั่น"], "medications": ["Oseltamivir", "พาราเซตามอล", "ยาแก้ปวดเมื่อย"]},
    {"name": "โควิด-19", "symptoms": ["ไข้", "ไอ", "เจ็บคอ", "สูญเสียกลิ่น", "หายใจลำบาก"], "medications": ["ฟ้าทะลายโจร", "Molnupiravir", "ยาลดไข้"]},
    {"name": "ไข้เลือดออก", "symptoms": ["ไข้สูง", "ปวดตา", "ผื่น", "เลือดออกง่าย"], "medications": ["พาราเซตามอล", "น้ำเกลือแร่", "พักผ่อน"]},
    {"name": "อาหารเป็นพิษ", "symptoms": ["อาเจียน", "ถ่ายเหลว", "ปวดท้อง", "คลื่นไส้"], "medications": ["ORS", "Domperidone", "ยาฆ่าเชื้อ"]},
    {"name": "กรดไหลย้อน", "symptoms": ["แสบร้อนกลางอก", "เรอเปรี้ยว", "ไอ", "แน่นหน้าอก"], "medications": ["Omeprazole", "Antacid", "Domperidone"]},
    {"name": "ไมเกรน", "symptoms": ["ปวดหัวข้างเดียว", "แพ้แสง", "คลื่นไส้"], "medications": ["Sumatriptan", "พาราเซตามอล", "ยาแก้คลื่นไส้"]},
    {"name": "หอบหืด", "symptoms": ["หายใจลำบาก", "ไอเรื้อรัง", "แน่นหน้าอก"], "medications": ["Salbutamol", "Budesonide", "Montelukast"]},
    {"name": "ท้องเสีย", "symptoms": ["ถ่ายเหลว", "ปวดท้อง", "อ่อนเพลีย"], "medications": ["ORS", "Loperamide"]},
    {"name": "ลมพิษ", "symptoms": ["ผื่น", "คัน", "บวม"], "medications": ["Cetirizine", "Loratadine"]},
    {"name": "โรคกระเพาะอาหาร", "symptoms": ["ปวดท้อง", "แสบกระเพาะ", "อาเจียน"], "medications": ["Omeprazole", "Antacid"]},
    {"name": "นิ่วในไต", "symptoms": ["ปวดหลัง", "ปัสสาวะเป็นเลือด"], "medications": ["ยาแก้ปวด", "ดื่มน้ำมาก"]},
    {"name": "เบาหวาน", "symptoms": ["ปัสสาวะบ่อย", "กระหายน้ำ", "น้ำหนักลด"], "medications": ["Metformin", "Insulin"]},
    {"name": "ความดันสูง", "symptoms": ["เวียนหัว", "มึนหัว", "ปวดท้ายทอย"], "medications": ["Amlodipine", "Losartan"]},
    {"name": "หัวใจขาดเลือด", "symptoms": ["เจ็บหน้าอก", "หายใจลำบาก"], "medications": ["Aspirin", "Nitroglycerin"]},
    {"name": "ตับอักเสบ", "symptoms": ["ตัวเหลือง", "คลื่นไส้", "ปัสสาวะสีเข้ม"], "medications": ["ยาต้านไวรัส", "พักผ่อน"]},
    {"name": "ไตวาย", "symptoms": ["บวม", "เหนื่อย", "ปัสสาวะน้อย"], "medications": ["ฟอกไต", "ยาแก้บวมน้ำ"]},
    {"name": "ไซนัสอักเสบ", "symptoms": ["แน่นจมูก", "ปวดหัว", "น้ำมูกข้น"], "medications": ["ยาลดบวม", "ยาปฏิชีวนะ"]},
    {"name": "ภูมิแพ้", "symptoms": ["จาม", "น้ำมูก", "คันจมูก"], "medications": ["Loratadine", "Cetirizine"]},
    {"name": "ต่อมทอนซิลอักเสบ", "symptoms": ["เจ็บคอ", "กลืนลำบาก", "ไข้"], "medications": ["Amoxicillin", "Paracetamol"]},
    {"name": "กระเพาะปัสสาวะอักเสบ", "symptoms": ["ปัสสาวะแสบ", "ปัสสาวะบ่อย", "ปวดท้องน้อย"], "medications": ["ยาปฏิชีวนะ", "ดื่มน้ำมาก"]},
    {"name": "มือเท้าปาก", "symptoms": ["แผลในปาก", "ผื่นที่มือและเท้า", "ไข้"], "medications": ["ยาลดไข้", "ดูแลตามอาการ"]},
    {"name": "อีสุกอีใส", "symptoms": ["ผื่นตุ่มน้ำ", "ไข้", "คัน"], "medications": ["พาราเซตามอล", "ยาทาแก้คัน", "Acyclovir"]},
    {"name": "หลอดลมอักเสบ", "symptoms": ["ไอเรื้อรัง", "เสมหะ", "แน่นหน้าอก"], "medications": ["ยาละลายเสมหะ", "ยาปฏิชีวนะ"]},
    {"name": "วัณโรค", "symptoms": ["ไอนาน", "น้ำหนักลด", "เหงื่อออกกลางคืน"], "medications": ["Isoniazid", "Rifampicin", "Ethambutol"]},
    {"name": "โรคซึมเศร้า", "symptoms": ["เบื่ออาหาร", "นอนไม่หลับ", "รู้สึกเศร้า"], "medications": ["Fluoxetine", "Sertraline"]},
    {"name": "วิตกกังวล", "symptoms": ["ใจสั่น", "เหงื่อออก", "นอนไม่หลับ"], "medications": ["Diazepam", "Alprazolam"]},
    {"name": "อัลไซเมอร์", "symptoms": ["ลืมง่าย", "หลงลืม", "สับสนเวลา"], "medications": ["Donepezil", "Memantine"]},
    {"name": "ลมชัก", "symptoms": ["ชัก", "หมดสติ", "เกร็ง"], "medications": ["Phenytoin", "Valproic acid"]},
    {"name": "เก๊าท์", "symptoms": ["ปวดข้อ", "บวมแดง", "ข้อร้อน"], "medications": ["Colchicine", "Allopurinol"]},
    {"name": "ข้อเข่าเสื่อม", "symptoms": ["ปวดข้อ", "ข้อฝืด", "เดินลำบาก"], "medications": ["Paracetamol", "Glucosamine"]},
    {"name": "กระดูกพรุน", "symptoms": ["กระดูกเปราะ", "หลังค่อม", "ปวดหลัง"], "medications": ["Calcium", "Vitamin D", "Bisphosphonate"]},
    {"name": "คออักเสบ", "symptoms": ["เจ็บคอ", "กลืนเจ็บ", "เสียงแหบ"], "medications": ["พาราเซตามอล", "ยาอมแก้เจ็บคอ"]},
    {"name": "ตาแดง", "symptoms": ["ตาแดง", "แสบตา", "น้ำตาไหล"], "medications": ["ยาหยอดตา", "Antibiotic eye drop"]},
    {"name": "กระดูกหัก", "symptoms": ["ปวดมาก", "บวม", "เคลื่อนไหวไม่ได้"], "medications": ["ใส่เฝือก", "ยาแก้ปวด"]},
    {"name": "เหน็บชา", "symptoms": ["ชาที่แขนขา", "กล้ามเนื้ออ่อนแรง"], "medications": ["Vitamin B1", "พักผ่อน"]},
    {"name": "มะเร็งปอด", "symptoms": ["ไอเรื้อรัง", "ไอเป็นเลือด", "น้ำหนักลด"], "medications": ["เคมีบำบัด", "ผ่าตัด", "ยารักษามะเร็ง"]},
    {"name": "มือชา", "symptoms": ["ชามือ", "รู้สึกเหมือนเข็มทิ่ม", "อ่อนแรง"], "medications": ["วิตามินบี", "ยาต้านอักเสบ"]},
    {"name": "ปอดบวม", "symptoms": ["ไอ", "ไข้", "หายใจหอบ"], "medications": ["ยาปฏิชีวนะ", "ยาลดไข้"]},
    {"name": "กล้ามเนื้ออักเสบ", "symptoms": ["ปวดกล้ามเนื้อ", "อ่อนแรง", "บวม"], "medications": ["ยาลดอักเสบ", "พักผ่อน"]},
    {"name": "หูน้ำหนวก", "symptoms": ["มีน้ำออกจากหู", "ปวดหู", "ได้ยินไม่ชัด"], "medications": ["ยาหยอดหู", "ยาปฏิชีวนะ"]},
    {"name": "ขาดน้ำ", "symptoms": ["ปากแห้ง", "เหนื่อย", "เวียนหัว"], "medications": ["น้ำเกลือแร่", "ดื่มน้ำมาก"]},
    {"name": "โรคประสาท", "symptoms": ["วิตกกังวล", "คิดมาก", "ปวดหัว"], "medications": ["ยาคลายเครียด", "พักผ่อน"]},
    {"name": "เครียด", "symptoms": ["นอนไม่หลับ", "หัวใจเต้นเร็ว", "หงุดหงิด"], "medications": ["Diazepam", "Sertraline"]},
    {"name": "ไส้ติ่งอักเสบ", "symptoms": ["ปวดท้องขวาล่าง", "คลื่นไส้", "เบื่ออาหาร"], "medications": ["ผ่าตัดไส้ติ่ง", "ยาแก้ปวด"]},
    {"name": "หลอดอาหารอักเสบ", "symptoms": ["แสบร้อนอก", "เจ็บเวลากลืน"], "medications": ["Omeprazole", "ยาลดกรด"]},
]

def match_disease(user_symptoms):
    input_text = user_symptoms.lower()
    tokens = word_tokenize(input_text, keep_whitespace=False)
    best_match = None
    max_match = 0
    for d in diseases:
        match_count = sum(sym in tokens for sym in d["symptoms"])
        if match_count > max_match:
            max_match = match_count
            best_match = d
    return best_match, max_match

# ฟังก์ชัน AI zero-shot classification
from transformers import pipeline
def ai_predict_disease(user_symptoms):
    candidate_labels = [d["name"] for d in diseases]
    # โหลด pipeline เฉพาะครั้งแรก (cache)
    if not hasattr(ai_predict_disease, "classifier"):
        ai_predict_disease.classifier = pipeline(
            "zero-shot-classification",
            model="lukkiddd/wangchanberta-base-att-spm-uncased"
        )
    classifier = ai_predict_disease.classifier
    result = classifier(user_symptoms, candidate_labels)
    top_label = result["labels"][0]
    score = result["scores"][0]
    # หา dict โรคที่ตรงกับ label
    best_match = next((d for d in diseases if d["name"] == top_label), None)
    return best_match, score

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <title>MEDIESCAN</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@400;700&family=Roboto:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body {
      font-family: 'Kanit', 'Roboto', Arial, sans-serif;
      background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
      min-height: 100vh;
      margin: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: flex-start;
    }
    .container {
      background: #fff;
      box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
      border-radius: 18px;
      padding: 2rem 2.5rem 2.5rem 2.5rem;
      margin-top: 40px;
      max-width: 480px;
      width: 100%;
      position: relative;
      animation: fadeIn 1s;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(30px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .header {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;a
      margin-bottom: 10px;
    }
    .header i {
      color: #007bff;
      font-size: 2.2rem;
    }
    h1 {
      font-size: 2rem;
      font-weight: 700;
      color: #007bff;
      margin: 0;
      letter-spacing: 1px;
    }
    label {
      font-size: 1.1rem;
      color: #333;
      font-weight: 500;
      margin-bottom: 8px;
      display: block;
    }
    textarea {
      width: 100%;
      min-height: 110px;
      font-size: 1.1rem;
      padding: 12px;
      border-radius: 10px;
      border: 1.5px solid #b3c6e0;
      background: #f7fbff;
      margin-bottom: 18px;
      transition: border-color 0.2s;
      box-sizing: border-box;
      resize: vertical;
    }
    textarea:focus {
      border-color: #007bff;
      outline: none;
    }
    .btn-analyze {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 13px 28px;
      font-size: 1.1rem;
      font-weight: 600;
      background: linear-gradient(90deg, #007bff 60%, #00c6ff 100%);
      color: #fff;
      border: none;
      border-radius: 10px;
      box-shadow: 0 2px 8px rgba(0,123,255,0.08);
      cursor: pointer;
      transition: background 0.2s, transform 0.1s;
      margin-bottom: 10px;
    }
    .btn-analyze:hover {
      background: linear-gradient(90deg, #0056b3 60%, #00aaff 100%);
      transform: translateY(-2px) scale(1.03);
    }
    #result {
      margin-top: 22px;
      background: linear-gradient(90deg, #e2ffe2 60%, #f7f7ff 100%);
      padding: 18px 15px;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
      white-space: pre-wrap;
      font-size: 1.08rem;
      color: #222;
      min-height: 40px;
      transition: background 0.2s;
      word-break: break-word;
    }
    .footer {
      margin-top: 40px;
      color: #888;
      font-size: 0.95rem;
      text-align: center;
      padding-bottom: 18px;
    }
    @media (max-width: 600px) {
      .container {
        padding: 1.2rem 0.7rem 1.5rem 0.7rem;
        max-width: 98vw;
      }
      h1 {
        font-size: 1.3rem;
      }
      .header i {
        font-size: 1.5rem;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <i class="fa-solid fa-stethoscope"></i>
      <h1>MEDIESCAN</h1>
    </div>
    <label for="symptoms">กรอกอาการของคุณ:</label>
    <textarea id="symptoms" placeholder="เช่น ไอ มีไข้ ปวดหัว"></textarea>
    <button class="btn-analyze" onclick="analyze()"><i class="fa-solid fa-magnifying-glass"></i> วิเคราะห์อาการ</button>
    <div style="margin-bottom: 10px;">
      <a href="/api/ai-info" target="_blank" style="display:inline-block;padding:8px 18px;background:#eaf6ff;color:#007bff;border-radius:8px;text-decoration:none;font-size:1rem;font-weight:500;box-shadow:0 1px 4px rgba(0,123,255,0.07);transition:background 0.2s;">
        <i class="fa-solid fa-robot"></i> ดูข้อมูล AI ที่ใช้งาน
      </a>
    </div>
    <div id="result">ผลลัพธ์จะแสดงที่นี่</div>
  </div>
  <div class="footer">
    &copy; 2025 MedieScan | Powered by Local AI | ออกแบบโดย ยศกร จารุพงศ์เดชา 664230027
  </div>
  <script>
    async function analyze() {
      const symptoms = document.getElementById("symptoms").value.trim();
      const resultDiv = document.getElementById("result");
      if (!symptoms) {
        resultDiv.style.background = 'linear-gradient(90deg, #ffe2e2 60%, #fff7f7 100%)';
        resultDiv.innerText = "❗ กรุณากรอกอาการก่อน";
        setTimeout(() => { resultDiv.style.background = ''; resultDiv.innerText = "ผลลัพธ์จะแสดงที่นี่"; }, 1800);
        return;
      }
      resultDiv.style.background = 'linear-gradient(90deg, #e0eaff 60%, #f7f7ff 100%)';
      resultDiv.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> กำลังวิเคราะห์... กรุณารอสักครู่';
      try {
        const response = await fetch("/api/analyze", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ symptoms }),
        });
        const data = await response.json();
        resultDiv.style.background = 'linear-gradient(90deg, #e2ffe2 60%, #f7f7ff 100%)';
        resultDiv.innerText = data.result;
      } catch (error) {
        resultDiv.style.background = 'linear-gradient(90deg, #ffe2e2 60%, #fff7f7 100%)';
        resultDiv.innerText = "เกิดข้อผิดพลาด: " + error.message;
      }
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/analyze", methods=["POST"])
def analyze_symptoms():
    data = request.get_json()
    symptoms = data.get("symptoms", "")
    use_ai = data.get("use_ai", False)  # ให้เลือกใช้ AI หรือ rule-based

    if not symptoms:
        return jsonify({ "result": "❗ กรุณากรอกอาการ" }), 400

    if use_ai:
        try:
            best_match, score = ai_predict_disease(symptoms)
            if best_match and score > 0.3:
                meds = ', '.join(best_match.get('medications', []))
                result = (
                    f"🤖 AI คาดว่าอาจเป็น: {best_match['name']}\n"
                    f"ความมั่นใจ: {score:.2f}\n"
                    f"ยาแนะนำ: {meds}\n"
                    f"อาการของคุณ: {symptoms}"
                )
            else:
                result = "❗ AI ไม่สามารถวิเคราะห์อาการได้ โปรดลองใหม่"
        except Exception as e:
            result = f"เกิดข้อผิดพลาด AI: {str(e)}"
    else:
        best_match, max_match = match_disease(symptoms)
        if best_match and max_match > 0:
            meds = ', '.join(best_match.get('medications', []))
            result = (
                f"🦠 คาดว่าอาจเป็น: {best_match['name']}\n"
                f"ยาแนะนำ: {meds}\n"
                f"อาการของคุณ: {symptoms}"
            )
        else:
            result = "❗ ไม่สามารถวิเคราะห์อาการได้ โปรดลองใหม่"
    return jsonify({ "result": result })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051, debug=False)

# เพิ่ม API สำหรับแสดงข้อมูล AI ที่ใช้งานในระบบ
@app.route("/api/ai-info", methods=["GET"])
def ai_info():
    info = [
        {
            "name": "WangchanBERTa (zero-shot classification)",
            "description": "AI วิเคราะห์อาการโดยไม่ต้องเทรนเอง ใช้โมเดล lukkiddd/wangchanberta-base-att-spm-uncased จาก Hugging Face",
            "usage": "ส่ง use_ai=true ใน API /api/analyze เพื่อใช้งาน AI นี้"
        },
        {
            "name": "Rule-based matching",
            "description": "จับคู่อาการกับฐานข้อมูลโรคแบบตรงตัว ไม่ใช้ AI",
            "usage": "ส่ง use_ai=false หรือไม่ส่งใน API /api/analyze เพื่อใช้งานแบบ rule-based"
        }
    ]
    return jsonify({"ai_list": info})
