import re

def validate_iranian_national_id(national_id: str) -> bool:
    """
    Validates an Iranian National ID (Code Melli).
    
    Args:
        national_id: A string representing the national ID.
        
    Returns:
        True if valid, False otherwise.
    """
    if not re.match(r'^\d{10}$', national_id):
        return False

    check_digit = int(national_id[9])
    
    # Check if all digits are the same (e.g., 1111111111 is invalid)
    if len(set(national_id)) == 1:
        return False

    sum_digits = sum(int(national_id[i]) * (10 - i) for i in range(9))
    remainder = sum_digits % 11

    if remainder < 2:
        return check_digit == remainder
    else:
        return check_digit == (11 - remainder)
