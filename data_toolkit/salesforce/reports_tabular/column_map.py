from typing import Any, Mapping, Callable

from utils.raises.strings import raise_invalid_string

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

        self.col_keys_to_idx:         dict[str, int] = {}
        self._norm_col_keys_to_idx:   dict[str, int] = {}

        self.col_labels_to_idx:       dict[str, int] = {}
        self._norm_col_labels_to_idx: dict[str, int] = {}
        
        self.grp_keys_to_idx:         dict[str, int] = {}
        self._norm_grp_keys_to_idx:   dict[str, int] = {}
        
        self.grp_labels_to_idx:       dict[str, int] = {}
        self._norm_grp_labels_to_idx: dict[str, int] = {}

        self.agg_keys_to_idx:         dict[str, int] = {}
        self._norm_agg_keys_to_idx:   dict[str, int] = {}

        self.agg_labels_to_idx:       dict[str, int] = {}
        self._norm_agg_labels_to_idx: dict[str, int] = {}

        self._init_column_maps(payload)
        self._init_grouping_maps(payload)
        self._init_agg_maps(payload)

    def _init_agg_maps(self, payload: Mapping[Any, Any]):
        col_info = payload["reportExtendedMetadata"]["aggregateColumnInfo"]

        maps = self._extract_maps(col_info)

        self.agg_keys_to_idx         = maps["keys_to_idx"]
        self._norm_agg_keys_to_idx   = maps["norm_keys_to_idx"]
        self.agg_labels_to_idx       = maps["labels_to_idx"]
        self._norm_agg_labels_to_idx = maps["norm_labels_to_idx"]

    def _init_column_maps(self, payload: Mapping[Any, Any]):
        col_info = payload["reportExtendedMetadata"]["detailColumnInfo"]

        maps = self._extract_maps(col_info)

        self.col_keys_to_idx         = maps["keys_to_idx"]
        self._norm_col_keys_to_idx   = maps["norm_keys_to_idx"]
        self.col_labels_to_idx       = maps["labels_to_idx"]
        self._norm_col_labels_to_idx = maps["norm_labels_to_idx"]

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

    def _extract_maps(
            self, 
            col_info: dict[Any, Any]
        ) -> Mapping[str, Mapping[str, int]]:
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

    def _get_col_index_by_key(self, col_key_name: str) -> int:
        norm_name = normalize_string(col_key_name)
        if norm_name not in self._norm_col_keys_to_idx:  
            raise KeyError(
                f"Column key '{col_key_name}' not found"
                "Available keys come from report detailColumnInfo."
            )
        return self._norm_col_keys_to_idx[norm_name]
    
    def _get_col_index_by_label(self, col_label_name: str) -> int:
        norm_name = normalize_string(col_label_name)
        if norm_name not in self._norm_col_labels_to_idx:  
            raise KeyError(
                f"Column label '{col_label_name}' not found"
                 "Labels must match the report column labels"
            )
        return self._norm_col_labels_to_idx[norm_name]

    def _get_grp_index_by_key(self, grp_key_name: str) -> int:
        norm_name = normalize_string(grp_key_name)
        if norm_name not in self._norm_grp_keys_to_idx:  
            raise KeyError(
                f"Group column key '{grp_key_name}' not found"
                "Available keys come from report 'groupingColumnInfo'"
            )
        return self._norm_grp_keys_to_idx[norm_name]
    
    def _get_grp_index_by_label(self, grp_label_name: str) -> int:
        norm_name = normalize_string(grp_label_name)
        if norm_name not in self._norm_grp_labels_to_idx:  
            raise KeyError(
                f"Column label '{grp_label_name}' not found"
                 "Labels must match the report column labels."
            )
        return self._norm_grp_labels_to_idx[norm_name]
    
    def _get_agg_index_by_key(self, agg_key_name: str) -> int:
        norm_name = normalize_string(agg_key_name)
        if norm_name not in self._norm_agg_keys_to_idx:  
            raise KeyError(
                f"Aggregate column key '{agg_key_name}' not found"
                "Available keys come from report 'aggregateColumnInfo'"
            )
        return self._norm_agg_keys_to_idx[norm_name]
    
    def _get_agg_index_by_label(self, agg_label_name: str) -> int:
        norm_name = normalize_string(agg_label_name)
        if norm_name not in self._norm_agg_labels_to_idx:  
            raise KeyError(
                f"Aggregate label '{agg_label_name}' not found"
                 "Labels must match the report group by column labels."
            )
        return self._norm_agg_labels_to_idx[norm_name]

    def _dispatch_index_getter(self, column_type: str, id_type: str) -> Callable:
        
        raise_invalid_string(column_type, "column_type")
        raise_invalid_string(id_type, "id_type")

        norm_col_type = normalize_string(column_type)
        norm_id_type = normalize_string(id_type)

        col_to_id_types = {
            "column": {
                "key": self._get_col_index_by_key,
                "label": self._get_col_index_by_label
            },

            "group" : {
                "key": self._get_grp_index_by_key,
                "label": self._get_grp_index_by_label
            },

            "agg"   : {
                "key": self._get_agg_index_by_key,
                "label": self._get_agg_index_by_label,
            },
        }

        if norm_col_type not in col_to_id_types:
            raise KeyError(
                f"Invalid column type, got: {column_type}. "
                "available options: 'column', 'group', 'agg'"
            )

        if norm_id_type not in ('key', 'label'):
            raise KeyError(
                f"Invalid id type, got: {id_type}. "
                "available options: 'key', 'label'"
            )
    
        return col_to_id_types[norm_col_type][norm_id_type]

    def get_index(self, name: str, column_type: str, id_type: str) -> int:
        """
        universal entry for all index types
        
        column_types: 
          'detail': the columns from the table
          'group': the columns in the "group by" portion 
          'agg': the summary values produced by the grouped values 
            (e.g RowCount, Amount, etc)

        id_types:
          'key': the api name from payload
          'label' the name of the column on the report

        name: the name to get the column index for
          
        """
        raise_invalid_string(name, "name")
        raise_invalid_string(column_type, "column_type")
        raise_invalid_string(id_type, "id_type")

        getter = self._dispatch_index_getter(column_type, id_type)
        return getter(name)
        
        
