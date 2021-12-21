

class Line(object):
    def __init__(self, row: int = None, column: int = None):
        if [row, column].count(None) != 1:
            raise ValueError(f'{type(self)} should only get column or row')
        self.row = row
        self.column = column

    def is_coordinate_on_line(self, row: int, column: int):
        return self.row == row or self.column == column

    def get_intersection_point(self, other: 'Line'):
        row = self.row if self.row is not None else other.row
        column = self.column if self.column is not None else other.column
        if None not in (row, column):
            return row, column
        return None

    def __repr__(self):
        if self.row is None:
            return f'Line<column={self.column}>'
        return f'Line<row={self.row}>'
