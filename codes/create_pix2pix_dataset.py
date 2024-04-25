import geopandas as gpd
import osmnx as ox
import matplotlib.pyplot as plt
import random
from shapely.geometry import Point
import numpy as np
from PIL import Image
import os

"""
Given a geojson from TOPS, this script creates the image dataset for pix2pix.

Example Usage:
    python codes/create_pix2pix_dataset.py filename
This will use `filename` and creates two big maps, geographical maps and heatmaps,
splits these into patches and save it udner the `dataset` folder.
It will also create the baseline map (random heatmap) and create a dataset for it.
To use it for pix2pix, you also need to run `datasets/combine_A_and_B.py' in the
pix2pix repository.
See docs/datasets.md in the pix2pix repo for details for their script.
"""

# Constants
EARTH_RADIUS = 6371000  # meters
ONE_DEG_LAT_IN_METERS = 111139  # meters


# Calculate one degree of longitude in meters at a given latitude
def longitude_degree_in_meters(latitude):
    return np.cos(np.radians(latitude)) * ONE_DEG_LAT_IN_METERS


# Define the bounding box around the center point
def get_bounding_box(center_point, distance):
    lat, lon = center_point
    lat_change = distance / ONE_DEG_LAT_IN_METERS
    lon_change = distance / longitude_degree_in_meters(lat)

    north = lat + lat_change
    south = lat - lat_change
    east = lon + lon_change
    west = lon - lon_change

    return north, south, east, west


# Generate random points within the bounding box
def generate_random_points(center_point, dist, num_points):
    north, south, east, west = get_bounding_box(center_point, dist)
    points = []

    for _ in range(num_points):
        random_lat = random.uniform(south, north)
        random_lon = random.uniform(west, east)
        points.append(Point(random_lon, random_lat))

    return gpd.GeoDataFrame(geometry=points)


# Center point and distance
center_point = (30.479203013085982, -84.3386654250425)
dist = 20000  # 20 km


