PROTECTED_GET_CASES: list[tuple[str, dict]] = [
    ("/api/v1/companies/search/by-radius", {"lon": 27.56, "lat": 53.90, "radius_m": 5000}),
    (
        "/api/v1/companies/search/by-rectangle",
        {"min_lon": 27.5, "min_lat": 53.88, "max_lon": 27.58, "max_lat": 53.92},
    ),
    ("/api/v1/companies/1", {}),
    ("/api/v1/companies", {"name": "Рог"}),
    ("/api/v1/buildings/1/companies", {}),
    ("/api/v1/activities/1/companies", {}),
    ("/api/v1/activities/1/companies/tree", {}),
]
