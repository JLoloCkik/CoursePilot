# src/ui_setup.py

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QScrollArea,
    QLabel, QSizePolicy, QFormLayout, QLineEdit, QListWidget, QDateEdit, QSpinBox
)

import config as cfg


def setup_search_bar(main_window_instance):
    """Sets up the search bar and connects its textChanged signal."""
    search_bar_widget = QWidget()
    search_layout = QHBoxLayout(search_bar_widget)
    search_layout.setContentsMargins(0, 0, 0, 0)
    main_window_instance.search_input = QLineEdit()
    main_window_instance.search_input.setPlaceholderText("Search courses by name...")
    main_window_instance.search_input.setStyleSheet(cfg.FIELD_EDIT_QSS)
    main_window_instance.search_input.textChanged.connect(main_window_instance.update_all_views)

    search_label = QLabel("Search:")  # Create the label
    search_label.setStyleSheet(cfg.FIELD_LABEL_QSS)  # Apply style
    search_layout.addWidget(search_label)
    search_layout.addWidget(main_window_instance.search_input)
    return search_bar_widget


def setup_tab_bar(main_window_instance):
    """Sets up the main navigation tab bar with buttons."""
    tab_bar = QWidget()
    tab_layout = QHBoxLayout(tab_bar)
    tab_layout.setContentsMargins(0, 0, 0, 0)
    tab_layout.setSpacing(1)

    main_window_instance.buttons = []
    for i, txt in enumerate(main_window_instance.tab_labels):
        btn = QPushButton(txt)
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        btn.clicked.connect(lambda _, idx=i: main_window_instance.on_tab_clicked(idx))
        btn.setStyleSheet(cfg.TAB_BUTTON_QSS)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        tab_layout.addWidget(btn)
        main_window_instance.buttons.append(btn)

    add_course_btn = QPushButton("Add Course")
    add_course_btn.setStyleSheet(cfg.TAB_BUTTON_QSS)
    add_course_btn.clicked.connect(main_window_instance.on_add_course_form_show)
    tab_layout.addWidget(add_course_btn)
    return tab_bar


def setup_pages_stack(main_window_instance, roadmap_page_widget):
    """Sets up the QStackedWidget and the individual pages."""
    main_window_instance.pages = QStackedWidget()
    main_window_instance.scrolls = []  # For Progress, Ready, Categories

    for _ in range(3):  # Progress, Ready, Categories
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")  # Remove scroll area border
        main_window_instance.pages.addWidget(scroll)
        main_window_instance.scrolls.append(scroll)

    # Planner Page (Index 3)
    main_window_instance.planner_page_widget = QWidget()
    _setup_planner_tab_content(main_window_instance, main_window_instance.planner_page_widget)
    main_window_instance.pages.addWidget(main_window_instance.planner_page_widget)

    # Roadmap Page (Index 4)
    main_window_instance.pages.addWidget(roadmap_page_widget)

    # Statistics Page (Index 5)
    main_window_instance.statistics_page_widget = QWidget()
    _setup_statistics_tab_content(main_window_instance, main_window_instance.statistics_page_widget)
    main_window_instance.pages.addWidget(main_window_instance.statistics_page_widget)

    # Budget Page (Index 6)
    main_window_instance.budget_page_widget = QWidget()
    _setup_budget_tab_content(main_window_instance, main_window_instance.budget_page_widget)
    main_window_instance.pages.addWidget(main_window_instance.budget_page_widget)

    return main_window_instance.pages


