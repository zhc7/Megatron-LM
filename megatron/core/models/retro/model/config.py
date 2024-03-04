# Copyright (c) 2023, NVIDIA CORPORATION. All rights reserved.

'''Configuration dataclass for a RetroModel.'''

import types
from dataclasses import dataclass

from megatron.core.transformer import TransformerConfig


@dataclass
class RetroConfig(TransformerConfig):

    """Configuration object for Retro models.

    Attributes:

        retro_project_dir (str): Retro project directory, which contains the
            preprocessed data for for pretraining. This directory is built during
            preprocessing (see tools/retro/README.md), and contains subdirectories
            for the chunk database and pretraining neighbors.
        retro_block_size (int): Number of records to load per data file, as
            saved during preprocessing. Block processing is used for efficient
            data preprocessing.
        retro_chunk_length (int): Chunk length used for performing chunked-
            cross-attention (CCA).
        retro_encoder_layers (int): Number of layers to use for the retrieval
            encoder.
        retro_encoder_hidden_dropout (float): Hidden dropout for retrieval
            encoder.
        retro_encoder_attention_dropout (float): Attention dropout for retrieval
            encoder.
        retro_neighbor_dirs (dict): Directory names of saved neighbor id files
            for train, valid, and test datasets.
        retro_num_neighbors (int): Number of neighbors to retrieve during
            pretraining.
        retro_num_retrieved_chunks (int): Number of chunks to retrieve from the
            retrieval database.
        retro_retrieved_length (int): Cached value of retro_num_retrieved_chunks *
            retro_chunk_length (i.e., the total number of retrieved tokens;
            neighbor + continuation).
        retro_split_preprocessing (str): Data split used during data preprocessing.
        retro_verify_neighbor_count (bool): Verify that len(GPT dataset) ==
            len(saved neighbors).
    """

    # Retro.
    retro_project_dir: str = None
    retro_block_size: int = None
    retro_chunk_length: int = None
    retro_encoder_num_layers: int = 2
    retro_encoder_hidden_dropout: float = 0.1
    retro_encoder_attention_dropout: float = 0.1
    retro_neighbor_dirs: dict = None
    retro_num_neighbors: int = 2
    retro_num_retrieved_chunks: int = 2
    retro_retrieved_length: int = None
    retro_split_preprocessing: str = None
    retro_verify_neighbor_count: bool = True

    def __post_init__(self) -> None:

        super().__post_init__()

        # Preprocessing split should be defined.
        assert self.retro_split_preprocessing is not None

        # Pre-compute retrieved length.
        self.retro_retrieved_length = self.retro_num_retrieved_chunks * self.retro_chunk_length