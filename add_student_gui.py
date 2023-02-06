import tkinter as tk
from _student import Student
from datetime import date

class Add_Student_GUI:

    def __init__(self, tk_level, current_class, add_button, add_label):
        self.st_ui = tk.Toplevel(tk_level)
        self.st_ui.geometry("350x100")
        self.st_ui.title("Add New Student")
        self.new_student_name = tk.StringVar()
        self.current_class = current_class
        self.add_button = add_button
        self.add_label = add_label

        self.this_label = tk.Label(self.st_ui, text = "Student Name", font = ('Arial', 15))
        self.this_label.place(x = 20, y = 20)

        self.new_name = tk.Entry(self.st_ui, textvariable = self.new_student_name)
        self.new_name.place(x = 20, y = 50, height = 25, width = 200)
        
        self.new_stdt_btn = tk.Button(self.st_ui, text = "Add Student", font = ('Arial', 12), background='green', fg='white', command= lambda: self.create_new_student(self.new_student_name.get()))
        self.new_stdt_btn.place(x = 230, y= 50, width=100, height=25)
    
    def create_new_student(self, studn_name: str):
        """
        Creates a New student with the name input on the window.
        Adds this to the class model and updates
        """
        highest_id = 0
        studentExists = False

        for student in self.current_class:
            if student.name == studn_name:
                studentExists = True
                break

            if student.student_id > highest_id:
                highest_id = student.student_id

        if not(studentExists):
            student_to_add = Student(highest_id + 1, studn_name, [{"date": str(date.today()), "num_breaks": 0, "total_break_time": 0}])
            self.current_class.add_student(student_to_add)
            print(f"Creating {student_to_add.name} with ID {student_to_add.student_id}")
            #add student buttons
            self.add_button(len(self.current_class.students) - 1, student_to_add.name)
            #append number of breaks label
            self.add_label("break_num_label", len(self.current_class.students) - 1)
            #append total time label
            self.add_label("total_break_time", len(self.current_class.students) - 1)
        else:
            print(f"Student {studn_name} already exists!")

        self.new_name.delete(0, len(studn_name))