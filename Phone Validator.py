import streamlit as st
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import pandas as pd
import sys
from pathlib import Path
import pycountry

# Add utils to path
sys.path.append(str(Path(__file__).parent))
from utils.phone_length_validator import validate_phone_length

st.set_page_config(page_title="Phone Number Validator", page_icon="📱", layout="wide")

st.title("📱 Phone Number Validator")
st.markdown("Validate and get detailed information about phone numbers from around the world.")

def checkphone(phone_input, display=True):
    """Validate and extract information from a phone number"""
    # Auto-add "+" if missing and input looks like an international number
    if not phone_input.startswith("+"):
        phone_input = "+" + phone_input.strip()
    
    def check_suspicious(phone_number):
        """Check if last 5 digits are all the same"""
        clean_number = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        if len(clean_number) >= 5:
            last_5 = clean_number[-5:]
            if len(set(last_5)) == 1:  # All digits are the same
                return True
        return False
    
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_input, None)
        
        # Validate the phone number
        is_valid = phonenumbers.is_valid_number(parsed_number)
        
        # Get region code for length validation
        region_code = phonenumbers.region_code_for_number(parsed_number)
        
        # Get detailed information
        # Use geocoder first, if it returns a region, get country name from region code
        geo_description = geocoder.description_for_number(parsed_number, "en")
        
        # Import pycountry to get proper country names
        try:
            country_obj = pycountry.countries.get(alpha_2=region_code)
            country = country_obj.name if country_obj else geo_description
        except:
            country = geo_description
            
        sim_carrier = carrier.name_for_number(parsed_number, "en")
        country_code = parsed_number.country_code
        national_number = parsed_number.national_number
        
        # Get timezone
        timezones = timezone.time_zones_for_number(parsed_number)
        tz_str = ", ".join(timezones) if timezones else "Unknown"
        
        # Format in different styles
        international_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        e164_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
        # NEW: Validate phone number length
        length_validation = validate_phone_length(e164_format, region_code)
        
        # NEW: Check if suspicious
        is_suspicious = check_suspicious(e164_format)
        
        # Only display results if requested (for single number validation)
        if display:
            # Validation status
            col_status1, col_status2 = st.columns(2)
            
            with col_status1:
                if is_valid:
                    st.success("✅ Valid phone number")
                else:
                    st.error("❌ Invalid phone number")
            
            with col_status2:
                # Display length validation
                if length_validation['is_valid_length'] is True:
                    st.success(f"✅ {length_validation['message']}")
                elif length_validation['is_valid_length'] is False:
                    st.error(f"❌ {length_validation['message']}")
                else:
                    st.info(f"ℹ️ {length_validation['message']}")
            
            # Suspicious number warning
            if is_suspicious:
                st.warning("⚠️ Suspicious: Last 5 digits are identical")
            
            # Compact info display
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Country:** {country if country else 'Unknown'}")
                st.write(f"**Country Code:** +{country_code}")
                st.write(f"**Region Code:** {region_code if region_code else 'Unknown'}")
            
            with col2:
                st.write(f"**Carrier:** {sim_carrier if sim_carrier else 'Unknown'}")
                st.write(f"**Timezone:** {tz_str}")
                if length_validation['expected_range']:
                    min_len, max_len = length_validation['expected_range']
                    if min_len == max_len:
                        st.write(f"**Expected Length:** {min_len} digits")
                    else:
                        st.write(f"**Expected Length:** {min_len}-{max_len} digits")
            
            with col3:
                st.write(f"**International:** {international_format}")
                st.write(f"**E.164:** {e164_format}")
                st.write(f"**Actual Length:** {length_validation['actual_length']} digits")
        
        # Return data for batch processing
        return {
            "original": phone_input,
            "is_valid": is_valid,
            "is_valid_length": length_validation['is_valid_length'],
            "is_suspicious": is_suspicious,
            "country": country if country else "Unknown",
            "region_code": region_code if region_code else "Unknown",
            "carrier": sim_carrier if sim_carrier else "Unknown",
            "international": international_format,
            "e164": e164_format,
            "timezone": tz_str,
            "actual_length": length_validation['actual_length'],
            "expected_length": f"{length_validation['expected_range'][0]}-{length_validation['expected_range'][1]}" 
                              if length_validation['expected_range'] and length_validation['expected_range'][0] != length_validation['expected_range'][1]
                              else str(length_validation['expected_range'][0]) if length_validation['expected_range'] else "N/A",
            "length_message": length_validation['message']
        }

    except phonenumbers.NumberParseException as e:
        if display:
            st.error(f"❌ Error parsing number: {e}")
        return {
            "original": phone_input,
            "is_valid": False,
            "is_valid_length": False,
            "is_suspicious": False,
            "country": "Error",
            "region_code": "Error",
            "carrier": "Error",
            "international": "Error",
            "e164": "Error",
            "timezone": "Error",
            "actual_length": "Error",
            "expected_length": "Error",
            "length_message": "Error parsing number",
            "error": str(e)
        }

