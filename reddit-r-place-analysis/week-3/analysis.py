import sys
from datetime import datetime
import time
import duckdb

def process(begin, end):
    try:
        start_time = datetime.strptime(begin, '%Y-%m-%d %H')
        end_time = datetime.strptime(end, '%Y-%m-%d %H')
    except ValueError as e:
        raise e
        
    if start_time > end_time:
        raise ValueError("start time must be before end time")
    
    conn = duckdb.connect()
    
    # rank colors by distinct users
    query = f"""
        WITH colors AS (
            SELECT
                pixel_color,
                COUNT(DISTINCT user_uniq_id) AS count
            FROM '../2022_place_canvas_history.parquet'
            WHERE timestamp >= '{start_time}' AND timestamp < '{end_time}'
            GROUP BY pixel_color
        )
        SELECT pixel_color, count
        FROM colors
        ORDER BY count DESC
        LIMIT 10
    """
    
    result = conn.execute(query).fetchall()
    print(f"Top 10 colors:\n{result}\n")
    
    # calculate average session length
    query = f"""
        WITH time_diffs AS (
            SELECT 
                user_uniq_id,
                timestamp,
                date_diff(
                    'second',
                    LAG(timestamp) OVER (
                        PARTITION BY user_uniq_id
                        ORDER BY timestamp
                    ),
                    timestamp
                ) AS time_diff
            FROM '../2022_place_canvas_history.parquet'
            WHERE timestamp >= '{start_time}' AND timestamp < '{end_time}'
        ),
        sessions AS (
            SELECT
                user_uniq_id,
                timestamp,
                SUM(CASE WHEN time_diff >= 900 OR time_diff IS NULL THEN 1 ELSE 0 END)
                    OVER (
                        PARTITION BY user_uniq_id
                        ORDER BY timestamp
                    ) AS session
            FROM time_diffs
        ),
        session_lengths AS (
            SELECT
                COUNT(*) AS pixels,
                date_diff(
                    'second',
                    MIN(timestamp),
                    MAX(timestamp)
                ) AS session_len
            FROM sessions
            GROUP BY user_uniq_id, session
        )
        SELECT 
            AVG(session_len) AS avg_session_len
        FROM session_lengths
        WHERE pixels > 1
    """
    
    result = conn.execute(query).fetchall()
    print(f"Average session length:\n{result}\n")
    
    # pixel placement percentiles, 50th 75th 90th 99th
    query = f"""
        WITH pixels_placed AS (
            SELECT COUNT(user_uniq_id) AS pixels
            FROM '../2022_place_canvas_history.parquet'
            WHERE timestamp >= '{start_time}' AND timestamp < '{end_time}'
            GROUP BY user_uniq_id
        )
        SELECT
            PERCENTILE_CONT(0.50) WITHIN GROUP (
                ORDER BY pixels
            ),
            PERCENTILE_CONT(0.75) WITHIN GROUP (
                ORDER BY pixels
            ),
            PERCENTILE_CONT(0.90) WITHIN GROUP (
                ORDER BY pixels
            ),
            PERCENTILE_CONT(0.99) WITHIN GROUP (
                ORDER BY pixels
            )
        FROM pixels_placed
    """
    
    result = conn.execute(query).fetchall()
    print(f"Pixel placement percentiles [(50, 75, 90, 99)]:\n{result}\n")
    
    # first-time users
    query = f"""
        WITH first AS (
            SELECT
                user_uniq_id,
                MIN(timestamp) AS first_pixel
            FROM '../2022_place_canvas_history.parquet'
            WHERE timestamp < '{end_time}'
            GROUP BY user_uniq_id
        )
        SELECT COUNT(*) AS users
        FROM first
        WHERE first_pixel >= '{start_time}'
    """
    
    result = conn.execute(query).fetchall()
    print(f"First-time users:\n{result}\n")
                    
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Not the correct number of arguments. Run as: python duck.py [start-time] [end-time]")
        
    prog_start = time.perf_counter_ns()
    process(sys.argv[1], sys.argv[2])
    print(f"time to process: {time.perf_counter_ns() - prog_start} ns")
