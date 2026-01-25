#  Smart Logistics

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Open In Kaggle](https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/code/trnchtng/notebook6d375cdcf5)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-4.0%2B-FD971F?style=for-the-badge&logo=gradio&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-Maps-77B829?style=for-the-badge&logo=leaflet&logoColor=white)
![OSRM](https://img.shields.io/badge/OSRM-Routing-blue?style=for-the-badge&logo=openstreetmap&logoColor=white)

##  System Architecture & Workflow Analysis

### 1. Business Process (Flowchart Analysis)
The system follows a comprehensive **Cross-functional Swimlane Diagram**, clearly delineating responsibilities between four key stakeholders: **Carrier (Logistics Provider)**, **Shop (Merchant)**, **E-commerce Platform**, and **Customer**.

> **Note:** Please refer to the system flowchart image in the `docs/` folder for a visual representation.

** Key Strengths**
* **Clear Separation of Concerns:** Distinct lanes for *Information Flow* (API updates, status sync) vs. *Physical Flow* (shipping, warehousing).
* **Exception Handling:** The workflow accounts for both "Happy Paths" (successful delivery) and complex **Reverse Logistics** scenarios (delivery failure $\rightarrow$ warehousing $\rightarrow$ return to shop).
* **Financial Reconciliation:** Logic distinguishes between **Pre-paid** orders and **COD** (Cash on Delivery), a critical requirement for the Vietnamese market.

** Scope for Improvement**
* [ ] **Retry Logic:** Future iterations will include a specific loop for "Re-delivery attempts" (typically 3 attempts) before initiating the Return process.
* [ ] **Early Cancellation:** Handling edge cases such as "User Cancellation" or "Out of Stock" events prior to the shipping phase.

---

### 2. Technical Implementation (POC)
The current codebase serves as a **Proof of Concept (POC)** focusing on the **Transportation Planning** module within the "Carrier" swimlane. You can run the live demo directly on Kaggle:

[** Click here to run the Notebook**](https://www.kaggle.com/code/trnchtng/notebook6d375cdcf5)

####  Tech Stack
| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | `Python` | Core logic and backend processing. |
| **Interface** | `Gradio` | Rapid UI development with responsive Blocks. |
| **Mapping** | `Folium` | Interactive map rendering. |
| **Routing** | `OSRM` | Open Source Routing Machine for real-world distances. |
| **Data** | `Pandas` | Data manipulation and tabular handling. |

####  Core Features & Technical Highlights
* **Advanced UI/UX (Bidirectional Map):** Utilizes a custom `postMessage` JavaScript bridge to capture coordinates from the `Folium` iframe and inject them back into the Python backend. This solves a major UX pain point regarding precise address entry.
* **Real-world Routing:** Integrates **OSRM** to calculate distances based on actual road networks (drivable distance), with a defensive fallback to Haversine distance for reliability.
* **Dynamic Costing Engine:** The `rule_cost` function accurately models logistics pricing, factoring in:
    * Volume metrics ($L \times W \times H$)
    * Cargo types (Fragile, Cold chain, High value)

####  Current Limitations & Roadmap
* **Geocoding:** Currently relies on `Nominatim` (OpenStreetMap), which has strict rate limits.
    * *Roadmap:* Production deployment will require a robust paid API (e.g., Google Maps API) or local caching.
* **Optimization Algorithm:** Uses a **Nearest Neighbor (Greedy)** approach.
    * *Roadmap:* Future versions will migrate to **Google OR-Tools** to handle complex **VRP (Vehicle Routing Problem)** constraints like vehicle capacity and time windows.