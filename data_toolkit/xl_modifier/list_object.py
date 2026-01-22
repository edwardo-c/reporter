import xlwings as xw

def drop_columns(
        list_object,
        *,
        columns: list | str, 
        keep_widths: bool = True
    ) -> None:
    
    """
    list_object: xw table object: wb.sheets['sheet_name'].tables['table_name']
    """

    if keep_widths:
        widths_map = {}
        col_count = list_object.api.ListColumns.Count
        sht = list_object.parent

        for i in range(1, col_count):
            col_name = list_object.api.ListColumns(i).Name
            col_width = sht[:, i].column_width
            widths_map[col_name] = col_width
    
    for c in columns:
        list_object.api.ListColumns(c).Delete()

    if widths_map:
        # recalculated to account for removed columns
        col_count = list_object.api.ListColumns.Count
        
        for i in range(1, col_count):
            col_name = list_object.api.ListColumns(i).Name
            col_width = widths_map[col_name]
            sht[:, i].column_width = col_width

def rename_columns(
        list_object,
        *, 
        rename_map: dict[str, str]
    ):
        for old_name, new_name in rename_map.items():
            list_object.api.ListColumns(old_name).Name = new_name