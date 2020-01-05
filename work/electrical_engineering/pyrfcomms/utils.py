import math
from scipy import constants


def eirp(power_transmit, loss, gain_transmit):  # dBW, dB, dBi
    return power_transmit + loss + gain_transmit


def g_over_t(gain_receive, noise_temperature): # dB, dBK
    return gain_receive - 10*math.log10(noise_temperature)


def ebn0():
    return


def path_loss_troposphere():
    return


def path_loss_ionosphere():
    return


def path_loss_free_space(distance, frequency):
    _path_loss_free_space = 20 * math.log10(( 4 * math.pi * distance * frequency )  / constants.value(u'speed of light in vacuum'))
    return _path_loss_free_space


def slant_range(mean_orbit_altitude, elevation_angle_degrees, object_radius):
    mean_orbit_radius = mean_orbit_altitude + object_radius
    elevation_angle_radians = math.radians(elevation_angle_degrees)
    _slant_range = object_radius * ((((mean_orbit_radius ** 2 / object_radius ** 2) - (math.cos(elevation_angle_radians)) ** 2) ** 0.5) - math.sin(elevation_angle_radians))
    return _slant_range


EARTH_RADIUS = 6378*1000
print(slant_range(500*1000, 10, EARTH_RADIUS))
print(path_loss_free_space(slant_range(500*1000, 10, EARTH_RADIUS), 8125000000))