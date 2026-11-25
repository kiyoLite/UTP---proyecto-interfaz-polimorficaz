from model.doctor import Doctor
from model.hospital import Hospital
from .conexion import obtener_conexion
from .icrud import ICrud


class ImpCrudHospital(ICrud):

    def obtener_por_id(self, id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            if isinstance(id, int) or (isinstance(id, str) and id.isdigit()):
                cursor.execute(
                    "SELECT hospital_id, hospital_name FROM hospital WHERE hospital_id = %s",
                    (int(id),),
                )
            else:
                cursor.execute(
                    "SELECT hospital_id, hospital_name FROM hospital WHERE TRIM(hospital_name) = %s",
                    (str(id).strip(),),
                )

            fila = cursor.fetchone()
            if not fila:
                return None

            hospital_id = fila[0]
            hospital_name = fila[1].strip()
            hospital = Hospital(hospital_name, hospital_id=hospital_id)

            # Cargar doctores asociados (relación Hospital 1 <---> 1..* Doctor)
            cursor.execute(
                "SELECT doctor_id, doctor_name, speciality FROM doctor WHERE hospital_id = %s ORDER BY doctor_id",
                (hospital_id,),
            )
            for doc_fila in cursor.fetchall():
                doctor = Doctor(
                    doc_fila[1].strip(),
                    doc_fila[2].strip(),
                    hospital_id=hospital_id,
                    doctor_id=doc_fila[0],
                )
                hospital.agregar_doctor(doctor)

            return hospital
        finally:
            cursor.close()
            conexion.close()

    def agregar(self, hospital):
        if isinstance(hospital, str):
            hospital_obj = Hospital(hospital.strip())
        else:
            hospital_obj = hospital

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO hospital (hospital_name) VALUES (%s) RETURNING hospital_id;",
                (hospital_obj.hospital_name,),
            )
            nuevo_id = cursor.fetchone()[0]
            hospital_obj.hospital_id = nuevo_id

            # Si el hospital incluye doctores asociados, se insertan vinculados
            for doc in hospital_obj.doctors:
                cursor.execute(
                    "INSERT INTO doctor (hospital_id, doctor_name, speciality) VALUES (%s, %s, %s) RETURNING doctor_id;",
                    (nuevo_id, doc.doctor_name, doc.speciality),
                )
                doc.doctor_id = cursor.fetchone()[0]
                doc.hospital_id = nuevo_id

            conexion.commit()
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
                "SELECT hospital_id, hospital_name FROM hospital ORDER BY hospital_id"
            )
            filas = cursor.fetchall()
            hospitales = []
            for fila in filas:
                h_id = fila[0]
                h_name = fila[1].strip()
                hospital = Hospital(h_name, hospital_id=h_id)

                # Cargar doctores asociados de cada hospital
                cursor.execute(
                    "SELECT doctor_id, doctor_name, speciality FROM doctor WHERE hospital_id = %s ORDER BY doctor_id",
                    (h_id,),
                )
                for doc_fila in cursor.fetchall():
                    doctor = Doctor(
                        doc_fila[1].strip(),
                        doc_fila[2].strip(),
                        hospital_id=h_id,
                        doctor_id=doc_fila[0],
                    )
                    hospital.agregar_doctor(doctor)

                hospitales.append(hospital)
            return hospitales
        finally:
            cursor.close()
            conexion.close()

    # Alias en español para flexibilidad
    anadir = agregar
    listar = listar_todos
