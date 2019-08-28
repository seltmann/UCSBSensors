# arable_physics
# operands are prefixed with x to distinguish them from variables and functions
# used elsewhere function defs are suffixed with _ to distinguish them from
# variables and functions used elsewhere


import calendar

from numpy import pi, log, exp, sin, cos, tan, arcsin, arccos
import numpy as np
import pandas as pd

# Physical constants

Mh2o = 18  # molecular weight of water: g/mol
Mco2 = 44  # molecular weight of CO2: g/mol
Mair = 29  # molecular weight of dry air: g/mol
R = 8.314  # gas constant: J / mol k gas constant
Cp = 1004.67  # specific heat per mass: J / kg air / k
Cp_mol = Cp / 1000 * Mair  # specific heat per mol: J / mol air / k
P = 101.325  # sea level pressure: kPa
SBC = 5.67e-8  # Stefan-Boltzman Const
g = 9.80665  # gravitational acceleration constant m/s^2
SUN = 1367.

seconds_per_day = 86400.

# General utility functions

def doy_(xDatetime):
    doy = xDatetime.dayofyear
    dayfrac = ((xDatetime.hour)*3600. + (xDatetime.minute)*60 + xDatetime.second) / seconds_per_day
    return doy+dayfrac

# Static properties of air

def Tk_(xT):  # pragma: no cover
    """

    :param xT - temperature (C):
    :return:
    """
    return xT + 273.2


def lambda_(xTk):  # pragma: no cover
    """ latent heat of vaporization: J / g

    :param xTk - temperature (K):
    :return:
    """
    return 3149 - 2.370 * xTk


def lambda_mol_(xTk):  # pragma: no cover
    """ latent heat of vaporization: J / mol

    :param xTk - temperature (C):
    :return:
    """
    return lambda_(xTk) * Mh2o


def esat_(xT):  # pragma: no cover
    """ saturation vapor pressure: kPa
        Paw U and Gao (1987) Ag For Met 43:121-145
        Applicaitons of solutions to non-linear energy budget equations

    :param xT - temperature (C):
    :return:
    """
    return (617.4 + 42.22 * xT + 1.675 * xT ** 2 + 0.01408 * xT ** 3 +
            0.0005818 * xT ** 4) / 1000  # Paw U formulation


def ea_(xT, xRH):
    """vapor pressure: kPa 
    
    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :return:
    """
    return esat_(xT)*xRH


def tdew(xT, xRH):
    """ Dewpoint temperature: C
         Eqn from Allen FAO 56
    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :return:    
    """
    ea = ea_(xT, xRH)
    return (116.91+237.3*log(ea)) / (16.78 - log(ea))


def s_(xT):  # pragma: no cover
    """ derivative of saturation vapor pressure: kPa / C
        Paw U and Gao (1987) Ag For Met 43:121-145
        Applicaitons of solutions to non-linear energy budget equations

    :param xT - temperature (C):
    :return:
    """
    return (42.22 + 2 * 1.675 * xT + 3 * 0.01408 * xT ** 2 +
            4 * 0.0005818 * xT ** 3) / 1000  # Paw U formulation


def dsdT_(xT):  # pragma: no cover
    """ second derivative of saturation vapor pressure: kPa / C^2
        Paw U and Gao (1987) Ag For Met 43:121-145
        Applicaitons of solutions to non-linear energy budget equations

    :param xT - temperature (C):
    :return:
    """
    return (2.0 * 1.675 + 6 * 0.01408 * xT + 12.0 * 0.0005818 * xT ** 2) / 1000.0  # NOQA


def ea_(xT, xRH):  # pragma: no cover
    """ vapor pressure: kPa

    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :return:
    """
    return esat_(xT) * xRH


def VPD_(xT, xRH):  # pragma: no cover
    """ vapor pressure deficit: kPa

    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :return:
    """
    return esat_(xT) * (1.0 - xRH)


def dry_air_(xT, xRH, xP=P):  # pragma: no cover
    """ mass of dry air: kg / m3   (n/V = P/RT)

    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :param xP - pressure (kPa):
    :return:
    """
    ea = ea_(xT, xRH)
    return ((xP - ea) * Mair) / (R * Tk_(xT))


def air_h2o_(xT, xRH, xP=P):  # pragma: no cover
    """ mass of water in air: gH2O / m3

    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :param xP - pressure (kPa):
    :return:
    """
    ea = ea_(xT, xRH)
    return (ea / xP) * 622.0 * dry_air_(xT, xRH)


def dry_air_mol_(xT, xRH, xP=P):  # pragma: no cover
    """ mass of dry air: mol / m3

    :param xT - temperature (C):
    :param xRH - relative humidity (0.0 - 1.0):
    :param xP - pressure (kPa):
    :return:
    """
    return dry_air_(xT, xRH, xP) * 1000.0 / Mair


def moist_air_(xT, xRH, xP=P):  # pragma: no cover
    """ mass of moist air: kg / m3

    :param xT:
    :param xRH:
    :param xP:
    :return:
    """
    return dry_air_(xT, xRH, xP) + air_h2o_(xT, xRH, xP) / 1000.0


def gamma_(xT, xP=P):  # pragma: no cover
    """ psychrometric constant kPa / C

    :param xT - temperature (C):
    :param xP - pressure (kPa):
    :return:
    """
    return Cp_mol / lambda_mol_(Tk_(xT)) * xP


