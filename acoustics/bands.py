"""
Bands
=====



"""


from __future__ import division

import numpy as np

from acoustics.decibel import dbsum

OCTAVE_CENTER_FREQUENCIES = np.array([16, 31.5, 63, 125, 250, 500,
                             1000, 2000, 4000, 8000, 16000])
"""
Preferred 1/1-octave band center frequencies.
"""

THIRD_OCTAVE_CENTER_FREQUENCIES = np.array([12.5,     16,    20,   25, 31.5,    40,
                                50,       63,    80,  100,  125,   160,
                                200,     250,   315,  400,  500,   630,
                                800,    1000,  1250, 1600, 2000,  2500,
                                3150,   4000,  5000, 6300, 8000, 10000,
                                12500, 16000, 20000])
"""
Preferred 1/3-octave band center frequencies.
"""


def octave(first, last):
    """
    Generate a Numpy array for central frequencies of octave bands.

    There are more information on how to calculate 'real' bands in
    http://blog.prosig.com/2006/02/17/standard-octave-bands/

    Parameters
    ----------
    first : scalar
        First octave centerfrequency.

    last : scalar
        Last octave centerfrequency.

    Returns
    -------
    octave_bands : array
        An array of centerfrequency octave bands.
    """
    octave_bands = OCTAVE_CENTER_FREQUENCIES
    low = np.where(octave_bands == first)[0]
    high = np.where(octave_bands == last)[0]
    return octave_bands[low: high+1]


def octave_low(first, last):
    return octave(first, last)/np.sqrt(2.0)


def octave_high(first, last):
    return octave(first, last)*np.sqrt(2.0)


def third(first, last):
    """
    Generate a Numpy array for central frequencies of third octave bands.

    Parameters
    ----------
    first : scalar
       First third octave centerfrequency.

    last : scalar
        Last third octave centerfrequency.

    Returns
    -------
    octave_bands : array
        An array of centerfrequency third octave bands.
    """
    third_oct_bands = THIRD_OCTAVE_CENTER_FREQUENCIES
    low = np.where(third_oct_bands == first)[0]
    high = np.where(third_oct_bands == last)[0]
    return third_oct_bands[low: high+1]


def third_low(first, last):
    return third(first, last)/2.0**(1.0/6.0)


def third_high(first, last):
    return third(first, last)*2.0**(1.0/6.0)

    
def third2oct(levels, axis=None):
    """
    Calculate Octave levels from third octave levels.
    
    :param levels: Array containing third octave levels.
    :type: :class:`np.ndarray`
    :param axis: Axis over which to perform the summation. 
    :type axis: :class:`int`
    
    :returns: Third octave levels
    :rtype: :class:`np.ndarray`
    
    .. note:: The number of elements along the summation axis should be a factor of 3.
    """
    
    levels = np.array(levels)
    axis = axis if axis is not None else levels.ndim - 1
    
    try:
        assert(levels.shape[axis]%3 == 0)
    except AssertionError:    
        raise ValueError("Wrong shape.")
    shape = list(levels.shape)
    shape[axis] = shape[axis] // 3
    shape.insert(axis+1, 3)
    levels = np.reshape(levels, shape)
    return np.squeeze(dbsum(levels, axis=axis+1))

def _check_band_type(freqs):
    """Check if an array contains octave or third octave bands values sorted
    or unsorted.
    """
    octave_bands = octave(16, 16000)
    third_oct_bands = third(12.5, 20000)

    def _check_sort(freqs, bands):
        index = np.where(np.in1d(bands, freqs))[0]
        band_pos = index - index[0]
        if (band_pos == np.arange(band_pos.size)).all():
            sorted = True
        else:
            sorted = False
        return sorted

    if np.in1d(freqs, octave_bands).all() == True:
        is_sorted = _check_sort(freqs, octave_bands)
        if is_sorted is True:
            band_type = 'octave'
        else:
            band_type = 'octave-unsorted'
    elif np.in1d(freqs, third_oct_bands).all() == True:
        is_sorted = _check_sort(freqs, third_oct_bands)
        if is_sorted is True:
            band_type = 'third'
        else:
            band_type = 'third-unsorted'
    else:
        band_type = None

    return band_type
