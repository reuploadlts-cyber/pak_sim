def normalize_query(value: str) -> str:
    return value.strip().replace(" ", "")


def is_mobile_with_leading_zero(value: str) -> bool:
    return value.isdigit() and len(value) == 11 and value.startswith("03")


def is_valid_mobile(value: str) -> bool:
    return value.isdigit() and len(value) == 10 and value.startswith("3")


def has_cnic_like_shape(value: str) -> bool:
    cleaned = value.replace("-", "")
    return cleaned.isdigit() and len(cleaned) == 13


def is_valid_cnic(value: str) -> bool:
    return value.isdigit() and len(value) == 13


def detect_query_type(value: str) -> str | None:
    normalized = normalize_query(value)

    if is_mobile_with_leading_zero(normalized):
        return "mobile_with_zero"

    if is_valid_mobile(normalized):
        return "mobile"

    if has_cnic_like_shape(normalized) and not is_valid_cnic(normalized):
        return "invalid_cnic"

    if is_valid_cnic(normalized):
        return "cnic"

    return None
