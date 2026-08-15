import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Widens Åkeri AB", 
    page_icon="🚛", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ڕێکخستنی دیزاین و فۆنت (Custom CSS)
custom_css = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Font & Card Styles */
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    .main-header {
        background-color: #fbd008;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 20px;
        color: #111;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# بەستنەوەی وێنەی ئایکۆنی ئەپ
IMAGE_URL = "https://raw.githubusercontent.com/Widens90/widens-app/main/Wedins%20Åkeri.jpeg"
app_icon_html = f"""
    <head>
        <link rel="apple-touch-icon" href="{IMAGE_URL}">
        <link rel="icon" type="image/jpeg" sizes="192x192" href="{IMAGE_URL}">
    </head>
"""
st.markdown(app_icon_html, unsafe_allow_html=True)

# فایلی زانیارییەکان
DATA_FILE = "drivers_data.csv"
USERS_FILE = "users_data.csv"

# فەرهەنگی وەرگێڕانی زمانەکان (Translations Dictionary)
TEXTS = {
    "SV": {
        "title": "🚛 Widens Åkeri AB",
        "welcome": "Välkommen",
        "logout": "Logga ut 👋",
        "login_tab": "🔒 Logga in",
        "signup_tab": "✍️ Skapa konto",
        "user_label": "Användarnamn",
        "pass_label": "Lösenord",
        "login_btn": "Logga in",
        "login_success": "Inloggningen lyckades!",
        "login_error": "Felaktigt användarnamn eller lösenord!",
        "nav_home": "📰 Hem",
        "nav_form": "➕ Formulär",
        "nav_doc": "📁 Dokument",
        "nav_emp": "🪪 Min anställning",
        "nav_tasks": "💼 Mina ärenden",
        "nav_edu": "🎓 Utbildningar",
        "nav_msg": "💬 Meddelande",
        "fullname": "Fullständigt namn",
        "phone": "Telefonnummer",
        "license": "Körkortstyp",
        "create_acc": "Skapa konto",
        "status_today": "Status idag",
        "avail_tomorrow": "Tillgänglighet imorgon",
        "save": "Spara uppgifter",
        "saved_msg": "Uppgifterna har sparats!",
        "assigned_route": "Nuvarande uppdrag",
        "overview": "📊 Översikt",
        "manage_users": "⚙️ Hantera förare",
        "assign_route": "✍️ Tilldela rutt"
    },
    "EN": {
        "title": "🚛 Widens Åkeri AB",
        "welcome": "Welcome",
        "logout": "Log out 👋",
        "login_tab": "🔒 Login",
        "signup_tab": "✍️ Sign up",
        "user_label": "Username",
        "pass_label": "Password",
        "login_btn": "Login",
        "login_success": "Login successful!",
        "login_error": "Invalid username or password!",
        "nav_home": "📰 Home",
        "nav_form": "➕ Forms",
        "nav_doc": "📁 Documents",
        "nav_emp": "🪪 My Employment",
        "nav_tasks": "💼 My Tasks",
        "nav_edu": "🎓 Training",
        "nav_msg": "💬 Messages",
        "fullname": "Full Name",
        "phone": "Phone Number",
        "license": "License Class",
        "create_acc": "Create Account",
        "status_today": "Status Today",
        "avail_tomorrow": "Availability Tomorrow",
        "save": "Save Details",
        "saved_msg": "Information saved!",
        "assigned_route": "Assigned Route",
        "overview": "📊 Overview",
        "manage_users": "⚙️ Manage Drivers",
        "assign_route": "✍️ Assign Route"
    }
}

# Load Data Functions
def load_driver_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, dtype=str).fillna("-")
        if "Telefon" not in df.columns: df["Telefon"] = "-"
        if "Körkort" not in df.columns: df["Körkort"] = "CE"
        return df
    else:
        df = pd.DataFrame({
            "Förare": ["Ahmed", "Karwan"],
            "Telefon": ["0701234567", "0709876543"],
            "Körkort": ["CE", "C"],
            "Status idag": ["I tjänst", "I tjänst"],
            "Tillgänglig imorgon?": ["🟢 Ja", "🔴 Nej"],
            "Fordon / Rutt": ["Scania 01 (Kalmar)", "Volvo 02 (Karlskrona)"]
        }, dtype=str)
        df.to_csv(DATA_FILE, index=False)
        return df

