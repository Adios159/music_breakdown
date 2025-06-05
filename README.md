# Music Breakdown

This project provides a small FastAPI application that accepts an audio file and separates it into six stems: vocals, drums, guitar, piano, bass, and other instruments. The separation is done using the [Demucs](https://github.com/facebookresearch/demucs) library's 6-stem model.

## Setup

Install the required packages (preferably inside a virtual environment):

```bash
pip install -r requirements.txt
```

Demucs will download pretrained weights on first run, so internet access is required for that step.

## Running the server

```bash
uvicorn app.main:app --reload
```

Then open `http://localhost:8000` in your browser to upload an audio file. The separated stems will be returned as a zip archive.
