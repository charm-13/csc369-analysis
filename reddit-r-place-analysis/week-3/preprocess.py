import polars as pl
import time

place_colors = {
    "Red": "#FF4500",
    "Orange": "#FFA800",
    "Yellow": "#FFD635",
    "Dark green": "#00A368",
    "Light green": "#7EED56",
    "Dark blue": "#2450A4",
    "Blue": "#3690EA",
    "Light blue": "#51E9F4",
    "Dark purple": "#811E9F",
    "Purple": "#B44AC0",
    "Light pink": "#FF99AA",
    "Brown": "#9C6926",
    "White": "#FFFFFF",
    "Light gray": "#D4D7D9",
    "Gray": "#898D90",
    "Black": "#000000",
    "Dark red": "#00A368",
    "Pink": "#FF3881",
    "Dark teal": "#00756F",
    "Teal": "#009EAA",
    "Indigo": "#493AC1",
    "Periwinkle": "#00A368",
    "Green": "#00CC78",
    "Dark brown": "#6D482F",
    "Burgandy": "#6D001A",
    "Pale yellow": "#FFF8D8",
    "Light teal": "#00CCC0",
    "Lavender": "#94B3FF",
    "Pale purple": "#E4ABFF",
    "Magenta": "#DE107F",
    "Beige": "#FFB470",
    "Dark gray": "#515252",
    "Pale yellow": "#FFF8B8",
    "Periwinkle": "#6A5CFF",
    "Maroon": "#BE0039"
}

def hex_to_name(hex: str) -> str:
    for place_name, place_hex in place_colors.items():
        if hex == place_hex:
            return place_name
       
    return "no"

def process_user_ids():
    print("processing user ids...")
    df = pl.read_csv("../2022_place_canvas_history.csv", columns=["user_id"], low_memory=True, infer_schema=False)
    
    uniq_ids = df.select(
            pl.col("user_id").unique().alias("user_id"),
        ).with_row_index(name="user_uniq_id")
    
    uniq_ids.write_parquet("./user_id_map.parquet", compression="lz4")
     

def process():
    print("processing...")
    uniq_ids = pl.scan_parquet("./user_id_map.parquet")
    
    reader = pl.read_csv_batched("../2022_place_canvas_history.csv", low_memory=True, infer_schema_length=0)
    collected_batches = []
    
    while batch := reader.next_batches(10):
        for df in batch:
            print(f"processing batch... {df.height}")
            df = df.lazy()
            
            df = df.join(uniq_ids, on="user_id", how="left").drop("user_id")
            
            df = df.with_columns(
                pl.col("timestamp").str.head(16).str.strptime(pl.Datetime, '%F %H:%M'),
                pl.col("pixel_color").map_elements(hex_to_name, return_dtype=str)
            )
            
            collected_batches.append(df.collect(streaming=True))
        
    if collected_batches:
        final = pl.concat(collected_batches)
        print(final.head())
        print(final.height)
        final.write_parquet("../2022_place_canvas_history.parquet")
        

if __name__ == "__main__":
    start = time.perf_counter_ns()
    # process_user_ids()
    process()
    print(f"time to process: {time.perf_counter_ns() - start} ns")
