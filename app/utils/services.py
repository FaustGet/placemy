from static.Dictionary import city_type
from static.services import Services_specialization
async def get_lang_offerData(offerData:dict):
 
    offerData['city'] = city_type.value.get(offerData['city'])
    for options in Services_specialization.value.get('options'):
        for suboptions in options.get("options"):
            if suboptions.get("value") == offerData['specialization']:
                offerData['specialization'] = suboptions.get("label")
                break
    return offerData