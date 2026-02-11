"""
Phone Number Length Validator with Toll-Free Detection
Validates phone numbers based on country-specific length requirements
and detects toll-free numbers
"""

# Country-specific phone number length requirements (min, max)
# Based on complete validation data - 90+ countries
COUNTRY_PHONE_LENGTHS = {
    # Europe
    "AL": (11, 12),  # Albania
    "AT": (8, 13),   # Austria
    "AZ": (12, 12),  # Azerbaijan
    "BE": (10, 10),  # Belgium
    "BG": (11, 11),  # Bulgaria
    "BA": (11, 11),  # Bosnia and Herzegovina
    "HR": (11, 12),  # Croatia
    "CY": (11, 11),  # Cyprus
    "CZ": (12, 12),  # Czech Republic
    "DK": (10, 10),  # Denmark
    "EE": (10, 10),  # Estonia
    "FI": (8, 12),   # Finland
    "FR": (11, 12),  # France
    "DE": (8, 15),   # Germany
    "GR": (12, 12),  # Greece
    "HU": (10, 10),  # Hungary
    "IE": (11, 13),  # Ireland
    "IT": (9, 13),   # Italy
    "LV": (11, 11),  # Latvia
    "LT": (11, 11),  # Lithuania
    "LU": (8, 11),   # Luxembourg
    "MT": (11, 11),  # Malta
    "MD": (11, 11),  # Moldova
    "ME": (9, 9),    # Montenegro
    "NL": (11, 11),  # Netherlands
    "MK": (11, 11),  # North Macedonia
    "NO": (10, 10),  # Norway
    "PL": (11, 11),  # Poland
    "PT": (12, 12),  # Portugal
    "RO": (11, 11),  # Romania
    "RS": (11, 12),  # Serbia
    "SK": (12, 12),  # Slovakia
    "SI": (11, 11),  # Slovenia
    "ES": (11, 11),  # Spain
    "SE": (9, 11),   # Sweden
    "CH": (11, 11),  # Switzerland
    "TR": (9, 12),   # Turkey
    "GB": (12, 12),  # United Kingdom
    
    # Africa
    "AO": (12, 12),  # Angola
    "BW": (10, 10),  # Botswana
    "EG": (10, 11),  # Egypt
    "ET": (12, 12),  # Ethiopia
    "GH": (12, 12),  # Ghana
    "KE": (12, 13),  # Kenya
    "MU": (10, 10),  # Mauritius
    "MZ": (11, 11),  # Mozambique
    "NA": (12, 12),  # Namibia
    "NG": (11, 13),  # Nigeria
    "RW": (12, 12),  # Rwanda
    "ZA": (11, 12),  # South Africa
    "UG": (12, 12),  # Uganda
    "ZW": (12, 13),  # Zimbabwe
    
    # Middle East
    "BH": (11, 11),  # Bahrain
    "IL": (11, 12),  # Israel
    "JO": (11, 11),  # Jordan
    "OM": (11, 11),  # Oman
    "QA": (10, 11),  # Qatar
    "SA": (12, 12),  # Saudi Arabia
    "AE": (10, 12),  # United Arab Emirates
    
    # Asia
    "AM": (11, 11),  # Armenia
    "CN": (11, 13),  # China
    "HK": (11, 11),  # Hong Kong
    "IN": (12, 12),  # India
    "ID": (8, 13),   # Indonesia
    "JP": (10, 11),  # Japan
    "KZ": (10, 11),  # Kazakhstan
    "KR": (9, 11),   # South Korea
    "MY": (10, 11),  # Malaysia
    "PH": (11, 12),  # Philippines
    "SG": (10, 10),  # Singapore
    "LK": (11, 11),  # Sri Lanka
    "TW": (11, 12),  # Taiwan
    "TH": (10, 11),  # Thailand
    "VN": (12, 12),  # Vietnam
    
    # Americas
    "AR": (10, 12),  # Argentina
    "BR": (12, 13),  # Brazil
    "CA": (11, 11),  # Canada
    "CL": (10, 11),  # Chile
    "CO": (10, 10),  # Colombia
    "MX": (12, 12),  # Mexico
    "PE": (10, 11),  # Peru
    "US": (11, 11),  # United States
    "UY": (11, 11),  # Uruguay
    
    # Oceania
    "AU": (11, 11),  # Australia
    "NZ": (10, 10),  # New Zealand
}

