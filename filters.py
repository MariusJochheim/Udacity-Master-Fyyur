#----------------------------------------------------------------------------#
# Filters
#----------------------------------------------------------------------------#

from datetime import datetime

import babel

from extensions import app


def format_datetime(value, format='medium'):
    if isinstance(value, datetime):
        date = value
    else:
        value_str = str(value)
        try:
            date = datetime.fromisoformat(value_str)
        except ValueError:
            date = datetime.strptime(value_str, "%Y-%m-%d %H:%M:%S")
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime
