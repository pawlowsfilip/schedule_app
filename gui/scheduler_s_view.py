import customtkinter
from PIL import Image
from CTkToolTip import *
from database.database import read_json, write_json


class SchedulerSView(customtkinter.CTkFrame):
    """ Frame for the 'Scheduler_S' option within the main application window. """
    DATABASE_PATH = r"C:\Users\Filip\PycharmProjects\ScheduleApp\database\database.json"

    def __init__(self, parent, gui):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.gui = gui
        self.pack(fill="both", expand=True)
        self.create_view()

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
                                     "Ex. 8:00-8:15, 9:00-9:15, etc.",
                             font=("Inter", 13),
                             alpha=0.9,
                             corner_radius=12,
                             text_color='#f2f2f2',
                             padding=(10, 10))

        # Time frames
        self.time_frames = customtkinter.CTkLabel(self.l_frame, text="Time frames",
                                                  font=("Inter", 18),
                                                  fg_color="#333333",
                                                  text_color="#f2f2f2",
                                                  justify="left",
                                                  anchor='w')
        self.time_frames.place(relx=0.15,
                               rely=0.175,
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
                                     rely=0.25,
                                     anchor=customtkinter.CENTER)

        self.add_time_frames = customtkinter.CTkButton(self.l_frame, text="Add",
                                                       width=75,
                                                       height=40,
                                                       fg_color="#f2f2f2",
                                                       text_color="#333333",
                                                       corner_radius=50,
                                                       hover_color='#a1a1a1',
                                                       font=("Inter", 14, 'bold'),
                                                       command=self.submit_time_frames)

        self.add_time_frames.place(relx=0.5,
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
                                     'Ex. 21:07: [7:00-10:00, 14:00-15:00],\n22.07: [8:00-15:00]',
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
                                                     font=("Inter", 20, 'bold'))

        self.export_button.place(relx=0.5,
                                 rely=0.85,
                                 anchor=customtkinter.CENTER)

    def setup_display_areas(self):
        pass

    def clear_database(self):
        write_json(self.DATABASE_PATH, [])

    def submit_time_frames(self):
        time_frames_value = self.time_frames_entry.get()
        if time_frames_value:
            new_data = [{'time_frames': time_frames_value}]
            self.update_database(new_data)

    def submit_worker_info(self):
        name_value = self.name_entry.get()
        availability_value = self.availability_entry.get()
        worse_availability_value = self.worse_availability_entry.get()

        if name_value and availability_value:
            worker_info = {
                'name': name_value,
                'availability': availability_value,
                'worse_availability': worse_availability_value
            }
            self.update_database([worker_info])

    def update_database(self, new_entries):
        # Overwrite the JSON file with the new entries
        write_json(self.DATABASE_PATH, new_entries)