def main(filename):
    # Load the geojson file
    gdf = gpd.read_file(filename)
    gdf.crs = "epsg:102100"  # Default epsg for TOPS is 102100
    gdf = gdf.to_crs(epsg=4326)

    # drop the duplicates
    gdf = gdf.drop_duplicates()

    # filter unnecessary data
    unwanted_locations = [
        "LEON CO DETENTION FACILITY",
        "TALLAHASSEE POLICE DEPARTMENT",
        "LCSO",
        "TPD",
        "LEON CO SHERIFFS OFFICE",
        "IMMIGRATION & CUSTOMS ENFORCEM",
    ]
    gdf = gdf[~gdf["LOCATION_TEXT"].isin(unwanted_locations)]
    unwanted_categories = [
        "COMMUNITY POLICING",
        "ADMIN",
        "RECOVERED PROP",
        "AUTO THEFT RECOVERY",
        "UNABLE TO VERIFY",
        "TRAFFIC",
    ]
    gdf = gdf[~gdf["DISPO_TEXT"].isin(unwanted_categories)]
    gdf["DISPO_TEXT"].unique()

    # Configure OSMnx
    ox.config(use_cache=True, log_console=True)

    # Define the center of Tallahassee (latitude, longitude) and distance (in meters)
    center_point = (30.479203013085982, -84.3386654250425)
    dist = 20000

    # Download street network around the specified center point
    streets = ox.graph_from_point(center_point, dist=dist, network_type="drive")

    # Download building footprints
    buildings = ox.geometries_from_point(
        center_point, tags={"building": True}, dist=dist
    )

    # Download parks
    parks = ox.geometries_from_point(center_point, tags={"leisure": "park"}, dist=dist)

    # Download water bodies
    water_bodies = ox.geometries_from_point(
        center_point, tags={"natural": "water"}, dist=dist
    )

    # ---------GEOGRAPHICAL MAP-----------

    # Initialize figure and axis
    fig, ax = plt.subplots(figsize=(256, 256))

    # Plot streets
    ox.plot_graph(
        streets,
        ax=ax,
        bgcolor="black",
        edge_color="gray",
        node_size=0,
        edge_linewidth=0.5,
        show=False,
    )

    buildings.plot(
        ax=ax, color="yellow", alpha=0.7
    )  # ls Adjust colors and alpha as needed
    parks.plot(ax=ax, color="green", alpha=0.7)  # Adjust colors and alpha as needed
    water_bodies.plot(
        ax=ax, color="blue", alpha=0.7
    )  # Adjust colors and alpha as needed

    fig.tight_layout(pad=0)
    plt.savefig("tallahassee_square_map_geo.png", dpi=64)

    # ---------ACTUAL CRIME HEATMAP-----------

    fig, ax = plt.subplots(figsize=(256, 256))
    # Plot invisible road map for alignment
    ox.plot_graph(
        streets,
        ax=ax,
        bgcolor="white",
        edge_color="white",
        node_size=0,
        edge_linewidth=0.5,
        show=False,
    )
    x = gdf.geometry.x
    y = gdf.geometry.y
    ax.scatter(
        x, y, alpha=0.2, c="black", s=10
    )  # Adjust alpha, color, and size as needed
    fig.tight_layout(pad=0)
    plt.savefig("tallahassee_square_map_heat.png", dpi=64)

    # ---------BASELINE HEATMAP-----------

    fig, ax = plt.subplots(figsize=(256, 256))
    # Plot invisible road map for alignment
    ox.plot_graph(
        streets,
        ax=ax,
        bgcolor="white",
        edge_color="white",
        node_size=0,
        edge_linewidth=0.5,
        show=False,
    )

    num_points = gdf.shape[0]

    random_points_df = generate_random_points(center_point, dist, num_points)
    x = random_points_df.geometry.x
    y = random_points_df.geometry.y

    ax.scatter(
        x, y, alpha=0.2, c="black", s=10
    )  # Adjust alpha, color, and size as needed
    fig.tight_layout(pad=0)
    plt.savefig("tallahassee_square_map_heat_baseline.png", dpi=64)

    for save_folder in ["pix2pix", "baseline"]:
        # Setup directories
        os.makedirs(f"../dataset/{save_folder}/A", exist_ok=True)
        os.makedirs(f"../dataset/{save_folder}/B", exist_ok=True)
        os.makedirs(f"../dataset/{save_folder}/A/train", exist_ok=True)
        os.makedirs(f"../dataset/{save_folder}/B/train", exist_ok=True)
        os.makedirs(f"../dataset/{save_folder}/A/test", exist_ok=True)
        os.makedirs(f"../dataset/{save_folder}/B/test", exist_ok=True)

        Image.MAX_IMAGE_PIXELS = 268435456
        # Load images
        image_A = Image.open("tallahassee_square_map_geo.png")
        if save_folder == "baseline":
            image_B = Image.open("tallahassee_square_map_heat_baseline.png")
        else:
            image_B = Image.open("tallahassee_square_map_heat.png")

        # Define the patch size and calculate the number of patches per row/column
        patch_size = 512
        num_patches = 16384 // patch_size

        # Initialize patch ID
        patch_id = 0

        # Iterate through each 2x2 block of patches
        for i in range(0, num_patches, 2):
            for j in range(0, num_patches, 2):
                # Select a random patch within the 2x2 block
                test_patch_x = i + random.randint(0, 1)
                test_patch_y = j + random.randint(0, 1)

                # Process each patch in the 2x2 block
                for x in range(2):
                    for y in range(2):
                        patch_x = i + x
                        patch_y = j + y
                        if patch_x < num_patches and patch_y < num_patches:
                            # Extract the patch
                            box = (
                                patch_x * patch_size,
                                patch_y * patch_size,
                                (patch_x + 1) * patch_size,
                                (patch_y + 1) * patch_size,
                            )
                            patch_A = image_A.crop(box)
                            patch_B = image_B.crop(box)

                            # Determine the folder based on whether it is a test patch
                            folder = (
                                "test"
                                if (patch_x == test_patch_x and patch_y == test_patch_y)
                                else "train"
                            )

                            # Save patches with the same ID across both images
                            patch_A.save(
                                f"../dataset/{save_folder}/A/{folder}/{patch_id}.png"
                            )
                            patch_B.save(
                                f"../dataset/{save_folder}/B/{folder}/{patch_id}.png"
                            )

                            # Increment patch ID
                            patch_id += 1

        print("Patches processed and saved.")

        # Remove big images
        os.remove("tallahassee_square_map_geo.png")
        os.remove("tallahassee_square_map_heat.png")
        os.remove("tallahassee_square_map_heat_baseline.png")
