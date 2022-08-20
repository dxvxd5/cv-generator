import enum

import click

from converters.prometheus.prometheus import PrometheusConverter

MSG_TYPE = enum.Enum("MSG_TYPE", "INFO SUCCESS ERROR")


def get_converter(template: str):
    if template == "prometheus":
        return PrometheusConverter
    else:
        raise ValueError(f"Unknown template: {template}")


def info(msg: str):
    print_msg(msg, MSG_TYPE.INFO)


def success(msg: str):
    print_msg(msg, MSG_TYPE.SUCCESS)


def error(msg: str):
    print_msg(msg, MSG_TYPE.ERROR)


def print_msg(msg: str, type: MSG_TYPE):
    if type == MSG_TYPE.INFO:
        icon = "i"
        color = "blue"
    elif type == MSG_TYPE.SUCCESS:
        icon = "✔"
        color = "green"
    elif type == MSG_TYPE.ERROR:
        icon = "✖"
        color = "red"
    else:
        raise ValueError(f"Unknown message type: {type}")

    click.secho(f"{icon} {msg}", fg=color)
