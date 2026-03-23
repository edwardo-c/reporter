import pandas as pd
from collections import defaultdict

def get_tree(df: pd.DataFrame, child_col: str, parent_col: str) -> defaultdict[str, list]:
    """
    converts a dataframe with child -> parent relationships
    
    per row to: parent: child, grandparent: child and grandchild

    example: 
    
    df = pd.DataFrame(
    data=[
        ('k425', 'karina', 'k926'),
        ('k926', 'kayla',  's711'),
        ('s711', 'susan',  's225'),
    ], 
    columns=['id', 'name', 'parent_id']
    )

    expected:
    {
        'k926': ['k425',]
        's711': ['k425', 'k926',]
        's225': ['k425', 'k926', 's711']  
    }

    """
    result = defaultdict(list)

    for r in df.itertuples():
        
        child = getattr(r, child_col)
        parent = getattr(r, parent_col)
        
        result[parent].append(child)

        """if child has children, add those children to current"""
        children = result.get(child, None)
        if children:
            existing = result[parent]
            result[parent] = [*existing, *children]

    return result