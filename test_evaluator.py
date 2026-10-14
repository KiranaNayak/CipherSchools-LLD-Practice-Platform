
from app.evaluator import RuleBasedEvaluator


def test_complete_parking_design():
    problem = {
        "required_concepts": ["Vehicle", "ParkingSpot", "Ticket"]
    }

    design = {
        "assumptions": (
            "The parking lot contains multiple floors "
            "and different types of parking spaces."
        ),
        "classes": (
            "Vehicle stores registration details. ParkingSpot "
            "tracks availability. Ticket records entry and exit."
        ),
        "relationships": (
            "The parking lot contains floors and spots. "
            "Vehicles are assigned to compatible parking spots."
        ),
        "key_flows": (
            "A vehicle enters and receives a ticket. "
            "On exit, payment is processed and the spot becomes available."
        ),
        "tradeoffs": (
            "Separating payment processing improves maintainability. "
            "Additional interfaces make the system more extensible."
        )
    }

    result = RuleBasedEvaluator().evaluate(problem, design)
    print("Total score:", result["score"])
    for item in result["feedback"]:
         print(item["criterion"], item["score"], item["suggestion"])
    assert result["score"] == 100
    assert len(result["feedback"]) == 6



def test_missing_design_sections():
    problem = {
        "required_concepts": ["Vehicle", "ParkingSpot", "Ticket"]
    }

    design = {
        "assumptions": "",
        "classes": "Vehicle",
        "relationships": "",
        "key_flows": "",
        "tradeoffs": ""
    }

    result = RuleBasedEvaluator().evaluate(problem, design)

    assert result["score"] < 100
    assert any(
        item["status"] == "Needs improvement"
        for item in result["feedback"]
    )


def test_short_answers_receive_lower_score():
    problem = {
        "required_concepts": ["Vehicle", "ParkingSpot", "Ticket"]
    }

    design = {
        "assumptions": "Multiple floors",
        "classes": "Vehicle",
        "relationships": "Spot linked",
        "key_flows": "Enter exit",
        "tradeoffs": "Use classes"
    }

    result = RuleBasedEvaluator().evaluate(problem, design)

    assert result["score"] < 100


def test_missing_concepts_are_reported():
    problem = {
        "required_concepts": ["Vehicle", "ParkingSpot", "Ticket"]
    }

    design = {
        "assumptions": (
            "The parking lot contains multiple floors and several types of parking spaces."
        ),
        "classes": (
            "Vehicle stores vehicle information and registration details."
        ),
        "relationships": (
            "The lot contains spots and assigns vehicles to available spaces."
        ),
        "key_flows": (
            "A vehicle enters, receives a ticket, parks, and exits after payment."
        ),
        "tradeoffs": (
            "Payment processing is separated from parking management."
        )
    }

    result = RuleBasedEvaluator().evaluate(problem, design)

    concept_feedback = next(
        item for item in result["feedback"]
        if item["criterion"] == "Required concepts"
    )

    assert concept_feedback["status"] == "Needs improvement"
    assert "ParkingSpot" in concept_feedback["suggestion"]
    assert "Ticket" in concept_feedback["suggestion"]


def test_missing_edge_cases_reduce_score():
    problem = {
        "title": "Parking Lot System",
        "required_concepts": ["Vehicle", "ParkingSpot", "Ticket"],
    }

    design = {
        "assumptions": "Assume multiple floors and different vehicle types.",
        "classes": (
            "Vehicle stores registration details. ParkingSpot tracks "
            "availability. Ticket records entry and exit."
        ),
        "relationships": (
            "The parking lot contains floors and spots. "
            "Vehicles are assigned to compatible parking spots."
        ),
        "key_flows": (
            "A vehicle enters and receives a ticket. "
            "On exit, payment is processed and the spot becomes available."
        ),
        "tradeoffs": (
            "Separating payment processing improves maintainability. "
            "Additional interfaces make the system more extensible."
        ),
    }

    result = RuleBasedEvaluator().evaluate(problem, design)

    key_flows_feedback = next(
        item for item in result["feedback"]
        if item["criterion"] == "Key flows"
    )

    assert key_flows_feedback["status"] == "Needs improvement"
    assert "payment failure" in key_flows_feedback["suggestion"]


def test_including_edge_cases_improves_score():
    problem = {
        "title": "Parking Lot System",
        "required_concepts": ["Vehicle", "ParkingSpot", "Ticket"],
    }

    design = {
        "assumptions": "Assume multiple floors and different vehicle types.",
        "classes": (
            "Vehicle stores registration details. ParkingSpot tracks "
            "availability. Ticket records entry and exit."
        ),
        "relationships": (
            "The parking lot contains floors and spots. "
            "Vehicles are assigned to compatible parking spots."
        ),
        "key_flows": (
            "A vehicle enters and receives a ticket. If the lot is full, "
            "reject entry. On exit, validate the ticket and handle payment "
            "failure before releasing the spot."
        ),
        "tradeoffs": (
            "Separating payment processing improves maintainability. "
            "Additional interfaces make the system more extensible."
        ),
    }

    result = RuleBasedEvaluator().evaluate(problem, design)

    key_flows_feedback = next(
        item for item in result["feedback"]
        if item["criterion"] == "Key flows"
    )

    assert key_flows_feedback["score"] > 10


def test_feedback_contains_six_criteria():
    problem = {
        "title": "Parking Lot System",
        "required_concepts": ["Vehicle", "ParkingSpot", "Ticket"],
    }

    design = {
        "assumptions": "Assume multiple floors and different vehicle types.",
        "classes": (
            "Vehicle stores registration details. ParkingSpot tracks "
            "availability. Ticket records entry and exit."
        ),
        "relationships": (
            "The parking lot contains floors and spots. "
            "Vehicles are assigned to compatible parking spots."
        ),
        "key_flows": (
            "A vehicle enters and receives a ticket. If the lot is full, "
            "reject entry. On exit, validate the ticket and handle payment "
            "failure before releasing the spot."
        ),
        "tradeoffs": (
            "Separating payment processing improves maintainability. "
            "Additional interfaces make the system more extensible."
        ),
    }

    result = RuleBasedEvaluator().evaluate(problem, design)

    assert len(result["feedback"]) == 6
    assert result["score"] <= 100


def test_class_names_without_responsibilities_need_improvement():
    problem = {
        "title": "Parking Lot System",
        "required_concepts": ["Vehicle", "ParkingSpot", "Ticket"],
    }

    design = {
        "assumptions": "Assume multiple floors and different vehicle types.",
        "classes": "Vehicle, ParkingSpot, Ticket, ParkingLot.",
        "relationships": (
            "The parking lot contains floors and spots. "
            "Vehicles are assigned to compatible parking spots."
        ),
        "key_flows": (
            "A vehicle enters and receives a ticket. "
            "On exit, payment is processed and the spot becomes available."
        ),
        "tradeoffs": (
            "Separating payment processing improves maintainability. "
            "Additional interfaces make the system more extensible."
        ),
    }

    result = RuleBasedEvaluator().evaluate(problem, design)

    class_feedback = next(
        item for item in result["feedback"]
        if item["criterion"] == "Classes and responsibilities"
    )

    assert class_feedback["status"] == "Needs improvement"