def _setup_statistics_tab_content(mw_instance, page_widget: QWidget):
    layout = QVBoxLayout(page_widget)
    layout.setAlignment(Qt.AlignTop)
    title = QLabel("Course Statistics")
    title.setStyleSheet(cfg.PAGE_LABEL_QSS);
    title.setAlignment(Qt.AlignCenter)
    layout.addWidget(title)
    stats_form_layout = QFormLayout();
    stats_form_layout.setLabelAlignment(Qt.AlignRight)
    mw_instance.stats_total_courses_label = QLabel("0")
    mw_instance.stats_completed_courses_label = QLabel("0")
    mw_instance.stats_inprogress_courses_label = QLabel("0")
    mw_instance.stats_pending_courses_label = QLabel("0")
    mw_instance.stats_total_hours_label = QLabel("0.0 h")
    mw_instance.stats_completed_hours_label = QLabel("0.0 h")
    mw_instance.stats_completion_percentage_label = QLabel("0.0 %")
    mw_instance.stats_estimated_finish_label = QLabel("N/A")
    for label_widget in [mw_instance.stats_total_courses_label, mw_instance.stats_completed_courses_label,
                         mw_instance.stats_inprogress_courses_label, mw_instance.stats_pending_courses_label,
                         mw_instance.stats_total_hours_label, mw_instance.stats_completed_hours_label,
                         mw_instance.stats_completion_percentage_label, mw_instance.stats_estimated_finish_label]:
        label_widget.setStyleSheet(cfg.STAT_VALUE_QSS)
    stats_form_layout.addRow(QLabel("Total Courses:", styleSheet=cfg.STAT_LABEL_QSS),
                             mw_instance.stats_total_courses_label)
    stats_form_layout.addRow(QLabel("Completed Courses:", styleSheet=cfg.STAT_LABEL_QSS),
                             mw_instance.stats_completed_courses_label)
    stats_form_layout.addRow(QLabel("In Progress Courses:", styleSheet=cfg.STAT_LABEL_QSS),
                             mw_instance.stats_inprogress_courses_label)
    stats_form_layout.addRow(QLabel("Pending Courses:", styleSheet=cfg.STAT_LABEL_QSS),
                             mw_instance.stats_pending_courses_label)
    stats_form_layout.addRow(QLabel("Total Course Hours:", styleSheet=cfg.STAT_LABEL_QSS),
                             mw_instance.stats_total_hours_label)
    stats_form_layout.addRow(QLabel("Completed Hours:", styleSheet=cfg.STAT_LABEL_QSS),
                             mw_instance.stats_completed_hours_label)
    stats_form_layout.addRow(QLabel("Overall Completion:", styleSheet=cfg.STAT_LABEL_QSS),
                             mw_instance.stats_completion_percentage_label)
    stats_form_layout.addRow(QLabel("Est. Finish (all courses):", styleSheet=cfg.STAT_LABEL_QSS),
                             mw_instance.stats_estimated_finish_label)
    layout.addLayout(stats_form_layout);
    layout.addStretch()


def _setup_budget_tab_content(mw_instance, page_widget: QWidget):
    layout = QVBoxLayout(page_widget);
    layout.setAlignment(Qt.AlignTop)
    title = QLabel("Budget & Expenses");
    title.setStyleSheet(cfg.PAGE_LABEL_QSS);
    title.setAlignment(Qt.AlignCenter)
    layout.addWidget(title)
    add_expense_form = QFormLayout()
    mw_instance.expense_name_input = QLineEdit();
    mw_instance.expense_name_input.setStyleSheet(cfg.FIELD_EDIT_QSS)
    mw_instance.expense_price_input = QLineEdit();
    mw_instance.expense_price_input.setStyleSheet(cfg.FIELD_EDIT_QSS)
    mw_instance.expense_date_input = QDateEdit(datetime.now().date());
    mw_instance.expense_date_input.setDisplayFormat("yyyy-MM-dd")
    mw_instance.expense_date_input.setCalendarPopup(True);
    mw_instance.expense_date_input.setStyleSheet(cfg.FIELD_EDIT_QSS)
    add_expense_form.addRow(QLabel("Item/Course Name:", styleSheet=cfg.FIELD_LABEL_QSS), mw_instance.expense_name_input)
    add_expense_form.addRow(QLabel("Price:", styleSheet=cfg.FIELD_LABEL_QSS), mw_instance.expense_price_input)
    add_expense_form.addRow(QLabel("Purchase Date:", styleSheet=cfg.FIELD_LABEL_QSS), mw_instance.expense_date_input)
    add_expense_button = QPushButton("Add Expense");
    add_expense_button.setStyleSheet(cfg.TAB_BUTTON_QSS)
    add_expense_button.clicked.connect(mw_instance.on_add_expense_clicked)  # Connect to MainWindow method
    add_expense_form.addRow(add_expense_button);
    layout.addLayout(add_expense_form)
    layout.addWidget(QLabel("Recorded Expenses:", styleSheet=cfg.PAGE_LABEL_QSS))
    mw_instance.expenses_list_widget = QListWidget();
    mw_instance.expenses_list_widget.setStyleSheet(cfg.LIST_WIDGET_QSS)
    layout.addWidget(mw_instance.expenses_list_widget)
    mw_instance.total_spent_label = QLabel("Total Spent: 0.00");
    mw_instance.total_spent_label.setStyleSheet(
        f"color: {cfg.THEME_TEXT_PRIMARY}; font: bold {cfg.FONT_SIZE} {cfg.FONT_FAMILY}; margin-top:10px;")
    mw_instance.total_spent_label.setAlignment(Qt.AlignRight);
    layout.addWidget(mw_instance.total_spent_label);
    layout.addStretch()


