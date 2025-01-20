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
    
    color = conn.execute(
        """
        SELECT 
            pixel_color,
            COUNT(pixel_color) AS cnt
        FROM '../2022_place_canvas_history.parquet'
        WHERE CAST(timestamp AS TIMESTAMP) BETWEEN $1 AND $2
        GROUP BY pixel_color
        ORDER BY cnt DESC
        LIMIT 1
        """, 
        [start_time, end_time]).fetchone()[0]
    
    coordinate = conn.execute(
        """
        SELECT 
            coordinate,
            COUNT(coordinate) AS cnt
        FROM '../2022_place_canvas_history.parquet'
        WHERE CAST(timestamp AS TIMESTAMP) BETWEEN $1 AND $2
        GROUP BY coordinate
        ORDER BY cnt DESC
        LIMIT 1
        """,
        [start_time, end_time]).fetchone()[0]
                    
    print(f"Most common color: {color},\nMost common location: {coordinate}")
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Not the correct number of arguments. Run as: python duck.py [start-time] [end-time]")
        
    prog_start = time.perf_counter_ns()
    process(sys.argv[1], sys.argv[2])
    print(f"time to process: {time.perf_counter_ns() - prog_start} ns")
