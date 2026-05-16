from unittest.mock import patch, MagicMock

from scanner.utils import run_command


def test_run_command_sudo_wrong_password():
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "sudo: 1 incorrect password attempt"

    with patch("scanner.utils.subprocess.run", return_value=mock_result):
        result = run_command("ufw status", sudo_password="wrongpass")

    assert result["success"] is False
    assert result["output"] == ""
    assert "Incorrect sudo password" in result["error"]
