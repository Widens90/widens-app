import streamlit as st
import pandas as pd
import os

st.set_page_config(
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

# Load driver data safely as string
def load_driver_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, dtype=str).fillna("-")
        if "Telefon" not in df.columns:
            df["Telefon"] = "-"
        if "Körkort" not in df.columns:
            df["Körkort"] = "CE"
        return df
    else:
        initial_data = {
            "Förare": ["Ahmed", "Karwan"],
            "Telefon": ["0701234567", "0709876543"],
            "Körkort": ["CE", "C"],
            "Status idag": ["I tjänst", "I tjänst"],
            "Tillgänglig imorgon?": ["🟢 Ja", "🔴 Nej"],
            "Fordon / Rutt": ["Scania 01 (Kalmar)", "Volvo 02 (Karlskrona)"]
        }
        df = pd.DataFrame(initial_data, dtype=str)
        df.to_csv(DATA_FILE, index=False)
        return df

# Load users data safely as string
def load_users():
    if os.path.exists(USERS_FILE):
        df = pd.read_csv(USERS_FILE, dtype=str).fillna("-")
        if "phone" not in df.columns:
            df["phone"] = "-"
        if "license" not in df.columns:
            df["license"] = "CE"
        return df
    else:
        initial_users = {
            "username": ["admin", "chauffor"],
            "password": ["123", "456"],
            "role": ["Transportledare", "Chaufför"],
            "driver_name": ["Admin", "Ahmed"],
            "phone": ["0700000000", "0701234567"],
            "license": ["CE", "CE"]
        }
        df = pd.DataFrame(initial_users, dtype=str)
        df.to_csv(USERS_FILE, index=False)
        return df

def save_driver_data(df):
    df.astype(str).to_csv(DATA_FILE, index=False)

