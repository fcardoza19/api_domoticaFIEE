from flask import Flask, request
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos de Azure MySQL con SSL
mydb = mysql.connector.connect(
    host="domoticadb.mysql.database.azure.com",
    user="admin_domoticadb",
    password="&re&KJi8j!%g(",
    database="domoticadb",
    ssl_ca='C:/Users/ferna/Descargas/DigiCertGlobalRootG2.crt.pem',  # Ruta al certificado SSL
    ssl_disabled=False
)

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
    sensor_value = request.form['sensorValue']
    cursor = mydb.cursor()
    query = "INSERT INTO sensor_data (value) VALUES (%s)"
    cursor.execute(query, (sensor_value,))
    mydb.commit()
    return "Datos insertados", 200

if __name__ == '__main__':
    app.run(debug=True)
