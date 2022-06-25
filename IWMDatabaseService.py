import abc


class IWMDatabaseService(abc.ABC):
    @abc.abstractmethod
    def get_most_recent_observation_date(self, default_observation_date):
        pass

    def get_latest_observations(self):
        pass

    def save_list_of_observations(self, observations):
        pass
