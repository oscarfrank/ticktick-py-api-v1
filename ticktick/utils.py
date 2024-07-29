import datetime
import pytz

def parse_date_or_datetime(date_input):
    if not date_input:
        return None
    if isinstance(date_input, (datetime.date, datetime.datetime)):
        return date_input
    if isinstance(date_input, str):
        if date_input.lower() == 'today':
            return datetime.date.today()
        if date_input.lower() == 'tomorrow':
            return datetime.date.today() + datetime.timedelta(days=1)
        try:
            # Try to parse as datetime first
            return datetime.datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                # If that fails, try to parse as date
                return datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
            except ValueError:
                print(f"Invalid date format: {date_input}. Please use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS")
                return None
    else:
        print(f"Invalid input type for date: {type(date_input)}. Please use string or datetime object.")
        return None

def format_date_for_api(date_obj):
    if isinstance(date_obj, datetime.datetime):
        # For datetime objects, use the full format with timezone
        return date_obj.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S.000+0000")
    elif isinstance(date_obj, datetime.date):
        # For date objects, use the date at midnight UTC
        return datetime.datetime.combine(date_obj, datetime.time.min).replace(tzinfo=pytz.utc).strftime("%Y-%m-%dT%H:%M:%S.000+0000")
    return None