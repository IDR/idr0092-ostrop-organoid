#!/usr/bin/env python
from ome_model.experimental import Plate, Image, create_companion

path = "/uod/idr/filesets/idr0092-ostrop-organoid/20200722-ftp/images"

filenames = []
with open("idr0092.files") as fp:
    line = fp.readline()
    while line:
        filenames.append(line.strip())
        line = fp.readline()

plates = ['Plate1', 'Plate2', 'Plate3', 'Plate4', 'Plate5', 'Plate6', 'Plate7', 'Plate8']
rows = ['01', '02', '03', '04', '05', '06']
columns = ['A','B','C', 'D']
timepoints = ['0h', '24h', '48h', '72h', '96h']
for plate_name in plates:
    plate = Plate(plate_name, len(rows), len(columns))
    for row in rows:
        for column in columns:
            well = plate.add_well(row, column)
            test = "{}_{}{}_0h.tiff".format(plate_name, column, row)
            if test in filenames:
                basename = "{}{}".format(column, row)
                image = Image(basename, 2080, 1552, 25, 0, len(timepoints))
                for i, timepoint in enumerate(timepoints):
                    filename = "{}/{}_{}{}_{}.tiff".format(path, plate_name, column, row, timepoint)
                    image.add_tiff(filename, c=0, z=0, t=i)
                well.add_wellsample(0, image)
    create_companion(plates=[plate], out="../companions/{}.companion.ome".format(plate_name))
