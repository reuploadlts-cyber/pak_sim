def clean_value(value) -> str:
    if value is None:
        return "Not available"

    normalized = str(value).strip()
    if not normalized or normalized.lower() == "none":
        return "Not available"

    return normalized


def prettify_key(key: str) -> str:
    normalized = str(key).strip().replace("_", " ")
    if not normalized:
        return "Field"
    return normalized.title()


def format_search_results(records: list[dict]) -> str:
    if not records:
        return "ℹ️ <b>No results found.</b>"

    lines: list[str] = [f"✅ <b>Total Records Found:</b> {len(records)}", ""]

    for index, record in enumerate(records, start=1):
        lines.append(f"📄 <b>Record {index}</b>")

        for key, value in record.items():
            lines.append(f"• <b>{prettify_key(key)}:</b> {clean_value(value)}")

        lines.append("")

    return "\n".join(lines).strip()