def load_users():
    if os.path.exists(USERS_FILE):
        df = pd.read_csv(USERS_FILE, dtype=str).fillna("-")
        if "phone" not in df.columns: df["phone"] = "-"
        if "license" not in df.columns: df["license"] = "CE"
        return df
    else:
        df = pd.DataFrame({
            "username": ["admin", "chauffor"],
            "password": ["123", "456"],
            "role": ["Transportledare", "Chaufför"],
            "driver_name": ["Admin", "Ahmed"],
            "phone": ["0700000000", "0701234567"],
            "license": ["CE", "CE"]
        }, dtype=str)
        df.to_csv(USERS_FILE, index=False)
        return df

def save_driver_data(df): df.astype(str).to_csv(DATA_FILE, index=False)
def save_users(df): df.astype(str).to_csv(USERS_FILE, index=False)

df_drivers = load_driver_data()
df_users = load_users()

# Session States Initialization
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False
if "user_role" not in st.session_state: st.session_state["user_role"] = None
if "username" not in st.session_state: st.session_state["username"] = ""
if "driver_name" not in st.session_state: st.session_state["driver_name"] = ""
if "lang" not in st.session_state: st.session_state["lang"] = "SV"

# --- TOP HEADER: Language Switcher ---
col_lang1, col_lang2 = st.columns([4, 1])
with col_lang2:
    selected_lang = st.selectbox("🌐 Språk / Language", ["🇸🇪 Svenska", "🇬🇧 English"], 
                                 index=0 if st.session_state["lang"] == "SV" else 1)
    st.session_state["lang"] = "SV" if "Svenska" in selected_lang else "EN"

t = TEXTS[st.session_state["lang"]]

