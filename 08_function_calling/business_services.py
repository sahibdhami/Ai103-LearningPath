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

def get_package_history(package_id:str) -> dict:
    allpackages={
        "UPS12345": [{
            "timestamp": "2023-10-10T10:00:00Z",
            "status": "Out for delivery",
            "location": "Atlanta, GA"
        },
        {
            "timestamp": "2023-10-09T14:00:00Z",
            "status": "In transit",
            "location": "Charlotte, NC"
        }],
        "UPS67890": [{
            "timestamp": "2023-10-10T10:00:00Z",
            "status": "Delivered",
            "location": "Dallas, TX"
        },
        {
            "timestamp": "2023-10-09T10:00:00Z",
            "status": "In Transit",
            "location": "SanAntonio, TX"
        }]}

    package_history = allpackages.get(package_id)

    return {"package_id": package_id, "history": package_history}
