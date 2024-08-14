# load_citybuf.py

from sys import argv
import resource
import CityBufReader

from flatCitybuf import Boundaries

fpath = argv[1]

maxrss = 0.0
no_solid = 0
no_msurface = 0

with open(fpath, "rb") as file:
    reader = CityBufReader.CityBufReader(file)

    for feature in reader.features():
        memory = resource.getrusage(resource.RUSAGE_SELF)
        a = memory.ru_maxrss / 1024 / 1024
        if a > maxrss:
            maxrss = a

        for i in range(feature.ObjectsLength()):
            obj = feature.Objects(i)
            for j in range(obj.GeometryLength()):
                geom = obj.Geometry(j)
                if geom.BoundariesType() == Boundaries.Boundaries.Solid:
                    no_solid += 1
                elif geom.BoundariesType() == Boundaries.Boundaries.MultiSurface:
                    no_msurface += 1

memory = resource.getrusage(resource.RUSAGE_SELF)
a = memory.ru_maxrss / 1024 / 1024
if a > maxrss:
    maxrss = a
    

print(maxrss)
# print(no_solid)
# print(no_msurface)