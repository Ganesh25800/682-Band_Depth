import numpy as np
import time
from itertools import combinations


def curveScore(curveData):

    print("\nStarting Phase-5: Computing Band Depth")
    time.sleep(1)

    curves, tim = curveData.shape

    scores = np.zeros(curves)
    total_pairs = 0

    print("\nComputing each curve for scoring...")
    

    for a, b in combinations(range(curves), 2):
        low = np.minimum(curveData[a], curveData[b])
        high = np.maximum(curveData[a], curveData[b])

        for i in range(curves):
            #proportion of hours curve i stays inside band here
            inside     = np.mean((curveData[i] >= low) & (curveData[i] <= high))
            scores[i] += inside

        total_pairs += 1  

        if total_pairs % 200 == 0:
            percent = (total_pairs / (curves*(curves-1)//2)) * 100
            print(f"Pairs done: {total_pairs} / {curves*(curves-1)//2}  ({percent:.1f}%)")

    scores = scores / total_pairs 


    print("\nPhase-5: Computing Band Depth Completed Successfully") 

    return scores          



    
