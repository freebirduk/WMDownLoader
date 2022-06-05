import abc


class IWMDatabaseService(abc.ABC):
    @abc.abstractmethod
    def get_most_recent_observation_date(self):
        pass

    def get_latest_observations(self):
        pass
