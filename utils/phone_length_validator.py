"""
Phone Number Length Validator
Validates phone numbers based on country-specific length requirements
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
    "PH": (11, 11),  # Philippines
    "SG": (10, 10),  # Singapore
    "LK": (11, 11),  # Sri Lanka
    "TW": (12, 12),  # Taiwan
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
    
    # Oceania
    "AU": (11, 11),  # Australia
    "NZ": (10, 10),  # New Zealand
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
            message = "Invalid Length as per MIS format"
        
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


def get_all_countries():
    """
    Get all countries with length validation data
    
    Returns:
        dict: Dictionary of country codes and their length requirements
    """
    return COUNTRY_PHONE_LENGTHS.copy()
