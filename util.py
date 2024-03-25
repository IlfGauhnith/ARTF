import numpy as np

def exclude_outliers(arr):
    # Calculate the first and third quartiles
    q1 = np.percentile(arr, 25)
    q3 = np.percentile(arr, 75)

    # Calculate the interquartile range (IQR)
    iqr = q3 - q1

    # Define the lower and upper bounds for outliers exclusion
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Exclude outliers
    filtered_arr = [x for x in arr if lower_bound <= x <= upper_bound]

    return filtered_arr