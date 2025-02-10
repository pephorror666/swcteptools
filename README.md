# SWC TepTools: Star Wars Combine Utility Suite

## Overview

SWC TepTools is a collection of web-based utilities designed to enhance the gameplay experience of Star Wars Combine (SWC). Built using Python and Streamlit, this application provides tools for:

*   **Route Planning:** Calculate estimated travel times (ETA) between systems, factoring in pilot skill and hyperspace capabilities.
*   **Cargo (Ship) Transport Planning:** Determine which ships in your fleet are capable of transporting a specified cargo of other ships, based on weight, volume, and docking bay requirements.

This project is created by Tep Hondor.

## Features

*   **Intuitive User Interface:**  A user-friendly interface built with Streamlit, making the tools accessible to all players.
*   **Route Planner:**
    *   Select origin and destination systems from a comprehensive galaxy database.
    *   Specify custom coordinates for deep space locations.
    *   Adjust pilot skill level and hyperspace speed for accurate ETA calculations.
    *   Generate detailed route reports for easy sharing and record-keeping.
*   **Cargo (Ship) Planner:**
    *   Select ships to transport from a database of SWC vessels.
    *   Calculate total weight and volume of the cargo.
    *   Identify suitable transport ships based on docking bay availability, weight capacity, and volume capacity.

## Installation

1.  **Clone the repository:**

    ```
    git clone [repository URL]
    cd [repository directory]
    ```

2.  **Install the required Python packages:**

    ```
    pip install streamlit pandas
    ```

3.  **Download the necessary data files:**

    *   `galaxy_db.csv`: Contains information about systems in the Star Wars Combine galaxy, including coordinates.  **Important**: Ensure this file is in the same directory as your script.
    *   `swc_ships_db.csv`: Contains data on various ships in SWC, including weight, volume, docking bay status, etc.  **Important**: Ensure this file is in the same directory as your script.

    *Note:* If you don't have these files, you'll need to create them. See "Data Files" section for the formatting.*

## Usage

1.  **Run the Streamlit application:**

    ```
    streamlit run your_script_name.py
    ```

    (Replace `your_script_name.py` with the actual name of your Python script.)

2.  **Access the application in your web browser:** Streamlit will provide a URL (usually `http://localhost:8501`). Open this URL in your browser to use the tools.

### Route Planner

1.  Select "Route Planner" from the sidebar.
2.  Choose a starting system from the "Select a system" dropdown.  If your origin is in deep space, select 'Deep Space' and enter the X and Y coordinates.
3.  Select Hyperspeed for the selected point.
4.  Click "Add to Route" to add this location to your route.
5.  Repeat steps 2-4 for each point in your route.
6.  Use the "Pilot Skill" slider to adjust the pilot's skill level.
7.  Click "Calculate ETA" to see the estimated time of arrival for each leg of the journey and the total ETA.
8.  Click "Generate Report" to create a text-based report of your route, including system coordinates, hyperspeed, and ETAs.

### Cargo (Ship) Planner

1.  Select "Cargo (ships) Planner" from the sidebar.
2.  In the sidebar under "Add Cargo to Transport":
    *   Select a ship class to filter the list of available ships.
    *   Choose the ship you want to transport from the "Select a ship to add to the cargo" dropdown.
    *   Enter the number of ships of that type you wish to transport.
    *   Click "Add Ship".
3.  Repeat step 2 to add all ships to your cargo.
4.  The "Current Cargo" section in the sidebar will display the list of ships you've added.
5.  The main section of the app will display a table of ships capable of transporting your selected cargo, considering weight, volume, and docking bay requirements.

## Data Files

The application relies on two CSV files for its data:

*   **galaxy\_db.csv:**
    *   `System` (string): The name of the star system.
    *   `Coordinate x` (numeric): The X coordinate of the system.
    *   `Coordinate y` (numeric): The Y coordinate of the system.
    *   `Sector` (string): The sector the system is located in
    *   `Owner` (string): The faction that owns the system

    Example:

    ```
    System,Coordinate x,Coordinate y,Sector,Owner
    "Bespin",10,-20,"Anoat sector","Rebel Alliance"
    "Hoth",-5,15,"Unknown","Galactic Empire"
    ```

*   **swc\_ships\_db.csv:**
    *   `Class` (string): The ship class (e.g., "Fighter", "Corvette", "Capital Ship").
    *   `Ship` (string): The name of the ship.
    *   `Weight` (numeric): The weight of the ship in tons.
    *   `Volume` (numeric): The volume of the ship in cubic meters.
    *   `Weight Cap` (numeric): The maximum weight the ship can carry (tons).
    *   `Volume Cap` (numeric): The maximum volume the ship can carry (cubic meters).
    *   `Docking Bay` (string): "Yes" if the ship has a docking bay, "No" otherwise.
    *   `Hyperspeed` (numeric): The hyperspeed rating of the ship
    *   `Hangar Bay` (string): Description of the hangar bay
    *   `Landing Capacity` (string): Description of the landing capacity
    *   `Tractor Beams` (string): Description of the tractor beams

    Example:

    ```
    Class,Ship,Weight,Volume,Weight Cap,Volume Cap,Docking Bay,Hyperspeed,Hangar Bay,Landing Capacity,Tractor Beams
    "Fighter","X-wing",10,15,5,20,"No",1,"","",""
    "Corvette","Corellian Corvette",300,500,200,600,"Yes",2,"","",""
    ```

    **Note:** Ensure that the units for weight are consistent (e.g., tons) throughout the `swc_ships_db.csv` file.

## Contributing

Contributions to SWC TepTools are welcome!  Feel free to submit pull requests with improvements, bug fixes, or new features.

## License

None

https://metalhead.club/@pephorror
