import streamlit as st
import cv2
import time
import numpy as np

def main():
    st.title("Laptop Webcam as IP Camera")

    # Simple password protection
    # password = st.text_input("Enter Password", type="password")
    # if password != "ServoPressKit":
    #     st.error("Incorrect password")
        # return

    run = st.checkbox('Run Camera')
    
    FRAME_WINDOW = st.empty()
    
    camera = cv2.VideoCapture(0)
    
    while run:
        ret, frame = camera.read()
        if not ret:
            st.error("Unable to access the webcam", icon="🚨")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)
        time.sleep(0.03)
    
    camera.release()

if __name__ == "__main__":
    main()
