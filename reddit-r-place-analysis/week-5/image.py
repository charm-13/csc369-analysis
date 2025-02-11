import os
import duckdb
from datetime import datetime
from webcolors import hex_to_rgb
from PIL import Image

def process_img(query):
    conn = duckdb.connect()
    conn.sql(f"""
        CREATE TABLE zero AS (
            {query}
        )
        """)
    
    timestamps = conn.sql("SELECT DISTINCT timestamp FROM zero ORDER BY timestamp").fetchall()
    timestamps = [row[0] for row in timestamps]
    base_image = Image.new("RGBA", (2000, 2000), (0, 0, 0, 0))
    
    for timestamp in timestamps:
        data = conn.sql(query + f" AND timestamp = '{timestamp}'").fetchall()
        image_data = []
        for row in data:
            coord = row[1].split(',')
            image_data.append((hex_to_rgb(row[0]), int(coord[0]), int(coord[1])))
        timestamp_image = Image.new("RGBA", (2000, 2000), (0, 0, 0, 0)) # Use RGBA for transparency
        pixels = timestamp_image.load()

        for color, x, y in image_data:
            pixels[x, y] = color + (255,) # alpha=255 (fully opaque)

        base_image = Image.alpha_composite(base_image, timestamp_image)

        intermediate_filename = os.path.join("img/", f"{timestamp.strftime('%Y-%m-%d_%H')}.png")
        base_image.save(intermediate_filename)
