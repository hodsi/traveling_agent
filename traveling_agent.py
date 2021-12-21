from copy import deepcopy
from typing import List, Optional, Iterator

from entities.route import Route
from entities.weights_matrix import WeightsMatrix


def subtract_rows(matrix: WeightsMatrix):
    for i in range(len(matrix)):
        row = matrix.matrix_of_weights[i]
        row_min = min(row)
        matrix.matrix_of_weights[i] = [max(0, value - row_min) for value in row]


def invert_matrix(matrix: WeightsMatrix):
    matrix.matrix_of_weights = [[*column] for column in zip(*matrix.matrix_of_weights)]


def calc_subtracted_matrix(weights_matrix: WeightsMatrix):
    weights_matrix_copy = deepcopy(weights_matrix)
    subtract_rows(weights_matrix_copy)
    # subtract columns
    invert_matrix(weights_matrix_copy)
    subtract_rows(weights_matrix_copy)
    invert_matrix(weights_matrix_copy)
    return weights_matrix_copy


def convert_matrix_for_circle_findings(matrix: WeightsMatrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j:
                matrix.matrix_of_weights[i][j] = False
            else:
                # It makes zeros to True, and the else to False
                matrix.matrix_of_weights[i][j] = not matrix.matrix_of_weights[i][j]


def get_the_truest_row_index(matrix: WeightsMatrix):
    number_of_truths = [sum(row) for row in matrix.matrix_of_weights]
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


def calc_approximate_route(weights_matrix: WeightsMatrix):
    subtracted_matrix = calc_subtracted_matrix(weights_matrix)
    convert_matrix_for_circle_findings(subtracted_matrix)
    possible_circles = [*find_circles(subtracted_matrix)]
    circles_to_take = min(possible_circles, key=(lambda circle: len(circle)))
    print(circles_to_take)
