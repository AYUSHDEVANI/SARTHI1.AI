from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from textblob import TextBlob
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

# from langdetect import detect, DetectorFactory
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet
from lingua import Language, LanguageDetectorBuilder
from typing import Dict, Text, Any, List
import requests
import geocoder

# rasa run --enable-api


class ActionDetectLanguage(Action):

    def name(self) -> str:
        return "action_detect_language"
    """Detects the text's language."""
    

    

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> list:
        # # translate_client = translate.Client()
        # user_message = tracker.latest_message.get('text')
        # detected_language = translate_client.detect_language(user_message)
        # print(detected_language["language"])
        # return [SlotSet("language", detected_language['language'])]

        languages = [Language.ENGLISH,Language.GUJARATI, Language.HINDI]
        detector = LanguageDetectorBuilder.from_languages(*languages).build()
        user_message = tracker.latest_message.get('text')
        language = detector.detect_language_of(user_message)
        print(language.name)
        return [SlotSet("language", language.name)]



    # result = translate_client.detect_language(text)

    # print(f"Text: {text}")
    # print("Confidence: {}".format(result["confidence"]))
    # print("Language: {}".format(result["language"]))

    # return result



# class ActionDetectLanguage(Action):
#     def name(self) -> str:
#         return "action_detect_language"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> list:
#         user_message = tracker.latest_message.get('text')
#         detected_language = self.detect_language(user_message)
#         return [SlotSet("language", detected_language)]

#     def detect_language(self, text: str) -> str:
#         try:
#             blob = TextBlob(text)
#             return blob.detect_language()
#         except Exception as e:
#             print(f"Error detecting language: {e}")
#             return "en"  # Default to English in case of an error
#         return "en"


import json

with open('PreprocessedData/crop.json', 'r', encoding='utf-8') as f:
    crop_data = json.load(f)

with open('PreprocessedData/f1.json' , 'r', encoding='utf-8') as f:

   fertilizer_data = json.load(f)

# print(fertilizer_data)

class ActionGreet(Action):
    def name(self):
        return "action_greet"

    def run(self, dispatcher, tracker, domain):
        language = tracker.get_slot("language")
        if language == 'GUJARATI':
            dispatcher.utter_message(text="હેલો! હું સારથી તમને કેવી રીતે મદદ કરી શકું?")
        elif language == 'HINDI':
            dispatcher.utter_message(text="नमस्ते! मैं सारथी आपकी कैसे मदद कर सक्ती हूँ?")
        else:
            dispatcher.utter_message(text="Hello! I am Sarthi How can I assist you today?")
        return []
    
class ActionFertilizerAdvice(Action):
    def name(self) -> str:
        return "action_fertilizer_advice"
    
    

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
     
        crop_type = str(tracker.get_slot("crop_type"))
        soil_type = str(tracker.get_slot("soil_type"))
        season = str(tracker.get_slot("season"))
        language = tracker.get_slot("language")

        if language == "GUJARATI":
            language = "gu"
        elif language == "HINDI":
            language = "hi"
        else:
            language = "en"
        # print("123")
        # print(type(language))
        print(crop_type)
        print(season)
        print(soil_type)
        

        for suggestion in fertilizer_data["crop_suggestions"]:
            # print("1")
            if ((str(suggestion["crop_type"][language]).lower() == crop_type.lower()) and
                str(suggestion["soil_type"][language]).lower() == soil_type.lower() and
                str(suggestion["season"][language]).lower() == season.lower()):
                
                print("HOI")
                suggestion = suggestion["suggested_fertilizer"][language]
                if language == "en":
                    dispatcher.utter_message(text=f"For {crop_type} in {season} season on {soil_type} soil, the suggested fertilizer is {suggestion}.")
                elif language == "hi":
                    dispatcher.utter_message(text=f"{crop_type} के लिए {soil_type} मिट्टी में {season} मौसम में, सुझाए गए उर्वरक {suggestion} हैं।")
                elif language == "gu":
                    dispatcher.utter_message(text=f"{crop_type} માટે {soil_type} માટીમાં {season} સીઝનમાં, સૂચવાયેલ ખાતર {suggestion} છે.")
                return []

        
        
        dispatcher.utter_message(text="Sorry, I couldn't find any fertilizer suggestion for the given inputs.")
        return []

