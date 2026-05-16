import subprocess


def run_command(command, sudo_password=None):
    """
    Runs a shell command safely and returns output.
    If sudo_password is provided, the command will be run with sudo.
    """
    if sudo_password is not None and not command.strip().startswith("sudo "):
        command = f"sudo -S {command}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            input=(sudo_password + "\n") if sudo_password is not None else None,
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if result.returncode != 0 and sudo_password is not None:
            low_err = stderr.lower()
            if (
                "sorry, try again" in low_err
                or "authentication failure" in low_err
                or "a password is required" in low_err
                or ("sudo:" in low_err and "password" in low_err)
            ):
                return {
                    "success": False,
                    "returncode": result.returncode,
                    "output": "",
                    "error": "Incorrect sudo password or sudo authentication failed",
                }

        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "output": stdout,
            "error": stderr,
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
        }


def build_result(check_id, name, status, data):
    normalized = status.upper()
    mapping = {
        "WARN": "WARNING",
        "PASS": "PASS",
        "FAIL": "FAIL",
        "UNKNOWN": "ERROR",
    }
    normalized = mapping.get(normalized, normalized)

    risk_map = {
        "PASS": "Low",
        "WARNING": "Medium",
        "FAIL": "High",
        "ERROR": "Unknown",
    }

    details = data.get("reason") or data.get("error") or data.get("details") or str(data)
    recommendation = "Review system configuration"
    if normalized == "FAIL":
        recommendation = "Remediate the identified security issue"
    elif normalized == "WARNING":
        recommendation = "Investigate and address the warning"
    elif normalized == "ERROR":
        recommendation = "Check the system state and rerun the check"
    elif normalized == "PASS":
        recommendation = "No action needed"

    return {
        "id": check_id,
        "name": name,
        "status": normalized,
        "risk": risk_map.get(normalized, "Unknown"),
        "details": details,
        "recommendation": recommendation,
        "data": data,
    }
