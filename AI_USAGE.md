# AI Usage Documentation

## Purpose

AI assistance was used during development to help understand requirements, plan the application structure, write initial code, and troubleshoot implementation steps.

## Areas Where AI Assisted

### 1. Project Planning

AI helped break the assignment into smaller implementation tasks and identify the core features needed for the prototype.

### 2. Backend Development

AI provided initial code examples for FastAPI routes, request validation, and integration with the rule-based evaluator.

### 3. Evaluation Logic

AI helped develop a basic evaluator that checks for required submission sections and expected problem concepts.

### 4. Database Persistence

AI assisted with an SQLite implementation for saving attempts, scores, and feedback.

### 5. Testing

AI helped create initial pytest cases for complete submissions and submissions with missing design sections.

## Technical Decisions

- FastAPI was used to build the backend.
- SQLite was selected to persist attempts without requiring a separate database server.
- Jinja2 templates, HTML, CSS, and JavaScript were used to build the web interface.
- A rule-based evaluator was selected to avoid requiring a paid AI API.
- Pytest was used to test the evaluator's basic behaviour.

## Limitations and Review

The initial evaluator checks completeness and the presence of expected concepts. Its score should not be interpreted as a complete assessment of design quality.

The generated code and suggestions were tested during development, and implementation decisions were adjusted to fit the assignment's requirements and available time.

## Future Improvements

Potential improvements include deeper design-quality checks, more comprehensive tests, and evaluation of additional design scenarios.
