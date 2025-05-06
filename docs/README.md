# CoursePilot Project

## Overview
CoursePilot is a personalized AI learning management system that helps with weekly learning planning and progress tracking, mainly on Udemy-based courses in AI topics (e.g., NLP, CV, DL). The goal is a complex tool that automates learning, including course management, weekly plans, and visualizations.

## Features
- **Course Management**: Add courses with name, category, length (in hours), and Udemy link; manage status (planned / in progress / completed); and categorize (e.g., NLP, CV, DL, MLOps).
- **Weekly Learning Management**: Set weekly study time (e.g., 10 hours); automatic daily breakdown; display "Daily Goal"; and dynamic replanning if a day is missed.
- **Progress Tracking**: Manual progress updates; Udemy scraping to automatically read percentage completion from course links; and calculate estimated hours from progress percentage.
- **Roadmap Dashboard**: Visual progress bars for courses; color-coded by status; and overall "AI Mastery" roadmap progress.
- **GUI**: Web app using Streamlit or Flask; main views: course list, weekly plan, roadmap, and daily goal.
- **Extra Features**: Daily learning logging; Pomodoro timer; visualizations (e.g., learning graphs); note-taking per course; and roadmap export (PDF/CSV).

## Technology Stack
- **Languages and Frameworks**: Python, Streamlit or Flask.
- **Data Storage**: JSON or SQLite.
- **Other Tools**: Selenium/Playwright for scraping; Plotly/Matplotlib for visualizations.
- **Version Control**: Git + GitHub.

## Installation
1. Clone the repo: `git clone https://github.com/JLoloCkik/CoursePilot`
2. Navigate to the directory: `cd CoursePilot`
3. Install dependencies: `pip install -r requirements.txt`
   - (Add to requirements.txt: streamlit, selenium, plotly, etc.)

## Usage
1. Run the app: `streamlit run src/app.py` (if using Streamlit).
2. Test features: For example, add courses in `src/courses.py`.
3. Develop further: Check `docs/architecture.md` for details.

## Project Status
Design phase: Currently working on specifications and architecture.

## Next Steps
- Expand the code in the `src/` directory.
- Test features in the `tests/` directory.
- Create issues on GitHub if needed.

## License
MIT License (or choose one).

Made with by JLolo.
