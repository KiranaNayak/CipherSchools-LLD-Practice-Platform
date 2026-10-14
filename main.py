
from fastapi import FastAPI
from app.database import initialize_database, save_attempt, get_attempts
from pathlib import Path
from fastapi import Request
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="LLD Practice Platform",
    description="Practice Low-Level Design problems and receive feedback.",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

@app.on_event("startup")
def startup():
    initialize_database()

@app.get("/")
def home():
    return {
        "message": "Welcome to the LLD Practice Platform!",
        "status": "Application is running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


problems = [
    {
        "id": 1,
        "title": "Parking Lot System",
        "difficulty": "Medium",
        "description": "Design a system to manage parking spaces and vehicles.",
        "requirements": [
            "Support different vehicle types.",
            "Assign an available parking spot.",
            "Generate a parking ticket.",
            "Handle vehicle exit and payment."
        ],
        "required_concepts": ["Vehicle", "ParkingSpot", "Ticket"]
    },
    {
        "id": 2,
        "title": "Vending Machine",
        "difficulty": "Easy",
        "description": "Design a vending machine that sells products.",
        "requirements": [
            "Display available products.",
            "Accept money from customers.",
            "Dispense the selected product.",
            "Return change when necessary."
        ],
        "required_concepts": ["Product", "Inventory", "Payment"]
    },
    {
        "id": 3,
        "title": "Elevator System",
        "difficulty": "Hard",
        "description": "Design an elevator system for a multi-floor building.",
        "requirements": [
            "Accept floor requests.",
            "Move between floors.",
            "Open and close doors safely.",
            "Handle multiple requests."
        ],
        "required_concepts": ["Elevator", "Floor", "Request"]
    },
    {
        "id": 4,
        "title": "Library Management",
        "difficulty": "Medium",
        "description": "Design a system to manage books and borrowing.",
        "requirements": [
            "Maintain book records.",
            "Register library members.",
            "Issue and return books.",
            "Track borrowing and due dates."
        ],
        "required_concepts": ["Book", "Member", "Loan"]
    }
]


@app.get("/api/problems")
def get_problems():
    return problems


@app.get("/api/problems/{problem_id}")
def get_problem(problem_id: int):
    for problem in problems:
        if problem["id"] == problem_id:
            return problem

    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Problem not found")


from pydantic import BaseModel
from app.evaluator import RuleBasedEvaluator


class DesignSubmission(BaseModel):
    problem_id: int
    assumptions: str
    classes: str
    relationships: str
    key_flows: str
    tradeoffs: str


@app.post("/api/submit")
def submit_design(design: DesignSubmission):
    problem = next(
        (p for p in problems if p["id"] == design.problem_id),
        None
    )

    if problem is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Problem not found"
        )

    evaluator = RuleBasedEvaluator()

    result = evaluator.evaluate(
        problem,
        design.model_dump()
    )

    attempt_id = save_attempt(
        problem,
        design.model_dump(),
        result
    )

    return {
        "message": "Design evaluated successfully",
        "attempt_id": attempt_id,
        "problem": problem["title"],
        "evaluation": result
    }

@app.get("/api/attempts")
def list_attempts():
    return get_attempts()

@app.get("/home", include_in_schema=False)
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"problems": problems}
    )

@app.get("/practice/{problem_id}", include_in_schema=False)
def practice_page(problem_id: int, request: Request):
    problem = next(
        (p for p in problems if p["id"] == problem_id),
        None
    )

    if problem is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Problem not found"
        )

    return templates.TemplateResponse(
        request=request,
        name="practice.html",
        context={"problem": problem}
    )

@app.get("/history", include_in_schema=False)
def history_page(request: Request):
    attempts = get_attempts()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={"attempts": attempts}
    )