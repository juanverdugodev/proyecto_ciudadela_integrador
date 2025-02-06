import mysql.connector
from mysql.connector import Error

# Variable global para mantener la conexión a la base de datos
connection = None

def connectionBD():
    global connection
    if connection is None or not connection.is_connected():
        print("Conectando a la base de datos...")
        try:
            connection = mysql.connector.connect(
                host="34.68.99.255",
                port=3306,
                user="Administrador_Servicios",
                passwd="@PI_2ciudadela",
                database="ciudadela",
                raise_on_warnings=True
            )
            if connection.is_connected():
                print("Conexión exitosa a la base de datos.")
        except mysql.connector.Error as error:
            print(f"No se pudo conectar a la base de datos.\nError encontrado: {error}\n")
    return connection

# Uso de la conexión de base de datos
db_connection = connectionBD()
