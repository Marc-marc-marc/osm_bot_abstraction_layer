from termcolor import colored
import re

def is_human_confirming():
    choice = input().lower()
    if choice == "y":
        return True
    return False

def list_of_address_tags():
    return ['addr:city', 'addr:town', 'addr:place', 'addr:street',
            'addr:housenumber', 'addr:postcode', 'addr:unit', 'addr:state',
            'phone', 'contact:phone', 'addr:country', 'addr:suburb',
            'addr:neighbourhood', 'addr:district', 'contact:fax']

def is_shop(tags):
    # list from https://github.com/gravitystorm/openstreetmap-carto/blob/master/project.mml#L1485
    if tags.get('shop') in ['supermarket', 'bag', 'bakery', 'beauty', 'bed',
                'books', 'butcher', 'clothes', 'computer', 'confectionery',
                'fashion', 'convenience', 'department_store',
                'doityourself', 'hardware', 'fishmonger', 'florist',
                'garden_centre', 'hairdresser', 'hifi', 'ice_cream',
                'car', 'car_repair', 'bicycle', 'mall', 'pet',
                'photo', 'photo_studio', 'photography', 'seafood',
                'shoes', 'alcohol', 'gift', 'furniture', 'kiosk',
                'mobile_phone', 'motorcycle', 'musical_instrument',
                'newsagent', 'optician', 'jewelry', 'jewellery',
                'electronics', 'chemist', 'toys', 'travel_agency',
                'car_parts', 'greengrocer', 'farm', 'stationery',
                'laundry', 'dry_cleaning', 'beverages', 'perfumery',
                'cosmetics', 'variety_store', 'wine', 'outdoor',
                'copyshop', 'sports', 'deli', 'tobacco', 'art',
                'tea', 'coffee', 'tyres', 'pastry', 'chocolate',
                'music', 'medical_supply', 'dairy', 'video_games']:
        return True
    return False

def is_settlement(tags):
    if tags.get('place') in ['hamlet', 'village', 'town', 'city']:
        return True
    return False

def is_fuel_station(tags):
    if tags.get('amenity') == "fuel":
        return True
    return False

def is_indoor_poi(tags):
    if is_shop(tags):
        return True
    if tags.get("amenity") in ["bank", "fuel", "cafe", "fast_food", "restaurant"]:
        return True
    return False

def is_food_place(tags):
    if tags.get("amenity") in ["cafe", "fast_food", "restaurant"]:
        return True
    return False

def all_iso_639_1_language_codes():
    #based on https://www.loc.gov/standards/iso639-2/php/English_list.php
    return ['ab', 'aa', 'af', 'ak', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'av',
            'ae', 'ay', 'az', 'bm', 'ba', 'eu', 'be', 'bn', 'bh', 'bi', 'nb',
            'bs', 'br', 'bg', 'my', 'es', 'ca', 'km', 'ch', 'ce', 'ny', 'ny',
            'zh', 'za', 'cu', 'cu', 'cv', 'kw', 'co', 'cr', 'hr', 'cs', 'da',
            'dv', 'dv', 'nl', 'dz', 'en', 'eo', 'et', 'ee', 'fo', 'fj', 'fi',
            'nl', 'fr', 'ff', 'gd', 'gl', 'lg', 'ka', 'de', 'ki', 'el', 'kl',
            'gn', 'gu', 'ht', 'ht', 'ha', 'he', 'hz', 'hi', 'ho', 'hu', 'is',
            'io', 'ig', 'id', 'ia', 'ie', 'iu', 'ik', 'ga', 'it', 'ja', 'jv',
            'kl', 'kn', 'kr', 'ks', 'kk', 'ki', 'rw', 'ky', 'kv', 'kg', 'ko',
            'kj', 'ku', 'kj', 'ky', 'lo', 'la', 'lv', 'lb', 'li', 'li', 'li',
            'ln', 'lt', 'lu', 'lb', 'mk', 'mg', 'ms', 'ml', 'dv', 'mt', 'gv',
            'mi', 'mr', 'mh', 'ro', 'ro', 'mn', 'na', 'nv', 'nv', 'nd', 'nr',
            'ng', 'ne', 'nd', 'se', 'no', 'nb', 'nn', 'ii', 'ny', 'nn', 'ie',
            'oc', 'oj', 'cu', 'cu', 'cu', 'or', 'om', 'os', 'os', 'pi', 'pa',
            'ps', 'fa', 'pl', 'pt', 'pa', 'ps', 'qu', 'ro', 'rm', 'rn', 'ru',
            'sm', 'sg', 'sa', 'sc', 'gd', 'sr', 'sn', 'ii', 'sd', 'si', 'si',
            'sk', 'sl', 'so', 'st', 'nr', 'es', 'su', 'sw', 'ss', 'sv', 'tl',
            'ty', 'tg', 'ta', 'tt', 'te', 'th', 'bo', 'ti', 'to', 'ts', 'tn',
            'tr', 'tk', 'tw', 'ug', 'uk', 'ur', 'ug', 'uz', 'ca', 've', 'vi',
            'vo', 'wa', 'cy', 'fy', 'wo', 'xh', 'yi', 'yo', 'za', 'zu']

def name_tags():
    return ['name', 'loc_name', 'alt_name', 'old_name', 'reg_name']

def payment_tags():
    return ['payment:visa', 'payment:mastercard', 'payment:girocard', 'payment:coins',
            'payment:maestro', 'payment:notes', 'payment:v_pay', 'payment:debit_cards',
            'payment:cash', 'payment:credit_cards']

def get_text_before_first_colon(text):
    parsed_link = re.match('([^:]*):(.*)', text)
    if parsed_link is None:
        return None
    return parsed_link.group(1)

def is_expected_tag(key, value, tags, special_expected):
    if special_expected.get(key) == value:
        return True
    if key in ['source']:
        return True
    if is_indoor_poi(tags):
        if key in ['opening_hours', 'website', 'contact:website', 'level', 'operator',
                    'brand:wikidata', 'brand:wikipedia', 'wheelchair', 'brand', 'wifi']:
            return True
        if key in list_of_address_tags():
            return True
    if is_shop(tags) or is_fuel_station(tags):
        if key in payment_tags():
            return True
    if is_fuel_station(tags):
        if get_text_before_first_colon(key) == "fuel":
            return True
    if tags.get('shop') == "clothes":
        if key == 'clothes':
            return True
    if is_food_place(tags):
        if key in ['cuisine', 'smoking']:
            return True
    if is_settlement(tags):
        if key in name_tags():
            return True
        if key in ['place', 'population', 'postal_code', 'is_in', 'wikipedia', 'wikidata',
                    #regional - Slovakia
                   'import_ref', 'region_id', 'city_id', 'city_type',
                   #regional - Poland
                   'teryt:simc', 'teryt:updated_by',
                   ]:
            return True
        for lang in all_iso_639_1_language_codes():
            for name_tag in name_tags():
                if name_tag + ":" + lang == key:
                    return True
    if key in ["ele"]:
        return True
    sourced_tag = re.match('source:(.*)', key)
    if sourced_tag != None:
        sourced_tag = sourced_tag.group(1)
    if sourced_tag != None:
        if tags.get(sourced_tag) != None:
            return True
    return False

def smart_print_tag_dictionary(tags, special_expected):
    for key, value in sorted(tags.items()):
        text = key + "=" + value
        if is_expected_tag(key, value, tags, special_expected):
            print(text)
        else:
            print(colored(text, 'yellow'))

