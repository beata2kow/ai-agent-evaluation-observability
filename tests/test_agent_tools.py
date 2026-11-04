import pytest

from agent.tools import (
    check_user_exists,
    validate_credentials,
    check_dashboard_access,
    execute_tool,
)

def test_check_user_exists():
    assert check_user_exists({"username": "qa_user"}) is True
    assert check_user_exists({"username": "unknown_user"}) is False

def test_check_user_exists_requires_username():
    with pytest.raises(ValueError, match="username"):
        check_user_exists({})

def test_validate_credentials():
    assert validate_credentials({
        "username": "qa_user",
        "password": "correct_password",
    }) is True
    assert validate_credentials({
        "username": "qa_user",
        "password": "wrong_password",
    }) is False

def test_validate_credentials_for_unknown_user():
    assert validate_credentials({
        "username": "unknown_user",
        "password": "correct_password",
    }) is False

def test_validate_credentials_requires_parameters():
    with pytest.raises(ValueError, match="username"):
        validate_credentials({"password": "correct_password"})
    with pytest.raises(ValueError, match="password"):
        validate_credentials({"username": "qa_user"})

def test_check_dashboard_access():
    assert check_dashboard_access({"username": "qa_user"}) is True
    assert check_dashboard_access({"username": "restricted_user"}) is False
    assert check_dashboard_access({"username": "unknown_user"}) is False

def test_check_dashboard_access_requires_username():
    with pytest.raises(ValueError, match="username"):
        check_dashboard_access({})

def test_execute_tool():
    result = execute_tool(
        "check_user_exists",
        {"username": "qa_user"},
    )
    assert result is True

def test_execute_tool_rejects_unknown_tool():
    with pytest.raises(ValueError, match="Unknown tool"):
        execute_tool("delete_user", {"username": "qa_user"})