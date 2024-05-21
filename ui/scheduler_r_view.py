import customtkinter
from CTkToolTip import *
from PIL import Image
from database.database import write_json
from resources.CTkXYFrame import *
import json


class SchedulerRView(customtkinter.CTkFrame):
    """ Frame for the 'Scheduler_R' option within the main application window. """
    DATABASE_PATH = r"C:\Users\Filip\PycharmProjects\ScheduleApp\database\database.json"

    def __init__(self, parent, gui):
        super().__init__(parent, fg_color='transparent')
        self.parent = parent
        self.gui = gui
        self.clear_database()
        self.pack(fill="both", expand=True)
        self.create_view()
        self.load_scheduler_data()

    def back_to_menu(self):
        # Method to switch back to the default view
        self.parent.change_view("DefaultView")  # Make sure the App class can handle this view name

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
        self.title_label = customtkinter.CTkLabel(self, text="Restaurant",
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
                             message="Accuracy is a measure how precise time frames will be.\n"
                                     "Ex. 1 is 1 hour time frame, 0.5 "
                                     "is 30 min time frame, etc.\n\n"
                                     "Allocation is number of workers allocated in a specific\n"
                                     'period of time. Ex. 7:00-10:00: 1, 10:00-14:00: 2 etc.',
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

        # Accuracy
        self.accuracy = customtkinter.CTkLabel(self.l_frame, text="Accuracy",
                                               font=("Inter", 18),
                                               fg_color="#333333",
                                               text_color="#f2f2f2",
                                               justify="left",
                                               anchor='w')
        self.accuracy.place(relx=0.15,
                            rely=0.34,
                            anchor=customtkinter.W)
        self.accuracy_entry = customtkinter.CTkEntry(self.l_frame,
                                                     placeholder_text='Type here...',
                                                     border_color="#2b2b2b",
                                                     width=250,
                                                     height=40,
                                                     fg_color="#2b2b2b",
                                                     text_color="#f2f2f2",
                                                     font=("Inter", 14))
        self.accuracy_entry.place(relx=0.5,
                                  rely=0.42,
                                  anchor=customtkinter.CENTER)

        # Allocation
        self.allocation = customtkinter.CTkLabel(self.l_frame, text="Allocation",
                                                 font=("Inter", 18),
                                                 fg_color="#333333",
                                                 text_color="#f2f2f2",
                                                 justify="left",
                                                 anchor='w')

        self.allocation.place(relx=0.15,
                              rely=0.50,
                              anchor=customtkinter.W)

        self.allocation_entry = customtkinter.CTkEntry(self.l_frame,
                                                       placeholder_text='Type here...',
                                                       border_color="#2b2b2b",
                                                       width=250,
                                                       height=40,
                                                       fg_color="#2b2b2b",
                                                       text_color="#f2f2f2",
                                                       font=("Inter", 14))

        self.allocation_entry.place(relx=0.5,
                                    rely=0.58,
                                    anchor=customtkinter.CENTER)

        # position
        self.position_priorities = customtkinter.CTkLabel(self.l_frame, text="Position priorities",
                                               font=("Inter", 18),
                                               fg_color="#333333",
                                               text_color="#f2f2f2",
                                               justify="left",
                                               anchor='w')

        self.position_priorities.place(relx=0.15,
                            rely=0.66,
                            anchor=customtkinter.W)

        self.position_priorities_entry = customtkinter.CTkEntry(self.l_frame,
                                                     placeholder_text='Type here...',
                                                     border_color="#2b2b2b",
                                                     width=250,
                                                     height=40,
                                                     fg_color="#2b2b2b",
                                                     text_color="#f2f2f2",
                                                     font=("Inter", 14))

        self.position_priorities_entry.place(relx=0.5,
                                  rely=0.74,
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
                                     'Ex. 21:07: [7:00-10:00, 14:00-15:00],\n22.07: [8:00-15:00]\n\n'
                                     'Worse availability is daily availability of the worker,\n'
                                     'but optional. If there is possibility to not come to work,\n'
                                     'worker would rather not come.\n'
                                     'Ex. 21:07: [7:00-10:00, 14:00-15:00],\n22.07: [8:00-15:00]\n\n'
                                     'Position is a position in work of the worker.\n'
                                     'Ex. Manager, CEO, Regular.',
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

        # position
        self.position = customtkinter.CTkLabel(self.m_frame, text="Position",
                                               font=("Inter", 18),
                                               fg_color="#333333",
                                               text_color="#f2f2f2",
                                               justify="left",
                                               anchor='w')

        self.position.place(relx=0.15,
                            rely=0.66,
                            anchor=customtkinter.W)

        self.position_entry = customtkinter.CTkEntry(self.m_frame,
                                                     placeholder_text='Type here...',
                                                     border_color="#2b2b2b",
                                                     width=250,
                                                     height=40,
                                                     fg_color="#2b2b2b",
                                                     text_color="#f2f2f2",
                                                     font=("Inter", 14))

        self.position_entry.place(relx=0.5,
                                  rely=0.74,
                                  anchor=customtkinter.CENTER)

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

        self.r_frame.place(relx=0.966, rely=0.48, anchor=customtkinter.E)

        # Data
        self.data = customtkinter.CTkLabel(self.r_frame, text="Data",
                                           font=("Inter", 25, 'bold'),
                                           fg_color="#333333",
                                           text_color="#f2f2f2",
                                           justify="left",
                                           anchor='w')
        self.data.place(relx=0.1,
                        rely=0.10,
                        anchor=customtkinter.W)

        # scrollable frame
        self.scrollable_frame = CTkXYFrame(self.r_frame,
                                           width=440,
                                           height=345,
                                           fg_color="#333333")

        self.scrollable_frame.place(relx=0.06,
                                    rely=0.53,
                                    anchor=customtkinter.W)

        # export_button
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
        accuracy_value = float(self.accuracy_entry.get())
        allocation_value = self.allocation_entry.get()
        position_priorities_value = self.position_priorities_entry.get()

        if day_value and accuracy_value and allocation_value:
            if position_priorities_value:
                properties = {
                    'day': day_value,
                    'accuracy': accuracy_value,
                    'allocation': allocation_value,
                    'position_priorities': position_priorities_value
                }
            else:
                properties = {
                    'day': day_value,
                    'accuracy': accuracy_value,
                    'allocation': allocation_value,
                    'position_priorities': ""
                }

            self.update_database([properties])
            self.load_scheduler_data()
            self.update_display_areas()

    def submit_worker_info(self):
        name_value = self.name_entry.get()
        availability_value = self.availability_entry.get()
        worse_availability_value = self.worse_availability_entry.get()
        position_value = self.position_entry.get()

        # Convert the availability values into dictionaries using separate functions
        availability_dict = self.parse_availability(availability_value)
        worse_availability_dict = self.parse_availability(worse_availability_value)

        if name_value and availability_dict:
            worker_info = {
                'name': name_value,
                'availability': availability_dict,
                'worse_availability': worse_availability_dict,
                'position': position_value
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
            self.gui.update_scheduler_r_from_json(self.DATABASE_PATH)
        else:
            print("GUI not initialized.")

    def clear_database(self):
        write_json(self.DATABASE_PATH, [])

    def clear_display_areas(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    @staticmethod
    def add_labels_to_scrollable_frame(frame, data, combined_keys):
        for entry in data:
            combined_text_list = []
            for key in combined_keys:
                if key in entry:
                    value = entry[key]
                    if isinstance(value, dict):
                        formatted_value = ", ".join([f"{k}: {v}" for k, v in value.items()])
                        combined_text_list.append(f"{key}: {formatted_value}")
                    else:
                        combined_text_list.append(f"{key}: {value}")

            combined_text = "\n".join(combined_text_list)

            label_button_frame = customtkinter.CTkFrame(frame, fg_color="#333333", width=475, height=60)
            label_button_frame.grid(sticky='w', padx=0, pady=3)

            label = customtkinter.CTkLabel(label_button_frame,
                                           text=combined_text,
                                           font=("Inter", 16),
                                           fg_color="#333333",
                                           text_color="#f2f2f2",
                                           width=391,
                                           height=65,
                                           justify="left",
                                           anchor='w')
            label.grid(row=0, column=1, sticky='w', padx=0, pady=0)

            button = customtkinter.CTkButton(label_button_frame, text="✕",
                                             width=30,
                                             height=20,
                                             fg_color="#333333",
                                             text_color="white",
                                             corner_radius=50,
                                             hover_color='#a1a1a1',
                                             font=("Inter", 25, 'bold'),
                                             command=lambda entry=entry: frame.delete_widget(label, entry))
            button.grid(row=0, column=0, sticky='e', padx=0, pady=0)

    def update_display_areas(self):
        data_entries = self.read_json_data(self.DATABASE_PATH)

        self.clear_display_areas()

        # Add new labels
        scheduler_combined_keys = ["day", "accuracy", "allocation", "position_priorities"]
        worker_combined_keys = ["name", "availability", "worse_availability", "position"]

        scheduler_data = [entry for entry in data_entries if "day" in entry and "allocation" in entry]
        worker_data = [entry for entry in data_entries if "name" in entry]

        self.add_labels_to_scrollable_frame(self.scrollable_frame, scheduler_data, scheduler_combined_keys)
        self.add_labels_to_scrollable_frame(self.scrollable_frame, worker_data, worker_combined_keys)

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
