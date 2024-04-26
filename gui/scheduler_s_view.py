import customtkinter

class SchedulerSView(customtkinter.CTkFrame):
    """ Frame for the 'Scheduler_S' option within the main application window. """

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.create_view()

    def create_view(self):
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
                                                          font=("Inter", 25, 'bold'),
                                                          fg_color="#333333",
                                                          text_color="#f2f2f2",
                                                          justify="left")
        self.schedule_properties.place(relx=0.5,
                                       rely=0.10,
                                       anchor=customtkinter.CENTER)

        # Time frames
        self.time_frames = customtkinter.CTkLabel(self.l_frame, text="Time frames",
                                               font=("Inter", 18),
                                               fg_color="#333333",
                                               text_color="#f2f2f2",
                                               justify="left")
        self.time_frames.place(relx=0.3,
                            rely=0.175,
                            anchor=customtkinter.CENTER)
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
                                             justify="left")
        self.worker.place(relx=0.275,
                          rely=0.10,
                          anchor=customtkinter.CENTER)

        # name
        self.name = customtkinter.CTkLabel(self.m_frame, text="Name",
                                           font=("Inter", 18),
                                           fg_color="#333333",
                                           text_color="#f2f2f2",
                                           justify="left")
        self.name.place(relx=0.22,
                        rely=0.175,
                        anchor=customtkinter.CENTER)
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
                                                   justify="left")

        self.availability.place(relx=0.275,
                                rely=0.34,
                                anchor=customtkinter.CENTER)

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
                                                         justify="left")

        self.worse_availability.place(relx=0.36,
                                      rely=0.50,
                                      anchor=customtkinter.CENTER)

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
