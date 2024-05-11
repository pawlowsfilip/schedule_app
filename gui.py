import logging
import json

from scheduler_factory import SchedulerFactory
from excel_exporter import ExcelExporter
from worker import Worker
from worker_manager import Worker_Manager

logger = logging.getLogger(__name__)

class Gui:
    def __init__(self, variant):
        logger.info("Initializing GUI for variant %s", variant)
        try:
            self.scheduler = SchedulerFactory().get_scheduler(variant)
            logger.debug("Scheduler object created successfully for variant %s", variant)
        except Exception as e:
            logger.error("Error initializing GUI: %s", e)
            raise

    def make_schedule(self):
        logger.info("Making schedule")
        try:
            schedule = self.scheduler.make_schedule()
            logger.debug("Schedule created: %s", schedule)
            return schedule
        except Exception as e:
            logger.error("Error making schedule: %s", e)
            raise

    def export_schedule(self):
        logger.info("Exporting schedule to Excel")
        try:
            schedule = self.make_schedule()
            logger.debug("Schedule data: %s", schedule)
            return ExcelExporter(schedule).export_to_excel()
        except Exception as e:
            logger.error("Error exporting schedule: %s", e)
            raise

    def update_day(self, day):
        try:
            self.scheduler.day = day
            logger.info("Day updated to: %s", day)
        except Exception as e:
            logger.error("Error updating day: %s", e)
            raise

    def update_accuracy(self, accuracy):
        try:
            self.scheduler.accuracy = accuracy
            logger.info("Accuracy updated to: %s", accuracy)
        except Exception as e:
            logger.error("Error updating accuracy: %s", e)
            raise

    def update_allocation(self, allocation):
        try:
            self.scheduler.allocation = allocation
            logger.info("Allocation updated to: %s", allocation)
        except Exception as e:
            logger.error("Error updating allocation: %s", e)
            raise

    def update_name(self, name):
        try:
            self.scheduler.name = name
            logger.info("Name updated to: %s", name)
        except Exception as e:
            logger.error("Error updating name: %s", e)
            raise

    def update_availability(self, availability):
        try:
            self.scheduler.availability = availability
            logger.info("Availability updated to: %s", availability)
        except Exception as e:
            logger.error("Error updating availability: %s", e)
            raise

    def update_worse_availability(self, worse_availability):
        try:
            self.scheduler.worse_availability = worse_availability
            logger.info("Worse availability updated to: %s", worse_availability)
        except Exception as e:
            logger.error("Error updating worse availability: %s", e)
            raise

    def update_position(self, position):
        try:
            self.scheduler.position = position
            logger.info("Position updated to: %s", position)
        except Exception as e:
            logger.error("Error updating position: %s", e)
            raise

    def update_workers(self, workers, position_priorities):
        try:
            self.scheduler.worker_manager = Worker_Manager(*workers)
            self.scheduler.worker_manager.set_position_priorities(position_priorities)
            logger.info("Workers updated and position priorities set")
        except Exception as e:
            logger.error("Error updating workers or setting priorities: %s", e)
            raise

    @staticmethod
    def read_json_data(filepath):
        logger.info("Reading JSON data from %s", filepath)
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                logger.debug("JSON data read successfully: %s", data)
                return data
        except Exception as e:
            logger.error("Error reading JSON data: %s", e)
            raise

    def update_scheduler_s_from_json(self, filepath):
        logger.info("Updating scheduler from JSON data in %s", filepath)
        try:
            data = self.read_json_data(filepath)
        except Exception as e:
            logger.error("Failed to read JSON data: %s", e)
            return

        allocation = {}
        workers = []

        for entry in data:
            day = entry.get("day")

            if not day:
                logger.warning("Skipping entry due to missing 'day' field: %s", entry)
                continue
            if "time_frames" in entry:
                time_frames_str = entry["time_frames"]

                if not time_frames_str:
                    logger.warning("Empty 'time_frames' for day: %s", day)
                    continue

                time_frames_list = [tf.strip() for tf in time_frames_str.split(";")]

                if day not in allocation:
                    allocation[day] = {}

                for tf in time_frames_list:
                    try:
                        time_frame, workers_needed = map(str.strip, tf.rsplit(": ", 1))
                        workers_needed = int(workers_needed)
                        allocation[day][time_frame] = workers_needed
                    except (ValueError, IndexError) as e:
                        logger.warning("Invalid time frame format for day %s: %s", day, e)
            else:
                logger.warning("Missing 'time_frames' field for day: %s", day)

            if "name" in entry:
                try:
                    worker = Worker(
                        name=entry["name"],
                        availability=entry["availability"],
                        worse_availability=entry["worse_availability"]
                    )
                    workers.append(worker)
                except Exception as e:
                    logger.warning("Error creating worker from entry: %s. Error: %s", entry, e)
            else:
                logger.warning("Missing 'name' field in worker entry: %s", entry)

        try:
            self.update_allocation(allocation)
            self.update_workers(workers)
            logger.info("Successfully updated scheduler with allocation and workers")
        except Exception as e:
            logger.error("Error updating scheduler allocation or workers: %s", e)

    def update_scheduler_r_from_json(self, filepath):
        logger.info("Updating scheduler R from JSON data in %s", filepath)
        try:
            data = self.read_json_data(filepath)
        except Exception as e:
            logger.error("Failed to read JSON data: %s", e)
            return

        allocation = {}
        accuracy = 1.0  # Default accuracy
        workers = []
        position_priorities = {}

        for entry in data:
            if "day" in entry and "accuracy" in entry:
                try:
                    day = entry["day"]
                    accuracy = float(entry["accuracy"])
                    allocation_str = entry["allocation"]

                    time_frames = [tf.strip() for tf in allocation_str.split(";")]

                    if day not in allocation:
                        allocation[day] = {}

                    for tf in time_frames:
                        try:
                            time_frame, workers_needed = map(str.strip, tf.split(": "))
                            workers_needed = int(workers_needed)
                            allocation[day][time_frame] = workers_needed
                        except (ValueError, IndexError) as e:
                            logger.warning("Invalid time frame format for day %s: %s", day, e)
                except (ValueError, KeyError) as e:
                    logger.warning("Error processing 'day' or 'accuracy' fields: %s", e)
            else:
                logger.warning("Missing 'day' or 'accuracy' field in entry: %s", entry)

            if "name" in entry:
                try:
                    worker = Worker(
                        name=entry["name"],
                        availability=entry.get("availability", ""),
                        worse_availability=entry.get("worse_availability", ""),
                        position=entry.get("position", "")
                    )
                    workers.append(worker)
                except Exception as e:
                    logger.warning("Error creating worker from entry: %s. Error: %s", entry, e)
            else:
                logger.warning("Missing 'name' field in worker entry: %s", entry)

            if "position_priorities" in entry:
                try:
                    position_priorities = entry["position_priorities"]
                except KeyError as e:
                    logger.warning("Error processing 'position_priorities': %s", e)
        try:
            self.update_accuracy(accuracy)
            self.update_allocation(allocation)
            self.update_workers(workers, position_priorities)
            logger.info("Successfully updated scheduler R with allocation, workers and position priorities")
        except Exception as e:
            logger.error("Error updating scheduler allocation, workers or position priorities: %s", e)
