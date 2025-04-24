import streamlit as st
from auth import signup_user, login_user, check_user_exists
from profile_utils import save_profile, load_profiles, display_profile
import os

st.set_page_config(page_title="Student Profile App", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Login / Signup
def login_page():
    st.image("assets/profile_banner.jpg", use_column_width=True)
    choice = st.radio("Login or Sign Up", ["Login", "Sign Up"])
    
    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        username = st.text_input("Choose Username")
        password = st.text_input("Choose Password", type="password")
        if st.button("Sign Up"):
            if check_user_exists(username):
                st.warning("Username already exists!")
            else:
                signup_user(username, password)
                st.success("Signup successful! Please login now.")

# Main App
def main_app():
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    menu = st.sidebar.selectbox("Navigation", ["Create Profile", "View Profile", "Logout"])

    if menu == "Create Profile":
        st.header("📘 Create Your Profile")
        with st.form("profile_form", clear_on_submit=True):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            degree = st.selectbox("Degree", ["B.Tech", "B.Sc", "B.Com", "M.Tech", "M.Sc", "MBA", "Other"])
            institute = st.text_input("Institution")
            graduation_year = st.number_input("Graduation Year", min_value=2000, max_value=2100, value=2025)
            projects = st.text_area("Projects (Separate by semicolon)")
            skills = st.text_area("Skills (Separate by comma)")
            certificates = st.text_area("Certificates (Separate by semicolon)")
            linkedin = st.text_input("LinkedIn URL")
            github = st.text_input("GitHub URL")
            submitted = st.form_submit_button("Save Profile")

            if submitted:
                save_profile(st.session_state.username, name, email, phone, degree, institute, graduation_year, projects, skills, certificates, linkedin, github)
                st.success("✅ Profile saved!")

    elif menu == "View Profile":
        st.header("📄 Your Profile")
        df = load_profiles(st.session_state.username)
        if df.empty:
            st.info("No profile found. Create one first.")
        else:
            display_profile(df.iloc[-1])

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Logged out successfully.")
        st.rerun()

if st.session_state.logged_in:
    main_app()
else:
    login_page()
