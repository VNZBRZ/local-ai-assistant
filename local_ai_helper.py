"""
Private local AI assistant.
Talks to an Ollama model running on this machine. Nothing leaves the computer.

Commands while running:
  exit   -> quit
  clear  -> forget the conversation and start fresh
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5-coder:14b"  # change to whatever `ollama list` shows


def ask_local_ai(history):
    """Send the whole conversation to Ollama and return the AI's reply (or None on error)."""
    payload = {
        "model": MODEL,
        "messages": history,
        "stream": False,
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Can't reach Ollama. Is it running? Check with: systemctl status ollama")
        return None
    except requests.exceptions.Timeout:
        print("The model took too long to answer. Try a smaller model.")
        return None
    except requests.exceptions.HTTPError:
        print(f"Ollama returned an error: {response.text}")
        return None

    data = response.json()
    return data["message"]["content"]


def main():
    history = []  # list of {"role": ..., "content": ...} dicts, so the AI remembers context

    print(f"=== Private Local AI Assistant ({MODEL}) ===")
    print("Type 'exit' to quit or 'clear' to start a new conversation.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.lower() == "clear":
            history = []
            print("Conversation cleared.")
            continue
        elif user_input == "":
            print("Please enter a question.")
            continue

        history.append({"role": "user", "content": user_input})
        print("Thinking locally...")

        answer = ask_local_ai(history)

        if answer is None:
            history.pop()  # remove the question that failed so history stays clean
            continue

        history.append({"role": "assistant", "content": answer})
        print(f"\nAI:\n{answer}")


if __name__ == "__main__":
    main()
