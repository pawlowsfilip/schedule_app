import customtkinter
from gui.scheduler_r_view import SchedulerRView
from gui.scheduler_s_view import SchedulerSView


class DefaultView(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill="both", expand=True)

        # Title Label
        self.title_label = customtkinter.CTkLabel(self, text="Scheduler",
                                                  font=("Inter", 90, "bold"),
                                                  text_color="#f2f2f2")
        self.title_label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        # Frame
        self.frame = customtkinter.CTkLabel(self, text='',
                                            width=350,
                                            height=450,
                                            font=("Inter", 90, "bold"),
                                            fg_color="#333333",
                                            corner_radius=50)

        self.frame.place(relx=0.5, rely=0.48, anchor=customtkinter.CENTER)

        # Instructional Label
        self.instruction_label = customtkinter.CTkLabel(self.frame, text="  1.  Select a schedule type.\n"
                                                                   "  2. Fill necessary data.\n"
                                                                   "  3. Export schedule.\n",
                                                        font=("Inter", 19),
                                                        fg_color="#333333",
                                                        text_color="#f2f2f2",
                                                        justify="left",
                                                        anchor='w')
        self.instruction_label.place(relx=0.15, rely=0.2, anchor=customtkinter.W)

        # Dropdown
        self.dropdown = customtkinter.CTkComboBox(self.frame,
                                                  values=["Restaurant", "School"],
                                                  command=lambda value: self.dropdown_callback(value),
                                                  width=225,
                                                  height=40,
                                                  font=("Inter", 14),
                                                  justify=customtkinter.CENTER,
                                                  dropdown_text_color="#f2f2f2",
                                                  text_color="#f2f2f2",
                                                  fg_color="#2b2b2b",
                                                  bg_color="#333333",
                                                  border_color="#2b2b2b",
                                                  button_color='#2b2b2b',
                                                  dropdown_font=("Inter", 14))
        self.dropdown.place(relx=0.5, rely=0.32, anchor=customtkinter.CENTER)
        self.dropdown.set("Choose schedule type")
        self.dropdown.bind("<FocusIn>", self.disable_text_input)

        # Location Info
        self.location_info = customtkinter.CTkLabel(self.frame, text="Default location of exported schedule is desktop.\nIt can be changed in config file.",
                                                    font=("Inter", 12),
                                                    fg_color="#333333",
                                                    text_color="#787878",
                                                    justify="left",
                                                    anchor='w')
        self.location_info.place(relx=0.12, rely=0.42, anchor=customtkinter.W)

    def dropdown_callback(self, value):
        self.parent.notify_view_change(value)

    def disable_text_input(self, event):
        self.focus_set()

    def change_view(self, view_name, variant):
        self.parent.change_view(view_name, variant)
