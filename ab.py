import json

with open('PreprocessedData/crop.json', 'r', encoding='utf-8') as f:
    crop_data = json.load(f)

with open('PreprocessedData/f1.json' , 'r', encoding='utf-8') as f:

   fertilizer_data = json.load(f)

# print(crop_data["suggestions"]["Loamy"]["Winter"]["gu"])
# print(fertilizer_data[0]["crop_type"])

# for data in fertilizer_data:
#     print(data["crop_type"].lower())
# fertilizer_data = fertilizer_data["crop_suggestions"]
# f_c = fertilizer_data
# print(f_c["crop_type"]["en" == "Rice"])


for suggestion in fertilizer_data:
            if ((str(suggestion["crop_type"]["en"]).lower() == "wheat".lower()) and
                str(suggestion["soil_type"]["en"]).lower() == "Cambisols".lower()):
                # str(suggestion["season"]["en"]).lower() == "Kharif".lower()):
                  print(suggestion["fertilizer"]["en"])

