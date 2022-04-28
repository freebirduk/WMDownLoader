import abc


class IWeatherUndergroundApiService(abc.ABC):
    @abc.abstractmethod
    def get_hourly_observations_for_date(self, date):
        pass
