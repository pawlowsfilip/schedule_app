import customtkinter
from CTkToolTip import *
from PIL import Image


class SchedulerRView(customtkinter.CTkFrame):
    """ Frame for the 'Scheduler_R' option within the main application window. """

    def __init__(self, parent, gui):
        super().__init__(parent, fg_color='transparent')
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

        # Accuracy
        self.accuracy = customtkinter.CTkLabel(self.l_frame, text="Accuracy",
                                               font=("Inter", 18),
                                               fg_color="#333333",
                                               text_color="#f2f2f2",
                                               justify="left",
                                               anchor='w')
        self.accuracy.place(relx=0.15,
                            rely=0.175,
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
                                  rely=0.25,
                                  anchor=customtkinter.CENTER)
        self.accuracy_entry.bind("<Return>", self.submit_accuracy)

        # Allocation
        self.allocation = customtkinter.CTkLabel(self.l_frame, text="Allocation",
                                                 font=("Inter", 18),
                                                 fg_color="#333333",
                                                 text_color="#f2f2f2",
                                                 justify="left",
                                                 anchor='w')

        self.allocation.place(relx=0.15,
                              rely=0.34,
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
                                    rely=0.42,
                                    anchor=customtkinter.CENTER)
        self.allocation_entry.bind("<Return>", self.submit_allocation)

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
        self.name_entry.bind("<Return>", self.submit_name)

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
        self.availability_entry.bind("<Return>", self.submit_availability)

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
        self.worse_availability_entry.bind("<Return>", self.submit_worse_availability)

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
        self.position_entry.bind("<Return>", self.submit_position)

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

        # showing data
        self.setup_display_areas()

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

    def setup_display_areas(self):
        # Labels to display data dynamically
        self.display_accuracy = customtkinter.CTkLabel(self.r_frame, text="Accuracy: ", font=("Inter", 16), fg_color="#333333", text_color="#f2f2f2", width=500, height=40, anchor='w')
        self.display_accuracy.place(relx=0.1, rely=0.2, anchor=customtkinter.W)

        self.display_allocation = customtkinter.CTkLabel(self.r_frame, text="Allocation: ", font=("Inter", 16), fg_color="#333333", text_color="#f2f2f2", width=500, height=40, anchor='w')
        self.display_allocation.place(relx=0.1, rely=0.3, anchor=customtkinter.W)

        self.display_name = customtkinter.CTkLabel(self.r_frame, text="Name", font=("Inter: ", 16), fg_color="#333333", text_color="#f2f2f2", width=500, height=40, anchor='w')
        self.display_name.place(relx=0.1, rely=0.4, anchor=customtkinter.W)

        self.display_availability = customtkinter.CTkLabel(self.r_frame, text="Availability: ", font=("Inter", 16), fg_color="#333333", text_color="#f2f2f2", width=500, height=40, anchor='w')
        self.display_availability.place(relx=0.1, rely=0.5, anchor=customtkinter.W)

        self.display_worse_availability = customtkinter.CTkLabel(self.r_frame, text="Worse availability: ", font=("Inter", 16), fg_color="#333333", text_color="#f2f2f2", width=500, height=40, anchor='w')
        self.display_worse_availability.place(relx=0.1, rely=0.6, anchor=customtkinter.W)

        self.display_position = customtkinter.CTkLabel(self.r_frame, text="Position", font=("Inter: ", 16), fg_color="#333333", text_color="#f2f2f2", width=500, height=40, anchor='w')
        self.display_position.place(relx=0.1, rely=0.7, anchor=customtkinter.W)

    def submit_accuracy(self, event):
        accuracy_value = self.accuracy_entry.get()
        if accuracy_value:
            self.display_accuracy.configure(text=f"Accuracy: {accuracy_value}")
            self.parent.update_scheduler_parameters({'accuracy': accuracy_value})

    def submit_allocation(self, event):
        allocation_value = self.allocation_entry.get()
        if allocation_value:
            self.display_allocation.configure(text=f"Allocation: {allocation_value}")
            self.parent.update_scheduler_parameters({'allocation': allocation_value})

    def submit_name(self, event):
        name_value = self.name_entry.get()
        if name_value:
            self.display_name.configure(text=f"Name: {name_value}")
            self.parent.update_scheduler_parameters({'name': name_value})

    def submit_availability(self, event):
        availability_value = self.availability_entry.get()
        if availability_value:
            self.display_availability.configure(text=f"Availability: {availability_value}")
            self.parent.update_scheduler_parameters({'availability': availability_value})

    def submit_worse_availability(self, event):
        worse_availability_value = self.worse_availability_entry.get()
        if worse_availability_value:
            self.display_worse_availability.configure(text=f"Worse availability: {worse_availability_value}")
            self.parent.update_scheduler_parameters({'worse_availability': worse_availability_value})

    def submit_position(self, event):
        position_value = self.position_entry.get()
        if position_value:
            self.display_position.configure(text=f"Position: {position_value}")
            self.parent.update_scheduler_parameters({'position': position_value})

    def export_scheduler(self):
        pass
