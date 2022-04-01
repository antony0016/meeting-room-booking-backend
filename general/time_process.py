from meeting_rooms.serializers import ReservationSerializer
from meeting_room_booking_backend.settings import SHOW_DETAIL
from datetime import datetime


# def time_relation(stand_time: dict, check_time: dict) -> int:
#     for key in stand_time.keys():
#         if int(check_time[key]) > int(stand_time[key]):
#             return 1
#         elif int(check_time[key]) < int(stand_time[key]):
#             return -1
#     return 0


def time_relation(stand_time: str, check_time: str) -> int:
    print(check_time, stand_time, check_time > stand_time)
    if check_time > stand_time:
        return 1
    elif check_time < stand_time:
        return -1
    return 0


def in_time_check(start_time: str, end_time: str, check_times: str) -> int:
    start_time = ":".join(["0" + value if len(value) == 1 else value for value in start_time.split(":")])
    end_time = ":".join(["0" + value if len(value) == 1 else value for value in end_time.split(":")])
    check_times = ":".join(["0" + value if len(value) == 1 else value for value in check_times.split(":")])
    start_relation = time_relation(start_time, check_times)
    end_relation = time_relation(end_time, check_times)

    if SHOW_DETAIL:
        print("in_time_check")
        # print(start_relation, end_relation)
        # print(start_time_obj, end_time_obj, check_times_obj)

    if start_relation + end_relation == -2:
        return -1
    elif start_relation + end_relation == 2:
        return 1
    return 0


def is_overlap(reservation1: ReservationSerializer.data, reservation2: ReservationSerializer.data):
    start_check = in_time_check(reservation1.get('start_time'), reservation1.get('end_time'),
                                reservation2.get('start_time'))
    end_check = in_time_check(reservation1.get('start_time'), reservation1.get('end_time'),
                              reservation2.get('end_time'))
    time = [str(datetime.now().time().hour), str(datetime.now().time().minute)]
    formatted_time = ["0" if len(t) == 1 else "" + t for t in time]
    now_time = ":".join(formatted_time)

    if SHOW_DETAIL:
        print('is_overlap')
        print(reservation1.get('start_time'), reservation1.get('end_time'))
        print(reservation2.get('start_time'), reservation2.get('end_time'))
        print(reservation2.get('start_time'), reservation2.get('end_time'))
        print(start_check, end_check)
    if start_check == 0:
        return True
    if end_check == 0:
        return True
    if start_check + end_check == 0:
        return True
    return False
