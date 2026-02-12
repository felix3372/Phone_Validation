"""
Phone Number Length Validator with Toll-Free Detection
Validates phone numbers based on country-specific length requirements,
detects toll-free numbers, and identifies duplicate country codes
"""

import phonenumbers
import re

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

# Country dial codes mapping (ISO alpha-2 to dial code)
COUNTRY_DIAL_CODES = {
    # Americas
    "US": "1", "CA": "1", "MX": "52", "BR": "55", "AR": "54", 
    "CL": "56", "CO": "57", "PE": "51", "UY": "598",
    
    # Europe
    "GB": "44", "DE": "49", "FR": "33", "IT": "39", "ES": "34",
    "NL": "31", "SE": "46", "CH": "41", "AT": "43", "BE": "32",
    "PL": "48", "NO": "47", "DK": "45", "FI": "358", "IE": "353",
    "PT": "351", "GR": "30", "CZ": "420", "RO": "40", "HU": "36",
    "BG": "359", "HR": "385", "SK": "421", "SI": "386", "LT": "370",
    "LV": "371", "EE": "372", "CY": "357", "MT": "356", "LU": "352",
    "AL": "355", "BA": "387", "RS": "381", "ME": "382", "MK": "389",
    "MD": "373", "TR": "90", "AZ": "994",
    
    # Asia Pacific
    "CN": "86", "JP": "81", "KR": "82", "IN": "91", "SG": "65",
    "HK": "852", "TW": "886", "MY": "60", "TH": "66", "ID": "62",
    "PH": "63", "VN": "84", "AU": "61", "NZ": "64", "LK": "94",
    "KZ": "7", "AM": "374",
    
    # Middle East
    "SA": "966", "AE": "971", "IL": "972", "QA": "974", "OM": "968",
    "BH": "973", "JO": "962",
    
    # Africa
    "ZA": "27", "EG": "20", "NG": "234", "KE": "254", "GH": "233",
    "ET": "251", "UG": "256", "ZW": "263", "AO": "244", "MZ": "258",
    "NA": "264", "BW": "267", "MU": "230", "RW": "250",
}


def check_duplicate_country_code(phone_number, country_code):
    """
    Check if the country code is duplicated in the phone number
    Example: +4949XXXXXXXX (Germany's code 49 appears twice)
    
    Args:
        phone_number (str): The full phone number (e.g., '+4949XXXXXXXX')
        country_code (str): ISO 3166-1 alpha-2 country code (e.g., 'DE')
    
    Returns:
        dict: {
            'has_duplicate': bool,
            'country_dial_code': str,
            'detected_pattern': str or None,
            'message': str
        }
    """
    # Input validation
    if not phone_number or not isinstance(phone_number, str):
        return {
            'has_duplicate': False,
            'country_dial_code': None,
            'detected_pattern': None,
            'message': 'Invalid phone number input'
        }
    
    # Normalize country code
    country_code = country_code.upper() if country_code else None
    
    if not country_code or country_code not in COUNTRY_DIAL_CODES:
        return {
            'has_duplicate': False,
            'country_dial_code': None,
            'detected_pattern': None,
            'message': f'Country code {country_code} not found in database'
        }
    
    # Get the dial code for this country
    dial_code = COUNTRY_DIAL_CODES[country_code]
    
    # Remove all non-digit characters except the leading +
    clean_number = phone_number.strip()
    has_plus = clean_number.startswith('+')
    digits_only = re.sub(r'[^\d]', '', clean_number)
    
    # Check if the dial code appears twice at the beginning
    # Pattern: +{dial_code}{dial_code}... or {dial_code}{dial_code}...
    duplicate_pattern = dial_code + dial_code
    
    if digits_only.startswith(duplicate_pattern):
        detected = f"+{duplicate_pattern}..." if has_plus else f"{duplicate_pattern}..."
        return {
            'has_duplicate': True,
            'country_dial_code': dial_code,
            'detected_pattern': detected,
            'message': 'Country Code Repeated'
        }
    
    return {
        'has_duplicate': False,
        'country_dial_code': dial_code,
        'detected_pattern': None,
        'message': ''  # Empty for valid cases
    }


