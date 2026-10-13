TOOLS = [
    {
        "type": "function",
        "name": "get_package_status",
        "description": (
            "Retrieve the current status of a package "
            "using its package ID."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "package_id": {
                    "type": "string",
                    "description": (
                        "Package tracking identifier"
                    ),
                }
            },
            "required": ["package_id"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_service_health",
        "description": (
            "Retrieve the health status of an "
            "application service."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {
                    "type": "string",
                    "description": "Name of the service",
                }
            },
            "required": ["service_name"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_delivery_policy",
        "description": (
            "Retrieve a delivery policy description "
            "for a supported policy type."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "policy_type": {
                    "type": "string",
                    "enum": [
                        "missed_delivery",
                        "signature_required",
                    ],
                }
            },
            "required": ["policy_type"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_package_history",
        "description": (
            "Retrieve the delivery history of a package "
            "using its package ID."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "package_id": {
                    "type": "string",
                    "description": (
                        "Package tracking identifier"
                    ),
                }
            },
            "required": ["package_id"],
            "additionalProperties": False,
        },
        "strict": True,
    }
]
