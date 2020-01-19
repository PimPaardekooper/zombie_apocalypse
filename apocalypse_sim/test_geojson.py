import pygeoj

data = pygeoj.load(filepath="provinces.geojson")
print(data)

for x in data:
    for pol in x.geometry.coordinates:
        print(pol)