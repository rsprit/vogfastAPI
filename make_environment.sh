#!/bin/bash

conda create -y -n fastapi python=3.8 pandas numpy biopython jupyterlab
conda install -y -n fastapi -c conda-forge fastapi=0.61.1 uvicorn pydantic
