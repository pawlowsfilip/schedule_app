import customtkinter
from gui.scheduler_r_view import SchedulerRView
from gui.scheduler_s_view import SchedulerSView
from gui.default_view import DefaultView
from main import Gui


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1366x768")
        self.resizable(False, False)
        self.title("Scheduler")
        self._set_appearance_mode("system")
        self.current_view = DefaultView(self)  # Initialize the default view

        self.gui = None

    def change_view(self, view_name):
        if self.current_view is not None:
            self.current_view.destroy()

        if view_name == "Restaurant":
            self.current_view = SchedulerRView(self, self.gui)
        elif view_name == "School":
            self.current_view = SchedulerSView(self, self.gui)
        elif view_name == "DefaultView":
            self.current_view = DefaultView(self)
        self.current_view.pack(fill="both", expand=True)

    def notify_view_change(self, selection):
        variant = 'R' if selection == "Restaurant" else 'S' if selection == "School" else None
        if variant:
            self.init_gui(variant)
        self.change_view(selection)

    def init_gui(self, variant):
        self.gui = Gui(variant)  # This sets up the backend based on the selection
        print(self.gui)

    def update_scheduler_parameters(self, parameters):
        if 'accuracy' in parameters:
            self.gui.update_accuracy(parameters['accuracy'])
        if 'allocation' in parameters:
            self.gui.update_allocation(parameters['allocation'])
        if 'name' in parameters:
            self.gui.update_name(parameters['name'])
        if 'availability' in parameters:
            self.gui.update_availability(parameters['availability'])
        if 'worse_availability' in parameters:
            self.gui.update_worse_availability(parameters['worse_availability'])
        if 'position' in parameters:
            self.gui.update_position(parameters['position'])

app = App()
app.mainloop()
