from worker import Worker
from worker_manager import Worker_Manager

if __name__ == '__main__':
    worker1 = Worker('Filip', {'21.07': '8:00-10:00,11:00-15:00', '22.07': '9:00-11:00'},
                     {'23.07': '11:00-13:00'}, 'Student')
    worker2 = Worker('Natalia', {'21.07': '8:00-10:00,11:00-15:00', '22.07': '9:00-11:00'},
                     {'23.07': '11:00-13:00'}, 'Student')


    '''TEST WORKING MANAGER'''
    wm1 = Worker_Manager(worker1, worker2)
    print(wm1)
    print(wm1.get_available_workers("21.07", "19:00-20:00"))
    print(wm1.get_available_workers_if_needed("23.07", "8:00-15:00"))


    # '''TEST WORKER'''
    # # co tutaj zrobic? worker jest dostepny ale tylko od 8:00 do 10:00, potem zostaje godzina do obstawienia
    # # mój pomysł jest taki, zeby iterować sobie może co godzine i patrzeć kto jest available
    # print(worker1.is_available('23.07', "8:00-15:00"))


