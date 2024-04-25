from arcgis.features import FeatureLayer
import pandas as pd
import geopandas as gpd
from datetime import datetime
import traceback
import argparse


"""
The script fetches data from the TOPS layer from Tallahassee's ArcGIS server.

Example usage:
    python codes/TOPSdatacollection.py --batch_size 4000 --oneyear
This will fetch data for the last 365 days in batches of 4000 features each.
If --oneyear is not specified, the script will fetch data for the last 24 hours.

Important note:
The arcgis package seems to be very sensitive with its dependencies. I recommend setting \
up a conda environment just for this script using python3.9. (venv personally didn't work\
You should install all packages needed and then run 'conda install -c esri arcgis'.
It seems that `esri` channel has issues with its packages, so install arcgis last.
"""


# Function to fetch data in batches
def fetch_data_in_batches(batch_size=4000, one_year=False):
    # Create a FeatureLayer
    if one_year:
        layer = FeatureLayer(
            "https://cotinter.leoncountyfl.gov/cotinter/rest/services/Vector/COT\
                _InterTOPS_D_WM/MapServer/2"
        )
    else:
        layer = FeatureLayer(
            "https://cotinter.leoncountyfl.gov/cotinter/rest/services/Vector/COT\
                _InterTOPS_D_WM/MapServer/3"
        )
    total_features = layer.query(return_count_only=True)
    ids = [str(i) for i in range(1, total_features + 1)]
    # Collecting the column labels
    spatial_df = layer.query(object_ids="1").sdf  # Get the first row
    spatial_df = pd.DataFrame(
        columns=spatial_df.columns
    )  # Remove that first row so that only labels remains
    while ids:
        ids_to_collect = ",".join(ids[: min(len(ids) - 1, batch_size)])
        query_result = layer.query(object_ids=ids_to_collect)
        print(
            f"Collected {len(query_result.features)} features starting from ID {ids[0]}"
        )
        del ids[: len(query_result.features)]
        spatial_df = pd.concat([spatial_df, query_result.sdf]).reset_index(drop=True)
        print(f"Currently has {spatial_df.shape[0]} entries")
    return spatial_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Collects data from the TOPS layer. The data is exported to a GeoJSON\
            file. By default, the data for the last 24 hours is fetched."
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=4000,
        help="The number of features to fetch in each batch",
    )
    parser.add_argument(
        "--oneyear", action="store_true", help="Fetch data for the last 365 days"
    )
    args = parser.parse_args()

    try:
        # Fetching all features in batches
        spatial_df = fetch_data_in_batches(args.batch_size, args.oneyear)
        # Create a GeoDataFrame and drop duplicates
        gdf = gpd.GeoDataFrame(spatial_df, geometry="SHAPE").drop_duplicates(
            ["OBJECTID"]
        )
        # Export the GeoDataFrame to a GeoJSON file
        date_string = datetime.now().strftime("%Y%m%d")
        if args.oneyear:
            gdf.to_file(f"TOPS_365days_{date_string}.geojson", driver="GeoJSON")
        else:
            gdf.to_file(f"TOPS_24hrs_{date_string}.geojson", driver="GeoJSON")
    except Exception as e:
        error_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"error-{error_time}.txt"
        with open(filename, "w") as file:
            file.write(f"An error occurred: {e}\n")
            traceback.print_exc(file=file)  # This writes the full traceback to the file
