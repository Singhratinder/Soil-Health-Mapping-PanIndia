import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load AEZ GeoJSON file
aez_gdf = gpd.read_file("./shc_data/Agro_Ecological_Regions.geojson")

# Ensure AEZ data is in the correct coordinate reference system (CRS)
aez_gdf = aez_gdf.to_crs(epsg=4326)  # Convert to WGS84 if not already

def segregate_by_aez(df):
    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df, 
        geometry=[Point(xy) for xy in zip(df["longitude"], df["latitude"])],
        crs="EPSG:4326"
    )
    
    # Spatial join: Find which AEZ each point belongs to
    joined_gdf = gpd.sjoin(gdf, aez_gdf, how="left", predicate="within")
    
    # Keep only relevant columns
    result_df = joined_gdf.drop(columns=["geometry", "index_right", 'GmlID', 'objectid', 'physio_reg', 'area_sqkm', 'st_area_shape_', 'st_length_shape_'])
    
    return result_df