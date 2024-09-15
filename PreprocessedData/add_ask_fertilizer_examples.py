import json
import yaml

# Load your JSON data
with open('PreprocessedData/fertilizers.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Prepare the training data
nlu_data = {
    "version": "2.0",
    "nlu": []
}
examples = []
# Add examples to the nlu_data for each language
for crop in data['crop_suggestions']:
    for lang, crop_type in crop['crop_type'].items():
        soil_type = crop['soil_type'][lang]
        season = crop['season'][lang]
        fertilizer = crop['suggested_fertilizer'][lang]
        
        example = f"What fertilizer should I use for [{crop_type}](crop_type) in [{season}](season) season on [{soil_type}](soil_type) soil?"
        examples.append(example)
        example = f"{crop_type} के लिए {soil_type} मिट्टी में {season} मौसम में कौन सा उर्वरक उपयोग करें?"
        examples.append(example)
        example = f"{crop_type} માટે {soil_type} માટીમાં {season} સીઝનમાં કયું ખાતર ઉપયોગ કરવું?"
        examples.append(example)
        




nlu_data = {
    "version": "3.0",
    "nlu": [
        {
            "intent": "ask_fertilizer",
            "examples": "\n".join(examples)
        }
    ]
}


with open('nlu.yml', 'w') as file:
    yaml.dump(nlu_data, file)