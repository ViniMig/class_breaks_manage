class ClassroomIter:

    def __init__(self, classroom):
        self._class_students = classroom.students
        self._current_index = 0
        self._class_size = len(self._class_students)

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_index < self._class_size:
            member = self._class_students[self._current_index]
            self._current_index += 1
            return member
        raise StopIteration