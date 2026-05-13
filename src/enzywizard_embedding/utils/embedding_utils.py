from __future__ import annotations
import torch
import esm
from typing import Tuple, Any, Dict, List
from functools import lru_cache

@lru_cache(maxsize=4)
def load_esm2(model_name: str = "esm2_t6_8M_UR50D") -> Tuple[torch.nn.Module, esm.data.Alphabet]:
    """
    Load ESM2 model + alphabet once (cached).
    """
    loader = getattr(esm.pretrained, model_name, None)
    if loader is None:
        raise ValueError(f"Unknown ESM2 model name: {model_name}")

    model, alphabet = loader()
    model.eval()
    return model, alphabet


def postprocess_embedding_report_to_schema(raw_report: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Postprocess the raw EnzyWizard-Embedding report to match the new JSON Schema.

    """

    if not isinstance(raw_report, dict):
        return None

    raw_output_type = raw_report.get("output_type")
    if raw_output_type != "enzywizard_embedding":
        return None

    raw_embeddings = raw_report.get("embeddings")
    if not isinstance(raw_embeddings, list):
        return None

    sequence_embeddings: List[Dict[str, Any]] = []

    allowed_residue_names = set("ACDEFGHIKLMNPQRSTVWY")

    for raw_item in raw_embeddings:
        if not isinstance(raw_item, dict):
            return None

        residue_index = raw_item.get("aa_id")
        residue_name = raw_item.get("aa_name")
        residue_embedding = raw_item.get("embedding")

        if not isinstance(residue_index, int):
            return None

        if not isinstance(residue_name, str):
            return None

        if residue_name not in allowed_residue_names:
            return None

        if not isinstance(residue_embedding, list):
            return None

        if len(residue_embedding) < 1:
            return None

        for value in residue_embedding:
            if not isinstance(value, (int, float)):
                return None

        sequence_embeddings.append(
            {
                "residue_index": residue_index,
                "residue_name": residue_name,
                "residue_embedding": residue_embedding,
            }
        )

    schema_report: Dict[str, Any] = {
        "report_type": "enzywizard_embedding",
        "sequence_embeddings": sequence_embeddings,
    }

    return schema_report