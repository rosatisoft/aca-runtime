def detect_declared_shift(text: str) -> dict:
    """
    Detects explicitly declared frame shifts.

    This does not infer psychological intention.
    It only detects whether the text explicitly declares
    a change of frame, such as factual, rhetorical,
    hypothetical, evidential, or conceptual.
    """

    normalized = text.lower()

    patterns = [
        {
            "shift_type": "rhetorical",
            "target_field": "rhetorical",
            "markers": [
                "rhetorical",
                "not factual",
                "as rhetoric",
                "as a rhetorical",
                "metaphor",
                "metaphorical",
                "symbolic",
                "as an analogy",
                "analogy",
            ],
        },
        {
            "shift_type": "factual",
            "target_field": "factual",
            "markers": [
                "evidence-based",
                "based on evidence",
                "return to evidence",
                "from the evidence",
                "factually",
                "as a factual",
                "factual claim",
                "empirical",
                "verify",
                "verified",
            ],
        },
        {
            "shift_type": "hypothetical",
            "target_field": "rhetorical",
            "markers": [
                "hypothetically",
                "suppose",
                "assume",
                "what if",
                "let's imagine",
                "imagine that",
                "for the sake of argument",
            ],
        },
        {
            "shift_type": "conceptual",
            "target_field": "foundational",
            "markers": [
                "conceptually",
                "in principle",
                "definition",
                "define",
                "logically",
                "from first principles",
                "as a principle",
            ],
        },
    ]

    for pattern in patterns:
        for marker in pattern["markers"]:
            if marker in normalized:
                return {
                    "declared_shift": True,
                    "shift_type": pattern["shift_type"],
                    "target_field": pattern["target_field"],
                    "evidence": marker,
                }

    return {
        "declared_shift": False,
        "shift_type": None,
        "target_field": None,
        "evidence": None,
    }