# Main input section
st.header("Single Number Validation")

col1, col2 = st.columns([3, 1])

with col1:
    phone_input = st.text_input(
        "Enter a phone number (with country code):",
        value="61872252566",
        help="Enter the number with country code. The '+' sign is optional.",
        placeholder="e.g., +1234567890 or 1234567890"
    )

with col2:
    st.write("")  # Spacing
    st.write("")  # Spacing
    validate_button = st.button("🔍 Validate", type="primary", use_container_width=True)

if phone_input and validate_button:
    st.markdown("---")
    checkphone(phone_input)

# Batch processing section
st.markdown("---")
st.header("Batch Processing")

tab1, tab2 = st.tabs(["📁 Upload File", "📝 Paste Numbers"])

with tab1:
    st.markdown("Upload a CSV or Excel file with phone numbers")
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'], label_visibility="collapsed")
    
    if uploaded_file:
        # Read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        column_name = st.selectbox("Select the column with phone numbers:", df.columns)
        
        if st.button("🚀 Process File", type="primary"):
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, phone in enumerate(df[column_name]):
                status_text.text(f"Processing {idx + 1}/{len(df)}...")
                result = checkphone(str(phone), display=False)  # No display during batch
                results.append(result)
                progress_bar.progress((idx + 1) / len(df))
            
            status_text.success(f"✅ Processed {len(results)} numbers!")
            progress_bar.empty()
            
            # Display results
            results_df = pd.DataFrame(results)
            st.dataframe(results_df, use_container_width=True)
            
            # Summary stats
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total Numbers", len(results_df))
            with col2:
                st.metric("Valid Format", results_df['is_valid'].sum())
            with col3:
                valid_length_count = results_df[results_df['is_valid_length'] == True].shape[0]
                st.metric("Valid Length", valid_length_count)
            with col4:
                suspicious_count = results_df['is_suspicious'].sum()
                st.metric("Suspicious", suspicious_count)
            with col5:
                invalid_count = (~results_df['is_valid']).sum()
                st.metric("Invalid", invalid_count)
            
            # Download button
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="phone_validation_results.csv",
                mime="text/csv"
            )

with tab2:
    st.markdown("Enter phone numbers (one per line)")
    bulk_input = st.text_area(
        "Phone numbers:",
        height=200,
        placeholder="61872252566\n+1234567890\n+447123456789",
        label_visibility="collapsed"
    )
    
    if st.button("🚀 Process Numbers", type="primary"):
        if bulk_input.strip():
            phone_numbers = [line.strip() for line in bulk_input.split('\n') if line.strip()]
            
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, phone in enumerate(phone_numbers):
                status_text.text(f"Processing {idx + 1}/{len(phone_numbers)}...")
                result = checkphone(phone, display=False)  # No display during batch
                results.append(result)
                progress_bar.progress((idx + 1) / len(phone_numbers))
            
            status_text.success(f"✅ Processed {len(results)} numbers!")
            progress_bar.empty()
            
            # Display results
            results_df = pd.DataFrame(results)
            st.dataframe(results_df, use_container_width=True)
            
            # Summary stats
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total Numbers", len(results_df))
            with col2:
                st.metric("Valid Format", results_df['is_valid'].sum())
            with col3:
                valid_length_count = results_df[results_df['is_valid_length'] == True].shape[0]
                st.metric("Valid Length", valid_length_count)
            with col4:
                suspicious_count = results_df['is_suspicious'].sum()
                st.metric("Suspicious", suspicious_count)
            with col5:
                invalid_count = (~results_df['is_valid']).sum()
                st.metric("Invalid", invalid_count)
            
            # Download button
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="phone_validation_results.csv",
                mime="text/csv"
            )
        else:
            st.warning("Please enter at least one phone number")

# Footer with info
st.markdown("---")
st.markdown("""
**Tips:**
- Country codes are required (e.g., +1 for USA, +44 for UK, +61 for Australia)
- The '+' sign is optional - it will be added automatically
- Batch process multiple numbers by uploading a CSV or Excel file
- **NEW:** Numbers are validated against country-specific length requirements
- **NEW:** Suspicious numbers (last 5 digits identical) are flagged
""")
