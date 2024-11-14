import streamlit as st

# Function to convert image size to MB based on the selected unit
def convert_image_size(image_size, image_size_unit):
    if image_size_unit == "KB":
        return image_size / 1024  # Convert KB to MB
    elif image_size_unit == "GB":
        return image_size * 1024  # Convert GB to MB
    elif image_size_unit == "TB":
        return image_size * 1024 * 1024  # Convert TB to MB
    else:
        return image_size  # If MB, no conversion needed

# Function to calculate the total bandwidth required and rejected bags
def calculate_bandwidth(image_size, throughput, rejection_rate, output_unit, image_size_unit, throughput_unit):
    # Convert image size to MB based on the selected unit
    image_size_in_mb = convert_image_size(image_size, image_size_unit)

    # Convert throughput based on selected unit
    if throughput_unit == "per hour":
        throughput_per_month = throughput * 24 * 30  # Convert per hour to per month
        time_unit = "per hour"
    elif throughput_unit == "per year":
        throughput_per_month = throughput / 12  # Convert per year to per month
        time_unit = "per year"
    else:
        throughput_per_month = throughput  # Already per month
        time_unit = "per month"

    # Total data per month (MB)
    total_data_per_month = throughput_per_month * image_size_in_mb  # in MB

    # Convert total data to megabits (Mb)
    total_data_in_mb = total_data_per_month * 8  # 1 MB = 8 Megabits

    # Convert to total seconds in a month (30 days)
    seconds_in_month = 30 * 24 * 60 * 60  # 30 days * 24 hours * 60 minutes * 60 seconds

    # Calculate bandwidth required per second in Mbps
    bandwidth_mbps = total_data_in_mb / seconds_in_month

    # Convert to the selected unit
    if output_unit == "Kbps":
        bandwidth = bandwidth_mbps * 1000  # 1 Mbps = 1000 Kbps
    elif output_unit == "Gbps":
        bandwidth = bandwidth_mbps / 1000  # 1 Gbps = 1000 Mbps
    else:
        bandwidth = bandwidth_mbps  # Mbps

    # Calculate rejected bags based on the throughput unit
    if throughput_unit == "per hour":
        rejected_bags = throughput * 24 * 30 * (rejection_rate / 100)  # Convert to per month
    elif throughput_unit == "per year":
        rejected_bags = throughput * (rejection_rate / 100)  # Keep it as per year
    else:
        rejected_bags = throughput * (rejection_rate / 100)  # Already per month

    return bandwidth, rejected_bags, time_unit

# Streamlit UI
# Set background color and animation for a smooth effect
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');  /* Adding Roboto font */
    
    .stApp {
        background: linear-gradient(to bottom right, black, #3E54AC);  /* Gradient from black to blue */
        padding: 0px;  /* Remove default padding */
        margin: 0px;   /* Remove default margin */
        width: 100vw;  /* Make the app take the full width of the page */
        height: 100vh;  /* Make the app take the full height of the page */
        position: relative;  /* Allow positioning inside the container */
    }
    h1 {
        text-align: center;
        color: #91D8E4;  /* Light blue color */
        font-weight: bold;
        font-size: 36px;  /* Slightly smaller font size for app title */
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4);
        margin-top: 100px;  /* Increased space above the title */
    }
    .company-name {
        position: absolute;
        top: 30px;
        left: 30px;
        font-family: 'Roboto', sans-serif;  /* Apply the Roboto font */
        font-size: 40px;
        font-weight: bold;
        margin-top: 20px;  /* Add some margin to avoid overlap */
    }
    .company-name .Smiths {
        color: #B9F3FC;  /* White color for "smith" to contrast against dark background */
    }
    .company-name .Detection {
        color: #ECF9FF;  /* Light blue color for "detection" */
    }
    .stTextInput input, .stNumberInput input {
        background-color: #fff;
        border: none;
        border-radius: 10px;
        padding: 12px;
        font-size: 18px;  /* Larger font size for inputs */
        width: 250px;
        color: #333;  /* Dark text for better readability */
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label, .stMultiselect label {
        color: #FFFFFF;  /* White color for input headings */
        font-size: 20px;  /* Increased font size for input labels */
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stSelectbox, .stMultiselect {
        background-color: transparent;  /* Transparent background to match page background */
        border: none;  /* Remove borders */
        border-radius: 10px;
        padding: 12px;
        font-size: 18px;  /* Larger font size for dropdowns */
        width: 150px;  /* Set width to match image size input box */
        color: white;  /* White text for better visibility */
    }
    .stSelectbox div, .stMultiselect div {
        background-color: transparent;  /* Transparent dropdown options background */
        color: white;  /* White text for dropdown options */
    }
    .stButton button {
        background-color: #BAD7E9;  /* New button color (tomato red) */
        color: white;
        font-size: 18px;
        border-radius: 12px;
        padding: 15px;
        width: 100%;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #FCFFE7;  /* Darker tomato color when hovered */
    }
    .stNumberInput input {
        padding-right: 40px;  /* Add padding to the right so the + and - buttons don't overlap */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Company name at the top left corner with increased spacing
st.markdown('<div class="company-name"><span class="Smiths">Smiths</span><span class="Detection"> Detection</span></div>', unsafe_allow_html=True)

# Heading with improved styling
st.markdown("<h1>Bandwidth Calculator</h1>", unsafe_allow_html=True)

# Layout for Image Size and Throughput input fields (with appropriate input field sizes)
col1, col2 = st.columns([3, 1])  # Adjusted column width to ensure both elements are on the same line
with col1:
    image_size = st.number_input("Enter Image Size (in MB)", min_value=1)  # Adjusted label
with col2:
    image_size_unit = st.selectbox("Select Unit", ["KB", "MB", "GB", "TB"])  # units dropdown

# Layout for Throughput input with expanded dropdown for time unit
col3, col4 = st.columns([3, 2])  # Adjusted column width to ensure alignment
with col3:
    throughput = st.number_input("Enter Throughput (Number of Bags)", min_value=1)  # Adjusted label
with col4:
    throughput_unit = st.selectbox("Select Throughput Time Unit", ["per month", "per hour", "per year"], index=0)

# Rejection rate input with matching font size and layout
st.markdown("<h3 style='color: white; font-size: 20px;'>Enter Rejection Rate (%)</h3>", unsafe_allow_html=True)  # Matching font size
rejection_rate = st.number_input("", min_value=0, max_value=100, key="rejection_rate")  # No label here to improve visual flow

# Dropdown for selecting output unit (Mbps, Kbps, or Gbps)
output_unit = st.selectbox("Select Output Unit", ["Mbps", "Kbps", "Gbps"], index=0)

# Calculate button with modern style
# Calculate button with modern style
if st.button("🔍 Calculate", use_container_width=True):
    # Calculate bandwidth and rejected bags
    bandwidth, rejected_bags, time_unit = calculate_bandwidth(image_size, throughput, rejection_rate, output_unit, image_size_unit, throughput_unit)

    # Display results with updated styles
    st.markdown(f"<h3 style='color: white;'>Total Bandwidth Required: {bandwidth:.2f} {output_unit}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: white;'>Number of Rejected Bags: {rejected_bags:.2f} (over {throughput} {time_unit})</h3>", unsafe_allow_html=True)
