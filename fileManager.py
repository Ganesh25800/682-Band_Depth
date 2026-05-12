import os
import zipfile
import glob
import json
import time


JSON_FILE = "RawCSVData/setup.json"

SINGLE_FILES = {
    "RawCSVData/hourly_O3.csv"  : "RawCSVData/hourly_O3.zip",
    "RawCSVData/hourly_NO2.csv" : "RawCSVData/hourly_NO2.zip",
}

YEARLY_FOLDERS = {
    "RawCSVData/Yearly_O3/"      : "RawCSVData/Yearly_O3/",
    "RawCSVData/Yearly_P.M2.5/" : "RawCSVData/Yearly_P.M2.5/",
}


def loadJson():
    if not os.path.exists(JSON_FILE):
        return False
    with open(JSON_FILE, "r") as f:
        data = json.load(f)
    return data.get("first_time_done", False)


def updateJson():
    data = {"first_time_done": True}
    with open(JSON_FILE, "w") as f:
        json.dump(data, f)
    print("Setup JSON updated successfully")


def checkFiles():
    print("\nChecking all required CSV files...")

    for csv_path, _ in SINGLE_FILES.items():
        if not os.path.exists(csv_path):
            print(f"MISSING: {csv_path}")
            return False
        print(f"OK: {csv_path}")

    for folder_path, _ in YEARLY_FOLDERS.items():
        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
        if len(csv_files) == 0:
            print(f"MISSING: No CSV files found in {folder_path}")
            return False
        print(f"OK: {folder_path} → {len(csv_files)} CSV files found")

    print("All files are present")
    return True


def extractFiles():
    print("\nExtracting zip files...")
    time.sleep(1)

    
    for csv_path, zip_path in SINGLE_FILES.items():

        if os.path.exists(csv_path):
            print(f"Already exists: {csv_path} → skipping")
            continue

        if not os.path.exists(zip_path):
            print(f"ERROR: Zip not found → {zip_path}")
            return False

        print(f"Extracting: {zip_path} ...")

        extract_dir = os.path.dirname(csv_path)

        with zipfile.ZipFile(zip_path, "r") as z:
            for member in z.namelist():
                filename = os.path.basename(member)
                if not filename:
                    continue
                out_path = os.path.join(extract_dir, filename)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with z.open(member) as source, open(out_path, "wb") as dest:
                    dest.write(source.read())

        print(f"Extracted: {csv_path}")
        time.sleep(0.5)

    
    for folder_path, _ in YEARLY_FOLDERS.items():

        zip_files = glob.glob(os.path.join(folder_path, "*.zip"))

        if len(zip_files) == 0:
            print(f"ERROR: No zip files found in {folder_path}")
            return False

        print(f"\nExtracting {len(zip_files)} zip files from {folder_path} ...")

        for zip_path in sorted(zip_files):

            zip_name     = os.path.basename(zip_path)
            expected_csv = zip_name.replace(".zip", ".csv")
            csv_path     = os.path.join(folder_path, expected_csv)

            if os.path.exists(csv_path):
                print(f"Already exists: {expected_csv} → skipping")
                continue

            print(f"Extracting: {zip_name} ...")

            with zipfile.ZipFile(zip_path, "r") as z:
                for member in z.namelist():
                    filename = os.path.basename(member)
                    if not filename:
                        continue
                    out_path = os.path.join(folder_path, filename)
                    with z.open(member) as source, open(out_path, "wb") as dest:
                        dest.write(source.read())

            print(f"Extracted: {expected_csv}")

        time.sleep(0.5)

    return True


def checkAndExtract():

    print("\n\nStarting File Manager")
    time.sleep(1)

    
    first_time_done = loadJson()

    if first_time_done:
        
        print("Setup JSON found → files were extracted before")
        print("Checking files are still present...")

        files_ok = checkFiles()

        if files_ok:
            print("\nAll files ready → Starting Pipeline")
            return True
        else:
            print("\nSome files missing → Re-extracting...")
           

    else:
        
        print("First time running → Starting extraction...")

    
    extracted = extractFiles()

    if not extracted:
        print("\nExtraction failed → Cannot start pipeline")
        return False

    
    files_ok = checkFiles()

    if not files_ok:
        print("\nFiles still missing after extraction → Cannot start pipeline")
        return False

    
    updateJson()

    print("\nAll files ready → Starting Pipeline")
    return True