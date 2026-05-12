# Band Depth Analysis — Air Quality (Boston, MA)

Band depth analysis on EPA air quality data to find the most central (median) curve among multiple time-series curves using Modified Band Depth (MBD2).

---

## Project Structure

```
BandDepth/
│
├── Main.py                        # Entry point — runs all pipelines
├── fileManager.py                 # Handles zip extraction and file validation
├── dataHandling.py                # Phase 1, 2, 3 — Load, Clean, Validate
├── curveMatrix.py                 # Phase 4 — Build curve matrix
├── curveScoring.py                # Phase 5 — Compute MBD2 band depth scores
├── rankCurves.py                  # Phase 6 — Rank curves by score
├── visulization.py                # Phase 7 — Generate plots
│
├── RawCSVData/
│   ├── setup.json                 # Auto-created after first run
│   ├── hourly_O3.zip              # Hourly O3 data 2025
│   ├── hourly_NO2.zip             # Hourly NO2 data 2025
│   ├── Yearly_O3/
│   │   ├── daily_44201_2015.zip
│   │   ├── daily_44201_2016.zip
│   │   ├── ...
│   │   └── daily_44201_2024.zip
│   └── Yearly_P.M2.5/
│       ├── daily_88101_2015.zip
│       ├── daily_88101_2016.zip
│       ├── ...
│       └── daily_88101_2024.zip
│
└── outputs/
    ├── hourly_O3_band_depth.png
    ├── hourly_NO2_band_depth.png
    ├── yearly_O3_band_depth.png
    ├── yearly_PM25_band_depth.png
    └── step3a_parametric_band_depth.png
```

---

## Data Sources

Download from EPA AQS Pre-generated Files:
https://aqs.epa.gov/aqsweb/airdata/download_files.html

| File | Description |
|------|-------------|
| hourly_44201_2025.zip | Hourly O3 data 2025 |
| hourly_42602_2025.zip | Hourly NO2 data 2025 |
| daily_44201_2015 to 2024.zip | Daily O3 data per year |
| daily_88101_2015 to 2024.zip | Daily PM2.5 data per year |

Place zip files in the correct folders as shown in the structure above.

---

## How to Run

```bash
pip install pandas numpy matplotlib scipy
python Main.py
```

On first run, zip files are automatically extracted. On subsequent runs, extraction is skipped.

---

## Steps Completed

| Step | Description | Median Curve |
|------|-------------|-------------|
| 1a | Hourly O3 — Summer Weekdays 2025 | 2025-07-23 |
| 1b | Hourly NO2 — Summer Weekdays 2025 | 2025-06-12 |
| 2a | Yearly Max O3 — 2015 to 2024 | 2024 |
| 2b | Yearly Mean PM2.5 — 2015 to 2024 | 2020 |
| 3a | Parametric NO2 vs O3 — Summer Weekdays 2025 | 2025-06-12 |
