# Research Note: LLD Practice Platform

## 1. Introduction

Low-Level Design (LLD) is the process of designing the internal structure of a software system. It involves identifying classes, defining their responsibilities, establishing relationships between objects, and describing how different components interact.

Practising LLD helps learners improve their object-oriented programming, problem-solving, and software design skills. However, learners also need feedback to identify missing concepts and improve their designs.

The LLD Practice Platform was developed to provide a simple environment where learners can practise common LLD problems, submit their designs, receive feedback, and review previous attempts.

## 2. Problem Statement

Learners practising LLD may find it difficult to determine whether their design covers the important components of a problem. They may overlook class responsibilities, relationships, assumptions, alternative approaches, and failure scenarios.

A practice platform should therefore provide:

- A collection of LLD problems with clear requirements.
- A structured way to submit a design.
- Feedback identifying missing information and expected concepts.
- A score that helps learners review their submissions.
- An attempt history that supports continued practice.

## 3. Research on Evaluation Approaches

Three possible approaches were considered for evaluating design submissions.

### 3.1 Rule-Based Evaluation

A rule-based evaluator checks submissions against predefined conditions, such as required sections, expected concepts, and relevant failure scenarios.

**Advantages:**
- Simple to implement and test.
- Produces predictable and explainable feedback.
- Does not require an external AI service or paid API.

**Limitations:**
- May depend heavily on keywords.
- Can miss valid explanations that use different wording.
- Cannot reliably determine whether a design is logically correct.

### 3.2 AI-Based Evaluation

An AI-based evaluator can review natural-language descriptions and provide feedback about responsibilities, relationships, design decisions, and possible improvements.

**Advantages:**
- Can provide more flexible, context-sensitive feedback.
- Can explain potential design weaknesses in natural language.

**Limitations:**
- May produce inaccurate or inconsistent suggestions.
- Requires careful evaluation of its responses.
- An external API may introduce usage limits, network dependencies, and privacy considerations.

### 3.3 Hybrid Evaluation

A hybrid approach combines deterministic rules with an AI reviewer. Rules can check required sections and concepts, while an AI model can provide deeper qualitative feedback.

This approach could offer a balance between predictable checks and flexible evaluation. However, AI feedback would still need validation and should not automatically be treated as correct.

## 4. Selected Approach

The current prototype uses **rule-based evaluation**. This approach was selected because it is straightforward to implement, test, and demonstrate within the project timeline.

The evaluator checks five submission sections: assumptions, classes and responsibilities, relationships, key flows, and design trade-offs. It also checks required concepts for the selected problem and looks for predefined failure scenarios.

The evaluator returns a score and criterion-specific suggestions. These results are saved with the submission so that learners can review their attempts later.

The current score measures predefined completeness indicators. It should not be interpreted as proof that a design is architecturally correct or optimal.

## 5. Scope of the Prototype

The application currently supports four practice problems:

1. Parking Lot System
2. Vending Machine
3. Elevator System
4. Library Management

Learners can select a problem, review its requirements, submit a structured design, view feedback, and access previous attempts.

The application uses FastAPI for the backend, Jinja2 templates with HTML, CSS, and JavaScript for the web interface, and SQLite for persistent storage. Pytest is used to verify evaluator behaviour.

## 6. Future Improvements

Possible improvements include more comprehensive design-quality checks, better handling of alternative terminology, additional test cases, more practice problems, and an optional AI reviewer.

Future evaluation should also examine whether feedback is useful, whether scores distinguish stronger designs from weaker ones, and whether the evaluator avoids rewarding irrelevant keyword usage.

## 7. Conclusion

The LLD Practice Platform provides a working foundation for structured design practice and feedback. The selected rule-based approach supports a simple, testable prototype while making its limitations explicit. Further improvements can focus on the accuracy and usefulness of feedback rather than increasing complexity unnecessarily.