from .conexion import obtener_conexion
from .icrud import ICrud
from .imp_crud_doctor import ImpCrudDoctor
from .imp_crud_hospital import ImpCrudHospital

__all__ = ["ICrud", "ImpCrudDoctor", "ImpCrudHospital", "obtener_conexion"]
