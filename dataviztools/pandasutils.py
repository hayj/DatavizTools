import pandas as pd

def coloriseDFColumns(*args, **kwargs):
    return colorise_df_columns(*args, **kwargs)
def colorise_df_columns(df, grey=None, blue=None, red=None, green=None,
                       grey_rgba=(150, 150, 150, 0.3),
                       green_rgba=(0, 155, 149, 0.3),
                       blue_rgba=(0, 122, 204, 0.3),
                       red_rgba=(242, 82, 82, 0.3)):
    """
        This function return a new DataFrame.
        Choose colors for columns you give in grey, blue, red and green lists.
        
        Usage example:
        
            df = colorise_df_columns(df, grey={'id'}, red={'score', 'loss'})
    """
    # Default are empty sets:
    colors = {'grey': grey, 'blue': blue, 'red': red, 'green': green}
    for color in colors:
        if colors[color] is None:
            colors[color] = set()
        elif isinstance(colors[color], str):
            colors[color] = {colors[color]}
    # Making a css_colors dict:
    css_colors = {'grey': grey_rgba, 'blue': blue_rgba, 'red': red_rgba, 'green': green_rgba}
    pre = 'background-color: rgba('
    post = ')'
    for css_color in css_colors:
        css_colors[css_color] = pre + ', '.join([str(e) for e in css_colors[css_color]]) + post
    # Checking if we have duplicates columns:
    union = set()
    total = 0
    for color in colors:
        for column in colors[color]:
            union.add(column)
            total += 1
    if total != len(union):
        raise Exception("Duplicates in columns between colors")
    # Removing elements not in df.columns:
    for color in colors:
        for column in set(colors[color]):
            if column not in df.columns:
                colors[color].remove(column)
    # We define the colorize funct:
    def colorize(df):
        df = pd.DataFrame('', index=df.index, columns=df.columns)
        for color in colors:
            current_css_color = css_colors[color]
            for column in colors[color]:
                column_index = df.columns.get_loc(column)
                df.iloc[:, column_index] = current_css_color
        return df
    # We apply and return the Styler object:
    return df.style.apply(colorize, axis=None)

def reorder_df_columns(*args, **kwargs):
    return reorderDFColumns(*args, **kwargs)
def reorderDFColumns(df, start=None, end=None):
    """
        This function reorder columns of a DataFrame.
        It takes columns given in the list `start` and move them to the left.
        Its also takes columns in `end` and move them to the right.
    """
    if start is None:
        start = []
    if end is None:
        end = []
    assert isinstance(start, list) and isinstance(end, list)
    cols = list(df.columns)
    for c in start:
        if c not in cols:
            start.remove(c)
    for c in end:
        if c not in cols or c in start:
            end.remove(c)
    for c in start + end:
        cols.remove(c)
    cols = list(start) + cols + list(end)
    return df[cols]