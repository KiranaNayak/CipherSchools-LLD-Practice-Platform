# LLD Practice Platform

## Overview

The LLD Practice Platform is a web application that helps learners practise Low-Level Design (LLD) problems and receive feedback on their solutions.

Users can select a problem, describe their design, submit it for evaluation, and review their previous attempts.

## Features

- Browse four LLD problems:
  - Parking Lot System
  - Vending Machine
  - Elevator System
  - Library Management
- View problem descriptions and requirements.
- Submit designs covering assumptions, classes, relationships, key flows, and design trade-offs.
- Receive rule-based evaluation scores and improvement suggestions.
- Save submissions and feedback using SQLite.
- Review previous attempts through the history page.

## Technology Stack

- Python 3.13
- FastAPI
- Uvicorn
- Jinja2
- SQLite
- HTML and CSS
- JavaScript
- Pytest

## Project Structure

```text
CipherSchools/
├── app/
│   ├── __init__.py
│   ├── evaluator.py
│   └── database.py
├── templates/
│   ├── home.html
│   ├── practice.html
│   └── history.html
├── main.py
├── test_evaluator.py
├── lld_practice.db
├── README.md
├── AI_USAGE.md
└── docs/
    ├── research.md
    └── design.md
```

## Installation

1. Install Python 3.10 or newer.
2. Open a terminal in the project directory.
3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate it on Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Install the dependencies:

   ```bash
   python -m pip install fastapi "uvicorn[standard]" jinja2 pytest
   ```

## Run the Application

Start the development server:

```bash
python -m uvicorn main:app --reload
```

Open these URLs in your browser:

- Home page: http://127.0.0.1:8000/home
- API documentation: http://127.0.0.1:8000/docs
- Attempt history: http://127.0.0.1:8000/history

## Run Tests

Run the automated tests using:

```bash
python -m pytest -v
```

The current tests cover complete design submissions and submissions with missing information.

## Evaluation Approach

The application uses a rule-based evaluator. It checks whether the learner has provided the required design sections and mentioned expected concepts for the selected problem.

The score reflects these basic completeness checks. It does not guarantee that a design is architecturally correct or optimal.

## Limitations

- Evaluation is rule-based and does not use an AI model.
- The current evaluator performs basic completeness checks rather than deep design analysis.
- The application does not currently include user accounts or authentication.


## Project Documentation

- [Research Note](docs/research.md)
- [Design Note](docs/design.md)
- [AI Usage Documentation](AI_USAGE.md)

## Current Test Status

The evaluator has 8 automated tests covering complete submissions,
missing information, required concepts, edge cases, and feedback structure.

Run the tests using:

```bash
python -m pytest -v
```

## Future Improvements

- Add more detailed design-quality checks.
- Improve evaluation of class responsibilities and relationships.
- Add more LLD practice problems.
- Improve feedback and test coverage.
