import abc


class IWMErrorService(abc.ABC):
    @abc.abstractmethod
    def handle_error(self,
                     message: str,
                     severity: str = 'Warning',
                     send_email: bool = False,
                     terminate: bool = False,
                     exc_info=None):
        pass
