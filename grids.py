def grid(cols, rows, colSize=1, rowSize=1):
    """
    Returns an iterator that provides coordinate tuples. Example:
    # for x, y in grid(10, 10, 12, 12):
    #     rect(x, y, 10, 10)
    """
    rowRange = range(int(rows))
    colRange = range(int(cols))
    for y in rowRange:
        for x in colRange:
            yield (x * colSize, y * rowSize)
