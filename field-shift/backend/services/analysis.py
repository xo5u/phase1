from mock_data.crops import CROP_PROFILES
from mock_data.environment import check_soil_ph, climate_for, soil_for
from schemas.farm import AnalysisResponse, FarmInput, RotationResponse

DISCLAIMER = (
    "Architecture demonstration using illustrative rules and mock data. "
    "Scores are not scientifically validated forecasts or farming advice."
)


def _crop_scores(farm: FarmInput, soil: dict, climate: dict) -> list[dict]:
    water_per_dunam = farm.available_water_m3 / farm.area_dunams
    previous = farm.previous_crop.strip().lower()
    scores = []

    for key, crop in CROP_PROFILES.items():
        score = 72
        reasons = []

        if water_per_dunam >= crop["water_need_m3_per_dunam"]:
            score += 14
            reasons.append("demo water allocation meets the sample threshold")
        else:
            score -= min(28, int((crop["water_need_m3_per_dunam"] - water_per_dunam) * 1.2))
            reasons.append("sample water need may exceed the entered allocation")

        low_ph, high_ph = crop["preferred_ph"]
        if low_ph <= soil["ph"] <= high_ph:
            score += 8
            reasons.append("mock soil pH is within the preferred range")
        else:
            score -= 10
            reasons.append("mock soil pH is outside the preferred range")

        low_temp, high_temp = crop["preferred_temperature_c"]
        temperature = climate["average_temperature_c"]
        if low_temp <= temperature <= high_temp:
            score += 8
            reasons.append("scenario temperature suits this crop")
        else:
            distance = low_temp - temperature if temperature < low_temp else temperature - high_temp
            score -= min(20, round(distance * 2))
            reasons.append("scenario temperature is outside the sample comfort range")

        if climate["annual_rainfall_mm"] < 250:
            score -= 8
            reasons.append("low scenario rainfall adds pressure")

        if soil["organic_matter_percent"] >= 2:
            score += 4

        if key == previous:
            score -= 25
            reasons.append("penalized to avoid repeating the previous crop")
        elif crop["family"].lower() == "legume" and previous in {"wheat", "barley"}:
            score += 6
            reasons.append("a legume follows the previous cereal")

        scores.append(
            {
                "crop": crop["name"],
                "score": max(0, min(100, score)),
                "reason": "; ".join(reasons).capitalize() + ".",
                "water_need_m3_per_dunam": crop["water_need_m3_per_dunam"],
            }
        )

    return sorted(scores, key=lambda item: item["score"], reverse=True)[:3]


def analyze_farm(farm: FarmInput) -> AnalysisResponse:
    climate = climate_for(farm.latitude)
    soil = soil_for(farm.longitude, farm.mock_soil_type)
    if farm.mock_temperature_c is not None:
        climate["average_temperature_c"] = farm.mock_temperature_c
        climate["source"] = "User-adjusted demo climate scenario"
    if farm.mock_rainfall_mm is not None:
        climate["annual_rainfall_mm"] = farm.mock_rainfall_mm
        climate["source"] = "User-adjusted demo climate scenario"
    if farm.mock_soil_ph is not None:
        soil["ph"] = farm.mock_soil_ph
        soil["ph_check"] = check_soil_ph(farm.mock_soil_type, farm.mock_soil_ph)
        soil["source"] = "User-adjusted demo soil scenario"
    if farm.mock_organic_matter_percent is not None:
        soil["organic_matter_percent"] = farm.mock_organic_matter_percent
        soil["source"] = "User-adjusted demo soil scenario"

    water_per_dunam = farm.available_water_m3 / farm.area_dunams
    crops = _crop_scores(farm, soil, climate)

    rainfall = climate["annual_rainfall_mm"]
    if water_per_dunam < 32 and rainfall < 300:
        water_level = "high"
    elif water_per_dunam < 45 or rainfall < 400:
        water_level = "medium"
    else:
        water_level = "low"
    temperature = climate["average_temperature_c"]
    heat_level = "high" if temperature > 30 else "medium" if temperature > 24 else "low"

    return AnalysisResponse(
        data_label="Demo / Mock Data",
        disclaimer=DISCLAIMER,
        request_summary=farm,
        climate=climate,
        soil=soil,
        suggested_crops=crops,
        risks=[
            {
                "type": "Water pressure",
                "level": water_level,
                "note": f"Based on {water_per_dunam:.1f} m³ per dunam and {rainfall} mm scenario rainfall.",
            },
            {
                "type": "Heat exposure",
                "level": heat_level,
                "note": f"Based on the {temperature:.1f}°C adjustable scenario temperature.",
            },
            {
                "type": "Rotation fatigue",
                "level": "medium" if farm.previous_crop.lower() in {"wheat", "barley"} else "low",
                "note": "A simple crop-family repeat check; no field history is stored.",
            },
        ],
    )


def suggest_rotation(farm: FarmInput) -> RotationResponse:
    climate = climate_for(farm.latitude)
    soil = soil_for(farm.longitude, farm.mock_soil_type)
    if farm.mock_temperature_c is not None:
        climate["average_temperature_c"] = farm.mock_temperature_c
    if farm.mock_rainfall_mm is not None:
        climate["annual_rainfall_mm"] = farm.mock_rainfall_mm
    if farm.mock_soil_ph is not None:
        soil["ph"] = farm.mock_soil_ph
    if farm.mock_organic_matter_percent is not None:
        soil["organic_matter_percent"] = farm.mock_organic_matter_percent
    crops = [item["crop"] for item in _crop_scores(farm, soil, climate)]

    explanations = [
        f"Highest current fit after moving away from the previous {farm.previous_crop} crop.",
        "Second-ranked option under the adjustable climate, soil, and water scenario.",
        "Third-ranked option adds variety after two contrasting seasons.",
    ]
    periods = ["Winter 2026", "Summer 2027", "Winter 2027"]

    return RotationResponse(
        data_label="Demo / Mock Data",
        disclaimer=DISCLAIMER,
        plan_name="Balanced three-season demo",
        seasons=[
            {"season": index + 1, "period": periods[index], "crop": crop, "explanation": explanations[index]}
            for index, crop in enumerate(crops)
        ],
    )
