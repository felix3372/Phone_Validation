import streamlit as st
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import pandas as pd
import sys
from pathlib import Path
import pycountry
from io import BytesIO

# Add utils to path
sys.path.append(str(Path(__file__).parent))
from utils.phone_length_validator import validate_phone_length

# Page configuration
st.set_page_config(
    page_title="Inspectra | Phone Validator",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Inspectra CSS ----
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }
    .inspectra-hero {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 1.2rem 2rem 1rem 2rem;
        border-radius: 20px;
        margin-top: 1rem;
        margin-bottom: 1.3rem;
        box-shadow: 0 8px 22px rgba(0,0,0,0.08);
        display: flex;
        justify-content: center;
        animation: fadeInHero 1.2s;
    }
    @keyframes fadeInHero {
        from { opacity: 0; transform: translateY(-32px);}
        to   { opacity: 1; transform: translateY(0);}
    }
    .inspectra-inline {
        display: inline-flex;
        align-items: center;
        gap: 1.3rem;
        white-space: nowrap;
    }
    .inspectra-title {
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        color: #fff;
        letter-spacing: -1.5px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    .inspectra-divider {
        font-weight: 400;
        color: #4a0066;
        opacity: 0.35;
    }
    .inspectra-tagline {
        font-size: 1.08rem;
        font-weight: 500;
        margin: 0;
        color: #f3e3ff;
        opacity: 0.94;
        position: relative;
        top: 2px;
        letter-spacing: 0.5px;
    }
    .section {
        background: #faf6fd;
        border-radius: 1.2rem;
        padding: 0.8rem 1.6rem 0.5rem 1.6rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 1px 9px 0 rgba(102,126,234,0.10);
        border-left: 5px solid #764ba2;
        animation: fadeInSection 0.85s;
    }
    @keyframes fadeInSection {
        from { opacity: 0; transform: translateY(36px);}
        to   { opacity: 1; transform: translateY(0);}
    }
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #764ba2;
        margin-bottom: 0rem;
        margin-top: 0;
        letter-spacing: -1px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .metric-card {
        background: #faf6fd;
        border-radius: 1.2rem;
        padding: 1.15rem 1.6rem 1.05rem 1.6rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 1px 9px 0 rgba(102,126,234,0.10);
        border-left: 5px solid #667eea;
        text-align: center;
        font-weight: 600;
        color: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

# ---- Hero ----
st.markdown("""
<div class="inspectra-hero">
  <div class="inspectra-inline">
    <span class="inspectra-title">Inspectra</span>
    <span class="inspectra-divider">|</span>
    <span class="inspectra-tagline">Phone Number Validator</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ---- Intro section ----
st.markdown("""
<div class="section">
  <div class="section-title">📱 What is this?</div>
  Validate phone numbers with country-specific length requirements, carrier detection, and suspicious number flagging — consistent with Inspectra's QA automation UX.
</div>
""", unsafe_allow_html=True)

# ---------- Core Functions ----------
def checkphone(phone_input, display=True):
    """Validate and extract information from a phone number"""
    if not phone_input.startswith("+"):
        phone_input = "+" + phone_input.strip()
    
    def check_suspicious(phone_number):
        """Check if last 5 digits are all the same"""
        clean_number = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        if len(clean_number) >= 5:
            last_5 = clean_number[-5:]
            if len(set(last_5)) == 1:
                return True
        return False
    
    try:
        parsed_number = phonenumbers.parse(phone_input, None)
        is_valid = phonenumbers.is_valid_number(parsed_number)
        region_code = phonenumbers.region_code_for_number(parsed_number)
        
        geo_description = geocoder.description_for_number(parsed_number, "en")
        try:
            country_obj = pycountry.countries.get(alpha_2=region_code)
            country = country_obj.name if country_obj else geo_description
        except:
            country = geo_description
            
        sim_carrier = carrier.name_for_number(parsed_number, "en")
        country_code = parsed_number.country_code
        
        timezones = timezone.time_zones_for_number(parsed_number)
        tz_str = ", ".join(timezones) if timezones else "Unknown"
        
        international_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        e164_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        
        length_validation = validate_phone_length(e164_format, region_code)
        is_suspicious = check_suspicious(e164_format)
        
        if display:
            col_status1, col_status2 = st.columns(2)
            
            with col_status1:
                if is_valid:
                    st.success("✅ Valid phone number")
                else:
                    st.error("❌ Invalid phone number")
            
            with col_status2:
                if length_validation['is_valid_length'] is True:
                    st.success(f"✅ {length_validation['message']}")
                elif length_validation['is_valid_length'] is False:
                    st.error(f"❌ {length_validation['message']}")
                else:
                    st.info(f"ℹ️ {length_validation['message']}")
            
            if is_suspicious:
                st.warning("⚠️ Suspicious: Last 5 digits are identical")
            
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

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Settings")
    show_carrier = st.checkbox("Show Carrier Information", value=True)
    show_timezone = st.checkbox("Show Timezone", value=True)
    flag_suspicious = st.checkbox("Flag Suspicious Numbers", value=True)
    
    st.divider()
    st.header("💡 About Validation")
    st.markdown("""
    **Phone Number Validation:**
    - Format validation using international standards
    - Country-specific length requirements
    - Suspicious number detection
    - 84+ countries supported
    
    **Validation Checks:**
    - Format correctness
    - Length validation
    - Last 5 digits pattern
    - Country code verification
    
    **Suspicious Numbers:**
    - Last 5 digits identical (e.g., 00000, 11111)
    - Commonly used for testing/fake numbers
    """)

# ---------- Main Content ----------
tab1, tab2, tab3 = st.tabs(["📱 Single Validation", "📄 Batch Processing", "ℹ️ Help"])

with tab1:
    st.subheader("Single Number Validation")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        phone_input = st.text_input(
            "Enter a phone number (with country code):",
            value="",
            help="Enter the number with country code. The '+' sign is optional.",
            placeholder="e.g., +1234567890 or 61872252566"
        )
    
    with col2:
        st.write("")
        st.write("")
        validate_button = st.button("🔍 Validate", type="primary", width="stretch")
    
    if phone_input and validate_button:
        st.markdown("---")
        checkphone(phone_input)

with tab2:
    st.subheader("Batch Phone Number Validation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        batch_input = st.text_area(
            "Enter multiple phone numbers (one per line):",
            height=300,
            placeholder="Example:\n+61872252566\n+12025551234\n+441234567890\n+919876543210",
            help="Enter one phone number per line"
        )
        
        if st.button("🚀 Validate Numbers", type="primary", width="stretch"):
            if batch_input.strip():
                phone_numbers = [line.strip() for line in batch_input.split('\n') if line.strip()]
                
                results = []
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for idx, phone in enumerate(phone_numbers):
                    status_text.text(f"Processing {idx + 1}/{len(phone_numbers)}...")
                    result = checkphone(phone, display=False)
                    results.append(result)
                    progress_bar.progress((idx + 1) / len(phone_numbers))
                
                status_text.success(f"✅ Processed {len(results)} numbers!")
                progress_bar.empty()
                
                df = pd.DataFrame(results)
                st.session_state['batch_results'] = df
            else:
                st.warning("⚠️ Please enter at least one phone number.")
    
    with col2:
        if 'batch_results' in st.session_state:
            results_df = st.session_state['batch_results']
            
            st.markdown(f'<div class="metric-card">✅ Validated {len(results_df)} phone numbers successfully!</div>', 
                       unsafe_allow_html=True)
            
            st.dataframe(results_df, width="stretch", height=300)
            
            # Summary stats
            col_a, col_b, col_c, col_d, col_e = st.columns(5)
            with col_a:
                st.metric("Total", len(results_df))
            with col_b:
                st.metric("Valid Format", results_df['is_valid'].sum())
            with col_c:
                valid_length_count = results_df[results_df['is_valid_length'] == True].shape[0]
                st.metric("Valid Length", valid_length_count)
            with col_d:
                suspicious_count = results_df['is_suspicious'].sum()
                st.metric("Suspicious", suspicious_count)
            with col_e:
                invalid_count = (~results_df['is_valid']).sum()
                st.metric("Invalid", invalid_count)
            
            # Export buttons
            st.markdown("---")
            col_x, col_y, col_z = st.columns(3)
            
            with col_x:
                csv_data = results_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name="phone_validation_results.csv",
                    mime="text/csv",
                    width="stretch"
                )
            
            with col_y:
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    results_df.to_excel(writer, index=False, sheet_name='Phone Validation')
                output.seek(0)
                st.download_button(
                    label="📥 Download Excel",
                    data=output,
                    file_name="phone_validation_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    width="stretch"
                )
            
            with col_z:
                json_data = results_df.to_json(orient='records', indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name="phone_validation_results.json",
                    mime="application/json",
                    width="stretch"
                )

with tab3:
    st.subheader("ℹ️ How to Use This App")
    st.markdown("""
    ### 🎯 Quick Start Guide
    
    **1. Single Validation:**
    - Enter a phone number with country code
    - Click "Validate" to see detailed information
    - View format, length, carrier, and timezone
    
    **2. Batch Processing:**
    - Paste multiple phone numbers (one per line)
    - Click "Validate Numbers" to process all
    - View results in table format
    - Download as CSV, Excel, or JSON
    
    **3. Configure Settings (Sidebar):**
    - **Show Carrier**: Display mobile carrier info
    - **Show Timezone**: Display timezone information
    - **Flag Suspicious**: Highlight suspicious patterns
    
    ### 📋 Validation Features
    
    **Format Validation:**
    - Checks international phone number format
    - Verifies country code validity
    - Validates number structure
    
    **Length Validation:**
    - Country-specific length requirements
    - 84+ countries supported
    - Handles variable-length countries
    
    **Suspicious Detection:**
    - Flags numbers with last 5 identical digits
    - Examples: 00000, 11111, 22222, etc.
    - Useful for identifying test/fake numbers
    
    ### 🌍 Supported Countries
    
    **Coverage includes:**
    - All major countries worldwide
    - Europe: 38 countries
    - Africa: 14 countries
    - Asia: 15 countries
    - Americas: 8 countries
    - Middle East: 7 countries
    - Oceania: 2 countries
    
    ### 💡 Tips
    
    - Country codes are required (e.g., +1 for USA, +44 for UK)
    - The '+' sign is optional - it will be added automatically
    - Empty lines are automatically skipped
    - Leading/trailing whitespace is trimmed
    - Export formats preserve all validation data
    
    ### ⚠️ Important Notes
    
    - Format can be valid while length is invalid
    - Some countries accept variable lengths
    - Suspicious flag is based on pattern detection
    - Carrier information may not always be available
    """)

# ---- Footer ----
st.divider()
st.markdown("""
<div style='text-align: center; font-size: 14px; color: #6c757d; padding: .5rem 0 1rem'>
    2025 Inspectra. All rights reserved. <br>
    Inspectra • Phone Number Validator.
</div>
""", unsafe_allow_html=True)
