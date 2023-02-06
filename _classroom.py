from _student import Student
from _classroom_iter import ClassroomIter
from datetime import date

class Classroom:
    """Creates classroom which consists of a list of students"""

    def __init__(self, student_list):
        self.students = [Student(student["id"], student["name"], student["dates"]) for student in student_list]

    def __iter__(self):
        return ClassroomIter(self)

    def check_today(self):
        """
        Checks if today exists for every student and if not adds a new day
        """
        for member in self.students:
            day_exists = False

            for day in member.date_list:
                if str(date.today()) in day.values():
                    day_exists = True
                    
            if not day_exists:
                member.create_new_day()

    def add_student(self, new_student):
        """
        Adds a new student to the classroom
        """
        self.students.append(new_student)

    def classroom_json_list(self):
        json_list = []
        for elem in self.students:
            json_list.append({
                "id": elem.student_id,
                "name": elem.name,
                "dates": elem.date_list
            }
            )
        return json_list
