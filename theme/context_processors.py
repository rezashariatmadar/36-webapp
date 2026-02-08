def legacy_runtime_flags(request):
    path = request.path or ""
    is_legacy_route = path.startswith("/legacy/")
    load_legacy_htmx = (
        path.startswith("/legacy/cafe/dashboard/")
    )
    return {
        "is_legacy_route": is_legacy_route,
        "load_legacy_htmx": load_legacy_htmx,
    }
