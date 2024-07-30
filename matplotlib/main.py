import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Function to load data and create visualizations
def visualize_data(data, price_col=None, area_col=None, selected_plots=[]):
    # Display basic information about the dataset
    st.write("### Dataset Information")
    buffer = io.StringIO()
    data.info(buf=buffer)
    info = buffer.getvalue()
    st.text(info)

    st.write("### Dataset Description")
    st.write(data.describe())

    # Automatically determine relevant columns if not specified
    if price_col is None or area_col is None:
        numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
        if len(numerical_columns) < 2:
            st.error("Not enough numerical data to visualize.")
            return
        price_col = numerical_columns[0] if price_col is None else price_col
        area_col = numerical_columns[1] if area_col is None else area_col

    # Check if the specified columns exist in the dataset
    if price_col not in data.columns or area_col not in data.columns:
        st.error(f"Specified columns '{price_col}' or '{area_col}' do not exist in the dataset.")
        return

    # Drop rows where either of the columns has NaN values
    filtered_data = data.dropna(subset=[price_col, area_col])

    # Visualize the data based on selected plots
    if 'Histogram' in selected_plots:
        st.write(f'### Histogram of {price_col}')
        fig, ax = plt.subplots()
        ax.hist(filtered_data[price_col], bins=30, edgecolor='black')
        ax.set_xlabel(price_col)
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

    if f'{area_col} vs {price_col}' in selected_plots:
        st.write(f'### {area_col} vs {price_col}')
        fig, ax = plt.subplots()
        ax.scatter(filtered_data[area_col], filtered_data[price_col], alpha=0.5)
        ax.set_xlabel(area_col)
        ax.set_ylabel(price_col)
        st.pyplot(fig)

    if f'{price_col} Trend' in selected_plots:
        st.write(f'### {price_col} Trend')
        fig, ax = plt.subplots()
        ax.plot(filtered_data[price_col].sort_values().values)
        ax.set_xlabel('Index')
        ax.set_ylabel(price_col)
        st.pyplot(fig)

    if 'Box Plot' in selected_plots:
        st.write(f'### Box Plot of {price_col}')
        fig, ax = plt.subplots()
        ax.boxplot(filtered_data[price_col])
        ax.set_ylabel(price_col)
        st.pyplot(fig)

    if 'Line Plot' in selected_plots:
        st.write(f'### Line Plot of {price_col}')
        fig, ax = plt.subplots()
        ax.plot(filtered_data[price_col])
        ax.set_xlabel('Index')
        ax.set_ylabel(price_col)
        st.pyplot(fig)

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

st.title('Data Visualization App')

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded file
    data = load_data(uploaded_file)

    # Sidebar for user inputs
    st.sidebar.title("Filter and Visualization Options")

    # User input for number of records to fetch
    num_records = st.sidebar.slider('Number of records to fetch', min_value=10, max_value=len(data), value=50, step=10)

    # Limit the data to the specified number of records
    data = data.head(num_records)

    # User input for column selection
    st.sidebar.write('Select columns for visualizations:')
    price_col = st.sidebar.selectbox('Select the price-like column', data.columns)
    area_col = st.sidebar.selectbox('Select the area-like column', data.columns)

    # User input for filtering specific values from the selected columns
    st.sidebar.write('Select specific values for filtering:')
    price_values = st.sidebar.multiselect(f'Select values from {price_col}', data[price_col].unique())
    area_values = st.sidebar.multiselect(f'Select values from {area_col}', data[area_col].unique())

    # Apply filtering based on selected values
    if price_values:
        data = data[data[price_col].isin(price_values)]
    if area_values:
        data = data[data[area_col].isin(area_values)]

    # User input for selecting which plots to display
    st.sidebar.write('Select plots to display:')
    plot_options = ['Histogram', f'{area_col} vs {price_col}', f'{price_col} Trend', 'Box Plot', 'Line Plot']
    selected_plots = st.sidebar.multiselect('Select plots', plot_options)

    # Visualize data
    visualize_data(data, price_col, area_col, selected_plots)

    # Display the first few rows of the dataset
    st.write("### First Few Rows of the Dataset")
    st.write(data.head())
