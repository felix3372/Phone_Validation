import streamlit as st
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Phone Number Validator | Felix",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
    }
    
    /* Content card */
    .block-container {
        background: white;
        border-radius: 24px;
        padding: 3rem 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        margin-bottom: 3rem;
        padding-bottom: 2rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: #6b7280;
        font-weight: 400;
    }
    
    .creator-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 1rem 1.5rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.05rem;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Card styling */
    .info-card {
        background: #f9fafb;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    
    /* Success/Error boxes */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border: none;
    }
    
    .stError {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border: none;
    }
    
    /* Warning box */
    .warning-box {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        border-radius: 12px;
        padding: 1.25rem;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(251, 191, 36, 0.3);
    }
    
    /* Metrics styling */
    .stMetric {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        border-color: #667eea;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.1);
    }
    
    .stMetric label {
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: #f9fafb;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        background: transparent;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 2rem;
        background: #f9fafb;
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        background: #f3f4f6;
        border-color: #764ba2;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    /* Section headers */
    h2 {
        color: #1f2937;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 2rem;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e5e7eb, transparent);
        margin: 2rem 0;
    }
    
    /* Text area */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 1rem;
        font-size: 1rem;
        font-family: 'Monaco', monospace;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        color: white;
        border: none;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
    }
    
    /* Tips section */
    .tips-section {
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        border-left: 4px solid #667eea;
    }
    
    .tips-section h3 {
        color: #667eea;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .tips-section ul {
        list-style: none;
        padding-left: 0;
    }
    
    .tips-section li {
        padding: 0.5rem 0;
        color: #4b5563;
        position: relative;
        padding-left: 2rem;
    }
    
    .tips-section li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #667eea;
        font-weight: 700;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <div class="main-title">📱 Phone Number Validator</div>
    <div class="main-subtitle">Validate and get detailed information about phone numbers from around the world</div>
    <div class="creator-badge">✨ Made by Felix</div>
</div>
""", unsafe_allow_html=True)

def checkphone(phone_input, display=True):
    """Validate and extract information from a phone number"""
    # Auto-add "+" if missing and input looks like an international number
    if not phone_input.startswith("+"):
        phone_input = "+" + phone_input.strip()
    
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_input, None)
        
        # Validate the phone number
        is_valid = phonenumbers.is_valid_number(parsed_number)
        
        # Get detailed information
        country = geocoder.description_for_number(parsed_number, "en")
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
        
        # CHECK FOR REPEATED DIGIT PATTERN
        digits = ''.join(filter(str.isdigit, phone_input))
        suspicious_patterns = ['11111', '22222', '33333', '44444', '55555', 
                              '66666', '77777', '88888', '99999', '00000']
        
        pattern_warning = None
        if len(digits) >= 5:
            last_5 = digits[-5:]
            if last_5 in suspicious_patterns:
                pattern_warning = f"Last 5 digits are same ({last_5}) - potentially fake/test number"
        
        # Only display results if requested
        if display:
            # Show pattern warning
            if pattern_warning:
                st.markdown(
                    f"""
                    <div class="warning-box">
                        <strong style="font-size: 1.1rem;">⚠️ Suspicious Pattern Detected</strong><br>
                        <span style="margin-top: 0.5rem; display: block;">{pattern_warning}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Validation status
            if is_valid:
                st.success("✅ Valid phone number")
            else:
                st.error("❌ Invalid phone number")
            
            # Information display in cards
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="info-card">
                    <div style="color: #6b7280; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">🌍 Location</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #1f2937; margin-bottom: 0.75rem;">{country if country else 'Unknown'}</div>
                    <div style="color: #6b7280; font-size: 0.9rem;">Country Code: <strong style="color: #667eea;">+{country_code}</strong></div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="info-card">
                    <div style="color: #6b7280; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">📡 Network</div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #1f2937; margin-bottom: 0.75rem;">{sim_carrier if sim_carrier else 'Unknown'}</div>
                    <div style="color: #6b7280; font-size: 0.9rem;">Timezone: <strong style="color: #667eea;">{tz_str}</strong></div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="info-card">
                    <div style="color: #6b7280; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">📞 Formats</div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">{international_format}</div>
                    <div style="color: #6b7280; font-size: 0.9rem; font-family: 'Monaco', monospace;">{e164_format}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Return data for batch processing
        return {
            "original": phone_input,
            "is_valid": is_valid,
            "country": country if country else "Unknown",
            "carrier": sim_carrier if sim_carrier else "Unknown",
            "international": international_format,
            "e164": e164_format,
            "timezone": tz_str,
            "pattern_warning": pattern_warning if pattern_warning else ""
        }

    except phonenumbers.NumberParseException as e:
        if display:
            st.error(f"❌ Error parsing number: {e}")
        return {
            "original": phone_input,
            "is_valid": False,
            "country": "Error",
            "carrier": "Error",
            "international": "Error",
            "e164": "Error",
            "timezone": "Error",
            "pattern_warning": "",
            "error": str(e)
        }

