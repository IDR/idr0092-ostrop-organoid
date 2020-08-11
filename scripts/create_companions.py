#!/usr/bin/env python
import sys
from ome_model.experimental import Plate, Image, create_companion
import subprocess

filenames = []
with open("idr0092.files") as fp:
    line = fp.readline()
    while line:
        filenames.append(line.strip())
        line = fp.readline()

plate_name = sys.argv[1]
columns = ['01', '02', '03', '04', '05', '06']
rows = ['A','B','C', 'D']
timepoints = ['0h', '24h', '48h', '72h', '96h']
print("Creating {}.companion.ome ...".format(plate_name))
plate = Plate(plate_name, len(rows), len(columns))
well_index = 0
for row_index, row in enumerate(rows):
    for column_index, column in enumerate(columns):
        well = plate.add_well(row_index, column_index)
        test = "{}_{}{}_0h.tiff".format(plate_name, row, column)
        if test in filenames:
            basename = "{}{}".format(row, column)
            image = Image(basename, 2080, 1552, 25, 3, len(timepoints),
                          order="XYZTC", type="uint8")
            image.add_channel("", -1, samplesPerPixel=3)
            for i, timepoint in enumerate(timepoints):
                filename = "{}_{}{}_{}.tiff".format(plate_name, row, column, timepoint)
                image.add_tiff(filename, c=0, z=0, t=i, planeCount=25)
                print("Add file {}".format(filename))
            well.add_wellsample(well_index, image)
            well_index += 1
companion_file = "../companions/{}.companion.ome".format(plate_name)
create_companion(plates=[plate], out=companion_file)

# Indent XML for readability
proc = subprocess.Popen(
    ['xmllint', '--format', '-o', companion_file, companion_file],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE)
(output, error_output) = proc.communicate()

print("Done.")
