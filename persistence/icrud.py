from abc import ABC, abstractmethod


class ICrud(ABC):

    @abstractmethod
    def obtener_por_id(self, id):
        pass

    @abstractmethod
    def agregar(self, entidad):
        pass

    @abstractmethod
    def listar_todos(self):
        pass
