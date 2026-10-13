def get_package_status(package_id: str) -> dict:
    packages = {
        "UPS12345": {
            "status": "Out for delivery",
            "location": "Atlanta, GA",
            "estimated_delivery": "2026-10-12",
        },
        "UPS67890": {
            "status": "Delivered",
            "location": "Dallas, TX",
            "estimated_delivery": "2026-10-10",
        },
    }

    package = packages.get(package_id)

    if package is None:
        return {
            "package_id": package_id,
            "found": False,
            "message": "Package not found",
        }

    return {
        "package_id": package_id,
        "found": True,
        **package,
    }


def get_service_health(service_name: str) -> dict:
    services = {
        "dispatcher": "Healthy",
        "tracking-api": "Healthy",
        "notification-service": "Degraded",
    }

    return {
        "service_name": service_name,
        "status": services.get(
            service_name, "Unknown"
        ),
    }


def get_delivery_policy(policy_type: str) -> dict:
    policies = {
        "missed_delivery": (
            "If a delivery attempt is unsuccessful, "
            "the package may be rescheduled according "
            "to the applicable delivery service rules."
        ),
        "signature_required": (
            "Packages requiring a signature must "
            "be received by an eligible recipient."
        ),
    }

    return {
        "policy_type": policy_type,
        "description": policies.get(
            policy_type, "Policy not found"
        ),
    }


def get_package_history(package_id: str) -> dict:
    histories = {
        "UPS12345": [
            {
                "time": "2026-10-10T08:00:00",
                "event": "Arrived at Atlanta facility",
            },
            {
                "time": "2026-10-10T14:00:00",
                "event": "Processing delay reported",
            },
            {
                "time": "2026-10-11T07:30:00",
                "event": "Released for delivery",
            },
        ],
        "UPS67890": [
            {
                "time": "2026-10-09T09:00:00",
                "event": "Package in transit",
            },
            {
                "time": "2026-10-10T11:20:00",
                "event": "Delivered",
            },
        ],
    }

    events = histories.get(package_id)

    if events is None:
        return {
            "package_id": package_id,
            "found": False,
            "events": [],
        }

    return {
        "package_id": package_id,
        "found": True,
        "events": events,
    }

