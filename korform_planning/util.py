import string

class FieldFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        value = None
        try:
            value = super(FieldFormatter, self).get_value(key, args, kwargs)
        except IndexError, KeyError:
            pass
        return value if value is not None else u""

date_format = "%b %d"
time_format = "%H:%M"
full_format = date_format + " " + time_format

def _choose_format(dt):
    is_midnight = dt.hour == 0 and dt.minute == 0 and dt.second == 0
    return date_format if is_midnight else full_format

def format_datetime(dt):
    return dt.strftime(_choose_format(dt))

def format_datetime_diff(dt1, dt2):
    return u"{0} - {1}".format(
        dt1.strftime(_choose_format(dt1)),
        dt2.strftime(_choose_format(dt2) if dt1.date() != dt2.date() else time_format)
    )
