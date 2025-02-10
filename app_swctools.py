# TOOLS FOR STAR WARS COMBINE BY TEP HONDOR
# CALCULATE ETA FOR ROUTES
# HELP TO TRANSPORT SHIPS AS CARGO IN A DOCKING BAY

import streamlit as st
import pandas as pd
import math
from collections import Counter

# --- General App Settings ---
PAGE_TITLE = "SWC Tools by Tep Hondor"
PAGE_ICON = "🚀"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

# --- Load Data ---
@st.cache_data
def load_galaxy_data():
    return pd.read_csv('galaxy_db.csv')

@st.cache_data
def load_ship_data():
    df = pd.read_csv("swc_ships_db.csv")
    def convert_weight(value):
        if isinstance(value, float):
            return value
        if isinstance(value, (int, float)):  # Handle numeric types directly
            return float(value)  # Convert to float if it's an integer
        value = str(value).lower().replace(',', '')
        if 'kg' in value:
            return float(value.split()[0]) / 1000  # Convert kg to tons
        elif 't' in value:
            return float(value.split()[0])  # Already in tons
        else:
            return float(value)  # Assume it's already in tons if no unit is specified

    # Convert weight-related columns
    for col in ['Weight Cap', 'Weight']:
        df[col] = df[col].apply(convert_weight)
    return df

galaxy_df = load_galaxy_data()
ship_df = load_ship_data()