def Tbb_(xLW):  # pragma: no cover
    """ effective blackbody temperature

    :param xLW - Longwave radiation (W/m2):
    :return:
    """
    return (xLW / SBC) ** (0.25) - 273.2


def LWbb_(xT):  # pragma: no cover
    """ Stefan Boltzman equation: W/m2

    :param xT - temperature (C):
    :return:
    """
    return SBC * (Tk_(xT) ** 4)


# Radiation and Solar energy

def solar_phi_(xLat):  # pragma: no cover
    """ Latitude in radians pi/2 at the poles, 0 at the equator

    :param xLat - Latitude (decimal degree):
    :return:
    """
    return xLat * pi / 180.0


def solar_utc_offset_(xDatetime, xLon):  # pragma: no cover
    """ difference between solar time and utc time, in fractions of a day

    :param xDatetime:
    :param xLon:
    :return:
    """  

    dayfrac = ((xDatetime.hour)*3600. + (xDatetime.minute)*60 + xDatetime.second) / seconds_per_day
    solar_utc_offset = xLon / 360.0 # fractions of day, ranging from -0.5 to +0.5
    
    return  dayfrac + solar_utc_offset

def solar_noon_(xDatetime, xLon, datetime=True):
    """ difference between solar time and utc time, in fractions of a day

    :param xDatetime:
    :param xLon:
    :return: datetime or decimal day
    """                  
    solar_noon_offset = 0.5 - (xLon / 360.0)
    
    td = pd.to_timedelta(solar_noon_offset, unit = 'd')#.to_pytimedelta()
    
    if (datetime):
        solar_noon = xDatetime.normalize() + td
    else:
        solar_noon = xDatetime.dayofyear + solar_noon_offset
        
    return solar_noon

def solar_delta_(xDatetime, xLon):  # pragma: no cover
    """ declination angle, varying over the year

    :param xDatetime:
    :return:
    """
    tropic = 23.45 * pi / 180.0
    leap = (xDatetime.year % 4 == 0) | (xDatetime.year % 100 == 0)
    yearl = np.ones((xDatetime.year.size)) * 365. + leap
    equinox = np.ones((xDatetime.year.size)) * 173. + leap
    solar_utc_offset = solar_utc_offset_(xDatetime, xLon)
    fdoy = (xDatetime.dayofyear - equinox + solar_utc_offset) / yearl # fractions of year
    return tropic * cos(2.0 * pi * fdoy)


def solar_theta_(xDatetime, xLon):  # pragma: no cover
    """ hour angle, the fraction of a full rotation has turned after local solar noon 
        cos(theta) is 1 at solar noon

    :param xDatetime:
    :param xLon:
    :return:
    """

    solar_utc_offset = solar_utc_offset_(xDatetime, xLon) - 0.5
    
    theta0 = (solar_utc_offset - 1)*(solar_utc_offset >= 1)
    theta1 = solar_utc_offset*((solar_utc_offset >= 0) & (solar_utc_offset < 1))
    theta2 = (solar_utc_offset + 1)*(solar_utc_offset < 0)
    theta = theta0 + theta1 + theta2
    
    return 2 * pi * theta


def solar_psi_(xDatetime, xLat, xLon):  # pragma: no cover
    """ solar zenith angle (0 overhead, pi/2 at horizon)
        typically, allowed to go 9 deg below the horizon

    :param xDatetime:
    :param xLat:
    :param xLon:
    :return:
    """
    phi = solar_phi_(xLat)
    delta = solar_delta_(xDatetime, xLon)
    theta = solar_theta_(xDatetime, xLon)
    psi = arccos(sin(phi) * sin(delta) + cos(phi) * cos(delta) * cos(theta))
    return psi


def solar_alpha_(xDatetime, xLat, xLon):  # pragma: no cover
    """ solar azimuth angle relative to due north
    # typically, allowed zero at night, ie when sza >9 deg below the horizon

    :param xDatetime:
    :param xLat:
    :param xLon:
    :return:
    """
    psi = solar_psi_(xDatetime, xLat, xLon)
    delta = solar_delta_(xDatetime, xLon)
    theta = solar_theta_(xDatetime, xLon)
    phi = solar_phi_(xLat)
    
    ca = (sin(delta) - sin(phi)*cos(psi)) / (cos(phi)*sin(psi))
    ca = np.clip(ca, -1.0, 1.0)
    
    solar_utc_offset = solar_utc_offset_(xDatetime, xLon)
    
    alpha0 = arccos(ca)*((theta >= pi) & (solar_utc_offset < 2*pi))  
    alpha1 = (2*pi - arccos(ca))*((theta >= 0.0) & (theta < pi))  
    
    return alpha0 + alpha1

def solar_daylength_(xDatetime, xLat, xLon):  # pragma: no cover
    """
    NOT TESTED

    :param xDatetime:
    :param xLat:
    :param xLon:
    :return:
    """
    phi = solar_phi_(xLat)
    delta = solar_delta_(xDatetime)
    return (2.0 * 24.0 / pi) * arccos(np.tan(phi) * tan(delta))


def SWpot_(xDatetime, xLat, xLon):
    
    psi = solar_psi_(xDatetime, xLat, xLon)
    
    etr0 = 0 * (cos(psi) < 0)
    etr1 = SUN * cos(psi) * (cos(psi) >= 0)
    
    return etr0 + etr1
