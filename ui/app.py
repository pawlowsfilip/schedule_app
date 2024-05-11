import customtkinter
from ui.scheduler_r_view import SchedulerRView
from ui.scheduler_s_view import SchedulerSView
from ui.default_view import DefaultView
from gui import Gui
import logging

logger = logging.getLogger(__name__)


class App(customtkinter.CTk):
    def __init__(self):
        try:
            logger.debug("Initializing the App")
            super().__init__()
            self.geometry("1366x768")
            self.resizable(False, False)
            self.title("Scheduler")
            self._set_appearance_mode("system")
            self.current_view = DefaultView(self)  # Initialize the default view
            self.iconbitmap(r"C:\Users\Filip\PycharmProjects\ScheduleApp\icons\scheduler.ico")
            self.gui = None
            logger.debug("App initialized successfully")
        except Exception as e:
            logger.error("Error initializing the App: %s", e)

    def change_view(self, view_name):
        try:
            logger.debug(f"Changing view to {view_name}")
            if self.current_view is not None:
                self.current_view.destroy()
                logger.debug("Current view destroyed")

            if view_name == "Restaurant":
                self.current_view = SchedulerRView(self, self.gui)
            elif view_name == "School":
                self.current_view = SchedulerSView(self, self.gui)
            elif view_name == "DefaultView":
                self.current_view = DefaultView(self)
            else:
                logger.warning(f"Unknown view name: {view_name}")
                return

            self.current_view.pack(fill="both", expand=True)
            logger.debug(f"View changed to {view_name}")
        except Exception as e:
            logger.error(f"Error changing view to {view_name}: {e}")

    def notify_view_change(self, selection):
        try:
            logger.debug(f"Notifying view change: {selection}")
            variant = 'R' if selection == "Restaurant" else 'S' if selection == "School" else None
            if variant:
                logger.debug(f"Initializing GUI with variant: {variant}")
                self.init_gui(variant)
            else:
                logger.warning(f"Unknown selection for view change: {selection}")

            self.change_view(selection)
        except Exception as e:
            logger.error(f"Error notifying view change: {e}")

    def init_gui(self, variant):
        try:
            logger.debug(f"Initializing GUI for variant {variant}")
            self.gui = Gui(variant)
            logger.debug(f"GUI initialized: {self.gui}")
        except Exception as e:
            logger.error(f"Error initializing GUI for variant {variant}: {e}")

    def update_scheduler_parameters(self, parameters):
        try:
            logger.debug(f"Updating scheduler parameters: {parameters}")
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

            current_state = {
                'accuracy': self.gui.scheduler.accuracy,
                'allocation': self.gui.scheduler.allocation,
                'name': getattr(self.gui.scheduler, 'name', None),
                'availability': getattr(self.gui.scheduler, 'availability', None),
                'worse_availability': getattr(self.gui.scheduler, 'worse_availability', None),
                'position': getattr(self.gui.scheduler, 'position', None)
            }

            logger.info(f"Scheduler parameters updated successfully. Current state: {current_state}")
        except Exception as e:
            logger.error(f"Error updating scheduler parameters: {e}")
