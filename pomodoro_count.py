from datetime import datetime


class ArgumentError(Exception):
    def __init__(self, message):
        self.message = message


def get_pomodoros(start, end, rest=0):
    if not isinstance(start, datetime):
        raise ArgumentError("Start is not a datetime and doesn't inherit from datetime.")

    if not isinstance(end, datetime):
        raise ArgumentError("End is not a datetime and doesn't inherit from datetime.")

    if start >= end:
        raise ArgumentError("Start date and time must be before the end date and time.")

    time_delta = end - start
    pomodoro_length = 60 * 30
    pomodoro_count = int(time_delta.total_seconds() / pomodoro_length)

    # if there's zero or one pomodoro, there's no need to calculate the rest period
    if pomodoro_count <= 1:
        return pomodoro_count

    # re-calculate possible number of pomodoros with a prolonged rest period between each
    while True:
        time_taken = (pomodoro_count * pomodoro_length) + ((pomodoro_count - 1) * rest)

        if time_taken > time_delta.total_seconds():
            pomodoro_count -= 1
        else:
            break

    return pomodoro_count
