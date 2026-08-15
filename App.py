import streamlit as st
import pandas as pd
import os

# Sidkonfiguration
st.set_page_config(page_title="Widens Åkeri AB", page_icon="🚛", layout="wide")

DATA_FILE = "drivers_data.csv"

# Användare och lösenord
USERS = {
    "admin": {"password": "123", "role": "Transportledare"},
    "chauffor": {"password": "456", "role": "Chaufför"}
}

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        initial_data = {
            "Förare": ["Ahmed", "Karwan", "Aras", "Soran"],
            "Status idag": ["I tjänst", "I tjänst", "Sjuk / Ledig", "Ledig"],
            "Tillgänglig imorgon?": ["Nej", "Nej", "Nej", "Ja"],
            "Fordon / Rutt": ["Scania 01 (Kalmar)", "Volvo 02 (Karlskrona)", "Ej tilldelad", "Ej tilldelad"]
        }
        df = pd.DataFrame(initial_data)
        df.to_csv(DATA_FILE, index=False)
        return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = None
    st.session_state["username"] = ""

def login_page():
    st.title("🚛 Widens Åkeri AB - Inloggning")
    st.subheader("Ange användarnamn och lösenord")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Användarnamn")
        password = st.text_input("Lösenord", type="password")
        
        if st.button("Logga in"):
            if username in USERS and USERS[username]["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["user_role"] = USERS[username]["role"]
                st.session_state["username"] = username
                st.success("Inloggningen lyckades!")
                st.rerun()
            else:
                st.error("Felaktigt användarnamn eller lösenord!")

if not st.session_state["logged_in"]:
    login_page()
else:
    st.sidebar.title(f"Välkommen, {st.session_state['username']}")
    if st.sidebar.button("Logga ut"):
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None
        st.session_state["username"] = ""
        st.rerun()

    role = st.session_state["user_role"]
    st.title("🚛 Widens Åkeri AB - Kalmar")

    if role == "Transportledare":
        st.header("📊 Transportledare - Översikt över chaufförer")
        st.dataframe(df, use_container_width=True)

        st.markdown("---")
        st.header("🆘 Tillgängliga ersättare för imorgon")
        standby_drivers = df[df["Tillgänglig imorgon?"] == "Ja"]
        
        if not standby_drivers.empty:
            st.success("Dessa chaufförer är tillgängliga för arbete imorgon:")
            st.table(standby_drivers[["Förare", "Status idag"]])
        else:
            st.warning("Ingen chaufför har anmält sig som tillgänglig ännu.")

        st.markdown("---")
        st.header("✍️ Tilldela fordon / rutt")
        col1, col2 = st.columns(2)
        with col1:
            selected_driver = st.selectbox("Välj chaufför:", df["Förare"])
        with col2:
            new_route = st.text_input("Fordon och rutt (t.ex. Scania 01 - Kalmar till Karlskrona):")

        if st.button("Spara uppdrag"):
            df.loc[df["Förare"] == selected_driver, "Fordon / Rutt"] = new_route
            save_data(df)
            st.success(f"Uppdraget för {selected_driver} har uppdaterats!")
            st.rerun()

    elif role == "Chaufför":
        st.header("👤 Chaufförsportal - Rapportera status")
        
        driver_name = st.selectbox("Välj ditt namn:", df["Förare"])
        driver_info = df[df["Förare"] == driver_name].iloc[0]
        
        st.info(f"Ditt nuvarande uppdrag: **{driver_info['Fordon / Rutt']}**")
        
        status_options = ["I tjänst", "Sjuk / Ledig", "Ledig"]
        current_status_index = status_options.index(driver_info["Status idag"]) if driver_info["Status idag"] in status_options else 0
        
        new_status = st.selectbox("Ange din status idag:", status_options, index=current_status_index)
        
        is_available = st.checkbox(
            "🙋‍♂️ Jag är tillgänglig för arbete imorgon (om någon är sjuk)", 
            value=(driver_info["Tillgänglig imorgon?"] == "Ja")
        )
        
        if st.button("Spara status"):
            df.loc[df["Förare"] == driver_name, "Status idag"] = new_status
            df.loc[df["Förare"] == driver_name, "Tillgänglig imorgon?"] = "Ja" if is_available else "Nej"
            save_data(df)
            st.success("Dina uppgifter har sparats!")
            st.rerun()
