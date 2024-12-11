#!/usr/bin/env python
import sys

from ome_types.model import OME
from ome_types.model import Channel
from ome_types.model import Image
from ome_types.model import ImageRef
from ome_types.model import Pixels
from ome_types.model import Plane
from ome_types.model import Plate
from ome_types.model import TiffData
from ome_types.model import Well
from ome_types.model import WellSample
import uuid

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

ome = OME()
plate = Plate(name=plate_name, rows=len(rows), columns=len(columns))
ome.plates.append(plate)

well_index = 0
for row_index, row in enumerate(rows):
    for column_index, column in enumerate(columns):
        well = Well(row=row_index, column=column_index)
        plate.wells.append(well)

        test = "{}_{}{}_0h.tiff".format(plate_name, row, column)
        if test in filenames:
            basename = "{}{}".format(row, column)
            pixels = Pixels(
                type='uint8',
                size_x=2080,
                size_y=1552,
                size_z=25,
                size_c=3,
                size_t=len(timepoints),
                dimension_order='XYZCT'
            )
            pixels.channels.append(Channel(samples_per_pixel=3))
            image = Image(
                name=basename,
                pixels=pixels
            )
            ome.images.append(image)

            for i, timepoint in enumerate(timepoints):
                filename = "{}_{}{}_{}.tiff".format(plate_name, row, column, timepoint)
                tiff_uuid = TiffData.UUID(
                    value=f"urn:uuid:{uuid.uuid4()}",
                    file_name=filename
                    )
                tiff = TiffData(
                    first_c=0,
                    first_t=i,
                    first_z=0,
                    plane_count=25,
                    uuid=tiff_uuid)
                pixels.tiff_data_blocks.append(tiff)
                for z in range(25):
                    pixels.planes.append(Plane(
                        delta_t=timepoint[:-1],
                        delta_t_unit="h",
                        the_c=0,
                        the_t=i,
                        the_z=z
                        )
                    )

            well.well_samples.append(
                WellSample(index=well_index, image_ref=ImageRef(id=image.id))
            )
            well_index += 1
companion_file = "../companions/{}.companion.ome".format(plate_name)
with open(companion_file, 'w') as f:
    f.write(ome.to_xml())


print("Done.")
