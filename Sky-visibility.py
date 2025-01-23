from astropy_healpix import HEALPix
import astropy.units as u
from geopy.geocoders import Nominatim
from math import log2, pi, acos


class InvalidResolution(Exception):
    pass


def initialize_healpix(resolution: int) -> HEALPix:
    return HEALPix(nside=resolution, order="nested")

def get_visible_pixels(longitude, latitude, healpix: HEALPix) -> HEALPix:
    return healpix.cone_search_lonlat(longitude * u.deg, latitude * u.deg, radius=1 * u.deg)

def compute_solid_angle(visible_pixels, healpix: HEALPix) -> float:
    return len(visible_pixels) * healpix.pixel_area

def compute_area_from_angle(solid_angle, radius=6371000 * u.m) -> u.Quantity:
    area = solid_angle * radius**2
    return area

def compute_cone_opening_angle(solid_angle) -> float:
    solid_angle_value = solid_angle.to_value(u.sr)
    return 2 * acos(1 - (solid_angle_value / (2 * pi)))

def lookup_location(longitude, latitude) -> str:
    geolocator = Nominatim(user_agent="sky_view_project")
    try:
        location = geolocator.reverse(f"{latitude},{longitude}")
        return location.address if location else "Location not found"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    resolution = int(input("Enter resolution (must be a power of 2): "))
    if not log2(resolution).is_integer():
        raise InvalidResolution("Resolution must be a power of 2!")

    longitude = float(input("Enter longitude: "))
    latitude = float(input("Enter latitude: "))

    healpix = initialize_healpix(resolution)
    visible_pixels = get_visible_pixels(longitude, latitude, healpix)

    solid_angle = compute_solid_angle(visible_pixels, healpix)
    area = compute_area_from_angle(solid_angle)
    cone_angle = compute_cone_opening_angle(solid_angle)

    location = lookup_location(longitude, latitude)

    print(f"Location: {location}")
    print(f"Solid angle (field of view): {solid_angle}")
    print(f"Cone angle (angular width): {cone_angle}")
    print(f"Surface area: {area}")