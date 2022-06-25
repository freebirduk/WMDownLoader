from datetime import date
from IDateTimeProvider import IDateTimeProvider


# Simply returns the current datetime. Other versions of this can return fake datetime for
# testing purposes.
class DateTimeProvider(IDateTimeProvider):

    def now(self):
        return date.today()
