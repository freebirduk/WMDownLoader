import abc


class IWMEmailService(abc.ABC):
    @abc.abstractmethod
    def send_email(self, message):
        pass
