# Mamba Hybrid

## Introduction

Here is the code used for <em>An Empirical Study of Large-Scale Mamba-based
Language Models</em>.

## Installation

Create and run a Docker container using the [Dockerfile](./Dockerfile).

```
docker build -t your_image_name:your_tag .
```

## Train

[`train.sh`](./train.sh) is an example pretraining script, showing how to run on
a single node. Select between 800M-scale and 8B-scale models by setting the
`MODEL_SCALE` variable. The 8B-scale hybrid model architecture is the same as
the one described in the paper.

## Text Generation

Use [`run_text_gen_server_8b.sh`](./run_text_gen_server_8b.sh) to start a text
generation server using an 8B hybrid checkpoint. This is configured to run the
8b hybrid model described in the paper, with tensor model parallel set to 1.
The arguments will need to be changed if using a checkpoint with a different
model parallel configuration or other differences, such as model architecture.

## Checkpoint Formats

For inference, the model must be configured to match the checkpoint file used,
including the hybrid layer configuration and model parallel configuration.

If you need to convert a hybrid checkpoint file to a different tensor parallel
or pipeline parallel size, use
[the hybrid conversion script](../../tools/checkpoint/hybrid_conversion.py).
There is an example run command at the end of that file.

Before running that script, you will need to set `PYTHONPATH` to include the
root directory of your Megatron-LM repository clone.

```
export PYTHONPATH=<path-to-megatron>:PYTHONPATH
```

## Hybrid Options

`--hybrid-attention-ratio ATT` specifies a target ratio of attention layers
to total layers. For example, 4 attention layers out of 48 total layers is
specified by `--hybrid-attention-ratio 0.08`.

`--hybrid-mlp-ratio MLP` specifies a target ratio of MLP layers to total
layers. For example, 24 MLP layers out of 48 total layers is specified by
`--hybrid-mlp-ratio 0.5`.

* (`ATT` + `MLP`) must be less than or equal to 1.0.
* (1.0 - `ATT` - `MLP`) is the hybrid mamba ratio, the ratio of mamba layers to
total layers.
* `ATT` = `MLP` = 0 is a pure Mamba model.
* `ATT` = `MLP` = 0.5 is a transfomer model.

If either `ATT` or `MLP` is greater than 0.0 or if `--hybrid-override-pattern`
is specified, the logfile will include information about the hybrid layer
pattern used. `--hybrid-override-pattern` can be used to specify a different
pattern than the default, algorithmically-generated one.

## Mamba1 vs Mamba2

The code instantiates Mamba2 by default. To select the Mamba1 code-path, change
the imports at the top of
[mamba_layer_specs.py](../../megatron/core/models/mamba/mamba_layer_specs.py),
as specified there.
