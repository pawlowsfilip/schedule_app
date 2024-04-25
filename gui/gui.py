import customtkinter

def combobox_callback(value):
    print("Combobox selected:", value)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("960x540")
        self.title("Scheduler")

        self.title_label = customtkinter.CTkLabel(self, text="Scheduler", font=("Inter", 40, "bold"))
        self.title_label.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

        self.dropdown = customtkinter.CTkComboBox(self,
                                                  values=["Scheduler_R", "Scheduler_S"],
                                                  command=combobox_callback,
                                                  width=200,
                                                  height=40,
                                                  font=("Inter", 14),
                                                  justify=customtkinter.CENTER,
                                                  dropdown_font=("Inter", 14))
        self.dropdown.pack(padx=200, pady=100)
        self.dropdown.set("Choose schedule type")

        # Use focus event to disable text selection and hide the cursor
        self.dropdown.bind("<FocusIn>", self.disable_text_input)

    def disable_text_input(self, event):
        # Focus on another widget or the main window to remove focus from CTkComboBox
        self.focus_set()

app = App()
app.mainloop()
