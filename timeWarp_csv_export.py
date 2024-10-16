# Licensing and Credits
# --------------------------------------------------
# Author: Isai Calderon III
# License: MIT License
# This script is provided "as is", without warranty of any kind.
# Feel free to modify and distribute it, as long as proper credit is given.
# --------------------------------------------------


import os
import csv
from maya import cmds as mc

timewarp_nodes = mc.ls(sl=1, typ='animCurveTT')
timewarp_node = timewarp_nodes[0]
end_time = mc.playbackOptions(q=1, max=1)
start_time = mc.playbackOptions(q=1, min=1)

# Get the workspace's data directory
workspace_path = mc.workspace(q=True, fullName=True)
output_dir = os.path.join(workspace_path, 'data')

# Create the data directory if it doesn't exist
if 'data' not in os.listdir(workspace_path):
    os.makedirs(output_dir)

# Define the output CSV file path
csv_file_path = os.path.join(output_dir, f"{timewarp_node}.csv")

# Open the CSV file for writing
with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    # Write the header
    csv_writer.writerow(["Frame", "Output Value"])

    # Loop through each frame and write data to CSV
    for i in range(int(start_time), int(end_time) + 1):
        output_value = mc.getAttr(timewarp_node + ".output", time=float(i))
        csv_writer.writerow([i, output_value])

print(f"CSV file written to: {csv_file_path}")
