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
    def __init__(self, payload: Mapping[Any, Any]):

        self.keys_to_idx:             dict[str, int] = {}
        self._norm_keys_to_idx:       dict[str, int] = {}

        self.labels_to_idx:           dict[str, int] = {}
        self._norm_labels_to_idx:     dict[str, int] = {}
        
        self.grp_keys_to_idx:         dict[str, int] = {}
        self._norm_grp_keys_to_idx:   dict[str, int] = {}
        
        self.grp_labels_to_idx:       dict[str, int] = {}
        self._norm_grp_labels_to_idx: dict[str, int] = {}

        self.agg_keys_to_idx:         dict[str, int] = {}
        self._norm_agg_keys_to_idx:   dict[str, int] = {}

        self.agg_labels_to_idx:       dict[str, int] = {}
        self._norm_agg_labels_to_idx: dict[str, int] = {}

        self._init_detail_maps(payload)
        self._init_grouping_maps(payload)
        self._init_agg_maps(payload)

    def _init_agg_maps(self, payload: Mapping[Any, Any]):
        col_info = payload["reportExtendedMetadata"]["aggregateColumnInfo"]

        maps = self._extract_maps(col_info)

        self.agg_keys_to_idx         = maps["keys_to_idx"]
        self._norm_agg_keys_to_idx   = maps["norm_keys_to_idx"]
        self.agg_labels_to_idx       = maps["labels_to_idx"]
        self._norm_agg_labels_to_idx = maps["norm_labels_to_idx"]

    def _init_detail_maps(self, payload: Mapping[Any, Any]):
        col_info = payload["reportExtendedMetadata"]["detailColumnInfo"]

        maps = self._extract_maps(col_info)

        self.keys_to_idx         = maps["keys_to_idx"]
        self._norm_keys_to_idx   = maps["norm_keys_to_idx"]
        self.labels_to_idx       = maps["labels_to_idx"]
        self._norm_labels_to_idx = maps["norm_labels_to_idx"]

    def _init_grouping_maps(self, payload: Mapping[Any, Any]):
        col_info = payload["reportExtendedMetadata"]["groupingColumnInfo"]

        maps = self._extract_maps(col_info)

        self.grp_keys_to_idx         = maps["keys_to_idx"]
        self._norm_grp_keys_to_idx   = maps["norm_keys_to_idx"]
        self.grp_labels_to_idx       = maps["labels_to_idx"]
        self._norm_grp_labels_to_idx = maps["norm_labels_to_idx"]

    @staticmethod
    def _raise_normalized_key_collision(
        norm_key: str, 
        norm_key_map: dict[str, int]
    ):
        if norm_key in norm_key_map:
                raise ValueError(
                    f"Normalized key collision '{norm_key}'"
                    "Multiple columns normalize to the same value"
                    "Use label names or disambiguate keys."
                )
    
    @staticmethod
    def _raise_normalized_label_collision(
        norm_label: str, 
        norm_label_map: dict[str, int]
    ):
        if norm_label in norm_label_map:
            raise ValueError(
            f"Normalized label collision '{norm_label}'"
                "Multiple columns normalize to the same value"
                "Use API names or disambiguate labels."
        )

    def _extract_maps(self, col_info: dict[Any, Any]):
        key_map = {}
        norm_key_map = {}
        label_map = {}
        norm_label_map = {}
        
        for idx, (raw_key, details) in enumerate(col_info.items()):
            
            raw_label = details['label']

            if raw_label in label_map: 
                raise ValueError(
                    f"Duplicate column label '{raw_label}' in report. "
                    "Labels must be unique to allow label-based lookup."
                )

            key_map[raw_key] = idx
            label_map[raw_label] = idx

            norm_key = normalize_string(raw_key)
            norm_label = normalize_string(raw_label)

            self._raise_normalized_key_collision(norm_key, norm_key_map)
            self._raise_normalized_label_collision(norm_label, norm_label_map)
            
            norm_key_map[norm_key] = idx
            norm_label_map[norm_label] = idx

        return {
            "keys_to_idx": key_map, 
            "norm_keys_to_idx": norm_key_map, 
            "labels_to_idx": label_map, 
            "norm_labels_to_idx": norm_label_map
        }

    def get_index_by_key(self, key_name: str) -> int:
        norm_name = normalize_string(key_name)
        if norm_name not in self._norm_keys_to_idx:  
            raise KeyError(
                f"Column key '{key_name}' not found"
                "Available keys come from report detailColumnInfo."
            )
        return self._norm_keys_to_idx[norm_name]
    
    def get_index_by_label(self, label_name: str) -> int:
        norm_name = normalize_string(label_name)
        if norm_name not in self._norm_labels_to_idx:  
            raise KeyError(
                f"Column label '{label_name}' not found"
                 "Labels must match the report column labels"
            )
        return self._norm_labels_to_idx[norm_name]

    def get_grp_index_by_key(self, grp_key_name: str) -> int:
        norm_name = normalize_string(grp_key_name)
        if norm_name not in self._norm_keys_to_idx:  
            raise KeyError(
                f"Group column key '{grp_key_name}' not found"
                "Available keys come from report 'groupingColumnInfo'"
            )
        return self._norm_grp_keys_to_idx[norm_name]
    
    def get_grp_index_by_label(self, grp_label_name: str) -> int:
        norm_name = normalize_string(grp_label_name)
        if norm_name not in self._norm_labels_to_idx:  
            raise KeyError(
                f"Column label '{grp_label_name}' not found"
                 "Labels must match the report column labels."
            )
        return self._norm_grp_labels_to_idx[norm_name]