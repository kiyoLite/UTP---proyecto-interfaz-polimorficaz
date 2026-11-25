from model.doctor import Doctor
from persistence.icrud import ICrud
from persistence.imp_crud_doctor import ImpCrudDoctor


class DoctorController:
    """
    Controlador para gestionar la lógica entre la GUI y la persistencia de Doctores.
    Depende de la interfaz ICrud (inyección de dependencias).
    """

    def __init__(self, crud: ICrud = None):
        self.crud = crud if crud is not None else ImpCrudDoctor()

    def obtener_por_id(self, id):
        if not id:
            raise ValueError("Debe ingresar un ID de doctor válido.")
        return self.crud.obtener_por_id(id)

    def agregar(self, doctor_name, speciality, hospital_id):
        if not doctor_name or not str(doctor_name).strip():
            raise ValueError("El nombre del doctor no puede estar vacío.")
        if not speciality or not str(speciality).strip():
            raise ValueError("La especialidad no puede estar vacía.")
        if not hospital_id:
            raise ValueError("Debe especificar el hospital_id asociado.")

        doctor = Doctor(
            doctor_name=str(doctor_name).strip(),
            speciality=str(speciality).strip(),
            hospital_id=int(hospital_id),
        )
        return self.crud.agregar(doctor, hospital_id=int(hospital_id))

    def listar_todos(self):
        return self.crud.listar_todos()

    # Alias semánticos para la GUI
    obtener_doctor_por_id = obtener_por_id
    agregar_doctor = agregar
    listar_doctores = listar_todos
