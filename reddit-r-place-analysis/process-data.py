import sys
import csv
from datetime import datetime
import time

def process_csv(file_name, begin, end):
    try:
        start_time = datetime.strptime(begin, '%Y-%m-%d %H')
        end_time = datetime.strptime(end, '%Y-%m-%d %H')
    except ValueError as e:
        raise e
        
    if start_time > end_time:
        raise ValueError("start time must be before end time")
    
    color_counter = {}
    coord_counter = {}
    
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        next(reader) # skip the header
            
        print("Processing data...")
        for row in reader:
            parsed_time = datetime.strptime(row[0][:13], '%Y-%m-%d %H')
            
            if start_time <= parsed_time <= end_time:
                pixel_color = row[2]
                pixel_location = row[3]
                
                curr_color = color_counter.get(pixel_color, 0) + 1
                color_counter[pixel_color] = curr_color
                if curr_color > max_color[1]:
                    max_color = [pixel_color, curr_color]
                
                curr_coord = coord_counter.get(pixel_location, 0) + 1
                coord_counter[pixel_location] = curr_coord
                if curr_coord > max_coord[1]:
                    max_coord = [pixel_location, curr_coord]
                
                
    print(f"Most common color: {max_color[0]},\nMost common location: {max_coord[0]}")
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Not the correct number of arguments. Run as: python main.py [start-time] [end-time]")
        
    prog_start = time.perf_counter_ns()
    process_csv("2022_place_canvas_history.csv", sys.argv[1], sys.argv[2])
    print(f"time to process: {time.perf_counter_ns() - prog_start}")