def login_register_page():
    st.markdown(f"<div class='main-header'><h1>{t['title']}</h1></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs([t["login_tab"], t["signup_tab"]])
    
    with tab1:
        username = st.text_input(t["user_label"], key="login_user")
        password = st.text_input(t["pass_label"], type="password", key="login_pass")
        if st.button(t["login_btn"]):
            user_match = df_users[(df_users["username"].astype(str) == str(username)) & (df_users["password"].astype(str) == str(password))]
            if not user_match.empty:
                st.session_state["logged_in"] = True
                st.session_state["user_role"] = str(user_match.iloc[0]["role"])
                st.session_state["username"] = str(username)
                st.session_state["driver_name"] = str(user_match.iloc[0]["driver_name"])
                st.success(t["login_success"])
                st.rerun()
            else:
                st.error(t["login_error"])

    with tab2:
        new_name = st.text_input(t["fullname"])
        new_phone = st.text_input(t["phone"])
        new_license = st.selectbox(t["license"], ["CE", "C"])
        new_username = st.text_input(t["user_label"], key="reg_u")
        new_password = st.text_input(t["pass_label"], type="password", key="reg_p")
        
        if st.button(t["create_acc"]):
            if new_name and new_username and new_password:
                if str(new_username) in df_users["username"].astype(str).values:
                    st.error("Användarnamnet upptaget!")
                else:
                    new_u = pd.DataFrame([{"username": str(new_username), "password": str(new_password), "role": "Chaufför", "driver_name": str(new_name), "phone": str(new_phone), "license": str(new_license)}], dtype=str)
                    save_users(pd.concat([df_users, new_u], ignore_index=True))
                    
                    new_d = pd.DataFrame([{"Förare": str(new_name), "Telefon": str(new_phone), "Körkort": str(new_license), "Status idag": "Ledig", "Tillgänglig imorgon?": "🔴 Nej", "Fordon / Rutt": "Ej tilldelad"}], dtype=str)
                    save_driver_data(pd.concat([df_drivers, new_d], ignore_index=True))
                    st.success(t["login_success"])
            else:
                st.warning("Fyll i alla fält!")

if not st.session_state["logged_in"]:
    login_register_page()
else:
    # Sidebar Navigation like the image design
    with st.sidebar:
        st.image(IMAGE_URL, use_container_width=True)
        st.markdown(f"### 👤 {st.session_state['driver_name']}")
        st.caption(f"Role: {st.session_state['user_role']}")
        st.markdown("---")
        
        menu_choice = st.radio(
            "Meny",
            [t["nav_home"], t["nav_form"], t["nav_doc"], t["nav_emp"], t["nav_tasks"], t["nav_edu"], t["nav_msg"]],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button(t["logout"]):
            st.session_state["logged_in"] = False
            st.session_state["user_role"] = None
            st.rerun()

    # Main Area Content
    st.markdown(f"<div class='main-header'><h2>{menu_choice}</h2></div>", unsafe_allow_html=True)
    role = st.session_state["user_role"]

    if menu_choice == t["nav_home"]:
        if role == "Transportledare":
            tab1, tab2, tab3 = st.tabs([t["overview"], t["manage_users"], t["assign_route"]])
            with tab1:
                st.dataframe(df_drivers, use_container_width=True)
            with tab2:
                selected_user = st.selectbox("Användare:", df_users["username"].astype(str))
                user_info = df_users[df_users["username"].astype(str) == str(selected_user)].iloc[0]
                edit_pass = st.text_input("Nytt lösenord:", value=str(user_info["password"]))
                if st.button("Spara"):
                    df_users.loc[df_users["username"].astype(str) == str(selected_user), "password"] = str(edit_pass)
                    save_users(df_users)
                    st.success(t["saved_msg"])
            with tab3:
                sel_drv = st.selectbox("Chaufför:", df_drivers["Förare"].astype(str))
                new_r = st.text_input("Rutt / Fordon:")
                if st.button("Tilldela"):
                    df_drivers.loc[df_drivers["Förare"].astype(str) == str(sel_drv), "Fordon / Rutt"] = str(new_r)
                    save_driver_data(df_drivers)
                    st.success(t["saved_msg"])

        elif role == "Chaufför":
            driver_name = str(st.session_state["driver_name"])
            if driver_name in df_drivers["Förare"].astype(str).values:
                driver_info = df_drivers[df_drivers["Förare"].astype(str) == driver_name].iloc[0]
                st.info(f"{t['assigned_route']}: **{driver_info['Fordon / Rutt']}**")
                
                col1, col2 = st.columns(2)
                with col1:
                    u_phone = st.text_input(t["phone"], value=str(driver_info.get("Telefon", "-")))
                with col2:
                    u_lic = st.selectbox(t["license"], ["CE", "C"], index=0 if driver_info.get("Körkort")=="CE" else 1)

                new_status = st.selectbox(t["status_today"], ["I tjänst", "Sjuk / Ledig", "Ledig"])
                avail_choice = st.radio(t["avail_tomorrow"], ["🟢 Ja", "🔴 Nej"])

                if st.button(t["save"]):
                    df_drivers.loc[df_drivers["Förare"].astype(str) == driver_name, "Status idag"] = str(new_status)
                    df_drivers.loc[df_drivers["Förare"].astype(str) == driver_name, "Tillgänglig imorgon?"] = str(avail_choice)
                    df_drivers.loc[df_drivers["Förare"].astype(str) == driver_name, "Telefon"] = str(u_phone)
                    df_drivers.loc[df_drivers["Förare"].astype(str) == driver_name, "Körkort"] = str(u_lic)
                    save_driver_data(df_drivers)
                    st.success(t["saved_msg"])

    else:
        st.info(f"Sidan **{menu_choice}** är under uppbyggnad.")
