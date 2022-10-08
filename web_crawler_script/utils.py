import os

import csv
import json
from urllib.parse import urlparse

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


def save_to_file(to_format: str, output: str, node: Node, base_url: str) -> None:
    """
    Function that saves results to the given path
    :param to_format: json or csv
    :param output: path to file
    :param node: main instance of Node()
    :return:
    """
    file_name = f"{base_url}.{to_format}"
    check_if_output_exist(output)

    get_all_nodes, _ = node.depth_first_search(array=[], to_format=to_format)

    to_format = to_format.lower()
    if to_format == "csv":
        columns = ["url", "title", "internal links count", "external links count",
                   "reference count"]

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


def is_valid(url: str) -> bool:
    """
    Checks whether 'url' is valid URL.
    Valid url means when it has schema (http or https) and netloc (e.g. www.google.com:80)
    :param url: website link
    :return: boolean
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)