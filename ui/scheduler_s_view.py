import customtkinter
from CTkToolTip import *
from PIL import Image
from database.database import write_json
import json


class SchedulerSView(customtkinter.CTkFrame):
    """ Frame for the 'Scheduler_S' option within the main application window. """
    DATABASE_PATH = r"C:\Users\Filip\PycharmProjects\ScheduleApp\database\database.json"

    def __init__(self, parent, gui):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.gui = gui
        self.clear_database()
        self.pack(fill="both", expand=True)
        self.create_view()
        self.load_scheduler_data()

    def back_to_menu(self):
        # Method to switch back to the default view
        self.parent.change_view("DefaultView")

    def create_view(self):
        # back button
        self.back_button = customtkinter.CTkButton(self, text="<",
                                                   command=self.back_to_menu,
                                                   width=50, height=50,
                                                   fg_color="#242424",
                                                   hover_color="#3e3e3e",
                                                   border_color="#f2f2f2",
                                                   border_width=2,
                                                   text_color="#f2f2f2",
                                                   font=("Inter", 20, "bold"),
                                                   corner_radius=10)
        self.back_button.place(relx=0.1, rely=0.1, anchor=customtkinter.CENTER)

        # Title Label
        self.title_label = customtkinter.CTkLabel(self, text="School",
                                                  font=("Inter", 90, "bold"),
                                                  text_color="#f2f2f2")
        self.title_label.place(relx=0.5,
                               rely=0.1,
                               anchor=customtkinter.CENTER)

        # left Frame
        self.l_frame = customtkinter.CTkLabel(self, text='',
                                              width=350,
                                              height=450,
                                              font=("Inter", 90, "bold"),
                                              fg_color="#333333",
                                              corner_radius=50)

        self.l_frame.place(relx=0.16,
                           rely=0.48,
                           anchor=customtkinter.CENTER)

        # schedule_properties
        self.schedule_properties = customtkinter.CTkLabel(self.l_frame, text="Schedule properties",
                                                          font=("Inter", 23, 'bold'),
                                                          fg_color="#333333",
                                                          text_color="#f2f2f2",
                                                          justify="left",
                                                          anchor='w')
        self.schedule_properties.place(relx=0.15,
                                       rely=0.10,
                                       anchor=customtkinter.W)

        # info
        self.info_icon = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\Filip\PycharmProjects\ScheduleApp\icons\info.png"),
            size=(15, 15))

        # Use the image in a label
        self.info_label = customtkinter.CTkLabel(self.l_frame,
                                                 text='',
                                                 image=self.info_icon, )
        self.info_label.place(relx=0.83, rely=0.103, anchor=customtkinter.CENTER)

        tooltip = CTkToolTip(self.info_label, delay=0.5,
                             message="Time frames are specific period of time\n"
                                     "which needs to be filled by workers.\n"
                                     "Time frames need to be separated by ';'\n"
                                     "Ex. 8:00-8:15; 9:00-9:15 etc.",
                             font=("Inter", 13),
                             alpha=0.9,
                             corner_radius=12,
                             text_color='#f2f2f2',
                             padding=(10, 10))

        # day
        self.day = customtkinter.CTkLabel(self.l_frame, text="Day",
                                          font=("Inter", 18),
                                          fg_color="#333333",
                                          text_color="#f2f2f2",
                                          justify="left",
                                          anchor='w')
        self.day.place(relx=0.15,
                       rely=0.175,
                       anchor=customtkinter.W)
        self.day_entry = customtkinter.CTkEntry(self.l_frame,
                                                placeholder_text='Type here...',
                                                border_color="#2b2b2b",
                                                width=250,
                                                height=40,
                                                fg_color="#2b2b2b",
                                                text_color="#f2f2f2",
                                                font=("Inter", 14))
        self.day_entry.place(relx=0.5,
                             rely=0.25,
                             anchor=customtkinter.CENTER)

        # Time frames
        self.time_frames = customtkinter.CTkLabel(self.l_frame, text="Time frames",
                                                  font=("Inter", 18),
                                                  fg_color="#333333",
                                                  text_color="#f2f2f2",
                                                  justify="left",
                                                  anchor='w')
        self.time_frames.place(relx=0.15,
                               rely=0.34,
                               anchor=customtkinter.W)

        self.time_frames_entry = customtkinter.CTkEntry(self.l_frame,
                                                        placeholder_text='Type here...',
                                                        border_color="#2b2b2b",
                                                        width=250,
                                                        height=40,
                                                        fg_color="#2b2b2b",
                                                        text_color="#f2f2f2",
                                                        font=("Inter", 14))
        self.time_frames_entry.place(relx=0.5,
                                     rely=0.42,
                                     anchor=customtkinter.CENTER)

        self.add_day_time_frame = customtkinter.CTkButton(self.l_frame, text="Add",
                                                       width=75,
                                                       height=40,
                                                       fg_color="#f2f2f2",
                                                       text_color="#333333",
                                                       corner_radius=50,
                                                       hover_color='#a1a1a1',
                                                       font=("Inter", 14, 'bold'),
                                                       command=self.submit_day_time_frame)

        self.add_day_time_frame.place(relx=0.5,
                                   rely=0.85,
                                   anchor=customtkinter.CENTER)

        # mid Frame
        self.m_frame = customtkinter.CTkLabel(self, text='',
                                              width=350,
                                              height=450,
                                              font=("Inter", 90, "bold"),
                                              fg_color="#333333",
                                              corner_radius=50)

        self.m_frame.place(relx=0.43,
                           rely=0.48,
                           anchor=customtkinter.CENTER)

        # worker
        self.worker = customtkinter.CTkLabel(self.m_frame, text="Worker",
                                             font=("Inter", 25, 'bold'),
                                             fg_color="#333333",
                                             text_color="#f2f2f2",
                                             justify="left",
                                             anchor='w')
        self.worker.place(relx=0.15,
                          rely=0.10,
                          anchor=customtkinter.W)

        # info
        self.info_icon = customtkinter.CTkImage(
            light_image=Image.open(r"C:\Users\Filip\PycharmProjects\ScheduleApp\icons\info.png"),
            size=(15, 15))

        # Use the image in a label
        self.info_label = customtkinter.CTkLabel(self.m_frame,
                                                 text='',
                                                 image=self.info_icon, )
        self.info_label.place(relx=0.44, rely=0.104, anchor=customtkinter.CENTER)

        tooltip = CTkToolTip(self.info_label, delay=0.5,
                             message="Name is the name of the worker.\n\n"
                                     "Availability is daily availability of the worker.\n"
                                     "Time frames must to be separated by ','\n"
                                     "Days must be separated by ';'\n"
                                     'Ex. 21.07: 8:00-8:30, 10:00-11:00; 22.07: 7:00-8:00\n\n'
                                     'Worse availability is daily availability of the worker,\n'
                                     'but optional. If there is possibility to not come to work,\n'
                                     'worker would rather not come.\n'
                                     'Ex. 21.07: 12:00-13:00; 22.07: 8:00-8:30',
                             font=("Inter", 13),
                             alpha=0.9,
                             corner_radius=12,
                             text_color='#f2f2f2',
                             padding=(10, 10))

        # name
        self.name = customtkinter.CTkLabel(self.m_frame, text="Name",
                                           font=("Inter", 18),
                                           fg_color="#333333",
                                           text_color="#f2f2f2",
                                           justify="left",
                                           anchor='w')
        self.name.place(relx=0.15,
                        rely=0.175,
                        anchor=customtkinter.W)
        self.name_entry = customtkinter.CTkEntry(self.m_frame,
                                                 placeholder_text='Type here...',
                                                 border_color="#2b2b2b",
                                                 width=250,
                                                 height=40,
                                                 fg_color="#2b2b2b",
                                                 text_color="#f2f2f2",
                                                 font=("Inter", 14))
        self.name_entry.place(relx=0.5,
                              rely=0.25,
                              anchor=customtkinter.CENTER)
        # self.name_entry.bind("<Return>", self.submit_name)

        # availability
        self.availability = customtkinter.CTkLabel(self.m_frame, text="Availability",
                                                   font=("Inter", 18),
                                                   fg_color="#333333",
                                                   text_color="#f2f2f2",
                                                   justify="left",
                                                   anchor='w')

        self.availability.place(relx=0.15,
                                rely=0.34,
                                anchor=customtkinter.W)

        self.availability_entry = customtkinter.CTkEntry(self.m_frame,
                                                         placeholder_text='Type here...',
                                                         border_color="#2b2b2b",
                                                         width=250,
                                                         height=40,
                                                         fg_color="#2b2b2b",
                                                         text_color="#f2f2f2",
                                                         font=("Inter", 14))

        self.availability_entry.place(relx=0.5,
                                      rely=0.42,
                                      anchor=customtkinter.CENTER)
        # self.availability_entry.bind("<Return>", self.submit_availability)

        # worse_availability
        self.worse_availability = customtkinter.CTkLabel(self.m_frame, text="Worse availability",
                                                         font=("Inter", 18),
                                                         fg_color="#333333",
                                                         text_color="#f2f2f2",
                                                         justify="left",
                                                         anchor='w')

        self.worse_availability.place(relx=0.15,
                                      rely=0.50,
                                      anchor=customtkinter.W)

        self.worse_availability_entry = customtkinter.CTkEntry(self.m_frame,
                                                               placeholder_text='Type here...',
                                                               border_color="#2b2b2b",
                                                               width=250,
                                                               height=40,
                                                               fg_color="#2b2b2b",
                                                               text_color="#f2f2f2",
                                                               font=("Inter", 14))

        self.worse_availability_entry.place(relx=0.5,
                                            rely=0.58,
                                            anchor=customtkinter.CENTER)
        # self.worse_availability_entry.bind("<Return>", self.submit_worse_availability)

        self.add_properties_button = customtkinter.CTkButton(self.m_frame, text="Add",
                                                             width=75,
                                                             height=40,
                                                             fg_color="#f2f2f2",
                                                             text_color="#333333",
                                                             corner_radius=50,
                                                             hover_color='#a1a1a1',
                                                             font=("Inter", 14, 'bold'),
                                                             command=self.submit_worker_info)

        self.add_properties_button.place(relx=0.5,
                                         rely=0.85,
                                         anchor=customtkinter.CENTER)

        # right Frame
        self.r_frame = customtkinter.CTkLabel(self, text='',
                                              width=540,
                                              height=450,
                                              font=("Inter", 90, "bold"),
                                              fg_color="#333333",
                                              corner_radius=50)

        self.r_frame.place(relx=0.769,
                           rely=0.48,
                           anchor=customtkinter.CENTER)

        # Data
        self.data = customtkinter.CTkLabel(self.r_frame, text="Data",
                                           font=("Inter", 25, 'bold'),
                                           fg_color="#333333",
                                           text_color="#f2f2f2",
                                           justify="left")
        self.data.place(relx=0.15,
                        rely=0.10,
                        anchor=customtkinter.CENTER)

        # showing data
        self.setup_display_areas()

        self.export_button = customtkinter.CTkButton(self, text="Export",
                                                     width=250,
                                                     height=50,
                                                     fg_color="#f2f2f2",
                                                     text_color="#333333",
                                                     corner_radius=50,
                                                     hover_color='#a1a1a1',
                                                     font=("Inter", 20, 'bold'),
                                                     command=self.gui.export_schedule)

        self.export_button.place(relx=0.5,
                                 rely=0.85,
                                 anchor=customtkinter.CENTER)

    def submit_day_time_frame(self):
        day_value = self.day_entry.get()
        time_frames_value = self.time_frames_entry.get()
        if time_frames_value and day_value:
            properties = {
                'day': day_value,
                'time_frames': time_frames_value
            }
            self.update_database([properties])
            self.load_scheduler_data()
            self.update_display_areas()

    def submit_worker_info(self):
        name_value = self.name_entry.get()
        availability_value = self.availability_entry.get()
        worse_availability_value = self.worse_availability_entry.get()

        # Convert the availability values into dictionaries using separate functions
        availability_dict = self.parse_availability(availability_value)
        worse_availability_dict = self.parse_availability(worse_availability_value)

        if name_value and availability_dict:
            worker_info = {
                'name': name_value,
                'availability': availability_dict,
                'worse_availability': worse_availability_dict
            }
            self.update_database([worker_info])
            self.load_scheduler_data()
            self.update_display_areas()

    def update_database(self, new_entries):
        try:
            with open(self.DATABASE_PATH, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.extend(new_entries)

        with open(self.DATABASE_PATH, 'w') as file:
            json.dump(data, file, indent=4)

    def load_scheduler_data(self):
        if self.gui:
            self.gui.update_scheduler_s_from_json(self.DATABASE_PATH)
        else:
            print("GUI not initialized.")

    def clear_database(self):
        write_json(self.DATABASE_PATH, [])

    def setup_display_areas(self):
        self.display_accuracy = customtkinter.CTkLabel(self.r_frame, text="Day: ", font=("Inter", 16), fg_color="#333333", text_color="#f2f2f2", width=500, height=40, anchor='w')
        self.display_accuracy.place(relx=0.1, rely=0.2, anchor=customtkinter.W)

        self.display_allocation = customtkinter.CTkLabel(self.r_frame, text="Time frames: ", font=("Inter", 16), fg_color="#333333", text_color="#f2f2f2", width=500, height=40, anchor='w')
        self.display_allocation.place(relx=0.1, rely=0.3, anchor=customtkinter.W)

        self.display_name = customtkinter.CTkLabel(self.r_frame, text="Name", font=("Inter: ", 16), fg_color="#333333", text_color="#f2f2f2", width=500, height=40, anchor='w')
        self.display_name.place(relx=0.1, rely=0.4, anchor=customtkinter.W)

        self.display_availability = customtkinter.CTkLabel(self.r_frame, text="Availability: ", font=("Inter", 16), fg_color="#333333", text_color="#f2f2f2", width=500, height=40, anchor='w')
        self.display_availability.place(relx=0.1, rely=0.5, anchor=customtkinter.W)

        self.display_worse_availability = customtkinter.CTkLabel(self.r_frame, text="Worse availability: ", font=("Inter", 16), fg_color="#333333", text_color="#f2f2f2", width=500, height=40, anchor='w')
        self.display_worse_availability.place(relx=0.1, rely=0.6, anchor=customtkinter.W)

    def update_display_areas(self):
        pass
        # data_entries = self.read_json_data(self.DATABASE_PATH)
        #
        # day_text = "Day: N/A"
        # time_frames_text = "Time frames: N/A"
        # name_text = "Name: N/A"
        # availability_text = "Availability: N/A"
        # worse_availability_text = "Worse availability: N/A"
        #
        # if data_entries:
        #     for entry in data_entries:
        #         if "day" in entry and "time_frames" in entry:
        #             day_text = f"Day: {entry['day']}"
        #             time_frames_text = f"Time frames: {entry['time_frames']}"
        #         if "name" in entry:
        #             name_text = f"Name: {entry['name']}"
        #             availability_text = f"Availability: {entry['availability']}"
        #             worse_availability_text = f"Worse availability: {entry['worse_availability']}"
        #         break
        #
        # self.display_accuracy.configure(text=day_text)
        # self.display_allocation.configure(text=time_frames_text)
        # self.display_name.configure(text=name_text)
        # self.display_availability.configure(text=availability_text)
        # self.display_worse_availability.configure(text=worse_availability_text)

    @staticmethod
    def parse_availability(availability_str):
        availability_dict = {}
        day_entries = availability_str.split(";")
        if availability_str:
            try:
                for entry in day_entries:
                    if ":" in entry:
                        day, time_frames = entry.split(": ", 1)
                        availability_dict[day.strip()] = time_frames.strip()
            except ValueError:
                print("Invalid availability format. Use 'day: time_frame'")
        return availability_dict

    @staticmethod
    def read_json_data(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
