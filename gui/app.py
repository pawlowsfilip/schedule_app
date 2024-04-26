import customtkinter
from gui.scheduler_r_view import SchedulerRView
from gui.scheduler_s_view import SchedulerSView
from gui.default_view import DefaultView


def dropdown_callback(value, app):
    print("Dropdown selected:", value)
    app.change_view(value)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        self.resizable(False, False)
        self.title("Scheduler")
        self._set_appearance_mode("system")

        self.current_view = DefaultView(self)  # Initialize the default view

    def change_view(self, view_name):
        # Remove the current view
        if self.current_view is not None:
            self.current_view.destroy()

        # Depending on the selection, load the appropriate view
        if view_name == "Scheduler_R":
            self.current_view = SchedulerRView(self)
        elif view_name == "Scheduler_S":
            self.current_view = SchedulerSView(self)


app = App()
app.mainloop()
