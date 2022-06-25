import abc


# Simply supplies the current system date. Facilitates testing so that fake date values can be generated.
class IDateTimeProvider(abc.ABC):
    @abc.abstractmethod
    def now(self):
        pass
