#!/usr/bin/env python
import sys
from ome_model.experimental import Plate, Image, create_companion

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
for row_index, row in enumerate(rows):
    for column_index, column in enumerate(columns):
        well = plate.add_well(row_index, column_index)
        test = "{}_{}{}_0h.tiff".format(plate_name, row, column)
        if test in filenames:
            basename = "{}{}".format(row, column)
            # have to set c=0 otherwise validate will fail;
            # manually replace SizeC="0" with SizeC="3"
            # in the generated companion files afterwards!
            image = Image(basename, 2080, 1552, 25, 0, len(timepoints))
            for i, timepoint in enumerate(timepoints):
                filename = "{}_{}{}_{}.tiff".format(plate_name, row, column, timepoint)
                image.add_tiff(filename, c=0, z=0, t=i)
                print("Add file {}".format(filename))
            well.add_wellsample(0, image)
            image = None
        well = None
create_companion(plates=[plate], out="../companions/{}.companion.ome".format(plate_name))
print("Done.")
