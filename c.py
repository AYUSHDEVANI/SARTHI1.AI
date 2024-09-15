# from httpx import Client

# with Client() as client:
#     # Get the soil type at the queried location
#     # and the probability of the top 3 most probable soil types
#     response = client.get(
#         url="https://api-test.openepi.io/soil/type",
#         params={"lat": 22.297, "lon": 73.194, "top_k": 3},
#     )


#     json = response.json()

#     # Get the soil type and probability for the second most probable soil type
#     soil_type = json["properties"]["probabilities"][1]["soil_type"]
#     probability = json["properties"]["probabilities"][1]["probability"]

#     print(f"Soil type: {soil_type}, Probability: {probability}")


import requests
lat = 20.004
lng = 73.214
response = requests.get(
    url="https://api-test.openepi.io/soil/type",
        params={"lat": lat, "lon": lng, "top_k": 3},
)
json = response.json()
print(json)


import geocoder
g = geocoder.ip('me')
print(g.latlng)

print(json["properties"]["most_probable_soil_type"])
# g = 
print(g.lat)
print(g.lng)
