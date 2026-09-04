import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

NUMERICAL_FEATURES = [
    'elevation_m', 'distance_to_coast_km', 'distance_to_river_km',
    'temperature_c', 'humidity_percent', 'rainfall_24h_mm', 'rainfall_mm',
    'rainfall_7d_mm', 'air_pressure_hpa', 'wind_speed_kmh', 'wind_gust_kmh',
    'wind_direction_deg', 'cloud_cover_percent', 'river_level_m',
    'river_flow_m3s', 'soil_moisture_percent', 'groundwater_level_m',
    'sea_level_anomaly_m', 'water_level_change_m', 'earthquake_magnitude',
    'earthquake_depth_km', 'distance_to_fault_km', 'ground_acceleration_g',
    'seismic_activity_index', 'cyclone_wind_speed_kmh', 'cyclone_pressure_hpa',
    'cyclone_distance_km', 'storm_surge_m', 'vegetation_index',
    'vegetation_dryness_index', 'fire_weather_index', 'fuel_moisture_percent',
    'burned_area_km2', 'land_surface_temperature_c', 'slope_degree',
    'soil_saturation_percent', 'terrain_roughness', 'landslide_susceptibility',
    'precipitation_anomaly_percent', 'temperature_anomaly_c',
    'soil_moisture_anomaly', 'water_storage_index', 'drought_index',
    'population_density', 'urban_density', 'building_density',
    'road_density_km_km2', 'critical_facilities_count', 'forest_cover_percent',
    'agricultural_area_percent', 'previous_disaster_count',
    'days_since_last_disaster', 'historical_risk_score'
]

CATEGORICAL_FEATURES = ['soil_type', 'previous_disaster_type']

def get_preprocessing_pipeline():
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, NUMERICAL_FEATURES),
            ('cat', cat_transformer, CATEGORICAL_FEATURES)
        ]
    )
    return preprocessor

def get_feature_names(preprocessor):
    num_cols = NUMERICAL_FEATURES
    cat_cols = []
    if hasattr(preprocessor, 'named_transformers_') and 'cat' in preprocessor.named_transformers_:
        cat_encoder = preprocessor.named_transformers_['cat'].named_steps['encoder']
        cat_cols = list(cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES))
    return num_cols + cat_cols