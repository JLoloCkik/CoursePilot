# src/roadmap_dashboard.py
import json
import os

from PySide6.QtGui import QTextOption  # For word wrap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

import config as cfg  # For theme and style constants

# Path to the roadmap JSON data file, relative to this script's location
# Assumes this script is in 'src' and 'data' is a sibling directory to 'src'
ROADMAP_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),  # Current script's directory (e.g., src)
    "..",  # Go up one level (to project root)
    "data",  # Go into 'data' directory
    "roadmap_data.json"  # The JSON file
)


class RoadmapWidget(QWidget):
    """
    A widget to display the learning roadmap from a JSON file
    as formatted HTML in a QTextEdit.
    """

    def __init__(self):
        super().__init__()
        self._setup_ui()
        self.load_and_display_roadmap()

    def _setup_ui(self):
        """Initializes the UI components for this widget."""
        self.layout = QVBoxLayout(self)  # Main layout for this widget
        self.layout.setContentsMargins(0, 0, 0, 0)  # No external margins for the layout itself

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  # User cannot edit the roadmap display
        self.text_edit.setStyleSheet(# Styles for the QTextEdit area itself
            f"QTextEdit {{"
            f" color: {cfg.THEME_TEXT_PRIMARY};"  # Default text color from config
            f" font: {cfg.FONT_SIZE} {cfg.FONT_FAMILY};"  # Base font from config
            f" background-color: {cfg.THEME_BACKGROUND_DARK};"  # Dark background
            f" border: none;"  # No border for the QTextEdit
            f" padding: 10px;"  # Internal padding
            f"}}")
        self.text_edit.setWordWrapMode(QTextOption.WordWrap)  # Enable word wrapping
        self.layout.addWidget(self.text_edit)  # Add QTextEdit to the layout

    def _generate_html_from_data(self, data: dict) -> str:

        # Start HTML content with a body tag for global text color
        html_content = f"<body style='color:{cfg.THEME_TEXT_PRIMARY};'>"

        # Main title and update information
        html_content += f"<h1>{data.get('title', 'Learning Roadmap')}</h1>"
        html_content += (f"<p style='font-size:10pt; color:{cfg.THEME_TEXT_SECONDARY}; margin-bottom:15px;'>"
                         f"<i>Updated: {data.get('updated', 'N/A')}</i></p>")

        # Summary section
        summary = data.get('summary', {})
        if summary:  # Only add summary if it exists
            html_content += f"<h2 style='color:{cfg.THEME_TEXT_SECONDARY}; border-bottom: 1px solid {cfg.THEME_BORDER}; padding-bottom: 5px;'>Summary</h2>"
            html_content += "<div style='padding-left: 10px; margin-bottom:15px;'>"  # Indent summary
            html_content += f"<p>Courses: {summary.get('courses_count', 'N/A')}<br>"
            html_content += f"Total Time: ~{summary.get('total_estimated_time_hours', 'N/A')} hours<br>"
            html_content += f"Knowledge Coverage: ~{summary.get('knowledge_coverage_percent', 'N/A')}% ({summary.get('knowledge_areas', 'N/A')})</p>"
            html_content += "</div>"
        # html_content += f"<hr style='border-color: {cfg.THEME_BORDER};'>" # Horizontal rule after summary

        # Iterate through sections and their courses
        for section in data.get('sections', []):
            html_content += f"<h2 style='color:{cfg.THEME_TEXT_PRIMARY}; margin-top:20px; border-bottom: 1px solid {cfg.THEME_BORDER_LIGHT}; padding-bottom:3px;'>{section.get('id', '')}. {section.get('title', 'Section')}</h2>"
            if section.get('goal'):
                html_content += f"<p style='color:{cfg.THEME_TEXT_SECONDARY}; font-style:italic; margin-left:10px;'>🎯 Goal: {section.get('goal')}</p>"
            if section.get('note'):
                html_content += f"<p style='color:{cfg.THEME_ACCENT}; font-weight:bold; margin-left:10px;'>{section.get('note')}</p>"

            html_content += "<ul style='list-style-type: none; padding-left: 15px; margin-top: 5px;'>"  # Indent course list
            for course in section.get('courses', []):
                status_icon = course.get('status_icon', '')
                course_name = course.get('name', 'Unknown Course')
                course_hours = course.get('hours', 'N/A')
                course_note = course.get('note', '')
                note_html = f" <i style='color:{cfg.THEME_TEXT_SECONDARY};'>({course_note})</i>" if course_note else ""

                html_content += (f"<li style='margin-bottom: 8px;'>"  # Increased margin for better readability
                                 f"<span style='font-size: 1.2em; margin-right: 5px;'>{status_icon}</span> "
                                 f"<strong>{course_name}</strong> – {course_hours}h{note_html}"
                                 "</li>")
            html_content += "</ul>"  # No <hr> after each section for a cleaner look, sections are separated by H2 with border-bottom
        html_content += "</body>"
        return html_content

    def load_and_display_roadmap(self):
        """Loads roadmap data from the JSON file and displays it as HTML."""
        try:
            with open(ROADMAP_JSON_PATH, 'r', encoding='utf-8') as f:
                roadmap_data = json.load(f)
        except FileNotFoundError:
            error_html = (f"<h2 style='color:{cfg.THEME_TEXT_PRIMARY};'>Roadmap Data Not Found!</h2>"
                          f"<p style='color:{cfg.THEME_TEXT_PRIMARY};'>Please create the file at:<br>{ROADMAP_JSON_PATH}</p>")
            self.text_edit.setHtml(error_html)
            return
        except json.JSONDecodeError as e:
            error_html = (f"<h2 style='color:{cfg.THEME_TEXT_PRIMARY};'>Error Decoding Roadmap Data!</h2>"
                          f"<p style='color:{cfg.THEME_TEXT_PRIMARY};'>Please check syntax in:<br>{ROADMAP_JSON_PATH}<br><br>Error: {e}</p>")
            self.text_edit.setHtml(error_html)
            return

        html_output = self._generate_html_from_data(roadmap_data)
        self.text_edit.setHtml(html_output)
