import os

import csv
import json
import numpy

import typer

from node_class import Node


class NumpyArrayEncoder(json.JSONEncoder):
    """
    Convert list object into json format
    """
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def save_to_file(to_format: str, output: str, node: Node) -> None:
    """
    Function that saves results to the given path
    :param to_format: json or csv
    :param output: path to file
    :param node: main instance of Node()
    :return:
    """
    file_name = f"data.{to_format}"
    check_if_output_exist(output)

    get_all_nodes, _ = node.depth_first_search(array=[], to_format=to_format)

    to_format = to_format.lower()
    if to_format == "csv":
        columns = ["link", "title", "number of internal links", "number of external links",
                   "number of times url was referenced by other pages"]

        with open(f"{output}/{file_name}", 'w', encoding='UTF-8') as f:
            writer = csv.writer(f)

            writer.writerow(columns)
            writer.writerows(get_all_nodes)

    elif to_format == "json":
        numpy_array = numpy.array(get_all_nodes)

        with open(f"{output}/{file_name}", 'w', encoding='UTF-8') as f:
            json.dump(numpy_array, f, cls=NumpyArrayEncoder)

    else:
        typer.secho("Please choose the correct format file | json or csv |", fg=typer.colors.RED)
        return


def check_if_output_exist(output: str) -> None:
    """Create new directory, if it doesn't exist
    :param output - path to file
    :return: boolean
    """
    is_exist = os.path.exists(output)
    if not is_exist:
        os.makedirs(output)
        typer.secho('New directory was created to save the results.', fg=typer.colors.YELLOW)
