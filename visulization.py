import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import time

def visualize(ranked, pollutant, unit, tag, mode="step1"):

    print("\n\nStarting Phase-7: Creating Visualization")
    time.sleep(1)

    X            = ranked["X"]
    dates        = ranked["dates"]
    scores       = ranked["scores"]

    median_idx   = ranked["median_idx"]
    median_date  = ranked["median_date"]
    median_score = ranked["median_score"]

    deep2_idx    = ranked["deep2_idx"]
    deep2_date   = ranked["deep2_date"]
    deep2_score  = ranked["deep2_score"]

    deep3_idx    = ranked["deep3_idx"]
    deep3_date   = ranked["deep3_date"]
    deep3_score  = ranked["deep3_score"]

    shallow_idx  = ranked["shallow_idx"]

    n = len(dates)

    if mode in ["step1", "step3"]:
        x_values = np.arange(24)
        x_ticks  = list(range(0, 24, 2))
        x_labels = [f"{h:02d}:00" for h in range(0, 24, 2)]
        x_label  = "Hour of Day"
        title    = f"Hourly {pollutant} Curves — Boston, Summer Weekdays 2025\nBand Depth Analysis (MBD2, j=2)"

    elif mode in ["step2a", "step2b"]:
        x_values = np.arange(1, 366)
        x_ticks  = list(range(1, 366, 30))
        x_labels = [str(d) for d in range(1, 366, 30)]
        x_label  = "Day of Year"
        title    = f"Daily {pollutant} Curves — Boston, Years {dates[0]} to {dates[-1]}\nBand Depth Analysis (MBD2, j=2)"

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{tag}_band_depth.png")

    fig, ax = plt.subplots(figsize=(14, 7))

    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")

    for i in range(n):
        ax.plot(
            x_values,
            X[i],
            color     = "#888888",
            alpha     = 0.30,
            linewidth = 0.8
        )

    for idx, i in enumerate(shallow_idx):
        label = "Shallowest / Outlier" if idx == 0 else ""
        ax.plot(
            x_values,
            X[i],
            color     = "#ff6b6b",
            alpha     = 0.85,
            linewidth = 1.6,
            label     = label
        )

    ax.plot(
        x_values,
        X[deep3_idx],
        color     = "#74b9ff",
        linewidth = 2.2,
        label     = f"3rd Deepest  —  {deep3_date}  (score: {deep3_score:.4f})"
    )

    ax.plot(
        x_values,
        X[deep2_idx],
        color     = "#a29bfe",
        linewidth = 2.5,
        label     = f"2nd Deepest  —  {deep2_date}  (score: {deep2_score:.4f})"
    )

    ax.plot(
        x_values,
        X[median_idx],
        color     = "#00e676",
        linewidth = 3.8,
        zorder    = 5,
        label     = f"Median Curve —  {median_date}  (score: {median_score:.4f})"
    )

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(
        x_labels,
        color    = "white",
        fontsize = 10,
        rotation = 30
    )

    ax.tick_params(colors="white")
    ax.yaxis.label.set_color("white")
    ax.xaxis.label.set_color("white")

    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")

    ax.set_xlabel(x_label, color="white", fontsize=13)
    ax.set_ylabel(f"{pollutant}  ({unit})", color="white", fontsize=13)
    ax.set_title(title, color="white", fontsize=15, pad=14)

    legend = ax.legend(
        facecolor  = "#1e1e2e",
        edgecolor  = "#555555",
        labelcolor = "white",
        fontsize   = 10,
        loc        = "upper left"
    )

    ax.text(
        0.99, 0.02,
        f"n = {n} curves   |   Method: MBD2 (j=2)   |   Location: Boston, MA",
        transform = ax.transAxes,
        ha        = "right",
        va        = "bottom",
        color     = "#aaaaaa",
        fontsize  = 9
    )

    plt.tight_layout()
    plt.savefig(
        output_path,
        dpi         = 150,
        bbox_inches = "tight",
        facecolor   = fig.get_facecolor()
    )
    plt.close()

    print("Phase-7: Visualization Completed Successfully")
    time.sleep(1)

    return output_path




def visualizeStep3(ranked, tag):

    print("\n\nStarting Phase-7: Creating Parametric Visualization")
    time.sleep(1)

    X_no2        = ranked["X"]
    X_o3         = ranked["X_o3"]
    dates        = ranked["dates"]
    scores       = ranked["scores"]

    median_idx   = ranked["median_idx"]
    median_date  = ranked["median_date"]
    median_score = ranked["median_score"]

    deep2_idx    = ranked["deep2_idx"]
    deep2_date   = ranked["deep2_date"]
    deep2_score  = ranked["deep2_score"]

    deep3_idx    = ranked["deep3_idx"]
    deep3_date   = ranked["deep3_date"]
    deep3_score  = ranked["deep3_score"]

    shallow_idx  = ranked["shallow_idx"]

    n = len(dates)

    output_dir  = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{tag}_band_depth.png")

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor("#0e1117")
    ax.set_facecolor("#0e1117")

    for i in range(n):
        ax.plot(X_no2[i], X_o3[i], color="#888888", alpha=0.30, linewidth=0.8)

    for idx, i in enumerate(shallow_idx):
        label = "Shallowest / Outlier" if idx == 0 else ""
        ax.plot(X_no2[i], X_o3[i], color="#ff6b6b", alpha=0.85, linewidth=1.6, label=label)

    ax.plot(X_no2[deep3_idx], X_o3[deep3_idx], color="#74b9ff", linewidth=2.2,
            label=f"3rd Deepest  —  {deep3_date}  (score: {deep3_score:.4f})")

    ax.plot(X_no2[deep2_idx], X_o3[deep2_idx], color="#a29bfe", linewidth=2.5,
            label=f"2nd Deepest  —  {deep2_date}  (score: {deep2_score:.4f})")

    ax.plot(X_no2[median_idx], X_o3[median_idx], color="#00e676", linewidth=3.8, zorder=5,
            label=f"Median Curve —  {median_date}  (score: {median_score:.4f})")

    ax.tick_params(colors="white")
    ax.yaxis.label.set_color("white")
    ax.xaxis.label.set_color("white")

    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")

    ax.set_xlabel("NO2  (ppm)", color="white", fontsize=13)
    ax.set_ylabel("O3  (ppm)",  color="white", fontsize=13)
    ax.set_title(
        "Parametric NO2 vs O3 Curves — Boston, Summer Weekdays 2025\nBand Depth Analysis (MBD2, j=2)",
        color="white", fontsize=15, pad=14
    )

    ax.legend(facecolor="#1e1e2e", edgecolor="#555555", labelcolor="white", fontsize=10, loc="upper left")

    ax.text(
        0.99, 0.02,
        f"n = {n} curves   |   Method: MBD2 (j=2)   |   Location: Boston, MA",
        transform = ax.transAxes,
        ha        = "right",
        va        = "bottom",
        color     = "#aaaaaa",
        fontsize  = 9
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()

    print("Phase-7: Parametric Visualization Completed Successfully")
    time.sleep(1)

    return output_path