#!/usr/bin/env python3

import json
import os.path
import sys
import typing
import unicodedata

filetype2length = {
    "rhr": 5,
    "pn": 5,
    "rte": 7,
    "operation": 4,
}
filetype2labels: typing.Dict[str, typing.Set[str]] = {
    "rhr": {"0", "1"},
    "pn": {"0", "1", "-1"},
    "rte": {"0", "1"},
}

filetype2judgeindex: typing.Dict[str, int] = {
    "rhr": 3,
    "pn": 3,
    "rte": 4,
}

filetype2contentspan: typing.Dict[str, typing.Tuple[int, int]] = {
    "rhr": (2, 3),
    "pn": (2, 3),
    "rte": (2, 4),
    "operation": (1, 4),
}


def _check_judge(text: str, labels: typing.Set[str]) -> typing.Optional[str]:
    judge = json.loads(text)
    if judge is None:
        return None

    if isinstance(judge, list):
        judge_keys = set()
        judge_vals = set()
        for j in judge:
            judge_keys |= set(j.keys())
            judge_vals |= set(j.values())
    else:
        judge_keys = set(judge.keys())
        judge_vals = set(judge.values())

    if len(judge_keys - labels) > 0:
        return f"Invalid judge: {judge}"
    for v in judge_vals:
        if not isinstance(v, int):
            return f"Invalid judge format: {v}"

    return None


def _check_evidence(text: str, hyp: str) -> typing.Optional[str]:
    evd = json.loads(text)
    if evd is None:
        return None

    if not isinstance(evd, list):
        return "Invalid format"

    for k, v in evd:
        if not isinstance(v, int):
            return "Invalid evidence format"
        elif not isinstance(k, str):
            return "Invalid evidence format"
        elif k not in {"<1>", "<unknown>"} and k not in hyp:
            return "Invalid evidence format"
    return None


def check_line(filetype: str, line: str) -> typing.List[str]:
    # NFKC check
    if line != unicodedata.normalize("NFKC", line):
        return ["Not NFKC normalized"]

    items = line[:-1].split("\t")
    errors = []

    if filetype is None:
        return ["Invalid filetype"]
    if filetype != "operation" and not items[0].startswith(filetype):
        errors.append("Invalid ID prefix")

    # Column number check
    length = filetype2length.get(filetype)
    if len(items) != length:
        errors.append(f"Invalid column number: {length}")

    if filetype == "operation":
        if items[2] not in {"replace", "insert"}:
            errors.append(f"Invalid operation: {items[2]}")
        if items[3] not in {"hypothesis", "premise"}:
            errors.append(f"Invalid target: {items[2]}")
        return errors

    labels = filetype2labels[filetype]
    if items[1] not in labels:
        errors.append(f"Invalid label: [{items[1]}]")

    if items[-1] not in {"train", "dev", "test"}:
        errors.append(f"Invalid usage: [{items[-1]}]")

    judge_index = filetype2judgeindex[filetype]
    err = _check_judge(items[judge_index], labels)
    if err:
        errors.append(err)

    if filetype == "rte":
        err = _check_evidence(items[5], items[2])
        if err:
            errors.append(err)

    return errors


def _get_id_and_content(filetype: str, line: str) -> typing.Tuple[str, str]:
    (c_start, c_end) = filetype2contentspan[filetype]
    items = line[:-1].split("\t")
    myid: str = items[0]
    return myid, "\t".join(items[c_start:c_end])


def check(path_in: str) -> bool:
    filetype = os.path.basename(path_in).split(".")[0]
    ng: bool = False
    ids = set()
    contents = set()
    with open(path_in, "r") as inf:
        for lid, line in enumerate(inf):
            errors = check_line(filetype, line)
            if len(errors) > 0:
                sys.stdout.write(f"Error\t{path_in}\t{line}\n")
                sys.stdout.write(f'{" ".join(errors)}\n')
                ng = True

            myid, content = _get_id_and_content(filetype, line)

            if myid in ids:
                sys.stdout.write(f"Error\t{path_in}\t{line} ({lid})\n")
                sys.stdout.write("ID is duplicated\n")
                ng = True
            else:
                ids.add(myid)

            if content in contents:
                sys.stdout.write(f"Error\t{path_in}\t{line}\n")
                sys.stdout.write("Content is duplicated\n")
                ng = True
            else:
                contents.add(content)

    return ng


def main() -> None:
    ng = False
    for fname in sys.argv[1:]:
        ng |= check(fname)

    if ng:
        sys.exit(1)


if __name__ == "__main__":
    main()
