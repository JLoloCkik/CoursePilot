# src/app.py

import sys
from datetime import datetime, timedelta

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox,
                               QFormLayout, QLabel, QLineEdit, QComboBox, QDateEdit, )

import config as cfg
import save_database as db
import tab_content_manager
# Import new UI setup and tab content manager
import ui_setup
from courses import Course
from roadmap_dashboard import RoadmapWidget

courses_list = []  # Global list, managed by MainWindow
expenses_list = []  # Global list, managed by MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CoursePilot App")
        self.setGeometry(100, 100, 1150, 850)  # Slightly wider for more tabs
        self.setStyleSheet(cfg.APP_STYLE)

        # This will be created by ui_setup
        self.roadmap_page = RoadmapWidget()  # Keep this if RoadmapWidget is complex

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)

        # Setup UI elements using ui_setup.py
        self.tab_labels = ["Progress", "Ready", "Categories", "Planner", "Roadmap", "Statistics", "Budget"]

        search_bar = ui_setup.setup_search_bar(self)  # Pass self (MainWindow instance)
        main_layout.addWidget(search_bar)

        tab_bar_widget = ui_setup.setup_tab_bar(self)
        main_layout.addWidget(tab_bar_widget)

        pages_stack = ui_setup.setup_pages_stack(self, self.roadmap_page)  # Pass self and roadmap_page
        main_layout.addWidget(pages_stack)

        # Initialize database and load data
        db.init_db()
        db.populate_db_from_json_if_empty()
        self.load_all_data()

        # Set default tab and update views
        if self.buttons:  # Ensure buttons list is not empty
            self.buttons[0].setChecked(True)
            self.pages.setCurrentIndex(0)
        self.update_all_views()

    def load_all_data(self):
        global courses_list, expenses_list
        loaded_courses = db.load_from_db()
        courses_list.clear()
        courses_list.extend(loaded_courses)
        loaded_expenses = db.load_expenses()
        expenses_list.clear()
        expenses_list.extend(loaded_expenses)

    def update_all_views(self):
        """Central method to refresh all dynamic views."""
        self.update_course_card_tabs()
        self.update_statistics_tab_content()
        self.update_budget_tab_content()

        current_tab_index = self.pages.currentIndex()
        if 0 <= current_tab_index < len(self.tab_labels):
            current_tab_label = self.tab_labels[current_tab_index]
            if current_tab_label == "Planner":
                self._load_planner_data_and_update_summary()  # From ui_setup, now a method of self
            elif current_tab_label == "Roadmap":
                roadmap_widget = self.pages.widget(current_tab_index)
                if isinstance(roadmap_widget, RoadmapWidget):
                    roadmap_widget.load_and_display_roadmap()

    def on_tab_clicked(self, index: int):
        self.pages.setCurrentIndex(index)
        # update_all_views will be called by setCurrentIndex if it triggers a signal,
        # or we can call it explicitly if needed.
        # For simplicity, let's assume setCurrentIndex doesn't auto-trigger a full view update
        # in a way that covers all our needs, so we call it.
        self.update_all_views()

    # --- Methods for specific tab content updates ---
    def update_statistics_tab_content(self):
        # ... (Logic from your previous app.py, ensure self.stats_..._labels are attributes of MainWindow)
        total_courses = len(courses_list)
        completed_courses = sum(1 for c in courses_list if c.status == "Completed")
        inprogress_courses = sum(1 for c in courses_list if c.status == "In Progress")
        pending_courses = sum(1 for c in courses_list if c.status == "Pending")
        total_hours_all_courses = sum(c.length for c in courses_list)
        total_completed_hours = sum(c.get_completed_hours() for c in courses_list)
        overall_completion_percentage = (
                total_completed_hours / total_hours_all_courses * 100) if total_hours_all_courses > 0 else 0.0

        # Ensure these labels are created in _setup_statistics_tab_content (now in ui_setup.py)
        # and are attributes of self (e.g., self.stats_total_courses_label)
        if hasattr(self, 'stats_total_courses_label'):
            self.stats_total_courses_label.setText(str(total_courses))
            self.stats_completed_courses_label.setText(str(completed_courses))
            self.stats_inprogress_courses_label.setText(str(inprogress_courses))
            self.stats_pending_courses_label.setText(str(pending_courses))
            self.stats_total_hours_label.setText(f"{total_hours_all_courses:.1f} h")
            self.stats_completed_hours_label.setText(f"{total_completed_hours:.1f} h")
            self.stats_completion_percentage_label.setText(f"{overall_completion_percentage:.1f} %")

            remaining_hours_total = total_hours_all_courses - total_completed_hours
            if remaining_hours_total <= 0:
                self.stats_estimated_finish_label.setText("All courses completed!")
            else:
                assumed_daily_study_hours = 1.0  # Placeholder
                if assumed_daily_study_hours > 0:
                    days_to_finish = remaining_hours_total / assumed_daily_study_hours
                    finish_date = datetime.now() + timedelta(days=days_to_finish)
                    self.stats_estimated_finish_label.setText(
                        f"Approx. {days_to_finish:.0f} days ({finish_date.strftime('%Y-%m-%d')})")
                else:
                    self.stats_estimated_finish_label.setText("N/A (set daily study hours)")

    def update_budget_tab_content(self):
        # ... (Logic from your previous app.py, ensure self.expenses_list_widget and self.total_spent_label are attributes)
        if hasattr(self, 'expenses_list_widget'):
            self.expenses_list_widget.clear()
            for expense in expenses_list:
                self.expenses_list_widget.addItem(f"{expense['date']} - {expense['name']}: {expense['price']:.2f}")
            total_spent = db.get_total_spent()
            self.total_spent_label.setText(f"Total Spent: {total_spent:.2f} USD")

    def on_add_expense_clicked(self):
        # ... (Logic from your previous app.py)
        name = self.expense_name_input.text();
        price_str = self.expense_price_input.text();
        date_str = self.expense_date_input.date().toString("yyyy-MM-dd")
        if not name or not price_str: QMessageBox.warning(self, "Input Missing",
                                                          "Please enter item name and price."); return
        try:
            price = float(price_str)
            if price < 0: QMessageBox.warning(self, "Invalid Input", "Price cannot be negative."); return
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid price.");
            return
        db.add_expense(name, price, date_str);
        global expenses_list
        loaded_expenses = db.load_expenses();
        expenses_list.clear();
        expenses_list.extend(loaded_expenses)
        self.update_budget_tab_content();
        self.expense_name_input.clear();
        self.expense_price_input.clear()
        self.expense_date_input.setDate(datetime.now().date())

    # --- Add Course Form Logic ---
    def on_add_course_form_show(self):
        # This should ideally be a separate QDialog class for better structure
        self.add_course_page = QWidget()
        self.add_course_page.setWindowTitle("Add New Course")  # Give the temp page a title
        form_layout = QFormLayout(self.add_course_page)
        self.add_course_inputs = {}
        fields_with_types = {"Name": QLineEdit, "Category": QLineEdit, "Length": QLineEdit, "Link": QLineEdit,
                             "Due Date": QDateEdit, "Priority": QComboBox, "Status": QComboBox}
        for field_name, WidgetType in fields_with_types.items():
            lbl = QLabel(f"{field_name}:");
            lbl.setStyleSheet(cfg.FIELD_LABEL_QSS)
            if WidgetType == QLineEdit:
                edit_widget = QLineEdit()
            elif WidgetType == QDateEdit:
                edit_widget = QDateEdit(QDate.currentDate());
                edit_widget.setCalendarPopup(True);
                edit_widget.setDisplayFormat("yyyy-MM-dd")
            elif WidgetType == QComboBox:
                edit_widget = QComboBox()
                if field_name == "Priority":
                    edit_widget.addItems(["Low", "Medium", "High"]);
                    edit_widget.setCurrentText("Medium")
                elif field_name == "Status":
                    edit_widget.addItems(["Pending", "In Progress", "Completed"]);
                    edit_widget.setCurrentText("Pending")
            edit_widget.setStyleSheet(cfg.FIELD_EDIT_QSS);
            form_layout.addRow(lbl, edit_widget);
            self.add_course_inputs[field_name] = edit_widget
        if "Length" in self.add_course_inputs: self.add_course_inputs["Length"].setPlaceholderText("e.g., 10.5")

        button_layout = QHBoxLayout()  # For Save and Cancel buttons
        save_btn = QPushButton("Save Course");
        save_btn.setStyleSheet(cfg.TAB_BUTTON_QSS);
        save_btn.clicked.connect(self.on_save_new_course_clicked)
        button_layout.addWidget(save_btn)
        cancel_btn = QPushButton("Cancel");
        cancel_btn.setStyleSheet(cfg.TAB_BUTTON_QSS);
        cancel_btn.clicked.connect(self.on_cancel_add_course)
        button_layout.addWidget(cancel_btn)
        form_layout.addRow(button_layout)  # Add the button layout to the form

        # Manage the temporary "Add Course" page
        if hasattr(self, 'add_course_page_index') and self.add_course_page_index < self.pages.count():
            old_page = self.pages.widget(self.add_course_page_index)
            if old_page and old_page != self.add_course_page:  # Ensure we are not removing a main tab
                self.pages.removeWidget(old_page)
                old_page.deleteLater()

        self.add_course_page_index = self.pages.addWidget(self.add_course_page)
        self.pages.setCurrentIndex(self.add_course_page_index)

    def on_save_new_course_clicked(self):
        try:
            name = self.add_course_inputs["Name"].text();
            category = self.add_course_inputs["Category"].text()
            length_str = self.add_course_inputs["Length"].text();
            link = self.add_course_inputs["Link"].text()
            status = self.add_course_inputs["Status"].currentText();
            priority = self.add_course_inputs["Priority"].currentText()
            due_date_qdate = self.add_course_inputs["Due Date"].date()
            due_date_str = due_date_qdate.toString(
                "yyyy-MM-dd") if due_date_qdate.isValid() and not due_date_qdate.isNull() else None
            if not name or not category or not length_str: QMessageBox.warning(self, "Input Missing",
                                                                               "Name, Category, and Length are required."); return
            length = float(length_str)
            if length < 0: QMessageBox.warning(self, "Invalid Input", "Length cannot be negative."); return
        except ValueError:
            QMessageBox.critical(self, "Error", "Length must be a valid number.");
            return
        except KeyError:
            QMessageBox.critical(self, "Error", "Form fields are not correctly initialized.");
            return
        if any(c.name.lower() == name.lower() for c in courses_list): QMessageBox.warning(self, "Duplicate Course",
                                                                                          f"A course named '{name}' already exists."); return

        new_course = Course(name, category, length, link, due_date_str, priority)
        new_course.update_status(status)

        courses_list.append(new_course);
        db.save_to_db(courses_list)
        self.remove_add_course_page_and_return()  # This will also call update_all_views

    def on_cancel_add_course(self):
        self.remove_add_course_page_and_return()

    def remove_add_course_page_and_return(self):
        if hasattr(self, 'add_course_page_index') and self.add_course_page_index >= len(
                self.tab_labels):  # Only remove if it's an extra page
            page_to_remove = self.pages.widget(self.add_course_page_index)
            if page_to_remove:  # Check if widget exists at that index
                self.pages.removeWidget(page_to_remove)
                page_to_remove.deleteLater()

        # Reset to the first main tab
        if self.buttons:
            self.buttons[0].setChecked(True)
            self.pages.setCurrentIndex(0)  # This will trigger on_tab_clicked -> update_all_views

    # --- Planner Tab Logic (moved from ui_setup to be methods of MainWindow) ---
    def _save_and_update_planner_goal(self):
        try:
            goal_hours = float(self.planner_weekly_goal_input.text())
            if goal_hours < 0: QMessageBox.warning(self, "Invalid Goal",
                                                   "Weekly goal hours cannot be negative."); return
            today = QDate.currentDate();
            week_start_date = today.addDays(-(today.dayOfWeek() - 1))
            week_start_str = week_start_date.toString("yyyy-MM-dd")
            db.save_weekly_goal(week_start_str, goal_hours);
            self._update_planner_summary()
            QMessageBox.information(self, "Goal Saved",
                                    f"Weekly goal of {goal_hours:.1f} hours saved for the week starting {week_start_str}.")
        except ValueError:
            QMessageBox.warning(self, "Invalid Goal", "Please enter a valid number for weekly goal hours.")

    def _load_planner_data_and_update_summary(self):
        today = QDate.currentDate();
        week_start_date = today.addDays(-(today.dayOfWeek() - 1))
        week_start_str = week_start_date.toString("yyyy-MM-dd")
        goal_hours = db.load_weekly_goal(week_start_str)
        if hasattr(self, 'planner_weekly_goal_input'):  # Check if UI is set up
            if goal_hours is not None:
                self.planner_weekly_goal_input.setText(str(goal_hours))
            else:
                self.planner_weekly_goal_input.setText("0")
            self._update_planner_summary()

    def _update_planner_summary(self):
        if not hasattr(self, 'planner_weekly_goal_input'): return  # UI not ready
        try:
            weekly_goal = float(self.planner_weekly_goal_input.text())
        except ValueError:
            weekly_goal = 0.0
        total_planned_hours = sum(day_input.value() for day_input in self.daily_hour_inputs.values())
        self.planner_total_planned_label.setText(
            f"Total Planned this Week: {total_planned_hours:.1f} / {weekly_goal:.1f} hours (Goal)")
        today_dt = datetime.now();
        current_day_of_week_idx = today_dt.weekday()
        days_left_for_planning = 7 - current_day_of_week_idx
        hours_still_to_achieve_goal = weekly_goal - total_planned_hours
        if hours_still_to_achieve_goal <= 0:
            self.planner_suggestion_label.setText("Goal reached or exceeded for the week!")
        elif days_left_for_planning > 0:
            suggested_daily_hours = hours_still_to_achieve_goal / days_left_for_planning
            self.planner_suggestion_label.setText(
                f"To reach goal: approx. {suggested_daily_hours:.2f} h/day for remaining {days_left_for_planning} day(s).")
        else:
            self.planner_suggestion_label.setText(f"To reach goal today: {hours_still_to_achieve_goal:.2f} hours.")

    # --- Course Card Interaction ---
    def on_course_data_changed(self, course: Course):  # Renamed from on_course_status_changed
        db.save_to_db(courses_list)  # Save the entire list (which includes the updated course)
        self.update_all_views()  # Refresh all views to reflect changes

    # --- Populating Course Card Tabs ---
    def update_course_card_tabs(self):
        search_term = self.search_input.text().lower()

        # Populate Progress Tab (Index 0)
        progress_courses = [c for c in courses_list if c.status == "In Progress" and search_term in c.name.lower()]
        tab_content_manager.populate_scroll_area_with_cards(self.scrolls[0], progress_courses,
                                                            self.on_course_data_changed)

        # Populate Ready Tab (Index 1)
        ready_courses = [c for c in courses_list if c.status == "Completed" and search_term in c.name.lower()]
        tab_content_manager.populate_scroll_area_with_cards(self.scrolls[1], ready_courses, self.on_course_data_changed)

        # Populate Categories Tab (Index 2)
        if hasattr(self, 'status_filters'):  # Ensure filters are initialized
            active_status_filters = [status for status, checkbox in self.status_filters.items() if checkbox.isChecked()]
            tab_content_manager.update_categories_tab(self.scrolls[2], courses_list, active_status_filters, search_term,
                                                      self.on_course_data_changed)
        else:  # Fallback if filters somehow not ready (should not happen)
            tab_content_manager.update_categories_tab(self.scrolls[2], courses_list,
                                                      ["Pending", "In Progress", "Completed"], search_term,
                                                      self.on_course_data_changed)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
