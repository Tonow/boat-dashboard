import numpy as np
from config import M_TO_MNI

def get_point_dist(df):
    r = 6371000 # meters
    df['theta'] = np.deg2rad(df['longitude'])
    df['phi'] = np.deg2rad(df['latitude'])
    df['x'] = r*np.cos(df['theta'])*np.sin(df['phi'])
    df['y'] = r*np.sin(df['theta'])*np.sin(df['phi'])
    df['z'] = r*np.cos(df['phi'])
    df['x2'] = df['x'].shift()
    df['y2'] = df['y'].shift()
    df['z2'] = df['z'].shift()
    df['distance'] = np.sqrt((df['x2']-df['x'])**2 + (df['y2']-df['y'])**2 + (df['z2']-df['z'])**2)
    df['central angle'] = np.arccos((df['x']*df['x2'] + df['y']*df['y2'] + df['z']*df['z2'])/r**2)
    df['arclength'] = df['central angle']*r
    df = df.drop(["theta", "phi", "x", "y", "z", "x2", "y2", "z2", "central angle"], axis=1)
    return df

def get_speed(df):
    df['speed'] = df['distance'] * 4 * (M_TO_MNI * 1000)  / (df.time.diff() / np.timedelta64(1, 's'))
    return df

def get_abs_speed(df):
    df['speed'] = df['speed'].fillna(0)
    # df['abs_speed'] = np.abs(df['speed']).astype("float32")
    df['abs_speed'] = np.abs(df['speed'])
    return df

def get_speeds(df):
    df = get_point_dist(df)
    df = get_speed(df)
    df = get_abs_speed(df)
    return df
