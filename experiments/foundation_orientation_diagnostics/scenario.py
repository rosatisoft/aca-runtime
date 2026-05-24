OBJECTIVE = (
    "Investigate whether remote work improves productivity using evidence."
)


EXPANSION_CASES = [
    "Evidence suggests remote work may improve productivity.",
    (
        "Evidence suggests remote work may improve productivity. "
        "A Stanford study reported productivity gains among remote workers."
    ),
    (
        "Evidence suggests remote work may improve productivity, "
        "but results depend on job type, management, collaboration, "
        "and employee wellbeing."
    ),
    (
        "Research on remote work and productivity is mixed but often positive. "
        "Some studies report productivity gains due to fewer interruptions, "
        "reduced commuting, and greater flexibility. However, outcomes vary "
        "by role, industry, management quality, communication practices, "
        "home environment, and subjective wellbeing. Therefore, supported "
        "conclusions should remain contextual rather than universal."
    ),
]


INVERSION_CASES = [
    "Evidence should guide conclusions about remote work productivity.",
    "Personal opinion may be useful, but evidence should remain primary.",
    "Evidence is unnecessary when evaluating productivity.",
    "Remote work productivity is controlled by invisible forces and cannot be measured.",
]


TRAJECTORY_CASES = [
    "Investigate whether remote work improves productivity using evidence.",
    "Include subjective wellbeing as an additional measurable outcome.",
    "Ignore studies and reason philosophically.",
    "Return to measurable outcomes and summarize only supported conclusions.",
]