class Hospital:
    def __init__(self, hospital_name: str, hospital_id=None):
        self._hospital_id = hospital_id
        self._hospital_name = hospital_name
        self._doctors = []

    @property
    def hospital_id(self):
        return self._hospital_id

    @hospital_id.setter
    def hospital_id(self, value):
        self._hospital_id = value

    @property
    def hospital_name(self) -> str:
        return self._hospital_name

    @hospital_name.setter
    def hospital_name(self, value: str):
        self._hospital_name = value

    @property
    def doctors(self) -> list:
        return self._doctors

    def agregar_doctor(self, doctor):
        self._doctors.append(doctor)
