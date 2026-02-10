from typing import Any, Mapping

"""
# example usage: 
cm = ColumnMap(payload)
cm.get_index_by_key("FULL_NAME")
"""

def normalize_string(s: str):
    if not isinstance(s, str):
        raise TypeError(f"expected type str, got: {type(s)}")
    return s.lower().strip()

class ColumnMap:
    def __init__(self, payload: Mapping[Any]):
        self.keys_to_idx:     dict[str, int] = {}
        self.label_to_idx:    dict[str, int] = {}
        self._norm_key_map:   dict[str, int] = {}
        self._norm_label_map: dict[str, int] = {}
        self._init_maps(payload)

    def _init_maps(self, payload):
        """single loop over detailColumnInfo to initialize all maps"""
        key_map = {}
        norm_key_map = {}
        label_map = {}
        norm_label_map = {}

        col_info = payload["reportExtendedMetadata"]["detailColumnInfo"]

        for idx, (key_name, details) in enumerate(col_info.items()):
            
            raw_label = details['label']

            if raw_label in label_map: 
                raise ValueError(
                    f"Duplicate column label '{raw_label}' in report. "
                    "Labels must be unique to allow label-based lookup."
                )

            key_map[key_name] = idx
            label_map[raw_label] = idx

            norm_key = normalize_string(key_name)
            norm_label = normalize_string(raw_label)

            if norm_key in norm_key_map:
                raise ValueError(
                    f"Normalized key collision '{norm_key}'"
                     "Multiple columns normalize to the same value"
                     "Use label names or disambiguate keys."
                )
            
            if norm_label in norm_label_map:
                    raise ValueError(
                    f"Normalized label collision '{norm_label}'"
                     "Multiple columns normalize to the same value"
                     "Use API names or disambiguate labels."
                )
            
            norm_key_map[norm_key] = idx
            norm_label_map[norm_label] = idx

        self.keys_to_idx = key_map
        self.label_to_idx = label_map
        self._norm_key_map = norm_key_map
        self._norm_label_map = norm_label_map

    def get_index_by_key(self, col_name: str) -> int:
        norm_col_name = normalize_string(col_name)
        if norm_col_name not in self._norm_key_map:  
            raise KeyError(
                f"Column key '{col_name}' not found"
                "Available keys come from report detailColumnInfo."
            )
        return self._norm_key_map[norm_col_name]
    
    def get_index_by_label(self, col_name: str) -> int:
        norm_col_name = normalize_string(col_name)
        if norm_col_name not in self._norm_label_map:  
            raise KeyError(
                f"Column label '{col_name}' not found"
                 "Labels must match the report column labels."
            )
        return self._norm_label_map[norm_col_name]
