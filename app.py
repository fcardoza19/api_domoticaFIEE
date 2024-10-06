from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos de Azure MySQL con SSL
try:
    mydb = mysql.connector.connect(
        host="domoticadb.mysql.database.azure.com",
        user="admin_domoticadb",
        password="&re&KJi8j!%g(",
        database="domoticadb",
        ssl_ca='C:/Users/ferna/Descargas/DigiCertGlobalRootG2.crt.pem',  # Ruta al certificado SSL
        ssl_disabled=False
    )
    mydb.ping(reconnect=True, attempts=3, delay=5)
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

# Ruta para la página de bienvenida
@app.route('/')
def home():
    return '''
        <h1>Bienvenido a mi API</h1>
        <p>Para insertar datos, realiza una solicitud POST a /api/insertdata</p>
    '''

# Ruta para insertar datos en la base de datos
@app.route('/api/insertdata', methods=['POST'])
def insert_data():
    try:
        esp_id = request.form['esp_id']
        ldr_status = request.form['ldr_status']
        cursor = mydb.cursor()
        query = "INSERT INTO sensor_data (esp_id, ldr_status) VALUES (%s, %s)"
        cursor.execute(query, (esp_id, ldr_status))
        mydb.commit()
        print("Datos insertados correctamente")
        return "Datos insertados", 200
    except Exception as e:
        print(f"Error al insertar datos: {e}")
        return "Error al insertar datos", 500

# Ruta para obtener el último estado del sensor
@app.route('/api/getlateststatus', methods=['GET'])
def get_latest_status():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT esp_id, ldr_status, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 1")
    result = cursor.fetchone()
    return jsonify(result) if result else jsonify({"ldr_status": "No hay datos"}), 200

if __name__ == '__main__':
    app.run(debug=True)
