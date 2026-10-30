import streamlit as st
import pandas as pd
import os

# 1. Configuration & Constants
st.set_page_config(page_title="Persistent Student Data Portal", layout="wide")
DATA_FILE = "student_data.csv"

st.title("💾 Persistent Student Health Dashboard")
st.write("Data entered here is saved to a local CSV file. The history loads automatically next time you open the app.")

# 2. Helper Functions to Handle CSV Database
def load_data():
    """Loads records from CSV file, creates one if it doesn't exist."""
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except Exception:
            # Handle fallback if file is corrupted
            return pd.DataFrame(columns=["Name", "Height (cm)", "Weight (kg)"])
    else:
        return pd.DataFrame(columns=["Name", "Height (cm)", "Weight (kg)"])

def save_data(dataframe):
    """Saves the dataframe to the local CSV file."""
    dataframe.to_csv(DATA_FILE, index=False)

# 3. Synchronize CSV with Streamlit's Session State
if "student_db" not in st.session_state:
    st.session_state.student_db = load_data()

# 4. Two-Column Layout (Form on Left, Dashboard on Right)
input_col, output_col = st.columns(2)

with input_col:
    st.subheader("📥 Student Data Form")
    
    with st.form(key="student_entry_form", clear_on_submit=True):
        name = st.text_input("Full Name:", placeholder="e.g., Jane Smith").strip()
        height = st.number_input("Height (cm):", min_value=50.0, max_value=250.0, value=165.0, step=0.5)
        weight = st.number_input("Weight (kg):", min_value=10.0, max_value=200.0, value=55.0, step=0.5)
        
        submit_button = st.form_submit_button(label="Submit and Save Data", type="primary")
        
    if submit_button:
        if name == "":
            st.error("Please enter a name before submitting.")
        else:
            new_row = {"Name": name, "Height (cm)": height, "Weight (kg)": weight}
            
            # Update Session State
            st.session_state.student_db = pd.concat(
                [st.session_state.student_db, pd.DataFrame([new_row])], 
                ignore_index=True
            )
            
            # Commit the update directly to the hard drive
            save_data(st.session_state.student_db)
            
            st.success(f"Successfully recorded and stored data for {name}!")
            st.rerun()

# 5. Right Column: Display Analytics Dashboard
with output_col:
    df = st.session_state.student_db
    
    if df.empty:
        st.info("💡 No saved data found. Fill out the form on the left to create your first record.")
    else:
        st.subheader("📌 Live Class Metrics")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Records Saved", f"{len(df)} Students")
        m2.metric("Class Avg Height", f"{df['Height (cm)'].mean():.1f} cm")
        m3.metric("Class Avg Weight", f"{df['Weight (kg)'].mean():.1f} kg")
        
        st.divider()
        
        # Tabs for visualization
        tab1, tab2, tab3 = st.tabs(["📊 Bar Charts", "📈 Scatter Analysis", "📂 Database Admin"])
        
        with tab1:
            st.write("##### Height Overview (cm)")
            st.bar_chart(data=df, x="Name", y="Height (cm)", color="#2ca02c")
            st.write("##### Weight Overview (kg)")
            st.bar_chart(data=df, x="Name", y="Weight (kg)", color="#d62728")
            
        with tab2:
            st.write("##### Height vs. Weight Distribution Matrix")
            st.scatter_chart(data=df, x="Height (cm)", y="Weight (kg)", color="Name", size=70)
            
        with tab3:
            st.write("##### 📁 Student Database (Double-click cells to edit; changes save automatically)")
            
            # 1. Use st.data_editor instead of st.dataframe
            # The key parameter allows Streamlit to track UI state changes
            edited_df = st.data_editor(
                df, 
                use_container_width=True, 
                hide_index=True,
                key="student_table_editor"
            )
            
            # 2. Check if the user has made any modifications to the table
            # If the current edited dataframe doesn't match session_state, data has changed
            if not edited_df.equals(st.session_state.student_db):
                # Update the database running in memory
                st.session_state.student_db = edited_df
                # Commit the updates directly to the local CSV file
                save_data(edited_df)
                st.toast("💾 Changes automatically saved to CSV!", icon="✅")
                # Force a page rerun so that charts and metric boxes update immediately
                st.rerun()
            
            st.divider()
            st.warning("⚠️ Administrative Actions:")
            if st.button("🚨 Wipe Local CSV and Clear History"):
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                st.session_state.student_db = pd.DataFrame(columns=["Name", "Height (cm)", "Weight (kg)"])
                st.success("Database file erased successfully.")
                st.rerun()
