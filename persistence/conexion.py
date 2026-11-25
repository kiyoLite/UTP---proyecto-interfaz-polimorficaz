import psycopg2


def obtener_conexion():
    return psycopg2.connect(
        dbname="programacion_IV",
        user="postgres",
        password="Arroz@11",
        host="localhost",
        port="5432",
    )
