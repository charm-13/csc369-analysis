import sys
from datetime import datetime
import time
import pandas as pd


def process(begin, end):
    try:
        start_time = datetime.strptime(begin, "%Y-%m-%d %H")
        end_time = datetime.strptime(end, "%Y-%m-%d %H")
    except ValueError as e:
        raise e

    if start_time > end_time:
        raise ValueError("start time must be before end time")

    df = pd.read_csv("../2022_place_canvas_history.csv", 
                     usecols=["timestamp", "pixel_color", "coordinate"],
                     dtype={"pixel_color": "category"})
    
    df["timestamp"] = pd.to_datetime(df["timestamp"].str[:-4], format='ISO8601')
    
    df = df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]

    color = (
        df["pixel_color"]
        .value_counts()
        .head(1)
        .index.item()
    )
    
    location = (
        df["coordinate"]
        .value_counts()
        .head(1)
        .index.item()
    )

    print(f"Most common color: {color},\nMost common location: {location}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "Not the correct number of arguments. Run as: python main.py [start-time] [end-time]"
        )

    prog_start = time.perf_counter_ns()
    process(sys.argv[1], sys.argv[2])
    print(f"time to process: {time.perf_counter_ns() - prog_start} ns")