# --- Route Planner Functions ---
def calculo_ETA(x_origen, y_origen, x_destino, y_destino, piloto_skill, hyperspeed):
    p_skill = int(piloto_skill)
    hyperspace = int(hyperspeed)
    x1, y1 = float(x_origen), float(y_origen)
    x2, y2 = float(x_destino), float(y_destino)

    if hyperspace < 1:
        hyperspace = 1

    coef_dict = {0: 1, 1: 6857/7200, 2: 1309/1440, 3: 313/360, 4: 5/6, 5: 4/5}
    coef = coef_dict.get(p_skill, 1)

    dist_x, dist_y = abs(x2 - x1), abs(y2 - y1)
    D = max(dist_x, dist_y)

    raw_eta = (120 * coef * D) / hyperspace

    dias = int(raw_eta // 1440)
    horas = int((raw_eta % 1440) // 60)
    minutos = int(raw_eta % 60)

    return f"{dias}D {horas}H {minutos}M"

# --- Ship Transport Planner Functions ---
def can_carry(ship, total_weight, total_volume):
    has_docking_bay = ship["Docking Bay"] == "Yes"
    has_enough_weight = ship["Weight Cap"] >= total_weight
    has_enough_volume = ship["Volume Cap"] >= total_volume
    return has_docking_bay and has_enough_weight and has_enough_volume

# --- Main App Layout ---
st.sidebar.title(f"{PAGE_ICON} SWC TepTools")
app_mode = st.sidebar.selectbox("Choose a tool:", ["Route Planner", "Cargo (ships) Planner"])

if app_mode == "Route Planner":
    st.title("Route Planner")

    # System selection
    system_options = ['Deep Space'] + galaxy_df['System'].tolist()
    selected_system = st.selectbox("Select a system", system_options)

    if selected_system == 'Deep Space':
        x = st.number_input("Enter X coordinate", step=1, format="%i")
        y = st.number_input("Enter Y coordinate", step=1, format="%i")
    else:
        system_data = galaxy_df[galaxy_df['System'] == selected_system].iloc[0]
        x, y = system_data['Coordinate x'], system_data['Coordinate y']

    # Hyperspeed selection for the point
    selected_hyperspeed = st.selectbox("Select Hyperspeed for this point", range(1, 9))

    if st.button("Add to Route"):
        if 'route' not in st.session_state:
            st.session_state.route = []

        if selected_system == 'Deep Space':
            st.session_state.route.append({
                'Sector': None,
                'System': 'Deep Space',
                'Coordinate x': x,
                'Coordinate y': y,
                'Owner': None,
                'Hyperspeed': selected_hyperspeed
            })
        else:
            system_entry = system_data.to_dict()
            system_entry['Hyperspeed'] = selected_hyperspeed
            st.session_state.route.append(system_entry)

    # Display route
    if 'route' in st.session_state and st.session_state.route:
        st.write("Current Route:")
        route_df = pd.DataFrame(st.session_state.route)
        st.table(route_df)

        # ETA calculation
        pilot_skill = st.slider("Pilot Skill", 1, 5, 3)

        if st.button("Calculate ETA"):
            total_eta = 0
            eta_details = []

            for i in range(1, len(st.session_state.route)):
                prev = st.session_state.route[i-1]
                curr = st.session_state.route[i]
                eta = calculo_ETA(prev['Coordinate x'], prev['Coordinate y'],
                                    curr['Coordinate x'], curr['Coordinate y'],
                                    pilot_skill, curr['Hyperspeed'])
                eta_details.append(f"ETA from {prev['System']} to {curr['System']}: {eta}")

                # Convert ETA to minutes for total calculation
                days, hours, minutes = map(int, eta.replace('D', '').replace('H', '').replace('M', '').split())
                total_eta += days * 1440 + hours * 60 + minutes

            st.write("ETA Details:")
            for detail in eta_details:
                st.write(detail)

            total_days = total_eta // 1440
            total_hours = (total_eta % 1440) // 60
            total_minutes = total_eta % 60

            st.write(f"Total ETA: {total_days}D {total_hours}H {total_minutes}M")

        # Generate report
        if st.button("Generate Report"):
            report = ""
            for i, point in enumerate(st.session_state.route, 1):
                report += f"POINT {i}\n"
                report += f"Sector: {point['Sector']}\n"
                report += f"System: {point['System']} ({point['Coordinate x']}, {point['Coordinate y']})\n"
                report += f"Hyperspeed: {point['Hyperspeed']}\n"

                if i > 1:
                    prev = st.session_state.route[i-2]
                    eta = calculo_ETA(prev['Coordinate x'], prev['Coordinate y'],
                                        point['Coordinate x'], point['Coordinate y'],
                                        pilot_skill, point['Hyperspeed'])
                    report += f"ETA: {eta} from {prev['System']} to {point['System']}\n"
                report += "\n"

            st.text_area("Route Report", report.strip(), height=400)

elif app_mode == "Cargo (ships) Planner":
    st.title("Cargo Planner")

    # Sidebar: Add cargo to transport
    st.sidebar.header("Add Cargo to Transport")

    # Initialize session state for cargo list
    if "cargo_list" not in st.session_state:
        st.session_state.cargo_list = []

    # Dropdown to select class
    selected_class = st.sidebar.selectbox(
        "Select a ship class:",
        options=["All"] + list(ship_df["Class"].unique()),
        help="Select a ship class or 'All' to see all ships."
    )

    # Filter ships based on selected class
    if selected_class != "All":
        filtered_data = ship_df[ship_df["Class"] == selected_class]
    else:
        filtered_data = ship_df

    # Dropdown to select ships to transport
    ship_to_add = st.sidebar.selectbox(
        "Select a ship to add to the cargo:",
        options=filtered_data["Ship"].unique(),
        help="Search and select a ship to add to the transport cargo."
    )

    # Input for number of ships
    num_ships = st.sidebar.number_input(
        "Number of ships to add:",
        min_value=1,
        value=1,
        step=1,
        help="Enter the number of ships to add to the cargo."
    )

    # Button to add the selected ship to the cargo list
    if st.sidebar.button("Add Ship"):
        for _ in range(num_ships):
            st.session_state.cargo_list.append(ship_to_add)
        st.sidebar.success(f"Added {num_ships} x {ship_to_add} to the cargo.")

    # Display current cargo list in the sidebar (grouped by type)
    st.sidebar.subheader("Current Cargo")
    if st.session_state.cargo_list:
        grouped_cargo = Counter(st.session_state.cargo_list)  # Group by type of ship
        for ship, count in grouped_cargo.items():
            st.sidebar.write(f"{count} x {ship}")

        if st.sidebar.button("Clear Cargo"):
            st.session_state.cargo_list = []
            st.sidebar.success("Cargo cleared.")
    else:
        st.sidebar.write("No cargo added yet.")

    # Calculate total weight, volume, and docking bay requirements for all added cargo
    total_weight = 0  # Total weight of all selected ships (in tons)
    total_volume = 0  # Total volume of all selected ships (in cubic meters)
    grouped_cargo = Counter(st.session_state.cargo_list)  # Group by type of ship
    for cargo_ship, count in grouped_cargo.items():
        ship_data = ship_df[ship_df["Ship"] == cargo_ship].iloc[0]
        total_weight += ship_data["Weight"] * count  # Multiply by count of each type of ship
        total_volume += ship_data["Volume"] * count

    # Main section: Display ships that can carry the cargo
    st.header("Available Ships for Transport")

    if grouped_cargo:
        # Display cargo summary
        st.subheader("Cargo Summary")
        for ship, count in grouped_cargo.items():
            st.write(f"{count} x {ship}")
        st.write(f"Total Weight: {total_weight:.2f} T")
        st.write(f"Total Volume: {total_volume:.2f} m³")

        # Filter ships that can carry the cargo based on docking bay, weight, and volume requirements
        suitable_ships = ship_df[
            ship_df.apply(
                lambda row: can_carry(row, total_weight, total_volume), axis=1
            )
        ]

        if not suitable_ships.empty:
            # Display suitable ships in a table
            st.subheader("Suitable Transport Ships")
            columns_to_display = ["Class", "Ship", "Hyperspeed", "Hangar Bay", "Landing Capacity", "Tractor Beams", "Weight Cap", "Volume Cap", "Docking Bay"]
            st.dataframe(suitable_ships[columns_to_display].reset_index(drop=True))
        else:
            # No suitable ships found
            st.warning("No ships available with enough capacity to transport the selected cargo.")
    else:
        # No cargo added yet
        st.info("Add some ships to transport in the sidebar to see available transport options.")
