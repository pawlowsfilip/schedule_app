from worker import Worker
from worker_manager import Worker_Manager

if __name__ == '__main__':
    worker_manager1 = Worker_Manager()
    worker_manager1.add_worker('Filip', {'21.07': '8:00-10:00,11:00-15:00', '22.07': '9:00-11:00'},
                               {'21.07': '10:00-11:00', '22.07': '11:00-13:00'}, 'Student')

    print(worker_manager1.get_days())
    print(worker_manager1.get_hours('22.07'))
    #print(worker_manager1.get_available_workers_via_availability('21.07', ))

