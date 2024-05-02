# from scheduler.variants.scheduler_s import Scheduler_s
#
# def test_get_time_frames_list_for_one_time_frame():
#     scheduler = Scheduler_s("S", {'21.07': [{"start": "8:00", "end": "8:15", "allocation": 1}]}, "7:00", "14:00")
#     assert len(scheduler._get_time_frames_list()) == 1
#
#
# def test_get_time_frames_list_for_more_than_one_time_frame():
#     scheduler = Scheduler_s("S", {'21.07': [{"start": "8:00", "end": "8:15", "allocation": 1},
#                                             {"start": "9:00", "end": "9:15", "allocation": 2}]}, "7:00", "14:00")
#     assert len(scheduler._get_time_frames_list()) == 2