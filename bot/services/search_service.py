from bot.services.api_client import fetch_provider_results
from bot.services.coin_service import deduct_coins, get_coin_balance, has_enough_coins
from bot.services.settings_service import get_search_cost_coins
from bot.services.user_service import add_search_count
from bot.utils.formatter import format_search_results
from bot.utils.validators import detect_query_type, normalize_query


def validate_search_query(raw_query: str) -> dict:
    normalized = normalize_query(raw_query)
    query_type = detect_query_type(normalized)

    return {
        "normalized_query": normalized,
        "query_type": query_type,
        "is_valid": query_type in {"mobile", "cnic"},
    }


async def process_search(telegram_id: int, raw_query: str) -> dict:
    validation = validate_search_query(raw_query)

    if not validation["is_valid"]:
        return {
            "success": False,
            "validation_only": True,
            "query_type": validation["query_type"],
            "records": [],
            "formatted_text": "",
            "search_configured": True,
            "current_coins": get_coin_balance(telegram_id),
            "required_coins": get_search_cost_coins(),
        }

    required_coins = get_search_cost_coins()
    current_coins = get_coin_balance(telegram_id)

    if current_coins is None:
        return {
            "success": False,
            "validation_only": False,
            "query_type": validation["query_type"],
            "records": [],
            "formatted_text": "",
            "search_configured": True,
            "insufficient_coins": False,
            "user_found": False,
            "current_coins": None,
            "required_coins": required_coins,
        }

    if not has_enough_coins(telegram_id, required_coins):
        return {
            "success": False,
            "validation_only": False,
            "query_type": validation["query_type"],
            "records": [],
            "formatted_text": "",
            "search_configured": True,
            "insufficient_coins": True,
            "user_found": True,
            "current_coins": current_coins,
            "required_coins": required_coins,
        }

    provider_result = await fetch_provider_results(
        query=validation["normalized_query"],
        query_type=validation["query_type"],
    )

    if not provider_result.get("configured", True):
        return {
            "success": False,
            "validation_only": False,
            "query_type": validation["query_type"],
            "records": [],
            "formatted_text": "",
            "search_configured": False,
            "insufficient_coins": False,
            "user_found": True,
            "current_coins": current_coins,
            "required_coins": required_coins,
        }

    if not provider_result.get("success", False):
        return {
            "success": False,
            "validation_only": False,
            "query_type": validation["query_type"],
            "records": [],
            "formatted_text": "",
            "search_configured": True,
            "insufficient_coins": False,
            "user_found": True,
            "current_coins": current_coins,
            "required_coins": required_coins,
        }

    records = provider_result.get("records", [])

    if records:
        deduct_coins(
            telegram_id=telegram_id,
            amount=required_coins,
            reason="search_deduction",
        )
        add_search_count(telegram_id)

    return {
        "success": True,
        "validation_only": False,
        "query_type": validation["query_type"],
        "records": records,
        "formatted_text": format_search_results(records),
        "search_configured": True,
        "insufficient_coins": False,
        "user_found": True,
        "current_coins": current_coins,
        "required_coins": required_coins,
    }
