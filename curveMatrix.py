import numpy as np
import time

def curveMatrix(validate_date, mode="step1"):

    print(f"\nStarting Phase 4: Building Curve Matrix")
    time.sleep(1)

    if mode in ["step1", "step3"]:

        dates_raw = sorted(validate_date["date"].unique())
        dates     = [str(d)[:10] for d in dates_raw]

        X = []

        for d in dates_raw:
            day_data = (
                validate_date[validate_date["date"] == d]
                .sort_values("hour")
            )
            curve = day_data["value"].values
            X.append(curve)

        X = np.array(X)

        if X.shape[1] != 24:
            print(f"Error Occured: Expected 24 hours but got {X.shape[1]}")
            return None, None

        if X.shape[0] < 5:
            print(f"Error Occured: Only {X.shape[0]} days — need at least 5")
            return None, None

    elif mode in ["step2a", "step2b"]:

        years = sorted(validate_date["year"].unique())
        dates = [str(int(y)) for y in years]

        X = []

        for y in years:
            year_data = (
                validate_date[validate_date["year"] == y]
                .sort_values("day_of_year")
            )
            values = year_data["value"].values

            if len(values) < 365:

                import pandas as pd

                s = pd.Series(values, index=year_data["day_of_year"].values)
                s = s.reindex(range(1, 366))
                s = s.interpolate(method="linear")
                s = s.bfill().ffill()
                values = s.values
            else:
                values = values[:365]

            X.append(values)

        X = np.array(X)

        if X.shape[0] < 3:
            print(f"Error Occured: Only {X.shape[0]} years — need at least 3")
            return None, None

    nan_count = np.isnan(X).sum()

    if nan_count > 0:
        print(f"Our Matrix Contains Nan Values - Replacing them with mean value")
        row_means        = np.nanmean(X, axis=1, keepdims=True)
        nan_mask         = np.isnan(X)
        X[nan_mask]      = np.broadcast_to(row_means, X.shape)[nan_mask]

    print("\nPhase 4 - Curve Matrix Completed")
    time.sleep(1)

    return X, dates




def curveMatrixStep3(merged_data):

    print(f"\nStarting Phase 4: Building Parametric Curve Matrix")
    time.sleep(1)

    dates_raw = sorted(merged_data["date"].unique())
    dates     = [str(d)[:10] for d in dates_raw]

    X_no2 = []
    X_o3  = []

    for d in dates_raw:
        day_data = (
            merged_data[merged_data["date"] == d]
            .sort_values("hour")
        )
        X_no2.append(day_data["no2"].values)
        X_o3.append(day_data["o3"].values)

    X_no2 = np.array(X_no2)
    X_o3  = np.array(X_o3)

    if X_no2.shape[0] < 5:
        print(f"Error Occured: Only {X_no2.shape[0]} days — need at least 5")
        return None, None, None

    nan_count = np.isnan(X_no2).sum() + np.isnan(X_o3).sum()

    if nan_count > 0:
        print(f"Our Matrix Contains Nan Values - Replacing them with mean value")
        for X in [X_no2, X_o3]:
            row_means   = np.nanmean(X, axis=1, keepdims=True)
            nan_mask    = np.isnan(X)
            X[nan_mask] = np.broadcast_to(row_means, X.shape)[nan_mask]

    print("\nPhase 4 - Parametric Curve Matrix Completed")
    time.sleep(1)

    return X_no2, X_o3, dates