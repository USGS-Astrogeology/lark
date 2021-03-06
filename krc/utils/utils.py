import functools
import logging
import math
import operator as op

import numpy as np

logger = logging.getLogger(__name__)

def computeinertia(inertia):
    """
    """
    ya = math.log(inertia[0])  # Low inertia
    yb = math.log(inertia[1])  # High inertia
    ninertia = inertia[2]  # Number of inertia steps
    norm = (yb - ya) / (ninertia - 1.0)
    iner = np.exp(ya + np.arange(ninertia) * norm)

    return iner

def enum(*sequential, **named):
    """Handy way to fake an enumerated type in Python
    http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def getnearest(iterable, value):
    """
    Given an iterable, get the index nearest to the input value

    Parameters
    ----------
    iterable : iterable
               An iterable to search

    value : int, float
            The value to search for

    Returns
    -------
        : int
          The index into the list
    """
    return min(enumerate(iterable), key=lambda i: abs(i[1] - value))

def checkbandnumbers(bands, checkbands):
    """
    Given a list of input bands, check that the passed
    tuple contains those bands.

    In case of THEMIS, we check for band 9 as band 9 is the temperature
    band required to derive thermal temperature.  We also check for band 10
    which is required for TES atmosphere calculations.

    Parameters
    -----------
    bands       tuple of bands in the input image
    checkbands  list of bands to check against

    Returns
    --------
    Boolean     True if the bands are present, else False
    """
    for c in checkbands:
        if c not in bands:
            return False
    return True

def checkdeplaid(incidence):
    """
    Given an incidence angle, select the appropriate deplaid method.

    Parameters
    -----------
    incidence       float incidence angle extracted from the campt results.

    """
    if incidence >= 95 and incidence <= 180:
        return 'night'
    elif incidence >=90 and incidence < 95:
        logger.error("Incidence angle is {}.  This is a twilight image, using night time deplaid.".format(incidence))
        return 'night'
    elif incidence >= 85 and incidence < 90:
        logger.error("Incidence angle is {}.  This is a twilight image, using daytime deplaid".format(incidence))
        return 'day'
    elif incidence >= 0 and incidence < 85:
        logger.error("Incidence angle is {}.  This is a daytime image, you may not want to use this product.".format(incidence))
        return 'day'
    else:
        logger.error("Incidence does not fall between 0 and 180.")
        return False

def check_change_by(iterable, by=1, piecewise=False):
    """
    Check that a given iterable increases by one with each index

    Parameters
    ----------
    iterable : iterable
               Any Python iterable object

    by : int
         The value by which the iterables should be increasing

    piecewise : boolean
                If false, return a boolean for the entire iterable,
                else return a list with elementwise monotinicy checks

    Returns
    -------
    monotonic : bool/list
                A boolean list of all True if monotonic, or including
                an inflection point
    """
    increasing = [True]  + [(by == i[1] - i[0]) for i in zip(iterable,iterable[1:])]
    if piecewise:
        return increasing
    else:
        return all(increasing)


def checkmonotonic(iterable, op=op.gt, piecewise=False):
    """
    Check if a given iterable is monotonically increasing.

    Parameters
    ----------
    iterable : iterable
                Any Python iterable object

    op : object
         An operator.operator object, e.g. op.gt (>) or op.geq(>=)

    piecewise : boolean
                If false, return a boolean for the entire iterable,
                else return a list with elementwise monotinicy checks

    Returns
    -------
    monotonic : bool/list
                A boolean list of all True if monotonic, or including
                an inflection point
    """
    monotonic =  [True] + [x < y for x, y in zip(iterable, iterable[1:])]
    if piecewise == True:
        return monotonic
    else:
        return all(monotonic)

def convert_mean_pressure(elevation):
    """
    Convert from raw elevation, in km, to pressure in Pascals using
    Hugh Kieffer's algorithm.

    689.7 is the constant pressure at sea level

    Parameters
    -----------
    elevation : float or ndarray
                elevation in km

    Returns
    --------
      : float
        Pressure in Pascals
    """
    return 689.7 * np.exp(-elevation / 10.8)

def find_in_dict(obj, key):
    """
    Recursively find an entry in a dictionary

    Parameters
    ----------
    obj : dict
          The dictionary to search
    key : str
          The key to find in the dictionary

    Returns
    -------
    item : obj
           The value from the dictionary
    """
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = find_in_dict(v, key)
            if item is not None:
                return item

# note that this decorator ignores **kwargs
def memoize(obj):
    cache = obj.cache = {}
    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer
