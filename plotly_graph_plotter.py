import sys
import pandas as pd
import pyttsx3
import plotly.express as px
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QComboBox,
    QLabel, QFileDialog, QMessageBox, QGraphicsScene, QGraphicsView, QScrollArea
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QStandardPaths
import google.generativeai as genai
from PIL import Image


# Configure API key directly
genai.configure(api_key="USE YOUR API KEY FORM GOOGLE gemini AI ")


# Base Window Class for Styling
class StyledWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: green;
                font-size: 16px;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: green;
                color: black;
                font-size: 16px;
                border: 1px solid green;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: lightgreen;
            }
            QComboBox {
                background-color: black;
                color: green;
                border: 1px solid green;
                padding: 5px;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
            }
            QScrollArea {
                background-color: #2f2f2f;
                border: 1px solid green;
            }
        """)
        self.setGeometry(100, 100, 1200, 800)  # Set size and position for all windows


class PlotlyGraphPlotter(QMainWindow, StyledWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plotly Graph Plotter with Analysis")
        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: green;
                font-size: 16px;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                background-color: green;
                color: black;
                font-size: 16px;
                border: 1px solid green;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: lightgreen;
            }
            QComboBox {
                background-color: black;
                color: green;
                border: 1px solid green;
                padding: 5px;
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: green;
            }
            QScrollArea {
                background-color: #2f2f2f;
                border: 1px solid green;
            }
            QGraphicsView {
                border: 2px solid green;
            }
        """)

        # Main layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Variables for graph plotting and analysis
        self.data_for_graph = None
        self.x_column = None
        self.y_column = None
        self.graph_image_path = QStandardPaths.writableLocation(QStandardPaths.TempLocation) + "/temp_graph.png"
        self.analysis_result = None

        # Buttons and inputs
        self.file_button = QPushButton("Upload CSV")
        self.file_button.setStyleSheet("background-color: #1f1f1f; color: white;")
        self.file_button.clicked.connect(self.load_csv)
        self.layout.addWidget(self.file_button)

        self.x_label = QLabel("Select X-axis Column:")
        self.layout.addWidget(self.x_label)
        self.x_combobox = QComboBox()
        self.layout.addWidget(self.x_combobox)

        self.y_label = QLabel("Select Y-axis Column:")
        self.layout.addWidget(self.y_label)
        self.y_combobox = QComboBox()
        self.layout.addWidget(self.y_combobox)

        self.graph_label = QLabel("Select Graph Type:")
        self.layout.addWidget(self.graph_label)
        self.graph_combobox = QComboBox()
        self.graph_combobox.addItems(["lineplot", "scatterplot", "barplot", "histogram", "boxplot", "violinplot", "areaplot", "piechart", "funnelplot", "densityheatmap", "densitycontour", "treemap", "sunburst", "parallelcoordinates", "parallelcategories"])
        self.layout.addWidget(self.graph_combobox)

        self.plot_button = QPushButton("Plot Graph")
        self.plot_button.setStyleSheet("background-color: #1f1f1f; color: white;")
        self.plot_button.clicked.connect(self.plot_graph)
        self.layout.addWidget(self.plot_button)

        self.download_button = QPushButton("Download Graph Image")
        self.download_button.setStyleSheet("background-color: #1f1f1f; color: white;")
        self.download_button.clicked.connect(self.download_graph_image)
        self.layout.addWidget(self.download_button)

        self.analyze_button = QPushButton("Analyze Graph")
        self.analyze_button.setStyleSheet("background-color: #1f1f1f; color: white;")
        self.analyze_button.clicked.connect(self.analyze_graph)
        self.layout.addWidget(self.analyze_button)

        # Image display
        self.graph_scene = QGraphicsScene()
        self.graph_view = QGraphicsView(self.graph_scene)
        self.layout.addWidget(self.graph_view)

        # Scroll area for analysis results
        self.analysis_label = QLabel("Analysis Results:")
        self.analysis_label.setStyleSheet("background-color: #2f2f2f; color: white; padding: 10px;")

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.analysis_label)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(150)
        self.layout.addWidget(self.scroll_area)

        self.speech_button = QPushButton("Read Analysis Aloud")
        self.speech_button.setStyleSheet("background-color: #1f1f1f; color: white;")
        self.speech_button.clicked.connect(self.read_analysis)
        self.layout.addWidget(self.speech_button)

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                self.data_for_graph = pd.read_csv(file_path)
                self.x_combobox.clear()
                self.y_combobox.clear()
                self.x_combobox.addItems(self.data_for_graph.columns)
                self.y_combobox.addItems(self.data_for_graph.columns)
                QMessageBox.information(self, "Success", "CSV file loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load CSV: {str(e)}")

    def plot_graph(self):
        if self.data_for_graph is None:
            QMessageBox.warning(self, "Warning", "Please upload a CSV file first.")
            return

        self.x_column = self.x_combobox.currentText()
        self.y_column = self.y_combobox.currentText()
        graph_type = self.graph_combobox.currentText()

        try:
            fig = None
            if graph_type == "lineplot":
                fig = px.line(self.data_for_graph, x=self.x_column, y=self.y_column, title="Line Plot")
            elif graph_type == "scatterplot":
                fig = px.scatter(self.data_for_graph, x=self.x_column, y=self.y_column, title="Scatter Plot")
            elif graph_type == "barplot":
                fig = px.bar(self.data_for_graph, x=self.x_column, y=self.y_column, title="Bar Plot")
            elif graph_type == "histogram":
                fig = px.histogram(self.data_for_graph, x=self.x_column, title="Histogram")
            elif graph_type == "boxplot":
                fig = px.box(self.data_for_graph, x=self.x_column, y=self.y_column, title="Box Plot")
            elif graph_type == "violinplot":
                fig = px.violin(self.data_for_graph, x=self.x_column, y=self.y_column, title="Violin Plot")
            elif graph_type == "areaplot":
                fig = px.area(self.data_for_graph, x=self.x_column, y=self.y_column, title="Area Plot")
            elif graph_type == "piechart":
                fig = px.pie(self.data_for_graph, names=self.x_column, values=self.y_column, title="Pie Chart")
            elif graph_type == "funnelplot":
                fig = px.funnel(self.data_for_graph, x=self.x_column, y=self.y_column, title="Funnel Plot")
            elif graph_type == "densityheatmap":
                fig = px.density_heatmap(self.data_for_graph, x=self.x_column, y=self.y_column, title="Density Heatmap")
            elif graph_type == "densitycontour":
                fig = px.density_contour(self.data_for_graph, x=self.x_column, y=self.y_column, title="Density Contour")
            elif graph_type == "treemap":
                fig = px.treemap(self.data_for_graph, path=[self.x_column], values=self.y_column, title="Treemap")
            elif graph_type == "sunburst":
                fig = px.sunburst(self.data_for_graph, path=[self.x_column], values=self.y_column, title="Sunburst")
            elif graph_type == "parallelcoordinates":
                fig = px.parallel_coordinates(self.data_for_graph, dimensions=[self.x_column, self.y_column], title="Parallel Coordinates")
            elif graph_type == "parallelcategories":
                fig = px.parallel_categories(self.data_for_graph, dimensions=[self.x_column, self.y_column], title="Parallel Categories")

            if fig:
                fig.write_image(self.graph_image_path)
                pixmap = QPixmap(self.graph_image_path)
                self.graph_scene.clear()
                self.graph_scene.addPixmap(pixmap)
                self.graph_view.setScene(self.graph_scene)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to plot graph: {str(e)}")

    def download_graph_image(self):
        if not self.graph_image_path:
            QMessageBox.warning(self, "No Graph", "No graph has been plotted.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Graph Image", "", "PNG Files (*.png)")
        if file_path:
            try:
                pixmap = QPixmap(self.graph_image_path)
                pixmap.save(file_path)
                QMessageBox.information(self, "Success", "Graph image saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save image: {str(e)}")

    def analyze_graph(self):
        if not self.graph_image_path:
            QMessageBox.warning(self, "Warning", "Please plot a graph first.")
            return

        try:
            with open(self.graph_image_path, "rb") as image_file:
                uploaded_file = genai.upload_file(image_file,mime_type="image/png")
                model = genai.GenerativeModel("gemini-1.5-flash")
                analysis_result = model.generate_content(
                    [uploaded_file, "give the best Analyze this graph."]
                )
                self.analysis_label.setText(analysis_result.text)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to analyze graph: {str(e)}")

    def read_analysis(self):
        if self.analysis_label.text():
            engine = pyttsx3.init()
            engine.say(self.analysis_label.text())
            engine.runAndWait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotlyGraphPlotter()
    window.show()
    sys.exit(app.exec_())
