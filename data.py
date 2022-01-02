class Data():
    def __init__(self) -> None:
        pass


class DynamicData(Data):
    def __init__(self) -> None:
        super().__init__()
        self.__zif = ''

    @property
    def zif(self):
        return self.__zif

    @zif.setter
    def zif(self, v):
        self.__zif = v