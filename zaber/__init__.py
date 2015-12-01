# See https://docs.python.org/2/tutorial/modules.html#packages 
# for info on why this file exists.

from pkg_resources import get_distribution
__version__ = get_distribution('zaber.serial').version
