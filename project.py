import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import seaborn as sns
import matplotlib.pyplot as plt
import plotly

st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir("https://github.com/shazdataconsult/supermarket-dashboard/tree/main")
    

def glowing_css():
    """
    Define CSS for glowing effect on cards.
    """
    st.markdown(
        """
        <style>
        .glow {
            box-shadow: 0 0 20px #00ff00;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 20px;
        }
        .card-title {
            font-size: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    

def create_card(title, value):
    """
    Create a custom card component to display a metric.
    """
    st.markdown(
        f"""
        <div class="glow">
            <h2 class="card-title">{title}</h2>
            <p>{value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    

def main():
    glowing_css()
    st.title("Data Analysis and Visualization")

    # Read the dataset
    df = pd.read_csv("./supermarket_sales.csv")  # Change path as necessary

    # Data preprocessing
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Extract Month Name
    df['Month Name'] = df['Date'].dt.strftime('%B')
    
    # Define the custom order for months
    month_order = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]

    # Convert Month Name to categorical with custom order
    df['Month Name'] = pd.Categorical(df['Month Name'], categories=month_order, ordered=True)

    # Sort the DataFrame by Month Name
    df = df.sort_values(by=['Month Name'])

    # Reset the index after sorting
    df = df.reset_index(drop=True)
    st.sidebar.image("./market.gif")

    # Sidebar for filtering by branch and customer type
    st.sidebar.title("Filters")
    branches = ["All Branches"] + sorted(df["Branch"].astype(str).unique())
    selected_branch = st.sidebar.selectbox("Select Branch", branches)
    
    # Convert the "Customer type" column to strings
    df["Customer type"] = df["Customer type"].astype(str)
    
    # Convert the "Gender" column to strings
    df["Gender"] = df["Gender"].astype(str)
    df["City"] = df["City"].astype(str)
    

    

# Now, create the select box for genders
    selected_gender = st.sidebar.selectbox("Select Gender", ["All Genders"] + sorted(df["Gender"].unique()))

# Now, create the select box for customer types
    selected_customer_type = st.sidebar.selectbox("Select Customer Type", ["All Customer Types"] + sorted(df["Customer type"].unique()))


    selected_city = st.sidebar.selectbox("Select City", ["All Cities"] + sorted(df["City"].unique()))

    
    # Filter the data based on selected branch and customer type
    if selected_branch != "All Branches":
        df = df[df["Branch"] == selected_branch]
    if selected_customer_type != "All Customer Types":
        df = df[df["Customer type"] == selected_customer_type]
    if selected_gender != "All Genders":
        df = df[df["Gender"] == selected_gender]
    if selected_city != "All Cities":
        df = df[df["City"] == selected_city]

    # Calculate total metrics
    total_sales = df["Total"].sum()
    total_cogs = df["cogs"].sum()  # Assuming you have a column named "cogs" for cost of goods sold
    total_profit = total_sales - total_cogs
    total_revenue = total_sales + total_profit
    profit_margin_percentage = (total_profit / total_revenue) * 100

    # Display total metrics using cards in columns
    st.subheader("Total Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        create_card("Total Sales", f"${total_sales:.2f}")
    with col2:
        create_card("Total Profit", f"${total_profit:.2f}")
    with col3:
        create_card("Total Revenue", f"${total_revenue:.2f}")
    with col4:
        create_card("Total Profit Margin", f"{profit_margin_percentage:.2f}%")
        
    col1, col2 = st.columns((2))
    

# Getting the min and max date 
    startDate = pd.to_datetime(df["Date"]).min()
    endDate = pd.to_datetime(df["Date"]).max()

    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date", startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date", endDate))

    df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()
    
    col1,col2=st.columns(2)

    with col1:
        st.subheader("City wise Sales")
        fig = px.pie(df, values = "Total", names = "City", hole = 0.5)
        fig.update_traces(text = df["City"], textposition = "outside")
        st.plotly_chart(fig,use_container_width=True)
    
    with col2:
        st.subheader("Product wise Sales")
        fig = px.bar(df, x = "Product line", y = "cogs", text = ['${:,.2f}'.format(x) for x in df["cogs"]],
        template = "seaborn")
        st.plotly_chart(fig,use_container_width=True, height = 200)
    
    cl1, cl2 = st.columns((2))
    with cl1:
        with st.expander("City_ViewData"):
            total_sales_per_city = df.groupby("City")["Total"].sum()
            st.write(total_sales_per_city)
            csv = total_sales_per_city.to_csv(index = False).encode('utf-8')
            st.download_button("Download Data", data = csv, file_name = "City.csv", mime = "text/csv",
            help = 'Click here to download the data as a CSV file')

    with cl2:
            with st.expander("Product_line_ViewData"):
                total_sales_by_product_line = df.groupby("Product line")["Total"].sum()
                st.write(total_sales_by_product_line)
                csv = total_sales_by_product_line.to_csv(index = False).encode('utf-8')
                st.download_button("Download Data", data = csv, file_name = "Product line.csv", mime = "text/csv",
                help = 'Click here to download the data as a CSV file')
    
    df["month_year"] = df["Date"].dt.to_period("M")
    st.subheader('Time Series Analysis')

    linechart = pd.DataFrame(df.groupby(df["month_year"].dt.strftime("%Y : %b"))["cogs"].sum()).reset_index()
    fig2 = px.line(linechart, x="month_year", y="cogs", labels={"cogs": "Amount"}, height=500, width=1000, template="gridon")
    
    for index, row in linechart.iterrows():
        fig2.add_annotation(x=row['month_year'], y=row['cogs'], text=f"${row['cogs']:.2f}", showarrow=False, font=dict(color="white"))

    st.plotly_chart(fig2, use_container_width=True)


    with st.expander("View Data of TimeSeries:"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')
    
    #Create a treem based on Region, category, sub-Category
    st.subheader("Hierarchical view of Sales using TreeMap")
    fig3 = px.treemap(df, path = ["City","Product line","Gender"], values = "cogs",hover_data = ["cogs"],
    color = "Gender")
    fig3.update_layout(width = 800, height = 650)
    st.plotly_chart(fig3, use_container_width=True)
    
    import plotly.figure_factory as ff
    st.subheader(":point_right: Month wise Sales Summary")
    with st.expander("Summary_Table"):
        df_sample = df[0:5][["Customer type","Branch","City","Total","cogs","Product line","Quantity"]]
        fig = ff.create_table(df_sample, colorscale = "Cividis")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("Month wise sub-Category Table")
        df["month"] = df["Date"].dt.month_name()
        sub_category_Year = pd.pivot_table(data = df, values = "cogs", index = ["City"],columns = "month")
        st.write(sub_category_Year.style.background_gradient(cmap="Blues"))
    
    
    
    chart1, chart2 = st.columns((2))
    with chart1:
        st.subheader('Payment wise Sales')
        fig = px.pie(df, values = "cogs", names = "Payment", template = "plotly_dark")
        fig.update_traces(text = df["Payment"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    with chart2:
        st.subheader('Customer wise Sales')
        fig = px.pie(df, values = "cogs", names = "Customer type", template = "gridon")
        fig.update_traces(text = df["Customer type"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)
    

    scatter_fig = px.scatter(df, x="Total", y="cogs", color="Customer type", size="Quantity", hover_name="Product line", 
                hover_data=["Branch", "City", "Gender", "Date", "Time", "Payment", "Rating"],
                labels={"Total": "Total Revenue", "cogs": "Cost of Goods Sold"},
                title="Scatter Plot of Total Revenue vs Cost of Goods Sold",
                template="plotly")

# Update layout
    scatter_fig.update_layout(title_font=dict(size=20), xaxis=dict(title="Total Revenue", title_font=dict(size=19)),
    yaxis=dict(title="Cost of Goods Sold", title_font=dict(size=19)))

    # Show the scatter plot
    st.plotly_chart(scatter_fig, use_container_width=True)
        
    col1, col2, col3, col4, col5 = st.columns(5)   
        # Total Sales Per Branch
    with col1:   
        st.markdown("<h3 style='font-size: 18px;'>Total Sales By Branch</h3>", unsafe_allow_html=True)
        total_sales_per_branch = df.groupby("Branch")["Total"].sum()
        st.write(total_sales_per_branch)
    with col2:
        # Total Sales Per City
        st.markdown("<h3 style='font-size: 18px;'>Total Sales By City</h3>", unsafe_allow_html=True)
        total_sales_per_city = df.groupby("City")["Total"].sum()
        st.write(total_sales_per_city)
    with col3:
        # Total Sales by Customer Type
        st.markdown("<h3 style='font-size: 18px;'>Total Sales By Customer</h3>", unsafe_allow_html=True)
        total_sales_by_customer_type = df.groupby("Customer type")["Total"].sum()
        st.write(total_sales_by_customer_type)
    with col4:
        # Total Sales by Gender
        st.markdown("<h3 style='font-size: 18px;'>Sales By Gender</h3>", unsafe_allow_html=True)
        total_sales_by_gender = df.groupby("Gender")["Total"].sum()
        st.write(total_sales_by_gender)
    with col5:
        # Total Sales by Product Line (assuming "Product line" column is present)
        st.markdown("<h3 style='font-size: 18px;'>Sales By Product Line</h3>", unsafe_allow_html=True)
        total_sales_by_product_line = df.groupby("Product line")["Total"].sum().round(1)
        st.write(total_sales_by_product_line)  
    col1, col2, col3, col4, col5 = st.columns(5) 
    
    with col1:
            # Average Unit Price
        st.markdown("<h3 style='font-size: 18px;'>Average Unit Price</h3>", unsafe_allow_html=True)
        average_unit_price = df["Unit price"].mean()
        st.write(average_unit_price)
    with col2:
        # Total Quantity Sold
        st.markdown("<h3 style='font-size: 18px;'>Total Quantity Sold</h3>", unsafe_allow_html=True)
        total_quantity_sold = df["Quantity"].sum()
        st.write(total_quantity_sold)
    with col3:
        # Total Tax Amount
        st.markdown("<h3 style='font-size: 18px;'>Total Tax Amount</h3>", unsafe_allow_html=True)
        total_tax_amount = df["Tax 5%"].sum()
        st.write(total_tax_amount)
    with col4:
        # Total Gross Income
        st.markdown("<h3 style='font-size: 18px;'>Total Gross Income</h3>", unsafe_allow_html=True)
        total_gross_income = df["gross income"].sum()
        st.write(total_gross_income)
    with col5:
        # Average Rating
        st.markdown("<h3 style='font-size: 18px;'>Average Rating</h3>", unsafe_allow_html=True)
        average_rating = df["Rating"].mean()
        st.write(average_rating)     

    # Radio button for selecting metric to plot
    st.sidebar.markdown("<h3 style='font-size: 16px;'>Select Metric to Plot</h3>", unsafe_allow_html=True)
    selected_metric = st.sidebar.radio("Metrics", ["Total", "cogs", "gross income", "Rating"])
    

    # Line chart based on selected metric
    st.subheader(f"{selected_metric} Over Months")
    chart_data = df.groupby('Month Name')[selected_metric].sum().reset_index()
    fig = px.line(chart_data, x='Month Name', y=selected_metric, title=f"{selected_metric} Over Months", width=1100)
    
    # Add data labels to the line chart
    for index, row in chart_data.iterrows():
        fig.add_annotation(x=row['Month Name'], y=row[selected_metric], text=f"${row[selected_metric]:.2f}", showarrow=False, font=dict(color="white"))
    
    st.plotly_chart(fig)
    
    col1, col2, col3 =st.columns(3)
    with col1:
        
        
        # Create a container
        container = st.container()

        # Place the image at the top corner of the chart
        with container:
        # Display the image
            st.image("./analytics3.gif", use_column_width=False,width=70)
    
        # Display the bar chart
            st.bar_chart(total_sales_by_product_line, use_container_width=True)
    with col2:
            
        # Create a container
        container = st.container()

        # Place the image at the top corner of the chart
        with container:
        # Display the image
            st.image("./barcode4.gif", use_column_width=False, width=70)
    
        # Display the bar chart
            st.bar_chart(total_sales_by_gender, use_container_width=True) 
    
    with col3:
            
        # Create a container
        container = st.container()

        # Place the image at the top corner of the chart
        with container:
        # Display the image
            st.image("./cal.gif", use_column_width=False, width=70)
    
        # Display the bar chart
            st.bar_chart(total_sales_per_city, use_container_width=True) 

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        create_card("Average Rating", f"${average_rating:.2f}")
    with col2:
        create_card("Average Rating", f"${total_quantity_sold:.2f}")
    with col3:
        create_card("Average Rating", f"${average_unit_price:.2f}")    
    with col4: 
        create_card("Average Rating", f"${total_gross_income:.2f}")
        
    col1,col2=st.columns(2)
    with col1:   
            target_rating = 8.0
            fig_rating = go.Figure(go.Indicator(
            mode="gauge+number",
            value=average_rating,
            domain={'x': [0, 0.5], 'y': [0, 1]},
            title={'text': "Average Customer Rating"},
            gauge={'axis': {'range': [None, 10]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, target_rating], 'color': "lightgray"},
                    {'range': [target_rating, 10], 'color': "gray"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': target_rating}}))
            st.plotly_chart(fig_rating)
            
    with col2:        
            target_sales = 5000
            fig_sales = go.Figure(go.Indicator(
            mode="gauge+number",
            value=(total_sales / target_sales) * 100,
            domain={'x': [0.5, 1], 'y': [0, 1]},
            title={'text': "Sales Performance"},
            gauge={'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}],
                'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}}))
            st.plotly_chart(fig_sales)
if __name__ == "__main__":
    main()
