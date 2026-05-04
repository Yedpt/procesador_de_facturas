def validate_invoice_totals(data: dict, tolerance: float = 0.01) -> dict:
    """
    Valida coherencia basica:
    - subtotal + tax - withholding == total
    - suma de line_items == subtotal (si hay line_items)
      Si los items vienen con IVA incluido, permite cuadrar con total.
    """
    errors = []

    subtotal = data.get("subtotal")
    tax = data.get("tax")
    total = data.get("total")
    withholding = abs(data.get("withholding", 0.0))
    line_items = data.get("line_items") or []

    # subtotal + tax - withholding == total
    calc_total = None
    if subtotal is not None and tax is not None and total is not None:
        calc_total = round(subtotal + tax - withholding, 2)
        if abs(calc_total - total) > tolerance:
            errors.append(
                f"Total no cuadra: subtotal+tax-withholding={calc_total} vs total={total}"
            )

    # sum(line_items) == subtotal (o == total si items incluyen IVA)
    items_sum = None
    items_match = None
    if line_items:
        items_sum = 0.0
        for item in line_items:
            if item.get("total") is not None:
                items_sum += item["total"]
        items_sum = round(items_sum, 2)

        if subtotal is not None and abs(items_sum - subtotal) <= tolerance:
            items_match = "subtotal"
        elif total is not None and abs(items_sum - total) <= tolerance:
            items_match = "total"

        if subtotal is not None and abs(items_sum - subtotal) > tolerance:
            if total is None or abs(items_sum - total) > tolerance:
                errors.append(
                    f"Subtotal no cuadra: suma_items={items_sum} vs subtotal={subtotal}"
                )

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "diagnostic": {
            "calc_total": calc_total,
            "subtotal": subtotal,
            "tax": tax,
            "withholding": withholding,
            "total": total,
            "items_sum": items_sum,
            "items_match": items_match,  # "subtotal", "total" o None
        },
    }