def validate_phone_length(phone_number, country_code):
    """
    Validate if a phone number's length is acceptable for its country
    
    Args:
        phone_number (str): The full phone number in E.164 format (e.g., '+61872252566')
        country_code (str): ISO 3166-1 alpha-2 country code (e.g., 'AU' for Australia)
    
    Returns:
        dict: {
            'is_valid_length': bool or None,
            'actual_length': int,
            'expected_range': tuple or None,
            'expected_range_display': str,
            'message': str
        }
    """
    # Input validation
    if not phone_number or not isinstance(phone_number, str):
        return {
            'is_valid_length': False,
            'actual_length': 0,
            'expected_range': None,
            'expected_range_display': 'N/A',
            'message': 'Invalid phone number input'
        }
    
    # Normalize country code to uppercase
    country_code = country_code.upper() if country_code else None
    
    # Remove all non-digit characters for accurate length calculation
    clean_number = re.sub(r'[^\d]', '', phone_number)
    actual_length = len(clean_number)
    
    # Get expected length range for this country
    if country_code and country_code in COUNTRY_PHONE_LENGTHS:
        min_length, max_length = COUNTRY_PHONE_LENGTHS[country_code]
        
        is_valid = min_length <= actual_length <= max_length
        
        # CRITICAL FIX: Use text format with single quotes to prevent Excel date conversion
        # Format as '10 to 11' instead of '10-11' to avoid date interpretation
        expected_display = f"'{min_length} to {max_length}'"
        
        if is_valid:
            message = f"✓ Length is valid ({actual_length} digits)"
        else:
            message = f"✗ Invalid length (expected {min_length}-{max_length}, got {actual_length})"
        
        return {
            'is_valid_length': is_valid,
            'actual_length': actual_length,
            'expected_range': (min_length, max_length),  # Tuple for programmatic use
            'expected_range_display': expected_display,   # String safe for CSV/Excel
            'message': message
        }
    else:
        # Country not in database - return neutral result
        return {
            'is_valid_length': None,  # Unknown
            'actual_length': actual_length,
            'expected_range': None,
            'expected_range_display': "'Not defined'",
            'message': 'Length not pre-defined for this country'
        }


