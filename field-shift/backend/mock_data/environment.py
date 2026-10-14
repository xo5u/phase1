
def climate_for(latitude: float) -> dict:
    """Return a deterministic demo climate band based only on latitude."""
    absolute_latitude = abs(latitude)

    if absolute_latitude < 23.5:
        return {
            "annual_rainfall_mm": 610,
            "average_temperature_c": 25.4,
            "growing_season": "October–May",
            "source": "Demo climate profile (future: NASA POWER)",
        }

    if absolute_latitude < 38:
        return {
            "annual_rainfall_mm": 420,
            "average_temperature_c": 20.8,
            "growing_season": "November–June",
            "source": "Demo climate profile (future: NASA POWER)",
        }

    return {
        "annual_rainfall_mm": 690,
        "average_temperature_c": 13.6,
        "growing_season": "April–September",
        "source": "Demo climate profile (future: NASA POWER)",
    }


def check_soil_ph(soil_type: str, ph: float) -> dict:
    """Compare soil pH with a demo range and return practical advice."""

    recommended_ranges = {
        "sandy": (5.5, 7.0),
        "loam": (6.0, 7.5),
        "silt": (6.0, 7.5),
        "clay": (6.0, 7.5),
        "peat": (4.0, 5.5),
    }

    soil_type = soil_type.lower()
    min_ph, max_ph = recommended_ranges.get(
        soil_type, recommended_ranges["loam"]
    )

    if ph < min_ph:
        return {
            "status": "Below recommended range",
            "current_ph": ph,
            "recommended_ph": {
                "min": min_ph,
                "max": max_ph,
            },
            "solution": (
                "The soil is too acidic for this demo range. Test the "
                "soil's lime requirement. If lime is recommended, apply "
                "agricultural lime. Calcitic lime supplies calcium, while "
                "dolomitic lime supplies calcium and magnesium. Choose "
                "the type and application rate based on soil test results."
            ),
        }

    if ph > max_ph:
        return {
            "status": "Above recommended range",
            "current_ph": ph,
            "recommended_ph": {
                "min": min_ph,
                "max": max_ph,
            },
            "solution": (
                "The soil is too alkaline for this demo range. Test for "
                "nutrient deficiencies and check for calcium carbonate. "
                "Elemental sulfur may lower pH in suitable soils, but "
                "the application rate must be based on a soil test. "
                "In calcareous soils, major pH reduction may be impractical. "
                "Consider alkaline-tolerant crops and correct confirmed "
                "iron or zinc deficiencies using locally appropriate advice."
            ),
        }

    return {
        "status": "Within recommended range",
        "current_ph": ph,
        "recommended_ph": {
            "min": min_ph,
            "max": max_ph,
        },
        "solution": (
            "No pH correction is indicated by this demo range. Choose "
            "crops according to their preferred pH and maintain soil "
            "fertility through soil-test-guided management."
        ),
    }


def soil_for(longitude: float, soil_type: str = "loam") -> dict:
    """Return a deterministic demo soil profile based on soil type."""

    profiles = {
        "clay": {
            "texture": "Clay",
            "ph": 7.4,
            "organic_matter_percent": 2.1,
        },
        "sandy": {
            "texture": "Sandy",
            "ph": 6.8,
            "organic_matter_percent": 1.6,
        },
        "loam": {
            "texture": "Loam",
            "ph": 7.1,
            "organic_matter_percent": 2.7,
        },
        "silt": {
            "texture": "Silt",
            "ph": 7.1,
            "organic_matter_percent": 2.7,
        },
        "peat": {
            "texture": "Peat",
            "ph": 5.5,
            "organic_matter_percent": 8.0,
        },
    }

    soil_type = soil_type.lower()
    profile = profiles.get(soil_type, profiles["loam"])

    return {
        **profile,
        "ph_check": check_soil_ph(soil_type, profile["ph"]),
        "source": "Demo soil profile (future: SoilGrids)",
    }
