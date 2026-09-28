class UnmappedStateError(Exception):
    """Raised when no mapping rule (including fallback) matches an event.

    This should never happen if seed_rules.yaml has a fallback row for
    every (system, type) pair — treat this as a bug in the mapping table,
    not an expected runtime condition.
    """


class AmbiguousRuleError(Exception):
    """Raised when more than one non-fallback rule's predicate matches.

    Indicates overlapping predicates in seed_rules.yaml that need to be
    made mutually exclusive.
    """
