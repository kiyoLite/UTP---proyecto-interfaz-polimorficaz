from model.doctor import Doctor
from .conexion import obtener_conexion
from .icrud import ICrud


class ImpCrudDoctor(ICrud):

    def obtener_por_id(self, id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT doctor_id, doctor_name, speciality, hospital_id FROM doctor WHERE doctor_id = %s",
                (id,),
            )
            fila = cursor.fetchone()
            if fila:
                return Doctor(fila[1].strip(), fila[2].strip(), hospital_id=fila[3], doctor_id=fila[0])
            return None
        finally:
            cursor.close()
            conexion.close()

    def agregar(self, doctor, hospital_id=None):
        h_id = hospital_id if hospital_id is not None else getattr(doctor, "hospital_id", None)
        if h_id is None:
            raise ValueError("Se requiere hospital_id para asociar el doctor al hospital.")

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO doctor (hospital_id, doctor_name, speciality) VALUES (%s, %s, %s) RETURNING doctor_id;",
                (h_id, doctor.doctor_name, doctor.speciality),
            )
            nuevo_id = cursor.fetchone()[0]
            conexion.commit()
            doctor.doctor_id = nuevo_id
            doctor.hospital_id = h_id
            return nuevo_id
        except Exception:
            conexion.rollback()
            raise
        finally:
            cursor.close()
            conexion.close()

    def listar_todos(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT doctor_id, doctor_name, speciality, hospital_id FROM doctor ORDER BY doctor_id"
            )
            filas = cursor.fetchall()
            return [
                Doctor(f[1].strip(), f[2].strip(), hospital_id=f[3], doctor_id=f[0])
                for f in filas
            ]
        finally:
            cursor.close()
            conexion.close()

    # Alias en español para flexibilidad
    anadir = agregar
    listar = listar_todos