# Main input section
st.markdown("<h2>🔍 Single Number Validation</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])

with col1:
    phone_input = st.text_input(
        "Enter a phone number (with country code):",
        value="",
        help="Enter the number with country code. The '+' sign is optional.",
        placeholder="e.g., +1234567890 or 61872252566",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
    validate_button = st.button("🔍 Validate", type="primary", use_container_width=True)

if phone_input and validate_button:
    st.markdown("---")
    checkphone(phone_input)

# Batch processing section
st.markdown("---")
st.markdown("<h2>📊 Batch Processing</h2>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📁 Upload File", "📝 Paste Numbers"])

with tab1:
    st.markdown("Upload a CSV or Excel file containing phone numbers for bulk validation")
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'], label_visibility="collapsed")
    
    if uploaded_file:
        # Read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        column_name = st.selectbox("Select the column with phone numbers:", df.columns)
        
        if st.button("🚀 Process File", type="primary", use_container_width=True):
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, phone in enumerate(df[column_name]):
                status_text.text(f"Processing {idx + 1}/{len(df)}...")
                result = checkphone(str(phone), display=False)
                results.append(result)
                progress_bar.progress((idx + 1) / len(df))
            
            status_text.success(f"✅ Processed {len(results)} numbers!")
            progress_bar.empty()
            
            # Display results
            results_df = pd.DataFrame(results)
            st.dataframe(results_df, use_container_width=True, height=400)
            
            # Summary stats
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Numbers", len(results_df))
            with col2:
                st.metric("Valid", results_df['is_valid'].sum())
            with col3:
                st.metric("Invalid", (~results_df['is_valid']).sum())
            with col4:
                suspicious_count = (results_df['pattern_warning'] != "").sum()
                st.metric("Suspicious", suspicious_count)
            
            # Download button
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="phone_validation_results.csv",
                mime="text/csv",
                use_container_width=True
            )

with tab2:
    st.markdown("Enter phone numbers, one per line, for quick batch validation")
    bulk_input = st.text_area(
        "Phone numbers:",
        height=200,
        placeholder="61872252566\n+1234567890\n+447123456789\n+919876543210",
        label_visibility="collapsed"
    )
    
    if st.button("🚀 Process Numbers", type="primary", use_container_width=True):
        if bulk_input.strip():
            phone_numbers = [line.strip() for line in bulk_input.split('\n') if line.strip()]
            
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
            
            # Display results
            results_df = pd.DataFrame(results)
            st.dataframe(results_df, use_container_width=True, height=400)
            
            # Summary stats
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Numbers", len(results_df))
            with col2:
                st.metric("Valid", results_df['is_valid'].sum())
            with col3:
                st.metric("Invalid", (~results_df['is_valid']).sum())
            with col4:
                suspicious_count = (results_df['pattern_warning'] != "").sum()
                st.metric("Suspicious", suspicious_count)
            
            # Download button
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="phone_validation_results.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.warning("⚠️ Please enter at least one phone number")

# Footer with tips
st.markdown("""
<div class="tips-section">
    <h3>💡 Tips & Guidelines</h3>
    <ul>
        <li>Country codes are required (e.g., +1 for USA, +44 for UK, +61 for Australia, +91 for India)</li>
        <li>The '+' sign is optional - it will be added automatically if missing</li>
        <li>Batch process multiple numbers by uploading a CSV/Excel file or pasting them directly</li>
        <li>Numbers ending in repeated digits (11111, 22222, etc.) are flagged as potentially fake/test numbers</li>
        <li>Supports international phone number formats from over 200 countries</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding-top: 2rem; border-top: 2px solid #f0f0f0; color: #6b7280;">
    <p style="margin-bottom: 0.5rem;">Built with ❤️ by <strong style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Felix</strong></p>
    <p style="font-size: 0.9rem;">Powered by Streamlit & phonenumbers library</p>
</div>
""", unsafe_allow_html=True)
