import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Configuración del correo (usar variables de entorno en Railway)
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "sabogaljulian27@gmail.com")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "ulwj vcpo tfal tdoi")
EMAIL_RECEIVER = os.environ.get("EMAIL_RECEIVER", "sabogaljulian27@gmail.com")

@app.route('/')
def home():
    return "¡Hola desde vercel!"

@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    msg = EmailMessage()
    msg["Subject"] = f"Nuevo mensaje de {name}"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content(f"Nombre: {name}\nEmail: {email}\nMensaje: {message}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        return jsonify({"message": "Correo enviado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usa el puerto asignado por Railway
    app.run(host='0.0.0.0', port=port)
