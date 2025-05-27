import streamlit as st # type: ignore
from PIL import Image # type: ignore
import openai # type: ignore
import io
import base64
from dotenv import load_dotenv # type: ignore
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("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")

# ROI Calculation Function
def calculate_roi(panel_watt, panel_count, cost_per_panel, electricity_rate, sun_hours_per_day=4.5):
    total_watt = panel_watt * panel_count
    annual_output_kwh = total_watt * sun_hours_per_day * 365 / 1000
    annual_savings = annual_output_kwh * electricity_rate
    total_cost = panel_count * cost_per_panel
    roi_years = round(total_cost / annual_savings, 2)
    return total_cost, annual_savings, roi_years

# Load image
image_path = r"c:\Users\itzra\OneDrive\Pictures\Screenshots\rooftop.png"
image = Image.open(image_path)

# UI
st.title("☀️ Solar Rooftop Analysis AI Tool")
st.markdown("Analyze a rooftop satellite image to estimate solar panel installation potential and ROI.")
st.image(image, caption="Sample Rooftop Image", use_container_width=True)

# Analyze Button
if st.button("🔍 Analyze Rooftop"):
    with st.spinner("Analyzing with GPT-4 Vision..."):

        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Prompt for GPT-4 Vision
        vision_prompt = (
            "Analyze this rooftop image and provide:\n"
            "1. Usable rooftop area (in m²)\n"
            "2. Recommended number and type of solar panels (with wattage)\n"
            "3. Estimated installation cost and ROI (in years)\n"
            "4. Notes on shading or obstacles"
        )

        try:
            # GPT-4o API call
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": vision_prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
                        ]
                    }
                ],
                max_tokens=800,
            )

            result = response["choices"][1]["message"]["content"]

            st.subheader("📊 AI Analysis Result")
            st.markdown(result)

        except openai.error.RateLimitError:
            st.error("🚫 Rate limit exceeded or quota reached. Please check your OpenAI billing and try again later.")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

# ROI Calculator (Manual Inputs)
st.subheader("🧮 ROI Calculator (Manual Entry)")
with st.form("roi_form"):
    panel_watt = st.number_input("Panel Wattage (W)", value=540)
    panel_count = st.number_input("Number of Panels", value=10)
    cost_per_panel = st.number_input("Cost per Panel (₹)", value=22000)
    electricity_rate = st.number_input("Electricity Rate (₹/kWh)", value=8.5)
    submitted = st.form_submit_button("Calculate ROI")

    if submitted:
        total_cost, savings, roi = calculate_roi(panel_watt, panel_count, cost_per_panel, electricity_rate)
        st.success(f"💰 Total Installation Cost: ₹{total_cost}")
        st.success(f"⚡ Annual Electricity Savings: ₹{round(savings, 2)}")
        st.success(f"📈 Estimated ROI: {roi} years")
