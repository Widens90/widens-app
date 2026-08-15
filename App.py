import streamlit as st
import pandas as pd
import os

st.se st.set_page_config(
    page_title="Widens Åkeri AB", 
    page_icon="🚛", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide top menu and toolbar
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


DATA_FILE = "drivers_data.csv"
USERS_FILE = "users_data.csv"

# Load driver data
def load_driver_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        initial_data = {
            "Förare": ["Ahmed", "Karwan"],
            "Status idag": ["I tjänst", "I tjänst"],
            "Tillgänglig imorgon?": ["Nej", "Nej"],
            "Fordon / Rutt": ["Scania 01 (Kalmar)", "Volvo 02 (Karlskrona)"]
        }
        df = pd.DataFrame(initial_data)
        df.to_csv(DATA_FILE, index=False)
        return df

# Load users
def load_users():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE)
    else:
        initial_users = {
            "username": ["admin", "chauffor"],
            "password": ["123", "456"],
            "role": ["Transportledare", "Chaufför"],
            "driver_name": ["Admin", "Ahmed"]
        }
        df = pd.DataFrame(initial_users)
        df.to_csv(USERS_FILE, index=False)
        return df

def save_driver_data(df):
    df.to_csv(DATA_FILE, index=False)

def save_users(df):
    df.to_csv(USERS_FILE, index=False)

df_drivers = load_driver_data()
df_users = load_users()

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = None
    st.session_state["username"] = ""
    st.session_state["driver_name"] = ""

def login_register_page():
    st.title("🚛 Widens Åkeri AB")
    
    tab1, tab2 = st.tabs(["🔒 Logga in (Login)", "✍️ Skapa konto (Sign up)"])
    
    with tab1:
        st.subheader("Ange användarnamn och lösenord")
        username = st.text_input("Användarnamn", key="login_user")
        password = st.text_input("Lösenord", type="password", key="login_pass")
        
        if st.button("Logga in"):
            user_match = df_users[(df_users["username"] == username) & (df_users["password"] == str(password))]
            if not user_match.empty:
                st.session_state["logged_in"] = True
                st.session_state["user_role"] = user_match.iloc[0]["role"]
                st.session_state["username"] = username
                st.session_state["driver_name"] = user_match.iloc[0]["driver_name"]
                st.success("Inloggningen lyckades!")
                st.rerun()
            else:
                st.error("Felaktigt användarnamn eller lösenord!")

    with tab2:
        st.subheader("Registrera ny chaufför (Register new driver)")
        new_name = st.text_input("Ditt fullständiga namn (Full name):")
        new_username = st.text_input("Välj användarnamn (Choose username):")
        new_password = st.text_input("Välj lösenord (Choose password):", type="password")
        
        if st.button("Skapa konto"):
            if new_name and new_username and new_password:
                if new_username in df_users["username"].values:
                    st.error("Detta användarnamn är redan upptaget!")
                else:
                    new_user_row = pd.DataFrame([{
                        "username": new_username, 
                        "password": str(new_password), 
                        "role": "Chaufför",
                        "driver_name": new_name
                    }])
                    updated_users = pd.concat([df_users, new_user_row], ignore_index=True)
                    save_users(updated_users)
                    
                    new_driver_row = pd.DataFrame([{
                        "Förare": new_name,
                        "Status idag": "Ledig",
                        "Tillgänglig imorgon?": "Nej",
                        "Fordon / Rutt": "Ej tilldelad"
                    }])
                    updated_drivers = pd.concat([df_drivers, new_driver_row], ignore_index=True)
                    save_driver_data(updated_drivers)
                    
                    st.success("Ditt konto har skapats! Du kan nu logga in.")
            else:
                st.warning("Fyll i alla fält!")

if not st.session_state["logged_in"]:
    login_register_page()
else:
    st.sidebar.title(f"Välkommen, {st.session_state['driver_name']}")
    if st.sidebar.button("Logga ut"):
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = None
        st.session_state["username"] = ""
        st.session_state["driver_name"] = ""
        st.rerun()

    role = st.session_state["user_role"]
    st.title("🚛 Widens Åkeri AB - Kalmar")

    if role == "Transportledare":
        st.header("📊 Översikt över alla chaufförer")
        st.dataframe(df_drivers, use_container_width=True)

        st.markdown("---")
        st.header("🆘 Tillgängliga ersättare för imorgon")
        standby_drivers = df_drivers[df_drivers["Tillgänglig imorgon?"] == "Ja"]
        
        if not standby_drivers.empty:
            st.success("Dessa chaufförer är tillgängliga för arbete imorgon:")
            st.table(standby_drivers[["Förare", "Status idag"]])
        else:
            st.warning("Ingen chaufför har anmält sig som tillgänglig ännu.")

        st.markdown("---")
        st.header("✍️ Tilldela fordon / rutt")
        col1, col2 = st.columns(2)
        with col1:
            selected_driver = st.selectbox("Välj chaufför:", df_drivers["Förare"])
        with col2:
            new_route = st.text_input("Fordon och rutt (Vehicle and route):")

        if st.button("Spara uppdrag"):
            df_drivers.loc[df_drivers["Förare"] == selected_driver, "Fordon / Rutt"] = new_route
            save_driver_data(df_drivers)
            st.success(f"Uppdraget för {selected_driver} har uppdaterats!")
            st.rerun()

    elif role == "Chaufför":
        st.header("👤 Chaufförsportal - Rapportera status")
        
        driver_name = st.session_state["driver_name"]
        
        if driver_name in df_drivers["Förare"].values:
            driver_info = df_drivers[df_drivers["Förare"] == driver_name].iloc[0]
            st.info(f"Ditt nuvarande uppdrag: **{driver_info['Fordon / Rutt']}**")
            
            status_options = ["I tjänst", "Sjuk / Ledig", "Ledig"]
            current_status_index = status_options.index(driver_info["Status idag"]) if driver_info["Status idag"] in status_options else 0
            
            new_status = st.selectbox("Ange din status idag (Set status today):", status_options, index=current_status_index)
            
            is_available = st.checkbox(
                "🙋‍♂️ Jag är tillgänglig för arbete imorgon (Available tomorrow)", 
                value=(driver_info["Tillgänglig imorgon?"] == "Ja")
            )
            
            if st.button("Spara status"):
                df_drivers.loc[df_drivers["Förare"] == driver_name, "Status idag"] = new_status
                df_drivers.loc[df_drivers["Förare"] == driver_name, "Tillgänglig imorgon?"] = "Ja" if is_available else "Nej"
                save_driver_data(df_drivers)
                st.success("Dina uppgifter har sparats!")
                st.rerun()
        else:
            st.error("Ditt namn hittades inte i systemet.")
