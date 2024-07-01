# MIMIC-AI - Exploring MIMIC Data Using LLM and Open-WebUI

This repository contains code for exploring MIMIC data using the LLM and Open-WebUI. Open-WebUI is a web-based user interface for exploring data.

## How to Run

```shell
docker run -d -p 3100:8080 --add-host=host.docker.internal:host-gateway \
  -v /Users/gmcjy/Documents/sourcecode/MIMIC_DATA/landing/2.0:/app/local_data \
  -v mimicai:/app/backend/data \
  -v ./db:/app/db \
  --name mimicai --restart always mimicai:0.2
```