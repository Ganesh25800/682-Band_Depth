import os
import time
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from dataHandling import load_Raw_Data
from dataHandling import cleanRawData
from dataHandling import dateValidation
from dataHandling import cleanStep3Data
from curveMatrix  import curveMatrix
from curveMatrix  import curveMatrixStep3
from curveScoring import curveScore
from rankCurves   import rankCurve
from visulization import visualize
from visulization import visualizeStep3
from fileManager import checkAndExtract


def run_pipeline(filePath, pollutant, unit, tag, mode="step1"):
    print(f"Starting Pipeline To Find Band Depth for {tag}")

    raw_data = load_Raw_Data(filePath, mode=mode)

    if raw_data is None:
        print("Pipeline Stoped Due to Empty File")
        return

    cleaned_data = cleanRawData(raw_data, mode=mode)

    if cleaned_data is None:
        return

    validate_date = dateValidation(cleaned_data, mode=mode)

    x, dates = curveMatrix(validate_date, mode=mode)

    if x is None:
        return

    curvescore = curveScore(x)

    ranks = rankCurve(x, dates, curvescore)

    output_path = visualize(ranks, pollutant, unit, tag, mode=mode)
    print(f"\nPipeline to find band depth for {tag} completed")
    print(f"Output saved in path: {output_path}\n")
    print("=============================================================")


def run_pipeline_step3(filePath_o3, filePath_no2, tag):
    print(f"Starting Pipeline To Find Band Depth for {tag}")

    merged_data = cleanStep3Data(filePath_o3, filePath_no2)

    if merged_data is None:
        return

    validate_date = dateValidation(merged_data, mode="step3")

    X_no2, X_o3, dates = curveMatrixStep3(validate_date)

    if X_no2 is None:
        return

    curvescore = curveScore(X_no2)

    ranks          = rankCurve(X_no2, dates, curvescore)
    ranks["X_o3"]  = X_o3

    output_path = visualizeStep3(ranks, tag)
    print(f"\nPipeline to find band depth for {tag} completed")
    print(f"Output saved in path: {output_path}\n")
    print("=============================================================")


if __name__ == "__main__":

    start = time.time()

    files_ready = checkAndExtract()

    if not files_ready:
        print("\nCannot start pipeline — files missing!")
    else:

        run_pipeline(
            filePath  = "RawCSVData/hourly_O3.csv",
            pollutant = "O3",
            unit      = "ppm",
            tag       = "hourly_O3",
            mode      = "step1"
        )

        run_pipeline(
            filePath  = "RawCSVData/hourly_NO2.csv",
            pollutant = "NO2",
            unit      = "ppm",
            tag       = "hourly_NO2",
            mode      = "step1"
        )

        run_pipeline(
            filePath  = "RawCSVData/Yearly_O3/",
            pollutant = "O3",
            unit      = "ppm",
            tag       = "yearly_O3",
            mode      = "step2a"
        )

        run_pipeline(
            filePath  = "RawCSVData/Yearly_P.M2.5/",
            pollutant = "PM2.5",
            unit      = "µg/m³",
            tag       = "yearly_PM25",
            mode      = "step2b"
        )

        run_pipeline_step3(
            filePath_o3  = "RawCSVData/hourly_O3.csv",
            filePath_no2 = "RawCSVData/hourly_NO2.csv",
            tag          = "step3a_parametric"
        )

    end = time.time()

    minutes = int((end - start) // 60)
    seconds = int((end - start) % 60)
    print(f"\nTotal Pipeline Time: {minutes} min {seconds} sec")
    print("\n========================================================")
    