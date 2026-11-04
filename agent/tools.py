from typing import Callable

# Synthetic test data.
# This is a mock environment, not a real authentication system.
USERS = {
    "qa_user": {
        "password": "correct_password",
        "dashboard_access": True,
    },
    "restricted_user": {
        "password": "correct_password",
        "dashboard_access": False,
    },
}

def check_user_exists(parameters: dict[str, str]) -> bool:
    """Check whether a user exists in the mock environment."""
    username = parameters.get("username")
    if not username:
        raise ValueError("Missing required parameter: username")
    return username in USERS

def validate_credentials(parameters: dict[str, str]) -> bool:
    """Validate user credentials against synthetic test data."""
    username = parameters.get("username")
    password = parameters.get("password")
    if not username:
        raise ValueError("Missing required parameter: username")
    if not password:
        raise ValueError("Missing required parameter: password")
    user = USERS.get(username)
    if user is None:
        return False
    return user["password"] == password

def check_dashboard_access(parameters: dict[str, str]) -> bool:
    """Check whether a user has access to the dashboard."""
    username = parameters.get("username")
    if not username:
        raise ValueError("Missing required parameter: username")
    user = USERS.get(username)
    if user is None:
        return False
    return user["dashboard_access"]

# Registry of available agent tools.
TOOL_REGISTRY: dict[str, Callable[[dict[str, str]], bool]] = {
    "check_user_exists": check_user_exists,
    "validate_credentials": validate_credentials,
    "check_dashboard_access": check_dashboard_access,
}

def execute_tool(
    tool_name: str,
    parameters: dict[str, str],
) -> bool:
    """Execute a tool by its registered name."""
    tool = TOOL_REGISTRY.get(tool_name)
    if tool is None:
        raise ValueError(f"Unknown tool: {tool_name}")
    return tool(parameters)