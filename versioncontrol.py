import pickle

from versions.version import Version
from versions.exceptions import VersionLockedError


class VersionControl(object):
    __controlled_objects = list()

    __flags = False
    __pickling = False

    def __init__(self, version=Version()):
        version._objects.append(self)

        self.__version = version
        self.version._built = True

    def __len__(self):
        return self.version.max + 1

    def __getitem__(self, item):
        if item >= len(self) - 1:
            self.version.switch(self.version.max)
            raise IndexError
        self.__version.switch(item + 1)
        return self

    def __setattr__(self, key, value):
        if '_VersionControl__version' in key or '__pickling' in key:
            object.__getattribute__(self, '__dict__')[key] = value
            return

        #
        version = object.__getattribute__(self, '_VersionControl__version')
        if not version._built:
            object.__getattribute__(self, '__dict__')[key] = value
            return

        if key not in object.__getattribute__(self, '__dict__'):
            object.__getattribute__(self, '_VersionControl__controlled_objects').append(key)

            control_value = [None for _ in range(len(version)+1)]
            control_value[version.current] = value

            object.__getattribute__(self, '__dict__')[key] = control_value

        else:
            if object.__getattribute__(self, '_VersionControl__flags') or version.current is version.max:
                object.__getattribute__(self, '__dict__')[key][version.current] = value
            else:
                raise VersionLockedError

    def __getattribute__(self, attr):
        skippables = ['__controlled_objects', '__pickling', '__flags', '__version', 'version']
        if not [True for skip in skippables if skip in attr]:
            if attr in object.__getattribute__(self, '_VersionControl__controlled_objects') and \
                    not object.__getattribute__(self, '_VersionControl__pickling'):
                return object.__getattribute__(self, attr)[object.__getattribute__(self, '_VersionControl__version').current]
        return object.__getattribute__(self, attr)

    def __setstate__(self, state):
        for key, value in state.items():
            object.__getattribute__(self, '_VersionControl__controlled_objects').append(key)
            object.__getattribute__(self, '__dict__')[key] = value

    """ Version Control Logic """

    def create_next(self):
        self.__version.create_next()

    @property
    def version(self):
        return self.__version

    @property
    def previous(self):
        """ Returns an object which has a dict of the previous versions data for lookup """
        return VersionInfoFinder(self, self.version.previous)

    """ Object Pickling """

    def save(self):
        self.__pickling = True
        with open('test.obj', 'wb') as file:
            pickle.dump(self, file)
        self.__pickling = False

    @staticmethod
    def load(location):
        global Version
        from versions.version import Version

        with open(location, 'rb') as file:
            obj = pickle.load(file)
        obj.version._built = True
        obj._finish_load()
        return obj

    def _finish_load(self):
        self.__pickling = False


class VersionInfoFinder(object):
    def __init__(self, version_object, version):
        self.__filter = list()
        self.__version = version

        self.__title = "%r" % version_object

        for key, values in version_object.__dict__.items():
            self.__filter.append(key)
            self.__dict__[key] = values

    def __getitem__(self, item):
        try:
            return self.__dict__[item][self.__version]
        except IndexError:
            return None

    def __getattribute__(self, item):
        if item not in object.__getattribute__(self, '_VersionInfoFinder__filter'):
            return object.__getattribute__(self, item)
        return object.__getattribute__(self, item)[object.__getattribute__(self, '_VersionInfoFinder__version')]

    def __repr__(self):
        return '<Info %s>' % self.__title