# Toll-free number prefixes by country
# Comprehensive list of toll-free prefixes worldwide
TOLLFREE_PREFIXES = {
    # North America
    "united states": ["800", "888", "877", "866", "855", "844", "833", "822", "811", "899"],
    "canada": ["800", "888", "877", "866", "855", "844", "833", "822", "811", "899"],
    "mexico": ["800"],
    
    # Europe
    "united kingdom": ["800", "808"],
    "germany": ["800"],
    "france": ["800"],
    "italy": ["800"],
    "netherlands": ["0800"],
    "spain": ["900"],
    "sweden": ["020"],
    "switzerland": ["0800"],
    
    # Asia Pacific
    "australia": ["1800", "1300", "800", "300"],
    "new zealand": ["0800"],
    "india": ["1800"],
    "japan": ["0120", "0800"],
    "china": ["400", "800"],
    "singapore": ["1800", "800"],
    "hong kong": ["800"],
    
    # Latin America
    "brazil": ["0800"],
    "argentina": ["0800"],
    "chile": ["800"],
    
    # Africa
    "south africa": ["0800"],
    
    # Add more countries as needed
}

# Country dial codes mapping (ISO alpha-2 to dial code)
COUNTRY_DIAL_CODES = {
    # Americas
    "us": "1", "ca": "1", "mx": "52", "br": "55", "ar": "54", 
    "cl": "56", "co": "57", "pe": "51", "uy": "598",
    
    # Europe
    "gb": "44", "de": "49", "fr": "33", "it": "39", "es": "34",
    "nl": "31", "se": "46", "ch": "41", "at": "43", "be": "32",
    "pl": "48", "no": "47", "dk": "45", "fi": "358", "ie": "353",
    "pt": "351", "gr": "30", "cz": "420", "ro": "40", "hu": "36",
    "bg": "359", "hr": "385", "sk": "421", "si": "386", "lt": "370",
    "lv": "371", "ee": "372", "cy": "357", "mt": "356", "lu": "352",
    "al": "355", "ba": "387", "rs": "381", "me": "382", "mk": "389",
    "md": "373", "tr": "90", "az": "994",
    
    # Asia Pacific
    "cn": "86", "jp": "81", "kr": "82", "in": "91", "sg": "65",
    "hk": "852", "tw": "886", "my": "60", "th": "66", "id": "62",
    "ph": "63", "vn": "84", "au": "61", "nz": "64", "lk": "94",
    "kz": "7", "am": "374",
    
    # Middle East
    "sa": "966", "ae": "971", "il": "972", "qa": "974", "om": "968",
    "bh": "973", "jo": "962",
    
    # Africa
    "za": "27", "eg": "20", "ng": "234", "ke": "254", "gh": "233",
    "et": "251", "ug": "256", "zw": "263", "ao": "244", "mz": "258",
    "na": "264", "bw": "267", "mu": "230", "rw": "250",
}


def validate_phone_length(phone_number, country_code):
    """
    Validate if a phone number's length is acceptable for its country
    
    Args:
        phone_number (str): The full phone number in E.164 format (e.g., '+61872252566')
        country_code (str): ISO 3166-1 alpha-2 country code (e.g., 'AU' for Australia)
    
    Returns:
        dict: {
            'is_valid_length': bool,
            'actual_length': int,
            'expected_range': tuple or None,
            'message': str
        }
    """
    # Remove '+' and any spaces/dashes for length calculation
    clean_number = phone_number.replace('+', '').replace(' ', '').replace('-', '')
    actual_length = len(clean_number)
    
    # Get expected length range for this country
    if country_code in COUNTRY_PHONE_LENGTHS:
        min_length, max_length = COUNTRY_PHONE_LENGTHS[country_code]
        
        is_valid = min_length <= actual_length <= max_length
        
        if is_valid:
            message = f"✓ Length is valid ({actual_length} digits)"
        else:
            message = "Invalid Phone Number Length"
        
        return {
            'is_valid_length': is_valid,
            'actual_length': actual_length,
            'expected_range': (min_length, max_length),
            'message': message
        }
    else:
        # Country not in database - return neutral result
        return {
            'is_valid_length': None,  # Unknown
            'actual_length': actual_length,
            'expected_range': None,
            'message': "Length Not Pre-Defined"
        }


