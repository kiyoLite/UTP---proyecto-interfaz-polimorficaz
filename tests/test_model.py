import unittest
from model.doctor import Doctor
from model.hospital import Hospital


class TestModel(unittest.TestCase):
    """
    Pruebas unitarias para las entidades del Componente de Modelo.
    Evalúa la creación de instancias, encapsulamiento y composición de objetos.
    """

    def test_creacion_doctor(self):
        doctor = Doctor(doctor_name="Dr. Juan Perez", speciality="Pediatria", hospital_id=1, doctor_id=100)
        self.assertEqual(doctor.doctor_name, "Dr. Juan Perez")
        self.assertEqual(doctor.speciality, "Pediatria")
        self.assertEqual(doctor.hospital_id, 1)
        self.assertEqual(doctor.doctor_id, 100)

    def test_modificar_atributos_doctor(self):
        doctor = Doctor(doctor_name="Dr. Ana Lopez", speciality="Neurologia")
        doctor.doctor_name = "Dra. Ana Maria Lopez"
        doctor.speciality = "Neurocirugia"
        self.assertEqual(doctor.doctor_name, "Dra. Ana Maria Lopez")
        self.assertEqual(doctor.speciality, "Neurocirugia")

    def test_creacion_hospital(self):
        hospital = Hospital(hospital_name="Hospital San Vicente", hospital_id=5)
        self.assertEqual(hospital.hospital_name, "Hospital San Vicente")
        self.assertEqual(hospital.hospital_id, 5)
        self.assertEqual(len(hospital.doctors), 0)

    def test_composicion_hospital_doctores(self):
        """
        Verifica la relación de composición Hospital (1) <---> (1..*) Doctor.
        """
        hospital = Hospital(hospital_name="Hospital Universitario")
        doc1 = Doctor("Dr. Roberto Gomez", "Cardiologia")
        doc2 = Doctor("Dra. Sofia Diaz", "Dermatologia")

        hospital.agregar_doctor(doc1)
        hospital.agregar_doctor(doc2)

        self.assertEqual(len(hospital.doctors), 2)
        self.assertIn(doc1, hospital.doctors)
        self.assertIn(doc2, hospital.doctors)
        self.assertEqual(hospital.doctors[0].doctor_name, "Dr. Roberto Gomez")


if __name__ == "__main__":
    unittest.main()
