import pandas as pd
import os
import glob
import time

TARGET_STATE  = "25"
TARGET_COUNTY = "025"
DATE_START    = "2025-06-01"
DATE_END      = "2025-08-31"
WEEKDAYS      = [0, 1, 2, 3, 4]
YEAR_START    = 2015
YEAR_END      = 2024


def load_Raw_Data(filePath, mode="step1"):

    print("\n\nStarting Phase-1: Loading the Raw Data")

    if mode in ["step1", "step3"]:

        if not os.path.exists(filePath):
            print(f"\nFile not found in this location: {filePath}")
            return None

        try:
            rawData = pd.read_csv(filePath, dtype=str)
        except:
            print("\nError Occurred During Loading the file")
            return None

        if rawData is None:
            print("Pipeline Stoped Due to Empty File")
            return

        if rawData.empty:
            print("\nNo Data Found in the File")
            return None

        print("\nData Loaded Successfully ...")
        time.sleep(1)
        print("\nHere is the structure of the data")
        print(f"Shape  : {rawData.shape[0]:,} rows × {rawData.shape[1]} columns")

    elif mode in ["step2a", "step2b"]:

        if not os.path.exists(filePath):
            print(f"\nFolder not found in this location: {filePath}")
            return None

        all_files = glob.glob(os.path.join(filePath, "*.csv"))

        if len(all_files) == 0:
            print(f"\nNo CSV files found in folder: {filePath}")
            return None

        print(f"\nFound {len(all_files)} yearly files, Loading and combining...")
        time.sleep(1)

        dfs = []
        for f in sorted(all_files):
            df_temp = pd.read_csv(f, dtype=str)
            print(f"Loaded: {os.path.basename(f)} -> {len(df_temp):,} rows")
            dfs.append(df_temp)

        rawData = pd.concat(dfs, ignore_index=True)

        print("\nData Loaded Successfully ...")
        time.sleep(1)
        print("\nHere is the structure of the data")
        print(f"Shape  : {rawData.shape[0]:,} rows × {rawData.shape[1]} columns")

    return rawData




