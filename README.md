# Sales Analytics Dashboard

An interactive dashboard built with Streamlit and PyVizzu to visualize synthetic sales data.

## Features

- Interactive visualization of sales data by product category
- Animated transitions between different views
- Summary statistics
- Raw data view option
- Synthetic data generation for testing

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Data Structure

The dashboard uses synthetic data generated with the following structure:

### Product Nomenclature
- product_id: Unique identifier for each product
- product_type: Category (MEUBLE or DECO)
- product_name: Name of the product

### Transactions
- transaction_id: Unique identifier for each transaction
- date: Transaction date
- order_id: Order identifier
- client_id: Customer identifier
- prod_id: Product identifier
- prod_price: Product price
- prod_qty: Quantity sold

## Usage

1. The main chart shows product sales distribution
2. Use the animation controls to switch between different views
3. View summary statistics in the metrics section
4. Toggle the "Show Raw Data" checkbox to see the complete dataset

## Dependencies

- streamlit
- ipyvizzu
- pandas
- loguru
