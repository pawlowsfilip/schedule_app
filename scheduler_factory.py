from scheduler.variants.scheduler_r import Scheduler_r
from scheduler.variants.scheduler_s import Scheduler_s
import logging

logger = logging.getLogger(__name__)


class SchedulerFactory:
    @staticmethod
    def get_scheduler(variant, **kwargs):
        logger.info(f"Attempting to get a scheduler for variant: {variant} with parameters: {kwargs}")
        try:
            if variant == 'R':
                logger.debug("Creating Scheduler_r instance.")
                return Scheduler_r(variant, **kwargs)
            if variant == 'S':
                logger.debug("Creating Scheduler_s instance.")
                return Scheduler_s(variant, **kwargs)
            else:
                logger.warning(f"Unknown variant provided: {variant}. Returning None.")
                return None
        except Exception as e:
            logger.error(f"Error while creating scheduler for variant {variant}. Exception: {e}")
            return None
