from typing import Mapping, Any

def single_grp_to_agg(payload: Mapping[Any, Any]) -> Mapping[str, int]:
    """
    get group value (key) and aggregate value (value) in dict from payload

    payload: the salesforce api response of a predefined grouped report
    
    group_idx: the grouped column's index to be used in keys

    agg_idx: the index of the aggregate column to be used in values

    example out:
    {karina: 50, kayla: 700, edwardo: 36,}

    """
    d = {}

    for row_id, agg_detail in payload["factMap"].items():
        
        group_key = row_id.split("!")[0]
        
        try:
            group_key = int(group_key)
        except ValueError:
            continue

        k = payload["groupingsDown"]["groupings"][group_key]['value']
        v = agg_detail["aggregates"][1]["label"]
        d[k] = v

    return d
        