def save_users(df):
    df.astype(str).to_csv(USERS_FILE, index=False)

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
        username = st.text_input("Användarnamn (Username)", key="login_user")
        password = st.text_input("Lösenord (Password)", type="password", key="login_pass")
        
        if st.button("Logga in"):
            user_match = df_users[(df_users["username"].astype(str) == str(username)) & (df_users["password"].astype(str) == str(password))]
            if not user_match.empty:
                st.session_state["logged_in"] = True
                st.session_state["user_role"] = str(user_match.iloc[0]["role"])
                st.session_state["username"] = str(username)
                st.session_state["driver_name"] = str(user_match.iloc[0]["driver_name"])
                st.success("Inloggningen lyckades!")
                st.rerun()
            else:
                st.error("Felaktigt användarnamn eller lösenord!")

    with tab2:
        st.subheader("Registrera ny chaufför (Register new driver)")
        new_name = st.text_input("Ditt fullständiga namn (Full name):")
        new_phone = st.text_input("Telefonnummer (Phone number):")
        new_license = st.selectbox("Körkortstyp (License Class):", ["CE (Tung lastbil med släp)", "C (Tung lastbil)"])
        new_username = st.text_input("Välj användarnamn (Choose username):")
        new_password = st.text_input("Välj lösenord (Choose password):", type="password")
        
        license_code = "CE" if "CE" in new_license else "C"

        if st.button("Skapa konto"):
            if new_name and new_username and new_password:
                if str(new_username) in df_users["username"].astype(str).values:
                    st.error("Detta användarnamn är redan upptaget!")
                else:
                    new_user_row = pd.DataFrame([{
                        "username": str(new_username), 
                        "password": str(new_password), 
                        "role": "Chaufför",
                        "driver_name": str(new_name),
                        "phone": str(new_phone) if new_phone else "-",
                        "license": str(license_code)
                    }], dtype=str)
                    updated_users = pd.concat([df_users, new_user_row], ignore_index=True)
                    save_users(updated_users)
                    
                    new_driver_row = pd.DataFrame([{
                        "Förare": str(new_name),
                        "Telefon": str(new_phone) if new_phone else "-",
                        "Körkort": str(license_code),
                        "Status idag": "Ledig",
                        "Tillgänglig imorgon?": "🔴 Nej",
                        "Fordon / Rutt": "Ej tilldelad"
                    }], dtype=str)
                    updated_drivers = pd.concat([df_drivers, new_driver_row], ignore_index=True)
                    save_driver_data(updated_drivers)
                    
                    st.success("Ditt konto har skapats! Du kan nu logga in.")
            else:
                st.warning("Fyll i alla obligatoriska fält!")

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
        tab_admin1, tab_admin2, tab_admin3 = st.tabs([
            "📊 Översikt (Overview)", 
            "⚙️ Hantera förare & lösenord (Manage Drivers & Passwords)",
            "✍️ Tilldela rutt (Assign Route)"
        ])

        with tab_admin1:
            st.header("📊 Översikt över alla chaufförer")
            st.dataframe(df_drivers, use_container_width=True)

            st.markdown("---")
            st.header("🟢 Tillgängliga ersättare för imorgon")
            standby_drivers = df_drivers[df_drivers["Tillgänglig imorgon?"] == "🟢 Ja"]
            
            if not standby_drivers.empty:
                st.success("Dessa chaufförer är tillgängliga för arbete imorgon:")
                st.table(standby_drivers[["Förare", "Körkort", "Telefon", "Status idag"]])
            else:
                st.warning("Ingen chaufför har anmält sig som tillgänglig ännu.")

        with tab_admin2:
            st.header("🔑 Återställ lösenord / Ändra uppgifter (Reset Password & Edit Details)")
            
            selected_user = st.selectbox("Välj användare att redigera:", df_users["username"].astype(str))
            user_info = df_users[df_users["username"].astype(str) == str(selected_user)].iloc[0]

            st.info(f"Nuvarande lösenord för **{selected_user}**: `{user_info['password']}`")

            col1, col2 = st.columns(2)
            with col1:
                edit_name = st.text_input("Ändra namn (Edit Name):", value=str(user_info["driver_name"]))
                edit_phone = st.text_input("Ändra telefon (Edit Phone):", value=str(user_info["phone"]))
            with col2:
                current_lic = str(user_info.get("license", "CE"))
                edit_license = st.selectbox("Körkortstyp (License Class):", ["CE", "C"], index=0 if current_lic == "CE" else 1)
                edit_pass = st.text_input("Nytt lösenord (New Password):", value=str(user_info["password"]))

            if st.button("Spara ändringar (Save Changes)"):
                df_users.loc[df_users["username"].astype(str) == str(selected_user), "driver_name"] = str(edit_name)
                df_users.loc[df_users["username"].astype(str) == str(selected_user), "phone"] = str(edit_phone)
                df_users.loc[df_users["username"].astype(str) == str(selected_user), "license"] = str(edit_license)
                df_users.loc[df_users["username"].astype(str) == str(selected_user), "password"] = str(edit_pass)
                save_users(df_users)

                old_name = str(user_info["driver_name"])
                if old_name in df_drivers["Förare"].astype(str).values:
                    df_drivers.loc[df_drivers["Förare"].astype(str) == old_name, "Förare"] = str(edit_name)
                    df_drivers.loc[df_drivers["Förare"].astype(str) == old_name, "Telefon"] = str(edit_phone)
                    df_drivers.loc[df_drivers["Förare"].astype(str) == old_name, "Körkort"] = str(edit_license)
                    save_driver_data(df_drivers)

                st.success("Uppgifterna har uppdaterats!")
                st.rerun()

        with tab_admin3:
            st.header("✍️ Tilldela fordon / rutt")
            col1, col2 = st.columns(2)
            with col1:
                selected_driver = st.selectbox("Välj chaufför:", df_drivers["Förare"].astype(str))
                driver_lic = df_drivers[df_drivers["Förare"].astype(str) == str(selected_driver)]["Körkort"].values[0] if str(selected_driver) in df_drivers["Förare"].astype(str).values else "-"
                st.caption(f"💳 Körkort för valda chaufför: **{driver_lic}**")
            with col2:
                new_route = st.text_input("Fordon och rutt (t.ex. Scania CE med släp):")

            if st.button("Spara uppdrag"):
                df_drivers.loc[df_drivers["Förare"].astype(str) == str(selected_driver), "Fordon / Rutt"] = str(new_route)
                save_driver_data(df_drivers)
                st.success(f"Uppdraget för {selected_driver} har uppdaterats!")
                st.rerun()

    elif role == "Chaufför":
        st.header("👤 Chaufförsportal - Rapportera status")
        
        driver_name = str(st.session_state["driver_name"])
        
        if driver_name in df_drivers["Förare"].astype(str).values:
            driver_info = df_drivers[df_drivers["Förare"].astype(str) == driver_name].iloc[0]
            st.info(f"Ditt nuvarande uppdrag: **{driver_info['Fordon / Rutt']}**")
            
            col1, col2 = st.columns(2)
            with col1:
                current_phone = str(driver_info.get("Telefon", "-"))
                user_phone = st.text_input("Ditt telefonnummer (Phone number):", value=current_phone if current_phone != "-" else "")
            with col2:
                current_lic = str(driver_info.get("Körkort", "CE"))
                user_lic = st.selectbox("Ditt körkort (License Class):", ["CE", "C"], index=0 if current_lic == "CE" else 1)

            status_options = ["I tjänst", "Sjuk / Ledig", "Ledig"]
            current_status_index = status_options.index(driver_info["Status idag"]) if driver_info["Status idag"] in status_options else 0
            
            new_status = st.selectbox("Ange din status idag (Set status today):", status_options, index=current_status_index)
            
            st.markdown("### 📅 Tillgänglighet imorgon (Availability tomorrow)")
            availability_choice = st.radio(
                "Kan du arbeta imorgon om det behövs?",
                options=["🟢 Ja, jag kan arbeta (Green - Available)", "🔴 Nej, jag kan inte (Red - Not available)"],
                index=0 if "Ja" in str(driver_info["Tillgänglig imorgon?"]) else 1
            )
            
            if st.button("Spara status (Save Status)"):
                formatted_avail = "🟢 Ja" if "Ja" in availability_choice else "🔴 Nej"
                
                df_drivers.loc[df_drivers["Förare"].astype(str) == driver_name, "Status idag"] = str(new_status)
                df_drivers.loc[df_drivers["Förare"].astype(str) == driver_name, "Tillgänglig imorgon?"] = str(formatted_avail)
                df_drivers.loc[df_drivers["Förare"].astype(str) == driver_name, "Telefon"] = str(user_phone)
                df_drivers.loc[df_drivers["Förare"].astype(str) == driver_name, "Körkort"] = str(user_lic)
                save_driver_data(df_drivers)

                df_users.loc[df_users["driver_name"].astype(str) == driver_name, "phone"] = str(user_phone)
                df_users.loc[df_users["driver_name"].astype(str) == driver_name, "license"] = str(user_lic)
                save_users(df_users)

                st.success("Dina uppgifter har sparats!")
                st.rerun()
        else:
            st.error("Ditt namn hittades inte i systemet.")
