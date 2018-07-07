import abc

class NetworkType(abc.ABC):

    @abc.abstractmethod
    def get_socket(self):
        pass
