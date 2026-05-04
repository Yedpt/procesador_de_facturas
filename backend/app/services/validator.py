def validate_invoice_totals(data: dict, tolerance: float = 0.01) -> dict:
    """
    Valida coherencia basica:
    - subtotal + tax == total (con tolerancia)
    - suma de line_items == subtotal (si hay line_items)
    """
    errors = []

    subtotal = data.get("subtotal")
    tax = data.get("tax")
    total = data.get("total")
    line_items = data.get("line_items") or []

    # Validacion subtotal + tax == total
    if subtotal is not None and tax is not None and total is not None:
        calc_total = round(subtotal + tax, 2)
        if abs(calc_total - total) > tolerance:
            errors.append(
                f"Total no cuadra: subtotal+tax={calc_total} vs total={total}"
            )

    # Validacion sum(line_items) == subtotal
    if subtotal is not None and line_items:
        items_sum = 0.0
        for item in line_items:
            if item.get("total") is not None:
                items_sum += item["total"]
        items_sum = round(items_sum, 2)

        if abs(items_sum - subtotal) > tolerance:
            errors.append(
                f"Subtotal no cuadra: suma_items={items_sum} vs subtotal={subtotal}"
            )

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
    }