def cleanRawData(raw_Data, mode="step1"):

    time.sleep(1)
    print("\n\nStarting Phase-2: Cleaning & Filtering The Data")

    raw_Data.columns = (
        raw_Data.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print("\nStep-1: Normalization Completed")
    time.sleep(1)

    before_fliter = len(raw_Data)
    raw_Data = raw_Data[
        (raw_Data["state_code"] == TARGET_STATE) & (raw_Data["county_code"] == TARGET_COUNTY)
    ].copy()
    after_filter = len(raw_Data)

    if after_filter == 0:
        print(f"\nNo Data Found! for State: {TARGET_STATE} & County: {TARGET_COUNTY}")
        return None

    print(f"Step-2: Filtering State: {TARGET_STATE} & County: {TARGET_COUNTY}, Completed")
    time.sleep(1)

    raw_Data["date"] = pd.to_datetime(raw_Data["date_local"], errors="coerce", format="mixed")
    invalid_dates = raw_Data["date"].isna().sum()
    if invalid_dates > 0:
        raw_Data = raw_Data.dropna(subset=["date"])

    print("Step-3: Dates parsed Completed")
    time.sleep(1)

    if mode in ["step1", "step3"]:

        before_Dates = len(raw_Data)
        raw_Data = raw_Data[
            (raw_Data["date"] >= DATE_START) &
            (raw_Data["date"] <= DATE_END)
        ].copy()
        after_Dates = len(raw_Data)

        if after_Dates == 0:
            print(f"\nNo Dates Found! in range between {DATE_START} to {DATE_END}")
            return None

        print(f"Step-4: Dates between {DATE_START} to {DATE_END} filtered Completed")
        time.sleep(1)

        weekdays_before = len(raw_Data)
        raw_Data = raw_Data[raw_Data["date"].dt.weekday.isin(WEEKDAYS)].copy()
        weekdays_after = len(raw_Data)

        print("Step-5: WeekDays Filter Completed")

        raw_Data["hour"] = pd.to_numeric(
            raw_Data["time_local"].str.split(":").str[0],
            errors="coerce"
        )
        invalid_hours = raw_Data["hour"].isna().sum()
        if invalid_hours > 0:
            raw_Data = raw_Data.dropna(subset=["hour"])

        raw_Data["hour"] = raw_Data["hour"].astype(int)

        print("Step-6: Extracting Hours Completed")
        time.sleep(1)

        raw_Data["value"] = pd.to_numeric(raw_Data["sample_measurement"], errors="coerce")

        missing_values = raw_Data["value"].isna().sum()
        if missing_values > 0:
            raw_Data = raw_Data.dropna(subset=["value"])

        print("Step-7: Converting Measurment Values To Numeric Completed")

        before_negitive = len(raw_Data)
        raw_Data = raw_Data[raw_Data["value"] >= 0].copy()
        after_negitive = len(raw_Data)

        print("Step-8: Removing Negitive Values Completed")
        time.sleep(1)

        raw_Data = raw_Data[["date", "hour", "value"]].copy()

        print("Step-9: Removing Excess Columns Completed")
        time.sleep(1)

        before_sites = len(raw_Data)
        raw_Data = (
            raw_Data.groupby(["date", "hour"])["value"]
            .mean()
            .reset_index()
        )
        after_sites = len(raw_Data)

        print("Step-10: Removing Multiploe sites Completed")
        time.sleep(1)

        print("\nSummary of Cleaning Data:")
        print("----------------------------------------------")
        print(f"\nLocation: Before-> {before_fliter} rows, After -> {after_filter} rows")
        print(f"Parsing Dates: Invalid Dates Droped: {invalid_dates}")
        print(f"Filtered Dates: Before -> {before_Dates} rows, After -> {after_Dates} rows")
        print(f"Filtered WeekDays: Before -> {weekdays_before} rows, After -> {weekdays_after} rows")
        print(f"Invalid Hours Droped: {invalid_hours} ")
        print(f"Measrument Missing Values: {missing_values}")
        print(f"Droped Negitive Values: Before -> {before_negitive} rows, After -> {after_negitive} rows")
        print(f"Dropped Multiple Sites: Before -> {before_sites} rows, After -> {after_sites} rows\n")
        print(f"Total No.of Rows Left: {len(raw_Data)}")
        print("----------------------------------------------\n")

    elif mode == "step2a":

        before_Dates = len(raw_Data)
        raw_Data = raw_Data[
            (raw_Data["date"].dt.year >= YEAR_START) &
            (raw_Data["date"].dt.year <= YEAR_END)
        ].copy()
        after_Dates = len(raw_Data)

        if after_Dates == 0:
            print(f"\nNo Data Found! for years {YEAR_START} to {YEAR_END}")
            return None

        print(f"Step-4: Filtering Years {YEAR_START} to {YEAR_END} Completed")
        time.sleep(1)

        before_duration = len(raw_Data)
        raw_Data = raw_Data[raw_Data["sample_duration"].str.contains("8-HR RUN")].copy()
        after_duration = len(raw_Data)

        print("Step-5: Sample Duration Filter (8-HR RUN) Completed")
        time.sleep(1)

        raw_Data["value"] = pd.to_numeric(raw_Data["1st_max_value"], errors="coerce")

        missing_values = raw_Data["value"].isna().sum()
        if missing_values > 0:
            raw_Data = raw_Data.dropna(subset=["value"])

        print("Step-6: Converting 1st Max Value To Numeric Completed")
        time.sleep(1)

        before_negitive = len(raw_Data)
        raw_Data = raw_Data[raw_Data["value"] >= 0].copy()
        after_negitive = len(raw_Data)

        print("Step-7: Removing Negitive Values Completed")

        raw_Data["year"]        = raw_Data["date"].dt.year
        raw_Data["day_of_year"] = raw_Data["date"].dt.dayofyear

        print("Step-8: Adding Year and Day Of Year Columns Completed")
        time.sleep(1)

        raw_Data = raw_Data[["date", "year", "day_of_year", "value"]].copy()

        print("Step-9: Removing Excess Columns Completed")
        time.sleep(1)

        before_sites = len(raw_Data)
        raw_Data = (
            raw_Data.groupby(["year", "day_of_year"])["value"]
            .mean()
            .reset_index()
        )
        after_sites = len(raw_Data)

        print("Step-10: Removing Multiploe sites Completed")
        time.sleep(1)

        print("\nSummary of Cleaning Data:")
        print("----------------------------------------------")
        print(f"\nLocation: Before-> {before_fliter} rows, After -> {after_filter} rows")
        print(f"Parsing Dates: Invalid Dates Droped: {invalid_dates}")
        print(f"Filtered Years: Before -> {before_Dates} rows, After -> {after_Dates} rows")
        print(f"Duration Filter: Before -> {before_duration} rows, After -> {after_duration} rows")
        print(f"Measrument Missing Values: {missing_values}")
        print(f"Droped Negitive Values: Before -> {before_negitive} rows, After -> {after_negitive} rows")
        print(f"Dropped Multiple Sites: Before -> {before_sites} rows, After -> {after_sites} rows\n")
        print(f"Total No.of Rows Left: {len(raw_Data)}")
        print(f"Unique Years: {sorted(raw_Data['year'].unique().tolist())}")
        print("----------------------------------------------\n")

    elif mode == "step2b":

        before_Dates = len(raw_Data)
        raw_Data = raw_Data[
            (raw_Data["date"].dt.year >= YEAR_START) &
            (raw_Data["date"].dt.year <= YEAR_END)
        ].copy()
        after_Dates = len(raw_Data)

        if after_Dates == 0:
            print(f"\nNo Data Found! for years {YEAR_START} to {YEAR_END}")
            return None

        print(f"Step-4: Filtering Years {YEAR_START} to {YEAR_END} Completed")
        time.sleep(1)

        before_duration = len(raw_Data)
        raw_Data = raw_Data[raw_Data["sample_duration"].str.strip() == "24 HOUR"].copy()
        after_duration = len(raw_Data)

        print("Step-5: Sample Duration Filter (24 HOUR) Completed")
        time.sleep(1)

        raw_Data["value"] = pd.to_numeric(raw_Data["arithmetic_mean"], errors="coerce")

        missing_values = raw_Data["value"].isna().sum()
        if missing_values > 0:
            raw_Data = raw_Data.dropna(subset=["value"])

        print("Step-6: Converting Arithmetic Mean To Numeric Completed")
        time.sleep(1)

        before_negitive = len(raw_Data)
        raw_Data = raw_Data[raw_Data["value"] >= 0].copy()
        after_negitive = len(raw_Data)

        print("Step-7: Removing Negitive Values Completed")

        raw_Data["year"]        = raw_Data["date"].dt.year
        raw_Data["day_of_year"] = raw_Data["date"].dt.dayofyear

        print("Step-8: Adding Year and Day Of Year Columns Completed")
        time.sleep(1)

        raw_Data = raw_Data[["date", "year", "day_of_year", "value"]].copy()

        print("Step-9: Removing Excess Columns Completed")
        time.sleep(1)

        before_sites = len(raw_Data)
        raw_Data = (
            raw_Data.groupby(["year", "day_of_year"])["value"]
            .mean()
            .reset_index()
        )
        after_sites = len(raw_Data)

        print("Step-10: Removing Multiploe sites Completed")
        time.sleep(1)

        print("\nSummary of Cleaning Data:")
        print("----------------------------------------------")
        print(f"\nLocation: Before-> {before_fliter} rows, After -> {after_filter} rows")
        print(f"Parsing Dates: Invalid Dates Droped: {invalid_dates}")
        print(f"Filtered Years: Before -> {before_Dates} rows, After -> {after_Dates} rows")
        print(f"Duration Filter: Before -> {before_duration} rows, After -> {after_duration} rows")
        print(f"Measrument Missing Values: {missing_values}")
        print(f"Droped Negitive Values: Before -> {before_negitive} rows, After -> {after_negitive} rows")
        print(f"Dropped Multiple Sites: Before -> {before_sites} rows, After -> {after_sites} rows\n")
        print(f"Total No.of Rows Left: {len(raw_Data)}")
        print(f"Unique Years: {sorted(raw_Data['year'].unique().tolist())}")
        print("----------------------------------------------\n")

    time.sleep(0.5)
    print("Cleaning Data Completed Successfully")
    time.sleep(1)

    return raw_Data




def dateValidation(cleaned_data, mode="step1"):

    print("\n\nStarting Phase-3: Validating Date")
    time.sleep(1)

    if mode in ["step1", "step3"]:

        hours_per_day = (
            cleaned_data.groupby("date")["hour"]
            .nunique()
            .reset_index(name="hour_count")
        )

        complete_days   = hours_per_day[hours_per_day["hour_count"] == 24]["date"]
        incomplete_days = hours_per_day[hours_per_day["hour_count"] != 24]

        rows_before  = len(cleaned_data)
        validated_df = cleaned_data[cleaned_data["date"].isin(complete_days)].copy()
        rows_after   = len(validated_df)

        total_days = validated_df["date"].nunique()

        expected_hours = set(range(24))
        bad_days = []

        for date, group in validated_df.groupby("date"):
            actual_hours = set(group["hour"].astype(int).tolist())
            if actual_hours != expected_hours:
                missing = expected_hours - actual_hours
                bad_days.append((str(date)[:10], missing))

    elif mode in ["step2a", "step2b"]:

        days_per_year = (
            cleaned_data.groupby("year")["day_of_year"]
            .nunique()
            .reset_index(name="day_count")
        )

        complete_years = days_per_year[days_per_year["day_count"] >= 100]["year"]
        validated_df   = cleaned_data[cleaned_data["year"].isin(complete_years)].copy()

    print(f"\nPhase-3: Validating Dates Completed Successfully")
    time.sleep(1)

    return validated_df




def cleanStep3Data(filePath_o3, filePath_no2):

    time.sleep(1)
    print("\n\nStarting Phase-2: Cleaning & Filtering Step-3a Data")

    raw_o3  = pd.read_csv(filePath_o3,  dtype=str)
    raw_no2 = pd.read_csv(filePath_no2, dtype=str)

    def clean_single(raw_Data):

        raw_Data.columns = (
            raw_Data.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        raw_Data = raw_Data[
            (raw_Data["state_code"]  == TARGET_STATE) &
            (raw_Data["county_code"] == TARGET_COUNTY)
        ].copy()

        if len(raw_Data) == 0:
            return None

        raw_Data["date"] = pd.to_datetime(raw_Data["date_local"], errors="coerce", format="mixed")
        raw_Data = raw_Data.dropna(subset=["date"])

        raw_Data = raw_Data[
            (raw_Data["date"] >= DATE_START) &
            (raw_Data["date"] <= DATE_END)
        ].copy()

        raw_Data = raw_Data[raw_Data["date"].dt.weekday.isin(WEEKDAYS)].copy()

        raw_Data["hour"] = pd.to_numeric(
            raw_Data["time_local"].str.split(":").str[0],
            errors="coerce"
        )
        raw_Data = raw_Data.dropna(subset=["hour"])
        raw_Data["hour"] = raw_Data["hour"].astype(int)

        raw_Data["value"] = pd.to_numeric(raw_Data["sample_measurement"], errors="coerce")
        raw_Data = raw_Data.dropna(subset=["value"])
        raw_Data = raw_Data[raw_Data["value"] >= 0].copy()

        raw_Data = raw_Data[["date", "hour", "value"]].copy()
        raw_Data = (
            raw_Data.groupby(["date", "hour"])["value"]
            .mean()
            .reset_index()
        )

        return raw_Data

    df_o3  = clean_single(raw_o3)
    df_no2 = clean_single(raw_no2)

    if df_o3 is None or df_no2 is None:
        print("\nCleaning Failed for one of the files")
        return None

    merged = pd.merge(
        df_o3.rename(columns={"value": "o3"}),
        df_no2.rename(columns={"value": "no2"}),
        on=["date", "hour"],
        how="inner"
    )

    if len(merged) == 0:
        print("\nNo matching rows after merge")
        return None

    print(f"Step-2: Cleaning & Merging O3 and NO2 Completed")
    print(f"Total rows after merge: {len(merged):,}")
    print(f"Unique days: {merged['date'].nunique()}")
    time.sleep(1)

    print("Cleaning Data Completed Successfully")
    time.sleep(1)

    return merged