def is_tollfree_number(phone_number, country_code=None):
    """
    Check if a phone number is a toll-free number using the phonenumbers library
    
    Args:
        phone_number (str): The phone number to check (can be in E.164 format or local format)
        country_code (str, optional): ISO 3166-1 alpha-2 country code (e.g., 'US', 'AU')
    
    Returns:
        dict: {
            'is_tollfree': bool,
            'matched_prefix': str or None,
            'message': str
        }
    """
    if not phone_number or not isinstance(phone_number, str):
        return {
            'is_tollfree': False,
            'matched_prefix': None,
            'message': 'No phone number provided'
        }
    
    # Normalize country code
    country_code = country_code.upper() if country_code else None
    
    try:
        # Parse the phone number
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
            # Extract the prefix for display (first 3-4 digits of national number)
            national_number = str(parsed_number.national_number)
            prefix = national_number[:4] if len(national_number) >= 4 else national_number
            
            return {
                'is_tollfree': True,
                'matched_prefix': prefix,
                'message': '✓ Toll-free number (verified)'
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


def validate_phone_complete(phone_number, country_code):
    """
    Perform complete validation: length, toll-free status, and duplicate country code check
    
    Args:
        phone_number (str): The full phone number
        country_code (str): ISO 3166-1 alpha-2 country code
    
    Returns:
        dict: Complete validation results combining all checks
    """
    length_result = validate_phone_length(phone_number, country_code)
    tollfree_result = is_tollfree_number(phone_number, country_code)
    duplicate_result = check_duplicate_country_code(phone_number, country_code)
    
    return {
        'phone_number': phone_number,
        'country_code': country_code,
        'length_validation': length_result,
        'tollfree_check': tollfree_result,
        'duplicate_code_check': duplicate_result,
        'overall_valid': (
            length_result.get('is_valid_length') == True and 
            not duplicate_result.get('has_duplicate')
        )
    }


def get_country_length_info(country_code):
    """
    Get the acceptable phone number length range for a country
    
    Args:
        country_code (str): ISO 3166-1 alpha-2 country code
    
    Returns:
        tuple or None: (min_length, max_length) or None if not available
    """
    country_code = country_code.upper() if country_code else None
    return COUNTRY_PHONE_LENGTHS.get(country_code)


def add_country_length(country_code, min_length, max_length):
    """
    Add or update a country's phone number length requirement
    
    Args:
        country_code (str): ISO 3166-1 alpha-2 country code
        min_length (int): Minimum acceptable length
        max_length (int): Maximum acceptable length
    """
    country_code = country_code.upper() if country_code else None
    if country_code:
        COUNTRY_PHONE_LENGTHS[country_code] = (min_length, max_length)


def get_all_countries():
    """
    Get all countries with length validation data
    
    Returns:
        dict: Dictionary of country codes and their length requirements
    """
    return COUNTRY_PHONE_LENGTHS.copy()


def get_country_dial_code(country_code):
    """
    Get the dial code for a specific country
    
    Args:
        country_code (str): ISO 3166-1 alpha-2 country code
    
    Returns:
        str or None: Dial code (e.g., '1' for US) or None if not found
    """
    country_code = country_code.upper() if country_code else None
    return COUNTRY_DIAL_CODES.get(country_code)


# Example usage and testing
if __name__ == "__main__":
    # Test cases - including duplicate country codes for multiple countries
    test_cases = [
        # Duplicate country code tests (various countries)
        ("+4949123456789", "DE"),      # Germany - duplicate 49
        ("+11234567890", "US"),        # USA - duplicate 1
        ("+11234567890", "CA"),        # Canada - duplicate 1
        ("+4444123456789", "GB"),      # UK - duplicate 44
        ("+3333123456789", "FR"),      # France - duplicate 33
        ("+6161872252566", "AU"),      # Australia - duplicate 61
        ("+8686123456789", "CN"),      # China - duplicate 86
        
        # Valid numbers (no duplicates)
        ("+61872252566", "AU"),        # Valid Australian number
        ("+18001234567", "US"),        # US toll-free
        ("+442012345678", "GB"),       # Valid UK number
        ("+33123456789", "FR"),        # Valid French number
        ("+8613812345678", "CN"),      # Valid Chinese number
        
        # Invalid length
        ("+1234567890", "US"),         # Too short
    ]
    
    print("Phone Number Validation Test Results")
    print("=" * 80)
    print("\nTesting Duplicate Country Code Detection Across Multiple Countries:")
    print("=" * 80)
    
    for phone, country in test_cases:
        print(f"\nPhone: {phone}, Country: {country}")
        print("-" * 80)
        
        result = validate_phone_complete(phone, country)
        
        print(f"Length: {result['length_validation']['message']}")
        print(f"  Expected: {result['length_validation']['expected_range_display']}")
        print(f"  Actual: {result['length_validation']['actual_length']}")
        
        print(f"Toll-free: {result['tollfree_check']['message']}")
        
        dup_msg = result['duplicate_code_check']['message']
        if dup_msg:
            print(f"⚠️  SUSPICIOUS: {dup_msg}")
            print(f"  Pattern: {result['duplicate_code_check']['detected_pattern']}")
        else:
            print(f"Duplicate Code: ✓ OK")
        
        print(f"Overall Valid: {'✓ YES' if result['overall_valid'] else '✗ NO'}")
