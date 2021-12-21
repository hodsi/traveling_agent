from copy import deepcopy
from typing import List, Optional, Iterator

from entities.line import Line
from entities.route import Route
from entities.weights_matrix import WeightsMatrix


def subtract_rows(matrix: WeightsMatrix):
    for i in range(len(matrix)):
        row = matrix.matrix_of_weights[i]
        row_min = min(row)
        matrix.matrix_of_weights[i] = [value - row_min for value in row]


def invert_matrix(matrix: WeightsMatrix):
    matrix.matrix_of_weights = [[*column] for column in zip(*matrix.matrix_of_weights)]


def calc_subtracted_matrix(weights_matrix: WeightsMatrix) -> WeightsMatrix:
    weights_matrix_copy = deepcopy(weights_matrix)
    subtract_rows(weights_matrix_copy)
    # subtract columns
    invert_matrix(weights_matrix_copy)
    subtract_rows(weights_matrix_copy)
    invert_matrix(weights_matrix_copy)
    return weights_matrix_copy


def convert_matrix_for_circle_findings(matrix: WeightsMatrix, falsify_diagonal=True):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j and falsify_diagonal:
                matrix.matrix_of_weights[i][j] = False
            else:
                # It makes zeros to True, and the else to False
                matrix.matrix_of_weights[i][j] = not matrix.matrix_of_weights[i][j]


def get_the_truest_row_index(matrix: WeightsMatrix) -> int:
    number_of_truths = [row.count(True) for row in matrix.matrix_of_weights]
    return number_of_truths.index(max(number_of_truths))


def find_circles(
        matrix: WeightsMatrix, routes: Optional[List[Route]] = None, current_row: Optional[int] = None
) -> Iterator[List[Route]]:
    if current_row is None:
        current_row = get_the_truest_row_index(matrix)
    routes: List[Route] = routes or [Route([current_row])]
    if sum(len(route) for route in routes) == len(matrix):
        if matrix.matrix_of_weights[routes[-1].vertexes[-1]][routes[-1].vertexes[0]]:
            routes[-1].is_circle = True
            yield deepcopy(routes)
        return
    for i in range(len(matrix.matrix_of_weights[current_row])):
        if matrix.matrix_of_weights[current_row][i]:
            # if we completed a circle, or if we keep opening a valid circle
            if (
                    (i == routes[-1].vertexes[0]) or
                    (i not in sum((route.vertexes for route in routes), []))
            ):
                temp_row = matrix.matrix_of_weights[current_row]
                matrix.matrix_of_weights[current_row] = [False] * len(matrix)
                if i == routes[-1].vertexes[0]:
                    routes[-1].is_circle = True
                    truest_row_index = get_the_truest_row_index(matrix)
                    routes.append(Route([truest_row_index]))
                    yield from find_circles(matrix, routes, truest_row_index)
                    routes.pop()
                    routes[-1].is_circle = False
                else:
                    routes[-1].add_vertex(i)
                    yield from find_circles(matrix, routes, i)
                    routes[-1].vertexes.pop()
                matrix.matrix_of_weights[current_row] = temp_row


def get_covering_line(matrix: WeightsMatrix) -> Line:
    row = get_the_truest_row_index(matrix)
    row_truthes = matrix.matrix_of_weights[row].count(True)
    invert_matrix(matrix)
    column = get_the_truest_row_index(matrix)
    column_truthes = matrix.matrix_of_weights[column].count(True)
    invert_matrix(matrix)
    return Line(row=row) if row_truthes >= column_truthes else Line(column=column)


def falsify_line(matrix: WeightsMatrix, line: Line):
    for i in range(len(matrix)):
        if line.row is None:
            matrix.matrix_of_weights[i][line.column] = False
        else:
            matrix.matrix_of_weights[line.row][i] = False


def get_covering_lines(matrix: WeightsMatrix) -> List[Line]:
    covering_matrix = deepcopy(matrix)
    convert_matrix_for_circle_findings(covering_matrix, False)
    covering_lines = []
    while True in covering_matrix:
        line = get_covering_line(covering_matrix)
        covering_lines.append(line)
        falsify_line(covering_matrix, line)
    return covering_lines


def optimize_matrix_placement(matrix: WeightsMatrix):
    while len(covering_lines := get_covering_lines(matrix)) != len(matrix):
        uncovered_weights = []
        for i, row in enumerate(matrix.matrix_of_weights):
            for j, weight in enumerate(row):
                if not any(line.is_coordinate_on_line(i, j) for line in covering_lines):
                    uncovered_weights.append(weight)
        subtraction_number = min(uncovered_weights)
        for i, row in enumerate(matrix.matrix_of_weights):
            for j in range(len(row)):
                # if the coordinate is on an intersection
                covering_lines_count = [line.is_coordinate_on_line(i, j) for line in covering_lines].count(True)
                if covering_lines_count > 1:
                    matrix.matrix_of_weights[i][j] += subtraction_number
                elif covering_lines_count < 1:
                    matrix.matrix_of_weights[i][j] -= subtraction_number


def calc_approximate_route(weights_matrix: WeightsMatrix):
    subtracted_matrix = calc_subtracted_matrix(weights_matrix)
    optimize_matrix_placement(subtracted_matrix)
    convert_matrix_for_circle_findings(subtracted_matrix)
    possible_circles = [*find_circles(subtracted_matrix)]
    circles_to_take = min(possible_circles, key=(lambda circle: len(circle)))
    print(circles_to_take)
