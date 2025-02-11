import polars as pl
import time

def process():
    print("processing...")
    
    df = pl.read_csv("../2022_place_canvas_history.csv", low_memory=True, infer_schema_length=0, columns=['timestamp', 'pixel_color', 'coordinate'])
    
    df = df.lazy()
    
    df = df.with_columns(
        pl.col("timestamp").str.head(16).str.strptime(pl.Datetime, '%F %H:%M').dt.truncate("1h")
    )
    
    df.collect().write_parquet("userless_place_canvas.parquet")
        

if __name__ == "__main__":
    start = time.perf_counter_ns()
    process()
    print(f"time to process: {time.perf_counter_ns() - start} ns")
