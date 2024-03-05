import os
import geopandas as gpd
from shapely.geometry import Point


class AustraliaGeographyChecker:
    def __init__(self):
        base_path = os.path.dirname(__file__)  # Gets the directory in which this script is located
        map_base_path = os.path.join(base_path, 'map')  # Path to the 'map' directory

        self.states_shapefiles = {
            "New_South_Wales": os.path.join(map_base_path, "new_south_wales", "cstnswcd_r.shp"),
            "Victoria": os.path.join(map_base_path, "victoria", "cstviccd_r.shp"),
            "Queensland": os.path.join(map_base_path, "queensland", "cstqldmd_r.shp"),
            "Western_Australia": os.path.join(map_base_path, "western_australia", "cstwacd_r.shp"),
            "South_Australia": os.path.join(map_base_path, "south_australia", "cstsacd_r.shp"),
            "Tasmania": os.path.join(map_base_path, "tasmania", "csttascd_r.shp"),
            "Northern_Territory": os.path.join(map_base_path, "northern_territory", "cstntcd_r.shp"),
            "Australian_Capital_Territory": os.path.join(map_base_path, "australia",
                                                         "cstauscd_r.shp")
        }

        self.states_data = {
            state_name: gpd.read_file(shapefile).to_crs(epsg=4326)
            for state_name, shapefile in self.states_shapefiles.items()
        }

    def is_point_in_australia_state(self, lat, long):
        point = Point(long, lat)

        # Check each state to see if the point is within its boundary
        for state_name, state_data in self.states_data.items():
            if state_data.contains(point).any():
                return True, state_name

        return False, "Outside Australia"  # Point is not in any state, hence outside Australia


