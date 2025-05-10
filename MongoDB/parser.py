
from query_parser import nl_to_query
from mutation_parser import nl_to_mutation


def handle_input(user_input: str):
    lowered = user_input.lower()
    # 1. Data Mutation
    if any(keyword in lowered for keyword in ["add", "insert", "delete", "remove", "update", "change", "modify"]):
        return nl_to_mutation(user_input)

    # 2. Query (default fallback)
    else:
        return nl_to_query(user_input)