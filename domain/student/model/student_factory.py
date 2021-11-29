from domain.student.model.student import Student
from infrastructure.student.student_exceptions import StudentNotFoundException


class StudentFactory:
    def __init__(self,
                 student_repo):
        self.__student_repo = student_repo

    def student_create(self, name, surname, tel):
        student = Student(name=name, surname=surname, tel=tel)

        return student

    def student_to_update(self, _id, name, surname, tel):
        student = self.__student_repo.get_by_id(_id)
        if not student:
            raise StudentNotFoundException(_id)

        student.name = name
        student.surname = surname
        student.tel = tel

        return student
