#display.py
# Copyright (C) 2024 the PostPie developers
# (See DEVELOPERS FILE)

import csv
from postpie import PostPie

def create_csv( csvName, data):
    
    with open(f"{csvName}.csv", "w", newline="") as csvfile:
        write = csv.writer(csvfile)
        write.writerows(data)
