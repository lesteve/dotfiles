#!/usr/bin/env python3
import argparse
import os
import sys
from email.parser import BytesHeaderParser
from email.utils import format_datetime, parsedate_to_datetime
from pathlib import Path
from datetime import datetime


def first_header_boundary(data):
    # RFC email uses CRLF, but local Maildir files are often LF-only.
    for sep in (b"\r\n\r\n", b"\n\n"):
        index = data.find(sep)
        if index != -1:
            return index, sep
    return len(data), b"\n\n"


def header_line_ending(header_bytes):
    # Match the existing header style for the inserted Date line.
    if b"\r\n" in header_bytes:
        return b"\r\n"
    return b"\n"


def received_dates(message):
    for received in message.get_all("Received", []):
        # The date-time in a Received header conventionally follows the last ';'.
        if ";" not in received:
            continue

        candidate = received.rsplit(";", 1)[1].strip()
        try:
            yield parsedate_to_datetime(candidate)
        except (TypeError, ValueError, IndexError, OverflowError):
            continue


def date_from_received(message):
    dates = list(received_dates(message))
    if not dates:
        return None

    # Received headers are prepended by each hop. The last one is usually the
    # earliest visible handoff and closest available proxy for the message date.
    return dates[-1]


def date_for_message(path, message):
    date = date_from_received(message)
    if date is not None:
        return format_datetime(date), "Received"

    date =  datetime.fromtimestamp(path.stat().st_mtime).astimezone()
    return format_datetime(date), "mtime"


def add_date_header(path, dry_run=False):
    data = path.read_bytes()
    header_end, header_separator = first_header_boundary(data)
    header_bytes = data[:header_end]
    message = BytesHeaderParser().parsebytes(data)

    if message["Date"] is not None:
        return "skipped", "Date header already present"

    newline = header_line_ending(header_bytes)
    date_value, source = date_for_message(path, message)
    date_line = b"Date: " + date_value.encode("ascii") + newline

    if dry_run:
        return "would-update", f"would add Date from {source}: {date_value}"

    if header_end == 0:
        # no header in the original email
        updated = date_line + header_separator + data[len(header_separator) :]
    else:
        updated = date_line + data

    path.write_bytes(updated)
    return "updated", f"added Date from {source}: {date_value}"


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Add a Date header to mail files that do not already have one."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="mail files or directories to update",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report changes without rewriting files",
    )
    return parser.parse_args(argv)


def iter_files(paths):
    for path in paths:
        if path.is_dir():
            for root, _, files in os.walk(path):
                for name in files:
                    yield Path(root) / name
        else:
            yield path


def main(argv):
    args = parse_args(argv)
    exit_code = 0

    for path in iter_files(args.paths):
        try:
            if not path.is_file():
                print(f"{path} skipped: not a regular file")
                continue

            status, message = add_date_header(
                path,
                dry_run=args.dry_run,
            )
            print(f"{path} {status}: {message}")
        except OSError as exc:
            exit_code = 1
            print(f"{path} error: {exc}", file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
