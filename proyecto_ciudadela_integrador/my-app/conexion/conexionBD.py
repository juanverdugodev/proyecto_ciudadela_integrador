

# Importando Libreria mysql.connector para conectar Python con MySQL
import mysql.connector


def connectionBD():
    print("ENTRO A LA CONEXION")
    try:
        # connection = mysql.connector.connect(
        connection = mysql.connector.connect(
            host="34.68.99.255",
                #host="viaduct.proxy.rlwy.net",
            port=3306,
            user="Administrador",
            passwd="PI_ciudadela",
                #passwd="-D2eD6aDb5Bg6dEbhAAeBB6gd3EheaBg",
            database="ciudadela",
                #database="crud_python",
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            raise_on_warnings=True

        )
        if connection.is_connected():
            print("Conexión exitosa a la BD")
            return connection

    except mysql.connector.Error as error:
        print(f"No se pudo conectar: {error}")
