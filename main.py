from ui.app import App
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='scheduler.log',
    filemode='w',  # Overwrite the log file at each run
    format='%(asctime)s - %(name)s - %(levelname)s >> %(message)s'
)

# main logger object
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.debug("Starting the application")
        app = App()
        app.mainloop()
    except Exception as e:
        logger.critical(f"Critical error occurred while running the application: {e}", exc_info=True)
