from __future__ import annotations
from argparse import Namespace, ArgumentParser
from ..services.embedding_service import run_embedding_service

def add_embedding_parser(parser: ArgumentParser) -> None:
    parser.add_argument("-i", "--input_fasta",required=True,help="Path to input cleaned protein sequence file in FASTA format.")
    parser.add_argument("-o", "--output_dir",required=True,help="Directory to save the output JSON report.")
    parser.add_argument("--model_name", type=str,choices=["esm2_t6_8M_UR50D", "esm2_t12_35M_UR50D", "esm2_t30_150M_UR50D"],default="esm2_t6_8M_UR50D",help="Model for embedding generation: esm2_t6_8M_UR50D, esm2_t12_35M_UR50D, esm2_t30_150M_UR50D.")


    parser.set_defaults(func=run_embedding)

def run_embedding(args: Namespace) -> None:
    run_embedding_service(input_fasta=args.input_fasta, output_dir=args.output_dir, model_name=args.model_name)

