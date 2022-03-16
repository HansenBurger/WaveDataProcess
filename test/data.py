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


class PatientDomain(Data):
    def __init__(self):
        super().__init__()
        self.__ct = None
        self.__icu = None
        self.__age = None
        self.__pid = None
        self.__rid = None
        self.__sex = None
        self.__name = None
        self.__remark = None
        self.__machine = None

    @property
    def ct(self):
        return self.__ct

    @ct.setter
    def ct(self, v):
        self.__ct = v

    @property
    def icu(self):
        return self.__icu

    @icu.setter
    def icu(self, v):
        self.__icu = v

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, v):
        self.__age = v

    @property
    def pid(self):
        return self.__pid

    @pid.setter
    def pid(self, v):
        self.__pid = v

    @property
    def rid(self):
        return self.__rid

    @rid.setter
    def rid(self, v):
        self.__rid = v

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, v):
        self.__sex = v

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, v):
        self.__name = v

    @property
    def remark(self):
        return self.__remark

    @remark.setter
    def remark(self, v):
        self.__remark = v

    @property
    def machine(self):
        return self.__machine

    @machine.setter
    def machine(self, v):
        self.__machine = v