def _setup_planner_tab_content(mw_instance, page_widget: QWidget):
    layout = QVBoxLayout(page_widget);
    layout.setAlignment(Qt.AlignTop);
    layout.setSpacing(10)
    title = QLabel("Weekly Study Planner");
    title.setStyleSheet(cfg.PAGE_LABEL_QSS);
    title.setAlignment(Qt.AlignCenter);
    layout.addWidget(title)
    goal_layout = QHBoxLayout();
    goal_layout.addWidget(QLabel("Set Weekly Goal (hours):", styleSheet=cfg.FIELD_LABEL_QSS))
    mw_instance.planner_weekly_goal_input = QLineEdit();
    mw_instance.planner_weekly_goal_input.setPlaceholderText("e.g., 10")
    mw_instance.planner_weekly_goal_input.setStyleSheet(cfg.FIELD_EDIT_QSS);
    mw_instance.planner_weekly_goal_input.setFixedWidth(100)
    goal_layout.addWidget(mw_instance.planner_weekly_goal_input)
    set_goal_btn = QPushButton("Set/Update Goal");
    set_goal_btn.setStyleSheet(cfg.TAB_BUTTON_QSS)
    set_goal_btn.clicked.connect(mw_instance._save_and_update_planner_goal);
    goal_layout.addWidget(set_goal_btn)  # Connect to MainWindow method
    goal_layout.addStretch();
    layout.addLayout(goal_layout)
    mw_instance.planner_days_container = QWidget();
    mw_instance.planner_days_layout = QHBoxLayout(mw_instance.planner_days_container)
    mw_instance.planner_days_layout.setSpacing(10);
    mw_instance.daily_hour_inputs = {}
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for day_name in days_of_week:
        day_widget = QWidget();
        day_v_layout = QVBoxLayout(day_widget);
        day_v_layout.setAlignment(Qt.AlignCenter)
        day_label = QLabel(day_name);
        day_label.setStyleSheet(
            f"font: bold {cfg.PLANNER_DAY_FONT_SIZE} {cfg.FONT_FAMILY}; color: {cfg.THEME_TEXT_PRIMARY};")
        day_v_layout.addWidget(day_label)
        hour_input = QSpinBox();
        hour_input.setRange(0, 24);
        hour_input.setSuffix(" h")
        hour_input.setStyleSheet(cfg.FIELD_EDIT_QSS);
        hour_input.valueChanged.connect(mw_instance._update_planner_summary)  # Connect to MainWindow method
        day_v_layout.addWidget(hour_input);
        mw_instance.daily_hour_inputs[day_name] = hour_input
        mw_instance.planner_days_layout.addWidget(day_widget)
    layout.addWidget(mw_instance.planner_days_container)
    summary_layout = QVBoxLayout()
    mw_instance.planner_total_planned_label = QLabel("Total Planned this Week: 0.0 / 0.0 hours (Goal)")
    mw_instance.planner_total_planned_label.setStyleSheet(cfg.FIELD_LABEL_QSS);
    summary_layout.addWidget(mw_instance.planner_total_planned_label)
    mw_instance.planner_suggestion_label = QLabel("Daily suggestion: N/A hours")
    mw_instance.planner_suggestion_label.setStyleSheet(cfg.FIELD_LABEL_QSS);
    summary_layout.addWidget(mw_instance.planner_suggestion_label)
    layout.addLayout(summary_layout);
    layout.addStretch()
