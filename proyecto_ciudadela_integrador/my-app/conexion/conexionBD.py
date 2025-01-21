import mysql.connector
from mysql.connector import Error

def connectionBD():
    print("Conectando a la base de datos...")
    try:
        connection = mysql.connector.connect(
            host="34.68.99.255",
            port=3306,
            user="Administrador",
            passwd="PI_ciudadela",
            database="ciudadela",
            raise_on_warnings=True
        )
        
        if connection.is_connected():
            print("Conexión exitosa a la base de datos.")
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar a la base de datos.\nError encontrado: {error}\n")