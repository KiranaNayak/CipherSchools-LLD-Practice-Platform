
import re


class RuleBasedEvaluator:
    """Evaluates LLD submissions using explainable, problem-specific rules."""

    REQUIRED_SECTIONS = {
        "assumptions": "Assumptions",
        "classes": "Classes and responsibilities",
        "relationships": "Relationships",
        "key_flows": "Key flows",
        "tradeoffs": "Design trade-offs",
    }

    EDGE_CASES = {
        "Parking Lot System": [
            "full",
            "unavailable",
            "invalid ticket",
            "already",
            "payment failure",
        ],
        "Vending Machine": [
            "out of stock",
            "insufficient",
            "payment failure",
            "change",
            "refund",
        ],
        "Elevator System": [
            "overload",
            "door",
            "out of service",
            "multiple requests",
        ],
        "Library Management": [
            "unavailable",
            "overdue",
            "already borrowed",
            "invalid member",
            "lost",
        ],
    }

    SECTION_INDICATORS = {
        "assumptions": [
            "assume",
            "if ",
            "when ",
            "must",
            "only",
            "contains",
            "supports",
            "allows",
            "multiple",
            "different types",
            "available",
        ],
        "classes": [
            "manage",
            "handle",
            "store",
            "calculate",
            "track",
            "control",
            "create",
            "validate",
            "assign",
            "process",
            "maintain",
            "records",
            "responsible",
        ],
        "relationships": [
            "contains",
            "has",
            "belongs",
            "references",
            "associated",
            "inherits",
            "uses",
            "many",
            "one",
            "assigned",
            "connected",
        ],
        "key_flows": [
            "then",
            "after",
            "when",
            "if",
            "finally",
            "before",
            "request",
            "return",
            "create",
            "payment",
            "exit",
            "entry",
        ],
        "tradeoffs": [
            "because",
            "however",
            "but",
            "instead",
            "trade-off",
            "tradeoff",
            "alternative",
            "benefit",
            "limitation",
            "maintainability",
            "extensible",
        ],
    }

    def evaluate(self, problem, design):
        feedback = []
        total_score = 0

        # Evaluate the five required sections.
        for field, label in self.REQUIRED_SECTIONS.items():
            value = design.get(field, "")
            text = value.strip() if isinstance(value, str) else ""
            words = text.split()
            score = 0
            suggestions = []

            if not text:
                suggestions.append("This section is missing.")
            else:
                # Reward answers that provide sufficient detail.
                if len(words) >= 5:
                    score += 4
                else:
                    suggestions.append(
                        "Explain your answer in more detail."
                    )

                lower_text = text.lower()
                indicators = self.SECTION_INDICATORS[field]

                if any(term in lower_text for term in indicators):
                    score += 6
                else:
                    # Give section-specific feedback.
                    if field == "classes":
                        suggestions.append(
                            "Explain each class's responsibility. For "
                            "example, Vehicle stores registration details, "
                            "ParkingSpot tracks availability, and Ticket "
                            "records entry and exit. Listing class names "
                            "alone is not enough."
                        )
                    elif field == "relationships":
                        suggestions.append(
                            "Explain how classes interact, which class "
                            "owns or references another, and how they "
                            "collaborate."
                        )
                    elif field == "key_flows":
                        suggestions.append(
                            "Describe the operation step by step, including "
                            "what happens when it succeeds or fails."
                        )
                    elif field == "tradeoffs":
                        suggestions.append(
                            "Explain why you chose this design, an "
                            "alternative, and the advantages or limitations "
                            "of each approach."
                        )
                    elif field == "assumptions":
                        suggestions.append(
                            "State the assumptions, constraints, and "
                            "conditions your design relies on."
                        )
                    else:
                        suggestions.append(
                            f"Add details specific to {label.lower()}."
                        )

            score = min(score, 10)
            total_score += score

            feedback.append({
                "criterion": label,
                "status": "Good" if score >= 8 else "Needs improvement",
                "score": score,
                "max_score": 10,
                "suggestion": (
                    "The section contains useful design details."
                    if not suggestions
                    else " ".join(suggestions)
                ),
            })

        # Evaluate required concepts: 25 points maximum.
        classes_text = design.get("classes", "")
        if not isinstance(classes_text, str):
            classes_text = ""

        classes_lower = classes_text.lower()
        required = problem.get("required_concepts", [])

        found = [
            concept
            for concept in required
            if isinstance(concept, str)
            and re.search(
                r"\b" + re.escape(concept.lower()) + r"\b",
                classes_lower,
            )
        ]

        missing = [
            concept for concept in required
            if concept not in found
        ]

        concept_score = (
            round(25 * len(found) / len(required))
            if required
            else 25
        )
        total_score += concept_score

        feedback.append({
            "criterion": "Required concepts",
            "status": (
                "Good" if not missing else "Needs improvement"
            ),
            "score": concept_score,
            "max_score": 25,
            "suggestion": (
                "All required concepts are mentioned. Check that each "
                "has a clear responsibility."
                if not missing
                else "Consider adding these concepts to your design: "
                + ", ".join(missing)
            ),
        })

        # Evaluate failure scenarios within Key flows: 25 points maximum.
        key_flows = design.get("key_flows", "")
        if not isinstance(key_flows, str):
            key_flows = ""

        edge_terms = self.EDGE_CASES.get(
            problem.get("title"),
            [],
        )
        edge_text = key_flows.lower()

        mentioned = [
            term for term in edge_terms
            if term in edge_text
        ]
        missing_edges = [
            term for term in edge_terms
            if term not in mentioned
        ]

        edge_score = (
            round(25 * len(mentioned) / len(edge_terms))
            if edge_terms
            else 25
        )
        total_score += edge_score

        # Combine edge-case feedback with Key flows so there are
        # exactly six feedback criteria.
        key_flow_feedback = next(
            item for item in feedback
            if item["criterion"] == "Key flows"
        )

        key_flow_feedback["score"] += edge_score
        key_flow_feedback["max_score"] = 35
        key_flow_feedback["status"] = (
            "Good"
            if key_flow_feedback["score"] >= 8 and not missing_edges
            else "Needs improvement"
        )

        if missing_edges:
            key_flow_feedback["suggestion"] += (
                " Also consider how the system handles: "
                + ", ".join(missing_edges)
                + "."
            )
        else:
            key_flow_feedback["suggestion"] += (
                " Relevant failure scenarios are covered."
            )

        return {
            "score": min(round(total_score), 100),
            "feedback": feedback,
        }
