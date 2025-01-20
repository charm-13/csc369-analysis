import sys
from datetime import datetime
import time
import polars as pl


def process(begin, end):
    try:
        start_time = datetime.strptime(begin, "%Y-%m-%d %H")
        end_time = datetime.strptime(end, "%Y-%m-%d %H")
    except ValueError as e:
        raise e

    if start_time > end_time:
        raise ValueError("start time must be before end time")

    df = pl.scan_parquet("../2022_place_canvas_history.parquet")

    color = (
        df.filter(
            (pl.col("timestamp") >= start_time) & (pl.col("timestamp") <= end_time)
        )
        .group_by("pixel_color")
        .len()
        .sort("len", descending=True)
        .select(pl.col("pixel_color"))
        .head(1)
        .collect()
    ).item()
    
    location = (
        df.filter(
            (pl.col("timestamp") >= start_time) & (pl.col("timestamp") <= end_time)
        )
        .group_by("coordinate")
        .len()
        .sort("len", descending=True)
        .select(pl.col("coordinate"))
        .head(1)
        .collect()
    ).item()

    print(f"Most common color: {color},\nMost common location: {location}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "Not the correct number of arguments. Run as: python main.py [start-time] [end-time]"
        )

    prog_start = time.perf_counter_ns()
    process(sys.argv[1], sys.argv[2])
    print(f"time to process: {time.perf_counter_ns() - prog_start} ns")
