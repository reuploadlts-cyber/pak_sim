from typing import Any

import aiohttp

from bot.config import settings


def provider_is_enabled() -> bool:
    return settings.search_provider_enabled and bool(settings.search_provider_base_url)


def get_provider_name() -> str:
    return settings.search_provider_name


def _normalize_record(record: dict[str, Any]) -> dict[str, str]:
    normalized: dict[str, str] = {}

    for key, value in record.items():
        normalized[str(key)] = "" if value is None else str(value).strip()

    return normalized


async def fetch_provider_results(query: str, query_type: str) -> dict:
    if not provider_is_enabled():
        return {
            "success": False,
            "configured": False,
            "records": [],
            "provider": get_provider_name(),
            "message": "Provider disabled or base URL missing.",
            "raw_payload": None,
        }

    params = {"number": query}
    timeout = aiohttp.ClientTimeout(total=settings.search_provider_timeout)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(settings.search_provider_base_url, params=params) as response:
                if response.status != 200:
                    return {
                        "success": False,
                        "configured": True,
                        "records": [],
                        "provider": get_provider_name(),
                        "message": f"HTTP {response.status}",
                        "raw_payload": None,
                    }

                payload = await response.json(content_type=None)

    except aiohttp.ClientError as error:
        return {
            "success": False,
            "configured": True,
            "records": [],
            "provider": get_provider_name(),
            "message": f"Request error: {error}",
            "raw_payload": None,
        }
    except Exception as error:
        return {
            "success": False,
            "configured": True,
            "records": [],
            "provider": get_provider_name(),
            "message": f"Unexpected error: {error}",
            "raw_payload": None,
        }

    if not isinstance(payload, dict):
        return {
            "success": False,
            "configured": True,
            "records": [],
            "provider": get_provider_name(),
            "message": "Invalid JSON response shape.",
            "raw_payload": payload,
        }

    api_success = bool(payload.get("success", False))
    raw_data = payload.get("data", [])

    if not api_success:
        return {
            "success": False,
            "configured": True,
            "records": [],
            "provider": get_provider_name(),
            "message": str(payload.get("message", "Provider returned failure.")),
            "raw_payload": payload,
        }

    if not isinstance(raw_data, list):
        return {
            "success": False,
            "configured": True,
            "records": [],
            "provider": get_provider_name(),
            "message": "Invalid data field.",
            "raw_payload": payload,
        }

    records: list[dict[str, str]] = []
    for item in raw_data:
        if isinstance(item, dict):
            records.append(_normalize_record(item))

    return {
        "success": True,
        "configured": True,
        "records": records,
        "provider": get_provider_name(),
        "message": str(payload.get("message", "")),
        "raw_payload": payload,
        "query_type": query_type,
    }
