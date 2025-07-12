import json
import os

import streamlit as st

SETTINGS_FILE = "uvi_settings.json"

def save_uvi_settings():
    settings = {
        "uvi_scale": st.session_state.uvi_scale,
        "uvi_scale_upper": st.session_state.uvi_scale_upper
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def load_uvi_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
        st.session_state.uvi_scale = settings.get("uvi_scale", 1.0)
        st.session_state.uvi_scale_upper = settings.get("uvi_scale_upper", 0.0)
    else:
        st.session_state.uvi_scale = 1.0
        st.session_state.uvi_scale_upper = 0.0