import phonenumbers

def is_tollfree_number(phone_number, country_name=None, country_code=None):
    """
    Check if a phone number is a toll-free number using the phonenumbers library
    
    Args:
        phone_number (str): The phone number to check (can be in E.164 format or local format)
        country_name (str, optional): Full country name (not used, kept for compatibility)
        country_code (str, optional): ISO 3166-1 alpha-2 country code (e.g., 'US', 'AU')
    
    Returns:
        dict: {
            'is_tollfree': bool,
            'matched_prefix': str or None,
            'message': str
        }
    """
    if phone_number is None:
        return {
            'is_tollfree': False,
            'matched_prefix': None,
            'message': 'No phone number provided'
        }
    
    try:
        # Parse the phone number
        # If we have a country code, use it as the region hint
        parsed_number = phonenumbers.parse(phone_number, country_code)
        
        # Check if it's a valid number
        if not phonenumbers.is_valid_number(parsed_number):
            return {
                'is_tollfree': False,
                'matched_prefix': None,
                'message': 'Invalid phone number'
            }
        
        # Get the number type
        number_type = phonenumbers.number_type(parsed_number)
        
        # Check if it's toll-free
        is_tollfree = (number_type == phonenumbers.PhoneNumberType.TOLL_FREE)
        
        if is_tollfree:
            # Extract the prefix for display
            # Get the national number and extract prefix
            national_number = str(parsed_number.national_number)
            prefix = national_number[:4] if len(national_number) >= 4 else national_number[:3]
            
            return {
                'is_tollfree': True,
                'matched_prefix': prefix,
                'message': f'Toll-free number (verified)'
            }
        else:
            return {
                'is_tollfree': False,
                'matched_prefix': None,
                'message': 'Not a toll-free number'
            }
    
    except phonenumbers.phonenumberutil.NumberParseException as e:
        return {
            'is_tollfree': False,
            'matched_prefix': None,
            'message': f'Error parsing number: {str(e)}'
        }
    except Exception as e:
        return {
            'is_tollfree': False,
            'matched_prefix': None,
            'message': f'Error: {str(e)}'
        }


def get_country_length_info(country_code):
    """
    Get the acceptable phone number length range for a country
    
    Args:
        country_code (str): ISO 3166-1 alpha-2 country code
    
    Returns:
        tuple or None: (min_length, max_length) or None if not available
    """
    return COUNTRY_PHONE_LENGTHS.get(country_code)


def add_country_length(country_code, min_length, max_length):
    """
    Add or update a country's phone number length requirement
    
    Args:
        country_code (str): ISO 3166-1 alpha-2 country code
        min_length (int): Minimum acceptable length
        max_length (int): Maximum acceptable length
    """
    COUNTRY_PHONE_LENGTHS[country_code] = (min_length, max_length)


def add_tollfree_prefix(country_key, prefix):
    """
    Add a toll-free prefix for a country
    
    Args:
        country_key (str): Country name in lowercase (e.g., 'united states')
        prefix (str): Toll-free prefix to add (e.g., '800')
    """
    country_key = country_key.lower()
    if country_key not in TOLLFREE_PREFIXES:
        TOLLFREE_PREFIXES[country_key] = []
    if prefix not in TOLLFREE_PREFIXES[country_key]:
        TOLLFREE_PREFIXES[country_key].append(prefix)


def get_all_countries():
    """
    Get all countries with length validation data
    
    Returns:
        dict: Dictionary of country codes and their length requirements
    """
    return COUNTRY_PHONE_LENGTHS.copy()


def get_all_tollfree_countries():
    """
    Get all countries with toll-free detection data
    
    Returns:
        dict: Dictionary of country names and their toll-free prefixes
    """
    return TOLLFREE_PREFIXES.copy()
