from datetime import date
import time

class Student:
    """
    Class for managing student data: name, number of breaks and total time on break per day.
    If called with only name, creates new student, otherwise creates instance from the students list
    """
    def __init__(self, st_id, new_name, new_date_info):

        self.student_id = st_id
        self.name = new_name
        self.date_list = new_date_info
        self.today_breaks = 0
        self.today_total_time = 0
        self.time_units = 's'
        self.is_on_break = False
        self.current_time = 0

        for day_dict in self.date_list:
            if str(date.today()) in day_dict.values():
                self.today_breaks = day_dict["num_breaks"]
                current_total_time = day_dict["total_break_time"]
                if current_total_time > 60:
                    current_total_time /= 60
                    self.time_units = 'mins'
                self.today_total_time = int(current_total_time)

    def create_new_day(self):
        """Appends today to student data if not created"""
        today_exists = False
        for day_dict in self.date_list:
            if str(date.today()) in day_dict.values():
                today_exists = True
                break

        if not today_exists:
            self.date_list.append(
                    {
                        "date": str(date.today()),
                        "num_breaks": 0,
                        "total_break_time": 0
                    }
                )
    
    def start_counting(self):
        """Gets the current time to start counting the total time on break"""
        if not self.is_on_break:
            self.is_on_break = True
            self.current_time = time.perf_counter()

    def stop_counting(self):
        """Gets the current time and subtracts to the start for determining the total time on break"""
        if self.is_on_break:
            self.is_on_break = False
            self.current_time = time.perf_counter() - self.current_time
            self.update_times(self.current_time)
            self.current_time = 0


    def update_times(self, new_total):
        """Updates number of breaks and total time on break for the day"""
        for day_dict in self.date_list:
            if str(date.today()) in day_dict.values():
                day_dict["num_breaks"] += 1
                day_dict["total_break_time"] += new_total
                self.today_breaks += 1
                if new_total > 60:
                    new_total /= 60
                    self.time_units = 'mins'
                self.today_total_time += int(new_total)
    
    def get_breaks(self) -> tuple:
        """
        Returns the current number of breaks and the total break time.
        """
        for day_dict in self.date_list:
            if str(date.today()) in day_dict.values():
                return(day_dict["num_breaks"], day_dict["total_break_time"])