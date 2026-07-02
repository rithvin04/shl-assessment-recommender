import re

JOB_LEVELS = [
    "graduate",
    "entry-level",
    "manager",
    "director",
    "executive",
    "supervisor",
    "mid-professional",
    "front line manager",
    "junior",
    "mid",
    "senior"
]

ROLE_KEYWORDS = [
    "developer",
    "engineer",
    "analyst",
    "scientist",
    "manager",
    "consultant",
    "architect",
    "administrator",
    "tester",
    "sales",
    "hr",
    "recruiter",
    "marketing"
]

SKILL_KEYWORDS = [
    "python",
    "java",
    "javascript",
    "c++",
    "sql",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "react",
    "node",
    "django",
    "flask",
    "spring",
    "sap"
]

CATEGORY_KEYWORDS = {
    "personality": [
        "personality",
        "behavior",
        "behaviour",
        "opq"
    ],
    "cognitive": [
        "cognitive",
        "ability",
        "reasoning",
        "numerical",
        "verbal"
    ],
    "technical": [
        "coding",
        "programming",
        "technical",
        "developer"
    ],
    "simulation": [
        "simulation",
        "automata"
    ]
}


def analyze_query(query: str):

    original_query = query
    query = query.lower()

    result = {
        "intent": "recommend",
        "role": None,
        "skills": [],
        "experience": None,
        "job_level": None,
        "remote": False,
        "adaptive": False,
        "duration": None,
        "categories": [],
        "comparison": [],
        "refinement": False,
        "off_topic": False
    }

    # ------------------------
    # Intent Detection
    # ------------------------

    if any(word in query for word in ["compare", "difference", "vs", "versus"]):
        result["intent"] = "compare"

    elif any(word in query for word in ["actually", "instead", "only", "add", "remove"]):
        result["intent"] = "refine"
        result["refinement"] = True

    # ------------------------
# Off-topic Detection
# ------------------------

    OFF_TOPIC_WORDS = [
        "ipl",
        "cricket",
        "football",
        "weather",
        "movie",
        "song",
        "joke",
        "news",
        "president",
        "prime minister"
    ]


    if any(word in query for word in OFF_TOPIC_WORDS):
        result["intent"] = "refuse"
        result["off_topic"] = True

    # ------------------------
    # Scope protection
    # ------------------------
    REFUSE_WORDS = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "legal",
        "law",
        "lawsuit",
        "hire this candidate",
        "should i hire",
        "employment law"
    ]

    if any(word in query for word in REFUSE_WORDS):
        result["intent"] = "refuse"
        result["off_topic"] = True

    # ------------------------
    # Remote
    # ------------------------

    if any(word in query for word in ["remote", "online", "virtual"]):
        result["remote"] = True

    # ------------------------
    # Adaptive
    # ------------------------

    if "adaptive" in query:
        result["adaptive"] = True

    # ------------------------
    # Duration
    # ------------------------

    match = re.search(r"(\d+)\s*(minute|min)", query)

    if match:
        result["duration"] = int(match.group(1))

    # ------------------------
    # Experience
    # ------------------------

    match = re.search(r"(\d+)\s*(year|years|yr|yrs)", query)

    if match:
        result["experience"] = int(match.group(1))

    # ------------------------
    # Job Level
    # ------------------------

    for level in JOB_LEVELS:

        if level in query:

            result["job_level"] = level
            break

    # ------------------------
    # Skills
    # ------------------------

    for skill in SKILL_KEYWORDS:

        if skill in query:
            result["skills"].append(skill)

    # ------------------------
    # Role
    # ------------------------

    for role in ROLE_KEYWORDS:

        if role in query:
            result["role"] = original_query
            break

    # ------------------------
    # Categories
    # ------------------------

    for category, words in CATEGORY_KEYWORDS.items():

        for word in words:

            if word in query:
                result["categories"].append(category)
                break

    # ------------------------
    # Comparison
    # ------------------------

    # ------------------------
# Comparison
# ------------------------

    if result["intent"] == "compare":
        comparison_text = re.sub(
        r"compare|difference between|what is the difference between",
        "",
        original_query,
        flags=re.IGNORECASE
        ).strip()

        names = re.split(
        r"\s+and\s+|\s+vs\.?\s+|\s+versus\s+",
        comparison_text,
        flags=re.IGNORECASE
        )

        result["comparison"] = [
            name.strip()
            for name in names
            if name.strip()
        ]
    return result
if __name__ == "__main__":
    print(
        analyze_query(
            "Compare Python (New) and Automata Pro (New)"
        )
    )
