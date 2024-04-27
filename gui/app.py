import customtkinter
from gui.scheduler_r_view import SchedulerRView
from gui.scheduler_s_view import SchedulerSView
from gui.default_view import DefaultView


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        self.resizable(False, False)
        self.title("Scheduler")
        self._set_appearance_mode("system")

        self.current_view = DefaultView(self)  # Initialize the default view

    def change_view(self, view_name):
        # Remove all widgets in the window
        for widget in self.winfo_children():
            widget.destroy()

        # Depending on the selection, load the appropriate view
        if view_name == "Restaurant":
            self.scheduler_r_view = SchedulerRView(self)
        elif view_name == "School":
            self.scheduler_s_view = SchedulerSView(self)
        elif view_name == "DefaultView":
            self.default_view = DefaultView(self)


app = App()
app.mainloop()
