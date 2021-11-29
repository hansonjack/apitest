from infrastructure.student.student_repository import StudentRepository
from domain.student.model.student_factory import StudentFactory


class StudentController:

    def __init__(self):
        self.__student_repo = StudentRepository()
        self.__student_factory = StudentFactory(self.__student_repo)

    def get_student_list(self):
        return self.__student_repo.get_all()

    def get_student(self, _id):
        return self.__student_repo.get_by_id(_id)

    def create_student(self, name, surname, tel):
        new_student = self.__student_factory.student_create(name, surname, tel)
        self.__student_repo.save(new_student)
        return new_student

    def update_student(self, _id, name, surname, tel):
        student = self.__student_factory.student_to_update(_id, name, surname, tel)
        self.__student_repo.save(student)
