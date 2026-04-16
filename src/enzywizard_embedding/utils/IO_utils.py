from __future__ import annotations

from pathlib import Path

from ..utils.logging_utils import Logger
import json
import tempfile
from ..utils.common_utils import convert_to_json_serializable, InlineJSONEncoder, wrap_leaf_lists_as_rawjson, get_clean_filename, get_optimized_filename
from typing import List, Dict,Any, Tuple




def file_exists(path: str | Path) -> bool:
    p = Path(path)
    return p.exists() and p.is_file()

def get_stem(input_path: str | Path) -> str:
    return Path(input_path).stem

MAXFILENAME=150

def check_filename_length(name: str, logger: Logger) -> bool:
    if len(name) > MAXFILENAME:
        logger.print(f"[ERROR] Filename too long (>{MAXFILENAME}): {name}")
        return False
    return True


def write_json_from_dict(dict_data: dict, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dict_data=convert_to_json_serializable(dict_data)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(dict_data, f, indent=2, ensure_ascii=False)

def write_json_from_dict_inline_leaf_lists(dict_data: dict, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dict_data = convert_to_json_serializable(dict_data)
    dict_data = wrap_leaf_lists_as_rawjson(dict_data)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(
            dict_data,
            f,
            cls=InlineJSONEncoder,
            indent=2,
            ensure_ascii=False
        )


def load_fasta(path: str | Path, logger: Logger) -> Dict[str, str] | None:
    p = Path(path)

    try:
        header: str | None = None
        seq_parts: list[str] = []

        with p.open("r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.rstrip("\n").strip()

                if not line:
                    continue

                if line.startswith(">"):
                    if header is not None:
                        logger.print(f"[ERROR] Multiple sequences found in FASTA file: {str(p)}")
                        return None

                    header = line[1:].strip()
                else:
                    if header is None:
                        logger.print(f"[ERROR] Invalid FASTA format in {str(p)}: sequence line appears before header.")
                        return None
                    seq_parts.append(line)

        if header is None:
            logger.print(f"[ERROR] No header found in FASTA file: {str(p)}")
            return None

        sequence = "".join(seq_parts)

        if sequence.strip() == "":
            logger.print(f"[ERROR] Empty sequence found in FASTA file: {str(p)}")
            return None

        return {"header": header, "sequence": sequence}

    except Exception as e:
        logger.print(f"[ERROR] Exception in loading FASTA from {str(p)}: {e}")
        return None
