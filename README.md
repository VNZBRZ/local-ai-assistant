# Local AI Assistant 🔒

A small command-line chat assistant in Python that talks to a **locally running AI model** through [Ollama](https://ollama.com).
Everything runs on my own Linux PC, so prompts and code never leave the machine.

I built this to learn how companies can use AI **without sending sensitive data to cloud services**, and to practise Python, Linux, Docker and REST APIs.

## How it works

```
 local_ai_helper.py ──HTTP POST (JSON)──▶ Ollama (systemd service, localhost:11434) ──▶ open-weight model (on my GPU)
 Browser ─────────────────────────────▶ Open WebUI (Docker container) ──▶ Ollama
```

- **Ollama** runs as a background service (systemd) and serves an open-weight model through a local REST API.
- **local_ai_helper.py** sends the conversation as JSON to `http://localhost:11434/api/chat` and prints the answer.
  It keeps the chat history in a list, so the model remembers earlier questions.
- **Open WebUI** runs in a Docker container and gives a ChatGPT-style browser interface for the same local models.

## Features

- Fully offline after the model has been downloaded
- Remembers the conversation (`clear` starts a new one)
- Clear error messages if Ollama isn't running or the model is too slow

## Setup (Arch-based Linux, tested on CachyOS with an AMD Radeon RX 7900 XTX)

```bash
# 1. Install Ollama with AMD GPU support (ROCm) and uv. Use ollama-cuda for NVIDIA GPUs.
sudo pacman -S ollama-rocm uv
sudo systemctl enable --now ollama

# 2. Download a model
ollama pull qwen2.5-coder:14b

# 3. Set up Python in a virtual environment (with uv)
uv venv venv
source venv/bin/activate.fish   # fish shell; use venv/bin/activate in bash
uv pip install -r requirements.txt

# 4. Run
python local_ai_helper.py
```

### Optional: browser interface with Docker

```bash
sudo pacman -S docker
sudo systemctl enable --now docker
sudo docker run -d --network=host -v open-webui:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

Then open http://localhost:8080.

`--network=host` is needed because Ollama only listens on `127.0.0.1` by default, and inside a normal container
`localhost` means the container itself, not the host.

## What I learned

- Running a Linux service with `systemd` and installing packages with `pacman`
- Managing a Python virtual environment and dependencies with `uv`
- How a REST API works: sending JSON with an HTTP POST request and reading the JSON response
- Handling errors with `try` / `except` so the program doesn't crash
- Running an app in an isolated Docker container (images, containers, volumes, networking)
- Trade-offs between local models (privacy, no costs) and cloud models (much stronger, but data leaves the company)

## Next steps

- [ ] Reproduce the setup on an Ubuntu Server virtual machine
- [ ] Stream answers word by word instead of waiting for the full response
- [ ] Let the assistant read a local file and answer questions about it
- [ ] Package the script in its own Docker container (Dockerfile)
