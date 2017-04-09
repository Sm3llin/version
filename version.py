class Version(object):
    def __init__(self):
        self._built = False
        self.__current_version = 1
        self.__max_version = 1

        self._objects = list()

    def __len__(self):
        return self.__max_version

    def __repr__(self):
        return f'<Version total versions: {self.max}>'

    def create_next(self):
        for obj in self._objects:
            for key, value in obj.__dict__.items():
                if '__version' not in key:
                    obj.__dict__[key].append(value[self.max])

        self.__max_version += 1
        self.__current_version = self.__max_version

        return self.__max_version

    def switch(self, version):
        self.__current_version = version

    @property
    def max(self):
        return self.__max_version

    @property
    def current(self):
        return self.__current_version

    @property
    def previous(self):
        return self.current - 1

    @property
    def next(self):
        return self.current + 1
