import unittest
from persistence import ImpCrudDoctor, ImpCrudHospital, obtener_conexion
from model.doctor import Doctor
from model.hospital import Hospital


class TestPersistence(unittest.TestCase):
    """
    Pruebas unitarias e integración para el componente Persistence (ICrud).
    Evalúa consultas, inserciones y la integridad relacional con PostgreSQL.
    """

    def setUp(self):
        self.crud_doctor = ImpCrudDoctor()
        self.crud_hospital = ImpCrudHospital()

    def test_listar_todos_hospitales(self):
        hospitales = self.crud_hospital.listar_todos()
        self.assertIsInstance(hospitales, list)
        self.assertGreater(len(hospitales), 0)
        primer_h = hospitales[0]
        self.assertIsInstance(primer_h, Hospital)
        self.assertTrue(hasattr(primer_h, "hospital_name"))

    def test_listar_todos_doctores(self):
        doctores = self.crud_doctor.listar_todos()
        self.assertIsInstance(doctores, list)
        self.assertGreater(len(doctores), 0)
        primer_d = doctores[0]
        self.assertIsInstance(primer_d, Doctor)
        self.assertTrue(hasattr(primer_d, "doctor_name"))

    def test_obtener_por_id_hospital(self):
        # Consultar por ID 1 existente
        hospital = self.crud_hospital.obtener_por_id(1)
        self.assertIsNotNone(hospital)
        self.assertEqual(hospital.hospital_id, 1)
        self.assertIsInstance(hospital.hospital_name, str)
        # Verificar que carga sus doctores asociados (composición 1..*)
        self.assertIsInstance(hospital.doctors, list)

    def test_obtener_por_id_doctor(self):
        # Tomar el primer doctor disponible y buscarlo por su ID
        todos = self.crud_doctor.listar_todos()
        if todos:
            primer_id = todos[0].doctor_id
            doctor = self.crud_doctor.obtener_por_id(primer_id)
            self.assertIsNotNone(doctor)
            self.assertEqual(doctor.doctor_id, primer_id)

    def test_agregar_y_limpieza_hospital_y_doctor(self):
        """
        Prueba la inserción de Hospital y Doctor, y limpia los datos de prueba.
        """
        nuevo_hospital = Hospital("Hospital de Pruebas Unitarias")
        nuevo_hospital.agregar_doctor(Doctor("Dr. Test 1", "Medicina General"))

        # Guardar hospital con doctor compuesto
        h_id = self.crud_hospital.agregar(nuevo_hospital)
        self.assertIsInstance(h_id, int)

        # Consultar hospital creado
        h_recuperado = self.crud_hospital.obtener_por_id(h_id)
        self.assertIsNotNone(h_recuperado)
        self.assertEqual(len(h_recuperado.doctors), 1)

        # Guardar un doctor adicional asociado a este hospital
        d_id = self.crud_doctor.agregar(Doctor("Dr. Test 2", "Infectologia"), hospital_id=h_id)
        self.assertIsInstance(d_id, int)

        # Limpiar registros creados durante la prueba
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("DELETE FROM doctor WHERE hospital_id = %s", (h_id,))
        cur.execute("DELETE FROM hospital WHERE hospital_id = %s", (h_id,))
        conn.commit()
        conn.close()


if __name__ == "__main__":
    unittest.main()
