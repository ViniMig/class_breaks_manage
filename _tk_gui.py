import tkinter as tk
from _classroom import Classroom
from _add_student_gui import Add_Student_GUI
import json

class ManagerGUI:
    
    def __init__(self):

         #read the class json
        with open('classroom.json') as classroom:
            self.classroom_json = json.load(classroom)
        
        #set current classroom class
        self.current_class = Classroom(self.classroom_json["students"])
        self.current_class.check_today()

        #start tkinter application
        self.root = tk.Tk()

        #window configuration
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d+0+0" % (w - 100, h - 100))
        self.root.title("Break time manager")
        self.root['background'] = '#856ff8'

        # create a vertical scrollbar-no need
        self.v_scroll = tk.Scrollbar(self.root, orient='vertical')
        # attach Scrollbar to root window on
        # the side
        self.v_scroll.pack(side = 'right', fill = 'y')

        #add title label
        self.label = tk.Label(self.root, text = "Break Time!", background='#856ff8', fg='#ffffff', font = ('Comic Sans MS', 32, 'bold italic'))
        self.label.pack(padx = 20, pady = 20)

        #button to add new student (opens popup)
        self.loadimage = tk.PhotoImage(file="imgs/people_plus_one_icon_155017.png")
        self.add_student_btn = tk.Button(self.root, image=self.loadimage, relief="raised", command=self.new_student_window)
        self.add_student_btn["border"] = "0"
        self.add_student_btn["bg"] = '#856ff8'
        self.add_student_btn.place(x = 50, y = 100, height = 50, width = 50)
        
        #label for student name group
        self.student_label = tk.Label(self.root, text = "Name", background='#856ff8', fg='#ffffff', font = ('Comic Sans MS', 18, 'bold italic'))
        self.student_label.place(x = 50, y = 170, height = 50, width = 250)

        #label for number of breaks group
        self.n_breaks_label = tk.Label(self.root, text = "Number of breaks today", background='#856ff8', fg='#ffffff', font = ('Comic Sans MS', 18, 'bold italic'))
        self.n_breaks_label.place(x = 500, y = 170, height = 50, width = 300)

        #label for total time on break group
        self.total_break_label = tk.Label(self.root, text = "Total break time today", background='#856ff8', fg='#ffffff', font = ('Comic Sans MS', 18, 'bold italic'))
        self.total_break_label.place(x = 900, y = 170, height = 50, width = 300)

        self.info_frame = tk.Frame(self.root, bg = '#856ff8')
        
        self.info_canvas = tk.Canvas(self.info_frame, bg = '#856ff8', highlightthickness = 0, yscrollcommand = self.v_scroll.set)
        self.info_frame.place(x = 0, y = 221, relheight = 1, relwidth = 0.991)
        self.info_canvas.place(x = 0, y = 0, relheight = 1, relwidth = 1)

        #keep track of student buttons
        #use same cycle to create other elements
        self.st_btns = []
        self.st_btns_state = []
        self.br_labels = []
        self.br_time_labels = []
        self.current_break_time = [0 for _ in range(len(self.current_class.students))]
        self.btn_x, self.btn_y, self.btn_w, self.btn_h = 50, 20, 250, 50
        self.br_label_x, self.br_label_y, self.br_label_w, self.br_label_h = 500, 20, 250, 50
        self.br_time_label_x, self.br_time_label_y, self.br_time_label_w, self.br_time_label_h = 900, 20, 250, 50

        for i, st in enumerate(self.current_class):
            #add student buttons
            self.add_student_button(i, st.name)
            
            #append number of breaks label
            self.add_label("break_num_label", i)
            
            #append total time label
            self.add_label("total_break_time", i)            

        #configure scrolling action
        #self.info_canvas.configure(height = 500, scrollregion=self.info_canvas.bbox("all"))
        self.v_scroll.config(command=self.info_canvas.yview)

        #Configure application close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def add_student_button(self, iter_num: int, name: str):
        """Add button with the specific student name"""
        #append button state
        self.st_btns_state.append(True)
        #append button
        self.st_btns.append(tk.Button(self.info_canvas, text=name, font = ('Arial', 15),
            background='#2596be', fg='#ffffff', command= lambda c=iter_num: self.st_btn_click(c)))
        #place elements in interface
        self.st_btns[iter_num].place(x = self.btn_x, y = self.btn_y, height = self.btn_h, width = self.btn_w)
        #increase y position for next element
        self.btn_y += self.btn_h + 10

    def add_label(self, label_type: str, iter_num: int):
        """Add label to interface"""
        if label_type == "break_num_label":
            self.br_labels.append(tk.Label(self.info_canvas, text = self.current_class.students[iter_num].today_breaks,
                background='#856ff8', fg='white', font = ('Comic Sans MS', 18, 'bold italic')))
            self.br_labels[iter_num].place(x = self.br_label_x, y = self.br_label_y, width = self.br_label_w, height = self.br_label_h)
            #increase y position for next element
            self.br_label_y += self.br_label_h + 10
        else:
            self.br_time_labels.append(tk.Label(self.info_canvas, text = str(self.current_class.students[iter_num].today_total_time) + self.current_class.students[iter_num].time_units,
                background='#856ff8', fg='white', font = ('Comic Sans MS', 18, 'bold italic'))) 
            self.br_time_labels[iter_num].place(x = self.br_time_label_x, y = self.br_time_label_y, width = self.br_time_label_w, height = self.br_time_label_h)
            #increase y position for next element
            self.br_time_label_y += self.br_time_label_h + 10
    
    def new_student_window(self):
        """Action to add a new Student to the model and update the main interface"""
        new_popup = Add_Student_GUI(self.info_canvas, self.current_class, self.add_student_button, self.add_label)

    def st_btn_click(self, btn_number: int):
        """Event for when clicking a student button change the state the color and act appropriately"""
        if self.st_btns_state[btn_number] is True:
            self.st_btns[btn_number].config(bg='red')
            self.st_btns_state[btn_number] = False
            self.current_class.students[btn_number].start_counting() 
        else:
            self.st_btns[btn_number].config(bg='#2596be')
            self.st_btns_state[btn_number] = True
            self.current_class.students[btn_number].stop_counting()
            self.br_labels[btn_number].config(text= self.current_class.students[btn_number].today_breaks)
            self.br_time_labels[btn_number].config(text = str(self.current_class.students[btn_number].today_total_time) + self.current_class.students[btn_number].time_units)
    
    def on_closing(self):
        """Capture closing event and confirm"""
        #TODO
        #implement asking if the user is sure to close the window
        
        data_json = {
            "students": self.current_class.classroom_json_list()
        }

        data_json_dumps = json.dumps(data_json)
        with open('classroom.json', 'w') as save_class:
            save_class.write(data_json_dumps)

        self.root.destroy()