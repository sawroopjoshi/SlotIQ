
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="SlotIQ",
    page_icon="🚗",
    layout="wide"
)

# Initialize parking data
if "parking_data" not in st.session_state:
    st.session_state.parking_data = pd.DataFrame({
        "Slot ID": [
            "A1", "A2", "A3", "A4", "A5",
            "B1", "B2", "B3", "B4", "B5"
        ],
        "Distance (m)": [5, 10, 15, 8, 20, 12, 6, 18, 9, 14],
        "Status": [
            "Available", "Occupied", "Available", "Occupied",
            "Available", "Occupied", "Available", "Available",
            "Occupied", "Available"
        ]
    })

if "selected_slot" not in st.session_state:
    st.session_state.selected_slot = None

if "message" not in st.session_state:
    st.session_state.message = None

# Header
st.title("🚗 SlotIQ")
st.subheader("Smart Parking Space Allocation System")
st.write(
    "Find and manage parking spaces efficiently "
    "using the Greedy Algorithm."
)

st.divider()

# Dashboard statistics
parking_data = st.session_state.parking_data

total_slots = len(parking_data)
available_slots = int(
    (parking_data["Status"] == "Available").sum()
)
occupied_slots = total_slots - available_slots

occupancy = (
    occupied_slots / total_slots * 100
    if total_slots > 0 else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Slots", total_slots)
col2.metric("Available Slots", available_slots)
col3.metric("Occupied Slots", occupied_slots)
col4.metric("Occupancy Rate", f"{occupancy:.0f}%")

st.divider()

# Parking lot layout
st.subheader("🅿️ Parking Lot Overview")
st.caption("🟢 Available | 🔴 Occupied")

for start in range(0, total_slots, 5):
    cols = st.columns(5)

    for col, (_, slot) in zip(
        cols,
        parking_data.iloc[start:start + 5].iterrows()
    ):
        with col:
            if slot["Status"] == "Available":
                st.success(
                    f"🟢 {slot['Slot ID']}\n\nAvailable"
                )
            else:
                st.error(
                    f"🔴 {slot['Slot ID']}\n\nOccupied"
                )

st.divider()

# Show confirmation message
if st.session_state.message:
    st.success(st.session_state.message)
    st.session_state.message = None

# Greedy parking allocation
st.subheader("🚘 Find and Allocate Parking")

st.write(
    "The Greedy Algorithm selects the available "
    "parking slot with the minimum distance."
)

if st.button("Find Nearest Slot", use_container_width=True):
    available_parking = st.session_state.parking_data[
        st.session_state.parking_data["Status"] == "Available"
    ]

    if available_parking.empty:
        st.session_state.selected_slot = None
        st.session_state.message = (
            "No parking slots are currently available."
        )
        st.rerun()
    else:
        nearest_index = available_parking["Distance (m)"].idxmin()
        nearest_slot = available_parking.loc[nearest_index]

        st.session_state.selected_slot = nearest_slot["Slot ID"]

selected_slot = st.session_state.selected_slot

if selected_slot is not None:
    current_data = st.session_state.parking_data

    selected_rows = current_data[
        current_data["Slot ID"] == selected_slot
    ]

    if not selected_rows.empty:
        selected_row = selected_rows.iloc[0]

        if selected_row["Status"] == "Available":
            st.success(
                f"Nearest Available Slot: {selected_row['Slot ID']}"
            )

            st.info(
                f"Distance from entrance: "
                f"{selected_row['Distance (m)']} metres"
            )

            if st.button(
                "✅ Allocate Parking",
                use_container_width=True
            ):
                st.session_state.parking_data.loc[
                    st.session_state.parking_data["Slot ID"]
                    == selected_slot,
                    "Status"
                ] = "Occupied"

                st.session_state.selected_slot = None
                st.session_state.message = (
                    f"Slot {selected_slot} allocated successfully!"
                )

                st.rerun()
        else:
            st.session_state.selected_slot = None

st.divider()

# Release parking slot
st.subheader("🔓 Release Parking Slot")

st.write(
    "Release an occupied parking slot when a vehicle leaves."
)

occupied_parking = st.session_state.parking_data[
    st.session_state.parking_data["Status"] == "Occupied"
]

if occupied_parking.empty:
    st.info("There are no occupied slots to release.")
else:
    slot_to_release = st.selectbox(
        "Select an occupied parking slot",
        occupied_parking["Slot ID"].tolist()
    )

    if st.button("Release Slot", use_container_width=True):
        st.session_state.parking_data.loc[
            st.session_state.parking_data["Slot ID"]
            == slot_to_release,
            "Status"
        ] = "Available"

        st.session_state.selected_slot = None
        st.session_state.message = (
            f"Slot {slot_to_release} released successfully!"
        )

        st.rerun()

st.divider()

# Parking records
st.subheader("📋 Parking Slot Records")

st.dataframe(
    st.session_state.parking_data,
    use_container_width=True,
    hide_index=True
)

# Parking statistics
st.subheader("📊 Parking Statistics")

chart_data = st.session_state.parking_data["Status"].value_counts()

available_count = int(chart_data.get("Available", 0))
occupied_count = int(chart_data.get("Occupied", 0))

fig, ax = plt.subplots()

ax.bar(
    ["Available", "Occupied"],
    [available_count, occupied_count]
)

ax.set_ylabel("Number of Slots")
ax.set_title("Parking Slot Status")
ax.set_ylim(0, max(total_slots, 1))

st.pyplot(fig)
plt.close(fig)

st.caption(
    "SlotIQ | Smart Parking Space Allocation Using Greedy Algorithm"
)

# python -m streamlit run app.py