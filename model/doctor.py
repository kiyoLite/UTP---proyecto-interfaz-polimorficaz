class Doctor:
    def __init__(self, doctor_name: str, speciality: str, hospital_id=None, doctor_id=None):
        self._doctor_id = doctor_id
        self._doctor_name = doctor_name
        self._speciality = speciality
        self._hospital_id = hospital_id

    @property
    def doctor_id(self):
        return self._doctor_id

    @doctor_id.setter
    def doctor_id(self, value):
        self._doctor_id = value

    @property
    def doctor_name(self) -> str:
        return self._doctor_name

    @doctor_name.setter
    def doctor_name(self, value: str):
        self._doctor_name = value

    @property
    def speciality(self) -> str:
        return self._speciality

    @speciality.setter
    def speciality(self, value: str):
        self._speciality = value

    @property
    def hospital_id(self):
        return self._hospital_id

    @hospital_id.setter
    def hospital_id(self, value):
        self._hospital_id = value
