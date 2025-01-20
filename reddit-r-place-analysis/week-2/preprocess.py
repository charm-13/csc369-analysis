import polars as pl

def process():
    print("processing...")
    df = pl.read_csv("../2022_place_canvas_history.csv")
    print("done reading! fixing user_ids...")
    
    uniq_ids = df.select(pl.col("user_id").unique().alias("user_id"))
    uniq_ids = uniq_ids.with_columns(
        pl.arange(1, uniq_ids.height + 1).alias("uniq_user_num")
    )
    
    df = df.join(uniq_ids, on="user_id", how="left").drop("user_id")
    
    print("fixed user_ids! adding to parquet...")
    
    df = df.select(
        pl.col("timestamp").str.head(-4).str.strptime(pl.Datetime, '%F %T%.3f'), 
        pl.col("uniq_user_num").alias("user_id"),
        pl.col("pixel_color"),
        pl.col("coordinate")
    )
    
    print(df.head())
    
    df.write_parquet("../2022_place_canvas_history.parquet")

if __name__ == "__main__":
    process()
