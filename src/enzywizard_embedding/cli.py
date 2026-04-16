from __future__ import annotations

import argparse

from .commands.embedding import add_embedding_parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="enzywizard-embedding",
        description="EnzyWizard-Embedding: Generate protein embeddings from a cleaned protein sequence and a detailed JSON report."
    )
    add_embedding_parser(parser)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)