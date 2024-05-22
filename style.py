class Table:
    style_cell_conditional = [
        {
            "if": {"column_id": "Исполнитель"},
            "textAlign": "left"
        }
    ]
    style_data_conditional = [
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "rgb(220, 220, 220)",
        }
    ]
    style_header = {
        "backgroundColor": "rgb(210, 210, 210)",
        "color": "black",
        "fontWeight": "bold"
    }
