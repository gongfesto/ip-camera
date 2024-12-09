import streamlit as st
import cv2
import time
import numpy as np
import os

@st.cache_data
def list_available_cameras(max_cameras=10):
    """
    Lists available camera indices.

    Args:
        max_cameras (int): Maximum number of camera indices to check.

    Returns:
        list: List of available camera indices.
    """
    available_cameras = []
    for index in range(max_cameras):
        # For Windows, use CAP_DSHOW to prevent warnings
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW if os.name == 'nt' else 0)
        if cap is not None and cap.isOpened():
            available_cameras.append(index)
            cap.release()
    return available_cameras

def main():
    st.title("Laptop Webcam as IP Camera")

    # Button to refresh camera list
    if 'cameras' not in st.session_state:
        st.session_state.cameras = []

    refresh = st.button("Refresh Cameras")

    if refresh:
        # Clear the cached camera list by invalidating the cache
        list_available_cameras.clear()
        st.session_state.cameras = []

    # If cameras are not cached yet or have been refreshed
    if not st.session_state.cameras:
        with st.spinner('Listing available cameras...'):
            cameras = list_available_cameras()
            st.session_state.cameras = cameras
        st.success('Camera listing completed!')
    else:
        cameras = st.session_state.cameras

    if not cameras:
        st.error("No cameras found. Please connect a camera and click 'Refresh Cameras'.", icon="🚨")
        return

    # Dropdown to select camera
    camera_options = {f"Camera {cam}": cam for cam in cameras}
    selected_camera_label = st.selectbox("Select Camera", list(camera_options.keys()))
    selected_camera_index = camera_options[selected_camera_label]

    # Checkbox to run the camera
    run = st.checkbox('Run Camera')

    FRAME_WINDOW = st.empty()

    if run:
        # Initialize the selected camera
        camera = cv2.VideoCapture(selected_camera_index, cv2.CAP_DSHOW if os.name == 'nt' else 0)

        if not camera.isOpened():
            st.error(f"Unable to access {selected_camera_label}", icon="🚨")
            return

        # Display camera properties (optional)
        width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = camera.get(cv2.CAP_PROP_FPS)

        st.write(f"**Camera Properties:**")
        st.write(f"- Resolution: {int(width)} x {int(height)}")
        st.write(f"- FPS: {fps if fps > 0 else 'Not Available'}")

        while run:
            ret, frame = camera.read()
            if not ret:
                st.error("Unable to access the webcam", icon="🚨")
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)
            time.sleep(0.03)

        camera.release()
    else:
        # Release the camera if not running
        pass

if __name__ == "__main__":
    main()
