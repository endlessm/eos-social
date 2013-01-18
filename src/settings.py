import ConfigParser
from defaults import Defaults


class MetaSettings(type):


    INI_FILE_PATH = '/etc/eos-social/social_bar.ini'
    config = None

    @classmethod
    def load_settings(cls):
        try:
            cls.config = ConfigParser.ConfigParser()
            cls.config.read(cls.INI_FILE_PATH)
        except:
            print 'loading failed ::%r' % cls.INI_FILE_PATH

    @classmethod
    def _get_value(cls, name):
        value = None
        try:
            value = cls.config.get('MAIN', name)
        except:
            print 'no value::%r in MAIN section' % name
            print 'fallback to default value ..'
            if hasattr(Defaults, name):
                value = getattr(Defaults, name)
                print 'found default value, using %r' % value
            else:
                print 'no default value for %r, using None' % name
        return value

    @classmethod
    def __getattr__(cls, name):
        return cls._get_value(name)


class Settings():
    __metaclass__ = MetaSettings


Settings.load_settings()
