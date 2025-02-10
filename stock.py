import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit UI
st.title("📊 Warehouse Stock Trend Visualization")

# Display required columns below the title
st.subheader("📌 **Required Columns:**")
st.write("The uploaded file must include the following columns:")
st.write("1. **Category**")
st.write("2. **Model**")
st.write("3. **In**")
st.write("4. **Out**")
st.write("5. **Closing Balance**")
st.write("6. **Opening Balance**")

# File upload
uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read the file
    file_extension = uploaded_file.name.split(".")[-1]
    
    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("📌 **Preview of Data:**")
    st.dataframe(df.head())
    
    df.columns = df.columns.str.strip()

    # Required columns
    required_columns = ["Category", "Model", "In", "Out", "Closing Balance", "Opening Balance"]
    
    missing_cols = [col for col in required_columns if col not in df.columns]

    if missing_cols:
        st.error(f"⚠️ Missing required columns: {', '.join(missing_cols)}")
    else:
        # Ensure required columns exist
        if all(col in df.columns for col in required_columns):
            
            # 📊 Bar Chart: Stock In vs. Stock Out by Model
            st.subheader("📌 Stock In vs. Stock Out by Model")
            fig_bar = px.bar(
                df,
                x="Model",
                y=["In", "Out"],
                title="Stock In vs. Stock Out",
                barmode="group",
                labels={"value": "Stock Count", "Model": "Laptop Model"}
            )
            st.plotly_chart(fig_bar)

            # 🥧 Pie Chart: Stock Distribution by Category
            st.subheader("📌 Stock Distribution by Category")
            fig_pie = px.pie(
                df,
                names="Category",
                values="Closing Balance",
                title="Stock Distribution by Category"
            )
            st.plotly_chart(fig_pie)

            # 📊 Stacked Bar Chart: Opening, In, Out, Closing
            st.subheader("📌 Stock Movement Overview")
            fig_stack = px.bar(
                df,
                x="Model",
                y=["Opening Balance", "In", "Out", "Closing Balance"],
                title="Opening vs. Stock In vs. Stock Out vs. Closing",
                barmode="relative",
                labels={"value": "Stock Count", "Model": "Laptop Model"}
            )
            st.plotly_chart(fig_stack)


            # 🧮 Automated Insights
            st.subheader("📌 Automated Insights")

            # Stock Depletion Rate (difference between opening balance and closing balance)
            df['Stock Depletion'] = df['Opening Balance'] - df['Closing Balance']
            avg_depletion_rate = df['Stock Depletion'].mean()
            st.write(f"📊 **Average Stock Depletion Rate:** {avg_depletion_rate:,.2f} units")

            # Total Stock In and Stock Out
            total_stock_in = df["In"].sum()
            total_stock_out = df["Out"].sum()
            st.write(f"📊 **Total Stock In:** {total_stock_in:,.0f} units")
            st.write(f"📊 **Total Stock Out:** {total_stock_out:,.0f} units")

            # Stock Movement by Category
            stock_movement_by_category = df.groupby("Category")[["In", "Out"]].sum()

            # Top 5 Models by Stock Turnover Rate
            df['Turnover Rate'] = df['Out'] / df['Opening Balance']
            turnover_rate = df[['Model', 'Turnover Rate']].sort_values(by='Turnover Rate', ascending=False).reset_index(drop=True).head(5)

            # Display side by side using columns
            col1, col2 = st.columns(2)

            # First column: Stock Movement by Category
            with col1:
                st.write("📊 **Stock Movement by Category:**")
                st.dataframe(stock_movement_by_category)
                
                    # Stock In vs Stock Out Comparison (identify if stock out exceeds stock in)
            stock_in_out_comparison = df[df['Out'] > df['In']]
            if not stock_in_out_comparison.empty:
                with col2:
                    st.write("⚠️ **Models Where Stock Out Exceeds Stock In:**")
                    st.dataframe(stock_in_out_comparison[['Model', 'In', 'Out']].reset_index(drop=True))

            # Low Stock Warning (models with less than 5 units)
            low_stock_threshold = 5
            low_stock_models = df[df['Closing Balance'] < low_stock_threshold]
            if not low_stock_models.empty:
                with col1:
                    st.write("⚠️ **Low Stock Models:**")
                    st.dataframe(low_stock_models[['Model', 'Closing Balance']].reset_index(drop=True))

                    # Second column: Top 5 Models by Stock Turnover Rate
            with col2:
                st.write("📊 **Top 5 Models by Stock Turnover Rate:**")
                st.dataframe(turnover_rate)

        else:
            missing_cols = [col for col in required_columns if col not in df.columns]
            st.warning(f"⚠️ Missing required columns: {', '.join(missing_cols)}")
