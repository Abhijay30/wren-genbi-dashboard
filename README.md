# Wren GenBI Dashboard 📊🤖

A premium, serverless **Generative Business Intelligence (GenBI)** dashboard built using the **Wren AI WebAssembly Semantic Engine (`wren-core-wasm`)** and **DuckDB WASM**. The application runs entirely in the web browser—loading semantic schemas, compiling SQL relationships, executing queries against local Parquet snapshots, and drawing dynamic visualizations client-side.

---

## 🌟 Key Features

* **Natural Language Query Assistant**: Ask questions in plain English (*"what was the least sold item"*, *"total revenue by store place"*) and watch the AI translate, execute, and plot the data instantly.
* **Hybrid Text & SQL Outputs**: Supports cognitive reasoning. If you ask a *"why"* question (*"why did sales peak in July 2022?"*), the dashboard splits the LLM response into markdown explanations and a background SQL query to chart the metrics.
* **Dynamic Visualization Switcher**: Automatically selects the best graph format depending on the results:
  * **Line Charts** for trends and time series (years/dates).
  * **Radar Charts** for multi-metric queries (e.g. comparing sales and volume across categories).
  * **Polar Area Charts** for medium-size categorical arrays.
  * **Doughnut Charts** for small comparison groups.
  * **Horizontal Bar Charts** for large items list to prevent text overlap.
* **Dual-Mode RAG (Retrieval-Augmented Generation)**:
  * **Local RAG**: Queries a local contextual database (`market_context.json`) containing historical and seasonal retail trends for 2021–2026 and injects them directly into the LLM prompt.
  * **Web Search Grounding (Gemini)**: Leverages native Google Search grounding to fetch live internet events to explain sales dips or spikes.
* **Defensive Date Parser**: Automatically auto-corrects unsupported date function syntax commonly hallucinated by smaller LLMs (like `YEAR()` or `MONTH()` into DuckDB-compatible `EXTRACT()` functions) before execution.

---

## 🛠️ Technology Stack

* **Semantic Layer**: [Wren AI WebAssembly Core](https://github.com/Canner/WrenAI)
* **In-Memory Database**: DuckDB WASM (running client-side)
* **Data Format**: Columns stored as optimized Apache Parquet tables
* **Frontend**: HTML5, Vanilla CSS (Glassmorphic Dark Mode), Tailwind Font tokens (Outfit), Chart.js
* **LLM Providers**: Local Ollama (`llama3.2`), Google Gemini, and OpenAI

---

## 📂 Project Structure

```
├── models/                     # Wren AI semantic schemas
│   ├── customers/metadata.yml
│   ├── invoices/metadata.yml
│   ├── product_categories/metadata.yml
│   └── purchase_places/metadata.yml
├── relationships.yml           # Relational joins mapping
├── target/                     # Compiled Wren MDL target files
│   └── mdl.json
├── apps/test_app/              # Web Dashboard Application
│   ├── index.html              # Main single-page GenBI application
│   ├── mdl.json                # Copied Wren compiled MDL config
│   └── data/                   
│       ├── customers.parquet   # Local database table snapshots
│       ├── invoices.parquet
│       ├── product_categories.parquet
│       ├── purchase_places.parquet
│       └── market_context.json # RAG knowledge base
├── shopping_data.duckdb        # Main DuckDB local database
├── prepare_duckdb.py           # Database parser & seed script
└── README.md
```

---

## 🚀 How to Run Locally

### Prerequisites
1. **Python 3** (to serve the app and compile database).
2. **Ollama** installed locally (to run queries offline).
   * Pull the Llama 3.2 model in your command line:
     ```bash
     ollama pull llama3.2
     ```
   * Make sure Ollama is running (`ollama serve` or via system tray).

### Step 1: Clone the Repository
```bash
git clone https://github.com/Abhijay30/wren-genbi-dashboard.git
cd wren-genbi-dashboard
```

### Step 2: Serve the Dashboard
You can serve the project using Python's built-in simple HTTP server:
```bash
python -m http.server -d apps/test_app 54841
```
*Open **[http://127.0.0.1:54841](http://127.0.0.1:54841)** in your web browser.*

### Step 3: Run Queries!
1. Wait for the page to display **"Engine Connected"** (it mounts your Parquet files into the browser-side database).
2. Set the **Provider** to `Local Ollama` and ensure the model name is `llama3.2`.
3. Type a query in the natural language search box and hit **Ask AI**!

---

## 📊 Sample Prompts to Try

* **Time Series Trend (Line Chart)**: 
  > *`show me the total sales vs years of the unit pants`*
* **Multi-Metric Comparison (Radar Chart)**: 
  > *`show me total quantity and total price grouped by product category`*
* **Small Category Parts (Doughnut Chart)**: 
  > *`total revenue by store place`*
* **Logical Reasoning & RAG (Text + Chart)**: 
  > *`why was the revenue max at 2022 07`*

---

## 🔒 Security Note
When configuring cloud LLM providers (Gemini or OpenAI), your API keys are entered directly in your browser tab, saved only in local temporary memory, and sent directly to Google/OpenAI endpoints. No keys are ever uploaded to any backend server.
