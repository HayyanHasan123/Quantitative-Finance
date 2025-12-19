# Business Analytics Dashboard (Calculation-Based)

# Overview
This project is a **Business Analytics Dashboard** built using **React**, **Recharts**, and **Lucide Icons**. The dashboard is designed to provide **data-driven insights** by visualizing key business performance metrics derived from underlying calculations rather than static values.

The system follows a **calculation-first approach**, where raw business data is processed to generate meaningful KPIs and visual analytics.

# Objectives
- Transform raw business data into actionable insights
- Perform revenue, profit, and growth calculations dynamically
- Visualize calculated metrics using interactive charts
- Demonstrate real-world business analytics dashboard design

# Key Performance Indicators (KPIs)
- Total Revenue (calculated from regional sales data)
- Total Orders
- Active Customers
- Revenue Growth Rate
- Monthly Revenue and Profit Trends

# Data Processing Logic
- Revenue values are aggregated from transactional data
- Product-wise sales percentages are computed for distribution analysis
- Regional revenues are calculated using grouped sales data
- Monthly revenue and profit are derived through time-based aggregation
- Growth rates are computed by comparing current and previous periods

# Charts and Visualizations
- Pie Chart: Product-wise sales distribution based on calculated percentages
- Bar Chart: Revenue contribution by region derived from aggregated data
- Line Chart: Monthly revenue and profit trends calculated over time
- KPI Cards: Display real-time computed business metrics

# Technologies Used
- React
- Recharts
- Lucide Icons
- JavaScript (ES6)
- CSS-in-JS Styling

# Dashboard Features
- Dynamic KPI updates based on calculated values
- Responsive layout for different screen sizes
- Interactive tooltips and legends
- Date range filtering for recalculating metrics
- Modular and scalable component structure

# Calculation Methodology
- Uses array transformations (`map`, `reduce`, `filter`) for analytics
- Aggregates raw data into summarized metrics
- Converts numerical results into chart-compatible formats
- Ensures separation between data logic and UI components

# Project Structure
- Raw data ingestion layer
- Calculation and aggregation layer
- Visualization and UI layer
- State management for user-selected filters

# Use Cases
- Business performance monitoring
- Sales and revenue analytics
- Management reporting dashboards
- Frontend data visualization projects
- Academic and portfolio demonstrations

# Scalability
- Can be connected to APIs or databases for live data
- Easily extendable to include additional KPIs
- Supports integration with backend analytics engines
- Suitable foundation for real-world SaaS dashboards

# Author
- Syed Muhammad Hayyan Hasan

# Disclaimer
This dashboard is developed for educational and portfolio purposes. All analytics and visualizations are intended to demonstrate calculation-based business intelligence concepts and should not be used as production-grade financial reporting.
