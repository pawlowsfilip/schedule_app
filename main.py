from models import Worker
import database


if __name__ == '__main__':
    database.create_db()
    worker = Worker('Filip', 'Student', '31/07/2023-06/08/2023', {
        'Mon': '8:00-10:00',
        'Tue': '8:00-10:00',
        'Wed': '8:00-10:00',
        'Thu': '8:00-10:00',
        'Fri': '8:00-10:00'
    })
    database.insert_schedule(worker)
    print(database.get_schedule('Filip'))
    print(database.get_db())
