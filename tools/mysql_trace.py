"""
MySQL concurrent command sequences visualizer.

This tool visually graphs connections and their sequence of commands.
This in intended to help you inspect and debug interacting connections' behaviors.

I recommend adding `session.execute(text("/* MY DEBUG MESSAGE */ SELECT 1;"))` lines to annotate complex transaction sequences.

Setup:
- Temporarily enable tracing to `mysql`.`general_log` using the root MySQL user (__this will reset when you restart the db instance__):
    SET GLOBAL log_output = 'TABLE';
    SET GLOBAL general_log = 'ON';

- Pip install python-dateutil, graphviz.
- Ensure the database is in the correct place.
- Call with `python tools/mysql_trace.py [command_count=40]`
- The graph should be displayed in a new window, and will be saved to `mysql_interactions.sv.png`.

Examples: See mysql_trace_example.png.
"""
from codecs import decode
from collections import Counter
from dataclasses import dataclass
from functools import cache
from json import loads
from pprint import pprint
from subprocess import run
from sys import argv

from dateutil.parser import parse
from graphviz import Digraph

sql_statement = bytearray(f"SELECT event_time, user_host, thread_id, command_type, argument FROM mysql.general_log ORDER BY event_time DESC LIMIT {argv[1] if len(argv) > 1 else 40}", "utf-8")

database_config = {
    "username": "root",
    "password": "root",
    "host": "127.0.0.1",
    "port": "3305",
    "database": "jasmine_web",
}

def dehexed(part):
    if part.startswith("0x"):
        return decode(part, "hex").decode("utf-8")
    else:
        return part

column_names = [
    "time",
    "host",
    "thread_id",
    "command_type",
    "argument",
]
column_name_length = max(len(column_name) for column_name in column_names)

@dataclass
class Entry:
    time: float
    host: str
    thread_id: int
    command_type: str
    argument: str


def display_rows(rows):
    for row in rows:
        for column_name, column_value in zip(column_names, row):
            print(f"{column_name.rjust(column_name_length)}: {column_value}")
        print()

def snake_case(value: str) -> str:
    return value.replace(" ", "_").lower()


@cache
def ip_hostnames():
    container_id_strs = [
        container_id
        for container_id in run("docker ps --format {{.ID}}".split(" "), capture_output=True).stdout.decode("utf-8").split("\n")
        if container_id
    ]

    container_infos = loads(
        run(
            f"docker container inspect {' '.join(container_id_strs)}".split(" "),
            capture_output=True
        ).stdout
    )
    ip_hostname = {}
    for container_info in container_infos:
        hostname = container_info["Name"]
        for network in container_info["NetworkSettings"]["Networks"].values():
            ip_hostname[network["IPAddress"]] = hostname[1:]
            ip_hostname[network["Gateway"]] = "root-host"

    return ip_hostname

def cleaned_up_hostname(host_ip_str):
    host_ip = (
        [
            part[1:-1]
            for part in host_ip_str.split()
            if part.startswith("[") and part.endswith("]")
            if len(part.split(".")) == 4
        ] + [host_ip_str]
    )[0]
    return ip_hostnames().get(host_ip, host_ip)

def display_graph(
    entries,
    render_path: str | None = None,
    show: bool = False,
):
    title = "MySQL Interactions"
    graph = Digraph(name=snake_case(title), comment=title, format="png", engine="neato")

    sequence_idents = {(cleaned_up_hostname(entry.host), entry.thread_id) for entry in entries}
    sequence_first_event_time = {}
    for entry in entries:
        sequence_ident = (cleaned_up_hostname(entry.host), entry.thread_id)
        entry_time = parse(entry.time).timestamp()
        if sequence_ident not in sequence_first_event_time:
            sequence_first_event_time[sequence_ident] = entry_time
        else:
            sequence_first_event_time[sequence_ident] = min(entry_time, sequence_first_event_time[sequence_ident])


    for column_index, (hostname, thread_id) in enumerate(
            sorted(sequence_idents, key=lambda s_id: sequence_first_event_time[s_id])
    ):
        elements = [
            (entry_index, entry)
            for entry_index, entry in enumerate(entries)
            if (cleaned_up_hostname(entry.host), entry.thread_id) == (hostname, thread_id)
        ]

        sequence_name = f"{hostname}@{thread_id}"

        for in_sequence_index, (element_index, element) in enumerate(elements):
            if in_sequence_index == 0:
                graph.node(sequence_name, sequence_name, pos=f"{column_index*3},-{element_index + 0.5}!", root="true", shape="box")

            if element.command_type != "Query":
                label = element.command_type
            else:
                label = element.argument
                if len(label) > 75:
                    label = label[:40] + "..." + label[-35:]

            graph.node(str(element_index), label, pos=f"{column_index*3},-{element_index + 1}!", pin="true")

        for (current_index, _), (next_index, _) in zip(elements, elements[1:]):
            graph.edge(str(current_index), str(next_index))

    graph.render(filename=render_path, cleanup=True, view=show)

def main():
    command_parts = [
        "mysql",
        "--user={username}",
        "--password={password}",
        "--host={host}",
        "--port={port}",
        "--database={database}",
    ]

    print(" ".join([part.format(**database_config) for part in command_parts]))
    run_proc = run(
        [part.format(**database_config) for part in command_parts],
        capture_output=True,
        input=sql_statement,
    )
    result = run_proc.stdout.decode("utf-8")

    rows = [[dehexed(part) for part in line.split('\t')] for line in reversed(result.split("\n")[1:]) if line]
    display_rows(rows)

    display_graph([Entry(*row) for row in rows], show=True)


if __name__ == "__main__":
    main()
