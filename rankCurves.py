import numpy as np
import time


def rankCurve(x,dates,scores):
    print("\nStarting Phase-6: Ranking Curves")
    time.sleep(1)

    rank_order = np.argsort(scores)[::-1]

    median_idx   = rank_order[0]
    median_date  = dates[median_idx]
    median_score = scores[median_idx]
    print(f"\nMedian Curve Identified... Curve Date: {median_date}, Score: {median_score}")

    deep2_idx   = rank_order[1]
    deep2_date  = dates[deep2_idx]
    deep2_score = scores[deep2_idx]
    print(f"Identified 2nd deepest curve...Date: {deep2_date}, Score: {deep2_score}")

    deep3_idx   = rank_order[2]
    deep3_date  = dates[deep3_idx]
    deep3_score = scores[deep3_idx]
    print(f"Identified 3nd deepest curve...Date: {deep3_date}, Score: {deep3_score}")


    shallow_idx   = rank_order[-5:]
    shallow_dates = [dates[i] for i in shallow_idx]
    shallow_scores = [scores[i] for i in shallow_idx]
    print(f"Identified Outliers, Total Outliers: {len(shallow_dates)}\n")

    ranked = {
        "X"            : x,
        "dates"        : dates,
        "scores"       : scores,
        "rank_order"   : rank_order,
 
        "median_idx"   : median_idx,
        "median_date"  : median_date,
        "median_score" : median_score,
 
        "deep2_idx"    : deep2_idx,
        "deep2_date"   : deep2_date,
        "deep2_score"  : deep2_score,
 
        "deep3_idx"    : deep3_idx,
        "deep3_date"   : deep3_date,
        "deep3_score"  : deep3_score,
 
        "shallow_idx"  : shallow_idx,
        "shallow_dates": shallow_dates,
        "shallow_scores": shallow_scores
    }

    print("Phase-6: Ranking Curves Completed Successfully")
    time.sleep(1)
 
    return ranked

