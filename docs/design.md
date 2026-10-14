# Design Note: LLD Practice Platform

## 1. Overview

The LLD Practice Platform is a web application that allows learners to practise Low-Level Design problems, submit design descriptions, receive rule-based feedback, and review their previous attempts.

The application uses a simple monolithic architecture. The backend, evaluator, database access, and web interface are maintained within one project, making the prototype easier to develop, test, and understand.

## 2. Architecture

The application consists of four main parts.

### 2.1 Web Interface

The web interface uses HTML, CSS, JavaScript, and Jinja2 templates.

It provides:
- A home page listing available problems.
- A practice page containing the problem requirements and design submission fields.
- A results area displaying the score and feedback.
- A history page showing previous attempts.

### 2.2 FastAPI Backend

FastAPI handles page requests, API endpoints, input validation, and submission processing.

The backend provides endpoints for retrieving problems, submitting designs, and viewing attempt history. It also serves the web pages through Jinja2 templates.

### 2.3 Rule-Based Evaluator

The `RuleBasedEvaluator` class evaluates submitted designs using predefined rules.

It checks five sections:
- Assumptions
- Classes and responsibilities
- Relationships
- Key flows
- Design trade-offs

It also checks required concepts for each problem and predefined failure scenarios. The evaluator returns a numerical score and feedback for the learner.

The evaluator is intentionally explainable, but it relies on keywords and heuristics. It does not fully understand natural-language meaning or guarantee architectural correctness.

### 2.4 SQLite Database

The database layer is implemented in `app/database.py`.

SQLite stores submission attempts, including the selected problem, submitted design, score, and evaluation feedback. The history feature retrieves saved attempts for display.

SQLite was selected because it does not require a separate database server and is suitable for this prototype.

## 3. Main Components

| Component | Responsibility |
|---|---|
| `main.py` | FastAPI application, problem definitions, routes, submission processing, and page rendering |
| `app/evaluator.py` | Rule-based design evaluation and feedback generation |
| `app/database.py` | Database initialization and persistence of attempts |
| `templates/home.html` | Displays available LLD problems |
| `templates/practice.html` | Collects the learner's design and displays evaluation results |
| `templates/history.html` | Displays previous attempts |
| `test_evaluator.py` | Tests evaluator behaviour |

## 4. Submission Data Model

A design submission contains the following fields:

- `problem_id`: Identifies the selected LLD problem.
- `assumptions`: Describes assumptions and constraints.
- `classes`: Lists classes and their responsibilities.
- `relationships`: Explains connections between classes.
- `key_flows`: Describes important operations and their sequence.
- `tradeoffs`: Explains design choices and their advantages or limitations.

FastAPI uses a Pydantic model to validate the structure of incoming submissions before evaluation.

## 5. Application Workflow

1. The learner opens the home page and selects an LLD problem.
2. The practice page displays the problem description and requirements.
3. The learner enters assumptions, classes, relationships, key flows, and trade-offs.
4. The frontend submits the design to the backend.
5. The backend validates the submission and identifies the selected problem.
6. The evaluator calculates a score and generates feedback.
7. The database saves the attempt and its evaluation.
8. The frontend displays the result.
9. The learner can open the history page to review previous attempts.

## 6. Evaluation Design

The evaluator uses predefined indicators and required concepts to produce repeatable results.

The current implementation awards points for section completeness, expected concepts, and failure scenarios. It also provides suggestions when information appears to be missing.

This approach is easy to test and does not require an external service. However, it can reward keyword presence without understanding whether the proposed design is correct.

For this reason, evaluation results are presented as guidance rather than a definitive measure of design quality.

## 7. Error Handling and Testing

The application returns an error when a requested problem does not exist. The submission endpoint also checks that the selected problem is valid before evaluation.

Pytest tests cover complete submissions, missing sections, short answers, missing concepts, edge-case feedback, and the number of feedback criteria.

The current tests focus primarily on evaluator behaviour. Broader tests for API routes, database operations, and the complete browser workflow would provide additional confidence.

## 8. Design Decisions and Trade-offs

### Monolithic architecture

Keeping the application in one project reduces setup complexity and makes the prototype easier to run. As the application grows, evaluation logic, API handling, and other responsibilities could be separated into dedicated modules.

### Rule-based evaluation

Rules provide predictable and explainable feedback without an external AI dependency. Their main limitation is their inability to reliably interpret design meaning.

### SQLite persistence

SQLite supports persistent attempt history with minimal configuration. A larger multi-user application could require a database better suited to concurrent access and operational growth.

### Server-rendered templates

Jinja2 templates keep the interface simple and work naturally with FastAPI. A separate frontend framework could be introduced if richer client-side interactions become necessary.

## 9. Future Extensions

Possible extensions include:
- Stronger design-quality checks and more comprehensive tests.
- Additional LLD problems and problem-specific evaluation rules.
- An optional AI reviewer with a rule-based fallback.
- User accounts and individual progress tracking.
- Improved comparison of successive attempts.
- More detailed reporting on recurring design weaknesses.

These extensions should be added only when their value justifies the additional complexity.

## 10. Conclusion

The application provides a working prototype for practising LLD problems and reviewing design submissions. Its simple architecture supports rapid development and clear separation of evaluation and persistence responsibilities. The current implementation prioritises a functional practice loop, explainable feedback, and persistent history while leaving deeper design assessment as a future improvement.