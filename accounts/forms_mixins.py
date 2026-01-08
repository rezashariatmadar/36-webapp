from .utils import normalize_digits

class DigitNormalizationMixin:
    """
    Mixin for Django forms to normalize Persian/Latin digits to ASCII 
    for specified fields in the POST data.
    """
    normalize_fields = []

    def clean(self):
        cleaned_data = super().clean()
        
        # If no fields specified, try to normalize all CharFields that look like numbers?
        # Better to be explicit per spec.
        fields_to_normalize = self.normalize_fields or []
        
        for field_name in fields_to_normalize:
            if field_name in cleaned_data and isinstance(cleaned_data[field_name], str):
                cleaned_data[field_name] = normalize_digits(cleaned_data[field_name])
        
        return cleaned_data
