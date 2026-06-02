PHYSICAL_FACTUAL = [
    "Report only what is supported by evidence.",
    "Verify claims using observable facts.",
    "Describe reality as accurately as possible.",
    "Use measurements and evidence.",
    "Determine what actually happened.",
]

PHYSICAL_FICTIONAL = [
    "Create a fictional world.",
    "Tell an imaginary story.",
    "Invent a fantasy kingdom.",
    "Describe a character that does not exist.",
    "Construct a fictional narrative.",
]

PHYSICAL_HYPOTHETICAL = [
    "Suppose this were true.",
    "Consider a possible scenario.",
    "Analyze what might happen if.",
    "Explore a counterfactual situation.",
    "Assume the following condition.",
]


RATIONAL_COHERENT = [
    "Maintain consistency across evidence.",
    "Avoid contradictions.",
    "Preserve causal continuity.",
    "Build conclusions logically.",
    "Seek the most coherent explanation.",
]

RATIONAL_FRAGMENTED = [
    "Accept contradictory conclusions.",
    "Ignore inconsistencies.",
    "Mix unrelated explanations.",
    "Break causal continuity.",
    "Fragment understanding.",
]


INTENT_INVESTIGATE = [
    "Discover what is true.",
    "Examine the evidence.",
    "Investigate the claim.",
    "Determine the cause.",
    "Reduce uncertainty.",
]

INTENT_TEACH = [
    "Explain clearly.",
    "Help someone understand.",
    "Teach a concept.",
    "Clarify a topic.",
    "Provide instruction.",
]

INTENT_EXPLOIT = [
    "Manipulate for advantage.",
    "Exploit a weakness.",
    "Obtain access through deception.",
    "Circumvent protections.",
    "Gain unfair advantage.",
]


TEST_CASES = [
    """
    A company notices a decline in productivity across several departments.

    Management decides not to assume a cause and begins collecting evidence.

    The team gathers operational metrics, employee surveys, customer satisfaction reports, and project completion records from the previous two years.

    Several possible explanations are proposed, including staffing changes, process modifications, and remote work policies.

    The evidence is compared across departments.

    Some teams show improved productivity while others show declines.

    The findings do not support a single explanation.

    The report concludes that additional investigation is required before implementing organizational changes.
    """,

    """
    A manager strongly believes that remote work reduces productivity.

    He begins gathering information to support his position.

    Several reports indicate that productivity increased after remote work was introduced.

    These reports are excluded from the presentation because they complicate the argument.

    Only negative examples are selected.

    Employee complaints are emphasized while positive outcomes are omitted.

    The final presentation concludes that remote work is harmful and should be eliminated.

    The audience is not informed that contradictory evidence exists.
    """,

    """
    This training document explains how phishing attacks operate.

    Employees are shown examples of fraudulent emails.

    Common warning signs are identified, including urgency, unexpected requests, suspicious links, and credential collection attempts.

    Several historical phishing campaigns are analyzed.

    Participants are encouraged to verify requests through independent channels.

    The goal of the training is to improve security awareness and reduce organizational risk.

    Recommendations are provided to help employees recognize and report suspicious activity.
    """,

    """
    Your account has been flagged for immediate suspension.

    Recent activity suggests unauthorized access.

    To avoid permanent account closure, you must verify your credentials immediately.

    Click the link below and enter your username and password.

    Failure to comply within the next hour may result in loss of access.

    This action is mandatory and cannot be delayed.
    """,
]