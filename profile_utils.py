import pandas as pd
import os
import streamlit as st

DATA_PATH = "data/profiles.csv"

def save_profile(username, name, email, phone, degree, institute, graduation_year, projects, skills, certificates, linkedin, github):
    os.makedirs("data", exist_ok=True)
    profile = {
        "Username": username,
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Degree": degree,
        "Institute": institute,
        "Graduation Year": graduation_year,
        "Projects": projects,
        "Skills": skills,
        "Certificates": certificates,
        "LinkedIn": linkedin,
        "GitHub": github
    }

    df = pd.DataFrame([profile])
    if os.path.exists(DATA_PATH):
        df.to_csv(DATA_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(DATA_PATH, index=False)

def load_profiles(username=None):
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        if username:
            return df[df["Username"] == username]
        return df
    else:
        return pd.DataFrame()

def display_profile(profile):
    st.markdown(f"### 👤 {profile['Full Name']}")
    st.markdown(f"- **Email**: {profile['Email']}")
    st.markdown(f"- **Phone**: {profile['Phone']}")
    st.markdown(f"- **Degree**: {profile['Degree']}")
    st.markdown(f"- **Institute**: {profile['Institute']}")
    st.markdown(f"- **Graduation Year**: {profile['Graduation Year']}")
    st.markdown(f"#### 💼 Projects")
    st.markdown(f"{profile['Projects'].replace(';', '<br>')}", unsafe_allow_html=True)
    st.markdown(f"#### 🛠 Skills")
    st.markdown(f"{', '.join([s.strip() for s in profile['Skills'].split(',')])}")
    st.markdown(f"#### 📜 Certificates")
    st.markdown(f"{profile['Certificates'].replace(';', '<br>')}", unsafe_allow_html=True)
    if profile['LinkedIn']:
        st.markdown(f"🔗[LinkedIn]({profile['LinkedIn']})")
    if profile['GitHub']:
        st.markdown(f"🐙[GitHub]({profile['GitHub']})")
