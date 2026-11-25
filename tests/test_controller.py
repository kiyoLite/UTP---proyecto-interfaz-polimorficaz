import unittest
from controller.hospital_controller import HospitalController
from controller.doctor_controller import DoctorController
from persistence.icrud import ICrud
from model.hospital import Hospital
from model.doctor import Doctor


class MockCrud(ICrud):
    """
    Mock que implementa ICrud para verificar que los controladores
    dependen de la abstracción ICrud y no están acoplados directamente.
    """

    def __init__(self):
        self.datos = []

    def obtener_por_id(self, id):
        for item in self.datos:
            if getattr(item, "id", None) == id or getattr(item, "hospital_id", None) == id:
                return item
        return None

    def agregar(self, entidad, **kwargs):
        self.datos.append(entidad)
        return 999

    def listar_todos(self):
        return list(self.datos)


class TestController(unittest.TestCase):
    """
    Pruebas unitarias para la capa de controladores (Controller).
    Evalúa validaciones de entrada de la GUI e inyección de dependencias hacia ICrud.
    """

    def test_hospital_controller_validaciones(self):
        controller = HospitalController()
        # Nombre vacío debe levantar ValueError
        with self.assertRaises(ValueError):
            controller.agregar("")
        with self.assertRaises(ValueError):
            controller.agregar("   ")
        # ID vacío en consulta debe levantar ValueError
        with self.assertRaises(ValueError):
            controller.obtener_por_id("")

    def test_doctor_controller_validaciones(self):
        controller = DoctorController()
        # Falta de datos requeridos debe levantar ValueError
        with self.assertRaises(ValueError):
            controller.agregar("", "Cardiologia", 1)
        with self.assertRaises(ValueError):
            controller.agregar("Dr. Carlos", "", 1)
        with self.assertRaises(ValueError):
            controller.agregar("Dr. Carlos", "Cardiologia", None)

    def test_inyeccion_dependencias_con_mock(self):
        """
        Demuestra la arquitectura desacoplada: el controlador funciona con cualquier
        implementación de ICrud (principio de Inversión de Dependencias).
        """
        mock_crud = MockCrud()
        mock_h = Hospital("Hospital Mock", hospital_id=999)
        mock_crud.datos.append(mock_h)

        controller = HospitalController(crud=mock_crud)
        resultado = controller.obtener_por_id(999)
        self.assertEqual(resultado.hospital_name, "Hospital Mock")

        lista = controller.listar_todos()
        self.assertEqual(len(lista), 1)

    def test_controladores_con_persistencia_real(self):
        hc = HospitalController()
        dc = DoctorController()

        hospitals = hc.listar_todos()
        self.assertIsInstance(hospitals, list)

        doctors = dc.listar_todos()
        self.assertIsInstance(doctors, list)


if __name__ == "__main__":
    unittest.main()
