import streamlit as st
import pandas as pd
from PIL import Image
import os
import base64

# Function to convert image to base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Initialize session state for image index if not already present
if 'image_index' not in st.session_state:
    st.session_state['image_index'] = 0

# Function to go to the next image
def next_image():
    if st.session_state['image_index'] < len(data) - 1:
        st.session_state['image_index'] += 1

# Function to go to the previous image
def prev_image():
    if st.session_state['image_index'] > 0:
        st.session_state['image_index'] -= 1

# Load the data
data = pd.read_csv('data/prices.csv')

# Define the CSS to center the image
center_image_css = """
<style>
.centered-image {
    display: block;
    margin-left: auto;
    margin-right: auto;
}
</style>
"""
st.markdown(center_image_css, unsafe_allow_html=True)

# Initialize session state for responses if not already present
if 'responses' not in st.session_state:
    st.session_state['responses'] = []

todays_date = pd.Timestamp.now().strftime('%Y-%m-%d')
cobbler_name = st.text_input("Enter your first name", value="")

if cobbler_name:
    file_name = f"{cobbler_name}_responses_{todays_date}.csv"

    # Function to save responses
    def save_responses(responses):
        df = pd.DataFrame(responses, columns=['image', 'original_price', 'correct_price'])
        df.to_csv(file_name, index=False)

    # Add "Previous" and "Next" buttons
    col1, col2 = st.columns([1,6])
    with col1:
        if st.button("Previous"):
            prev_image()
    with col2:
        if st.button("Next"):
            next_image()

    # Select an image to display based on the current index
    image_index = st.session_state['image_index']
    image_path = os.path.join('data/images', data.iloc[image_index]['image'])
    price = data.iloc[image_index]['price']


    # Display the image and price
    image_base64 = get_image_base64(image_path)
    st.markdown(f'<div style="text-align: center;"><img src="data:image/png;base64,{image_base64}" width="300"/></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center;"><p>Price: £{price}</p></div>', unsafe_allow_html=True)

    # Ask the user if they agree with the price
    st.write("Fault: [insert fault here]")
    agree = st.radio("Do you agree with the price?", ("Yes", "No"))

    if agree == "Yes":
        if st.button("Submit"):
            st.session_state['responses'].append([data.iloc[image_index]['image'], price, price])
            save_responses(st.session_state['responses'])
            st.success("Response recorded.")
    else:
        new_price = st.number_input("Enter the correct price", min_value=0, value=price)
        if st.button("Submit"):
            st.session_state['responses'].append([data.iloc[image_index]['image'], price, new_price])
            save_responses(st.session_state['responses'])
            st.success("Response recorded.")

    # Display recorded responses
    if st.checkbox("Show recorded responses"):
        st.write(pd.DataFrame(st.session_state['responses'], columns=['image', 'original_price', 'correct_price']))
