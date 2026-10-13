
from business_services import (
    get_package_status,
    get_package_history,
    get_service_health,
    get_delivery_policy,
)

FUNCTIONS = {
    "get_package_status": get_package_status,
    "get_package_history": get_package_history,
    "get_service_health": get_service_health,
    "get_delivery_policy": get_delivery_policy,
}

DESCRIPTIONS = {
    "get_package_status": (
        "Get the current package delivery status."
    ),
    "get_package_history": (
        "Get historical tracking events for a package."
    ),
    "get_service_health": (
        "Get the current operational health of a service."
    ),
    "get_delivery_policy": (
        "Get the applicable delivery policy."
    ),
}

PARAMETERS = {
    "get_package_status": "package_id",
    "get_package_history": "package_id",
    "get_service_health": "service_name",
    "get_delivery_policy": "policy_type",
}

TOOLS = []

for name, parameter in PARAMETERS.items():
    property_schema = {"type": "string"}

    if name == "get_delivery_policy":
        property_schema["enum"] = [
            "missed_delivery",
            "signature_required",
        ]

    TOOLS.append({
        "type": "function",
        "name": name,
        "description": DESCRIPTIONS[name],
        "parameters": {
            "type": "object",
            "properties": {
                parameter: property_schema
            },
            "required": [parameter],
            "additionalProperties": False,
        },
        "strict": True,
    })
