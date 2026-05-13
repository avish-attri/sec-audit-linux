import subprocess

from scanner.utils import build_result


def check_ssh_service():
    for unit in ("ssh", "sshd"):
        try:
            result = subprocess.run(
                ["systemctl", "is-active", unit],
                capture_output=True,
                text=True,
            )

            status_output = result.stdout.strip()
            if status_output == "active":
                return build_result(
                    "SERVICE-SSH",
                    "SSH Service Status",
                    "warn",
                    {
                        "service": unit,
                        "status": "active",
                        "reason": "SSH service exposed",
                    },
                )

            if status_output in {"inactive", "failed", "activating", "deactivating"}:
                return build_result(
                    "SERVICE-SSH",
                    "SSH Service Status",
                    "pass",
                    {
                        "service": unit,
                        "status": status_output,
                    },
                )

            # If the service unit is not present, try the next common unit name.
            if status_output == "unknown":
                continue

            return build_result(
                "SERVICE-SSH",
                "SSH Service Status",
                "pass",
                {
                    "service": unit,
                    "status": status_output,
                },
            )
        except Exception as e:
            return build_result(
                "SERVICE-SSH",
                "SSH Service Status",
                "unknown",
                {
                    "error": str(e),
                },
            )

    return build_result(
        "SERVICE-SSH",
        "SSH Service Status",
        "unknown",
        {
            "service": "ssh",
            "reason": "SSH service unit not found",
        },
    )


def check_running_services():
    try:
        result = subprocess.run(
            [
                "systemctl",
                "list-units",
                "--type=service",
                "--state=running",
            ],
            capture_output=True,
            text=True,
        )

        services = result.stdout.splitlines()
        count = len(services)
        status = "pass"

        if count > 150:
            status = "warn"

        return build_result(
            "SERVICE-RUNNING-COUNT",
            "Running Services Count",
            status,
            {
                "running_services": count,
            },
        )
    except Exception as e:
        return build_result(
            "SERVICE-RUNNING-COUNT",
            "Running Services Count",
            "unknown",
            {
                "error": str(e),
            },
        )
