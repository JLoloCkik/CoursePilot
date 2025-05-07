# src/tab_content_manager.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
import config as cfg
from course_card import CourseCard  # Assuming course_card.py is in the same directory (src)


def populate_scroll_area_with_cards(scroll_area_widget, courses_to_display, on_course_data_changed_callback):
    """
    Clears the given QScrollArea's widget and populates it with new CourseCards.
    Args:
        scroll_area_widget (QScrollArea): The scroll area to populate.
        courses_to_display (list[Course]): List of Course objects to display.
        on_course_data_changed_callback (callable): Callback for when card data changes.
    """
    content_widget = QWidget()
    vbox = QVBoxLayout(content_widget)
    vbox.setContentsMargins(5, 5, 5, 5)
    vbox.setSpacing(5)
    vbox.setAlignment(Qt.AlignTop)  # Align cards to the top

    if not courses_to_display:
        empty_label = QLabel("No courses match the current filters.")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setStyleSheet(cfg.PAGE_LABEL_QSS)  # Use a general page label style
        vbox.addWidget(empty_label)
    else:
        for course in courses_to_display:
            card = CourseCard(course, on_course_data_changed_callback)
            vbox.addWidget(card)

    vbox.addStretch()  # Ensures cards don't stretch vertically if few
    scroll_area_widget.setWidget(content_widget)


def update_categories_tab(scroll_area_widget, all_courses, active_status_filters, search_term,
                          on_course_data_changed_callback):
    """Updates the content of the Categories tab's QScrollArea."""
    content_widget = QWidget()
    vbox_cat = QVBoxLayout(content_widget)
    vbox_cat.setContentsMargins(5, 5, 5, 5)
    vbox_cat.setSpacing(10)  # More spacing between categories
    vbox_cat.setAlignment(Qt.AlignTop)

    cats = {}
    found_in_categories = False
    for c in all_courses:
        if c.status in active_status_filters and search_term in c.name.lower():
            cats.setdefault(c.category, []).append(c)
            found_in_categories = True

    if not found_in_categories:
        empty_label = QLabel("No courses match the current filters.")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setStyleSheet(cfg.PAGE_LABEL_QSS)
        vbox_cat.addWidget(empty_label)
    else:
        for cat, clist in sorted(cats.items()):
            header = QLabel(cat)
            header.setStyleSheet(
                f"font: bold 18pt {cfg.FONT_FAMILY}; color: {cfg.THEME_TEXT_PRIMARY}; margin-top: 10px; margin-bottom: 5px; border-bottom: 1px solid {cfg.THEME_BORDER}; padding-bottom: 2px;")
            vbox_cat.addWidget(header)
            if not clist:
                empty_cat_label = QLabel("  No courses in this category match the filters.")
                empty_cat_label.setStyleSheet(
                    f"font-style: italic; color: {cfg.THEME_TEXT_SECONDARY}; margin-left: 10px;")
                vbox_cat.addWidget(empty_cat_label)
            else:
                for course in clist:
                    vbox_cat.addWidget(CourseCard(course, on_course_data_changed_callback))
    vbox_cat.addStretch()
    scroll_area_widget.setWidget(content_widget)

