from model.hospital import Hospital
from persistence.icrud import ICrud
from persistence.imp_crud_hospital import ImpCrudHospital


class HospitalController:
    """
    Controlador para gestionar la lógica entre la GUI y la persistencia de Hospitales.
    Depende de la interfaz ICrud (inyección de dependencias).
    """

    def __init__(self, crud: ICrud = None):
        self.crud = crud if crud is not None else ImpCrudHospital()

    def obtener_por_id(self, id):
        if not id:
            raise ValueError("Debe ingresar un ID o nombre de hospital válido.")
        return self.crud.obtener_por_id(id)

    def agregar(self, hospital_name):
        if not hospital_name or not str(hospital_name).strip():
            raise ValueError("El nombre del hospital no puede estar vacío.")
        hospital = Hospital(str(hospital_name).strip())
        return self.crud.agregar(hospital)

    def listar_todos(self):
        return self.crud.listar_todos()

    # Alias semánticos para la GUI
    obtener_hospital_por_id = obtener_por_id
    agregar_hospital = agregar
    listar_hospitales = listar_todos
