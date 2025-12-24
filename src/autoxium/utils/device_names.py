"""
Device model to marketing name mapping database
This maps model numbers (like SM-A725F) to their marketing names (like Galaxy A72)
"""

# Samsung Galaxy devices mapping
SAMSUNG_MODELS = {
    # Galaxy S Series
    "SM-S918U": "Galaxy S23 Ultra",
    "SM-S918B": "Galaxy S23 Ultra",
    "SM-S918N": "Galaxy S23 Ultra",
    "SM-S916U": "Galaxy S23+",
    "SM-S916B": "Galaxy S23+",
    "SM-S911U": "Galaxy S23",
    "SM-S911B": "Galaxy S23",
    
    "SM-S908U": "Galaxy S22 Ultra",
    "SM-S908B": "Galaxy S22 Ultra",
    "SM-S906U": "Galaxy S22+",
    "SM-S906B": "Galaxy S22+",
    "SM-S901U": "Galaxy S22",
    "SM-S901B": "Galaxy S22",
    
    "SM-G998U": "Galaxy S21 Ultra",
    "SM-G998B": "Galaxy S21 Ultra",
    "SM-G996U": "Galaxy S21+",
    "SM-G996B": "Galaxy S21+",
    "SM-G991U": "Galaxy S21",
    "SM-G991B": "Galaxy S21",
    
    # Galaxy A Series
    "SM-A725F": "Galaxy A72",
    "SM-A725M": "Galaxy A72",
    "SM-A726B": "Galaxy A72 5G",
    
    "SM-A715F": "Galaxy A71",
    "SM-A716B": "Galaxy A71 5G",
    
    "SM-A546B": "Galaxy A54 5G",
    "SM-A546E": "Galaxy A54 5G",
    
    "SM-A536B": "Galaxy A53 5G",
    "SM-A536E": "Galaxy A53 5G",
    
    "SM-A525F": "Galaxy A52",
    "SM-A526B": "Galaxy A52 5G",
    
    "SM-A515F": "Galaxy A51",
    "SM-A516B": "Galaxy A51 5G",
    
    "SM-A346B": "Galaxy A34 5G",
    "SM-A336B": "Galaxy A33 5G",
    "SM-A326B": "Galaxy A32 5G",
    "SM-A325F": "Galaxy A32",
    
    "SM-A245F": "Galaxy A24",
    "SM-A235F": "Galaxy A23",
    "SM-A225F": "Galaxy A22",
    "SM-A217F": "Galaxy A21s",
    
    "SM-A146B": "Galaxy A14 5G",
    "SM-A145F": "Galaxy A14",
    "SM-A135F": "Galaxy A13",
    "SM-A125F": "Galaxy A12",
    "SM-A115F": "Galaxy A11",
    
    # Galaxy Note Series
    "SM-N986U": "Galaxy Note20 Ultra",
    "SM-N986B": "Galaxy Note20 Ultra",
    "SM-N981U": "Galaxy Note20",
    "SM-N981B": "Galaxy Note20",
    
    # Galaxy Z Series (Foldables)
    "SM-F936U": "Galaxy Z Fold4",
    "SM-F936B": "Galaxy Z Fold4",
    "SM-F926U": "Galaxy Z Fold3",
    "SM-F926B": "Galaxy Z Fold3",
    
    "SM-F721U": "Galaxy Z Flip4",
    "SM-F721B": "Galaxy Z Flip4",
    "SM-F711U": "Galaxy Z Flip3",
    "SM-F711B": "Galaxy Z Flip3",
    
    # Galaxy M Series
    "SM-M546B": "Galaxy M54 5G",
    "SM-M536B": "Galaxy M53 5G",
    "SM-M526B": "Galaxy M52 5G",
    "SM-M336B": "Galaxy M33 5G",
    "SM-M326B": "Galaxy M32 5G",
}

# Google Pixel devices - usually ro.product.model already contains the marketing name
GOOGLE_MODELS = {
    "Pixel 8 Pro": "Pixel 8 Pro",
    "Pixel 8": "Pixel 8",
    "Pixel 7 Pro": "Pixel 7 Pro",
    "Pixel 7": "Pixel 7",
    "Pixel 7a": "Pixel 7a",
    "Pixel 6 Pro": "Pixel 6 Pro",
    "Pixel 6": "Pixel 6",
    "Pixel 6a": "Pixel 6a",
    "Pixel 5": "Pixel 5",
    "Pixel 5a": "Pixel 5a",
    "Pixel 4a": "Pixel 4a",
    "Pixel 4": "Pixel 4",
    "Pixel 4 XL": "Pixel 4 XL",
}

# Xiaomi devices
XIAOMI_MODELS = {
    "M2101K6G": "Mi 11",
    "M2102K1G": "Mi 11 Lite 5G",
    "2201123G": "Redmi Note 11 Pro 5G",
    "2201117TG": "Redmi Note 11",
    "21061119DG": "11T Pro",
    "21061119AG": "11T",
}

# OnePlus devices
ONEPLUS_MODELS = {
    "CPH2449": "OnePlus 11",
    "CPH2413": "OnePlus 10 Pro",
    "LE2123": "OnePlus 9 Pro",
    "LE2121": "OnePlus 9",
    "IN2023": "OnePlus 8 Pro",
    "IN2013": "OnePlus 8",
}

def get_marketing_name(model_number: str, manufacturer: str = "") -> str:
    """
    Get the marketing name for a device model number
    
    Args:
        model_number: The device model number (e.g., "SM-A725F", "Pixel 7")
        manufacturer: The manufacturer name (optional, helps with lookup)
    
    Returns:
        Marketing name if found, otherwise returns the model_number unchanged
    """
    if not model_number:
        return ""
    
    # Remove /DS suffix from Samsung models (dual SIM variant)
    clean_model = model_number.replace("/DS", "")
    
    # Try Samsung models
    if clean_model in SAMSUNG_MODELS:
        return SAMSUNG_MODELS[clean_model]
    
    # Try Google Pixel (model number is usually already the marketing name)
    if clean_model in GOOGLE_MODELS:
        return GOOGLE_MODELS[clean_model]
    
    # Try Xiaomi
    if clean_model in XIAOMI_MODELS:
        return XIAOMI_MODELS[clean_model]
    
    # Try OnePlus
    if clean_model in ONEPLUS_MODELS:
        return ONEPLUS_MODELS[clean_model]
    
    # If manufacturer is known, try partial matching
    manufacturer_lower = manufacturer.lower()
    
    # For Google Pixel, the model is already the marketing name
    if manufacturer_lower == "google" and "pixel" in model_number.lower():
        return model_number
    
    # Return original model number if no mapping found
    return model_number
