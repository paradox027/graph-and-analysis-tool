# graph-and-analysis-tool

# PyQt5 Plotly Interactive Graph Plotting Tool

Overview

This project is a PyQt5-based application that integrates Plotly for interactive graph plotting and includes a user authentication system. It allows users to:

Sign up and log in using a secure authentication system with a MySQL backend.

Upload CSV files for data analysis and visualization.

Plot interactive graphs using Plotly.

Analyze the generated graphs and download them as images.

Use text-to-speech (TTS) for graph analysis.

# Features

1. Authentication

Sign Up: Create a new user account with unique credentials.

Login: Access the application by verifying credentials.

Error Handling: Displays appropriate messages for invalid inputs or duplicate usernames.

2. Graph Plotting

Upload CSV: Select a CSV file to populate the data columns.

Interactive Graphs: Plot various graph types (line, bar, scatter, pie) with options to customize axes.

Download Graphs: Save the plotted graphs as image files for offline use.

Graph Analysis: Generate textual insights based on the data visualization.

3. Additional Tools

Text-to-Speech: Convert the graph analysis text into speech using pyttsx3.

AI Integration (Optional): Use Google Generative AI for advanced data analysis.

Prerequisites

Software Requirements

Python 3.x

MySQL server (via XAMPP/WAMP or standalone installation)

Python Libraries

Install the required libraries using the command:

pip install -r requirements.txt

Dependencies:

PyQt5

pandas

mysql-connector-python

plotly

pyttsx3

Pillow

google-generativeai

Installation

Clone the repository:

git clone https://github.com/your-repo-url/pyqt5-plotly-tool.git
cd pyqt5-plotly-tool

Set up the MySQL database:

Start MySQL server using XAMPP/WAMP.

Create a database and table:

CREATE DATABASE user_auth;
USE user_auth;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

Install dependencies:

pip install -r requirements.txt

Run the application:

python app1.py

Usage

Authentication

Open the application.

Use the "Sign Up" form to register a new account.

Log in with valid credentials.

Graph Plotting

Upload a CSV file.

Select columns for the x and y axes.

Choose the graph type (line, bar, scatter, or pie).

Click "Plot" to generate the graph.

Save the graph as an image or analyze the graph using the provided tools.

Optional Features

Use the text-to-speech feature to hear the analysis.

Enable AI-based analysis by configuring the Google Generative AI API key.

Project Structure

project_directory/
│
├── app1.py                 # Main authentication logic
├── plotly_graph_plotter.py # Graph plotting and analysis logic
├── requirements.txt        # List of dependencies
├── README.md               # Documentation
└── sample_data.csv         # Sample dataset for testing

Configuration

Google Generative AI API

To use AI-based analysis, set up the API key:

Obtain an API key from Google.

Add it to the plotly_graph_plotter.py file:

import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")

Troubleshooting

Common Issues

Database Connection Errors:

Ensure the MySQL server is running.

Verify database credentials in the app1.py file.

Library Import Errors:

Ensure all dependencies are installed using pip install -r requirements.txt.

Graph Not Displaying:

Verify the CSV file format and ensure selected columns contain numeric data.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments

PyQt5: For GUI development.

Plotly: For interactive graph visualization.

Google Generative AI: For advanced graph analysis.

MySQL: For managing user authentication.

