class Version(object):
    def __init__(self):
        self._built = False
        self.__current_version = 1
        self.__max_version = 1

    def __len__(self):
        return self.__max_version

    def __repr__(self):
        return f'<Version total versions: {self.max}>'

    def create_next(self):
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