class ActionCropAdvice(Action):
    def name(self) -> Text:
        return "action_crop_advice"
    
    # def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
    #     # Custom logic for fertilizer advice
    #     dispatcher.utter_message(text="Based on your input, here's some advice on fertilizers.")
    #     return []

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        soil_type = tracker.get_slot("soil_type")
        season = tracker.get_slot("season")
        language = tracker.get_slot("language")  # Assuming you have a slot for language
        if language == "GUJARATI":
            language = "gu"
        elif language == "HINDI":
            language = "hi"
        else:
            language = "en"

        
            
        print(soil_type)
                
        suggestion = crop_data["suggestions"][soil_type][season][language]["crop"]
        if language == "ENGLISH":
            dispatcher.utter_message(text=f"For {season} season on {soil_type} soil, the suggested crop is {suggestion}.")
        elif language == "HINDI":
            dispatcher.utter_message(text=f"{soil_type} के लिए, मिट्टी में {season} मौसम में, सुझाए गए फसल {suggestion} हैं।")
        elif language == "GUJARATI":
            dispatcher.utter_message(text=f"{soil_type} માટીમાં {season} સીઝનમાં, સૂચવાયેલ પાક {suggestion} છે.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any fertilizer suggestion for the given inputs.")
        return []

class ActionQualityCheck(Action):
    def name(self) -> str:
        return "action_quality_check"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        crop_type = tracker.get_slot("crop_type")
        quality_check_advice = f"To check the quality of {crop_type}, ensure it meets market standards for color, size, and texture."
        dispatcher.utter_message(quality_check_advice)
        return []

class ActionBidding(Action):
    def name(self) -> str:
        return "action_bidding"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        crop_type = tracker.get_slot("crop_type")
        quality = tracker.get_slot("quality")
        bidding_info = f"For {crop_type}, the starting bid is ₹{quality}-based."
        dispatcher.utter_message(bidding_info)
        return []



class ActionFertilizerSuggestion(Action):

    def name(self) -> str:
        return "action_fertilizer_suggestion"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        crop_name = tracker.get_slot('crop_name')
        g = geocoder.ip('me')
        lat = g.lat
        lng = g.lng
        # lat = 21.2686832
        # lng = 71.3411637
        # print(g.latlng)
        soil_type = requests.get(
            url="https://api-test.openepi.io/soil/type",
            params={"lat": lat, "lon": lng, "top_k": 3},
            )
        soil_type = soil_type.json()
        soil_type = soil_type["properties"]["most_probable_soil_type"]

        language = tracker.get_slot("language")

        if language == "GUJARATI":
            language = "gu"
        elif language == "HINDI":
            language = "hi"
        else:
            language = "en"

        for suggestion in fertilizer_data:
            if ((str(suggestion["crop_type"][language]).lower() == crop_name.lower()) and
                str(suggestion["soil_type"][language]).lower() == soil_type.lower()):
                # str(suggestion["season"]["en"]).lower() == "Kharif".lower()):
                #   print(suggestion["fertilizer"]["en"])
                
                print("HOI")
                fertilizers = suggestion["fertilizer"][language]
                # Language-specific response
                # language = tracker.get_slot('language')
                if language == 'en':
                    message = f"For the crop {crop_name}, the suggested fertilizers are: {fertilizers}."
                elif language == 'hi':
                    message = f"फसल {crop_name} के लिए सुझावित उर्वरक हैं: {fertilizers}."
                elif language == 'gu':
                    message = f"પાક {crop_name} માટે સૂચિત ખાતર છે: {fertilizers}."
                
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="Sorry, I couldn't fetch the fertilizer suggestions. Please try again later.")

        # return [SlotSet("fertilizers", fertilizers)]
        return []

        # Example API call
        # api_url = f"http://example-api.com/fertilizers?crop={crop_name}"
        # response = requests.get(api_url)

        # if response.status_code == 200:
        #     data = response.json()
        #     fertilizers = data.get('fertilizers', 'No suggestions available')

        #     # Language-specific response
        #     language = tracker.get_slot('language')
        #     if language == 'en':
        #         message = f"For the crop {crop_name}, the suggested fertilizers are: {fertilizers}."
        #     elif language == 'hi':
        #         message = f"फसल {crop_name} के लिए सुझावित उर्वरक हैं: {fertilizers}."
        #     elif language == 'gu':
        #         message = f"પાક {crop_name} માટે સૂચિત ખાતર છે: {fertilizers}."

        #     dispatcher.utter_message(text=message)
        # else:
        #     dispatcher.utter_message(text="Sorry, I couldn't fetch the fertilizer suggestions. Please try again later.")

        # return [SlotSet("fertilizers", fertilizers)]
    


class ActionAskCropName(Action):
    def name(self) -> str:
        return "action_ask_crop_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        dispatcher.utter_message(text="Please tell me the crop name you're asking about.")
        return []