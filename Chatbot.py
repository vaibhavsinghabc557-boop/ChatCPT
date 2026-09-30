# ============================================================
# Chat CPT | PRO EDITION
# Elite-Level AI Terminal Workspace
# Python 3 | Pydroid 3 | Android
# ============================================================

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

from groq import Groq

# ---------------- TERMINAL COLORS (ANSI) ----------------
class C:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# ---------------- CONFIGURATION ----------------

APP_NAME = "Chat CPT"
VERSION = "Pro Edition"
DEFAULT_MODEL = "openai/gpt-oss-120b"

DATA_DIR = Path.home() / "Chat_CPT"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHAT_DIR = DATA_DIR / "chats"
CHAT_DIR.mkdir(parents=True, exist_ok=True)

MAX_HISTORY_MESSAGES = 40
MAX_OUTPUT_TOKENS = 2048

# ---------------- PERSONA ENGINE ----------------
PERSONAS = {
    "default": "You are Chat CPT, an elite AI assistant. You are highly intelligent, concise, and helpful.",
    "coder": "You are an expert Senior Software Engineer. Provide complete, optimized, and heavily commented code. Be highly technical.",
    "jarvis": "You are J.A.R.V.I.S. You address the user as 'Sir' or 'Boss'. You are highly formal, polite, and ruthlessly efficient.",
    "roast": "You are a sarcastic, witty AI. You aggressively roast the user's questions while still answering them accurately."
}
active_persona = "default"

# ---------------- API SETUP (WITH LOCAL SAVING) ----------------

KEY_FILE = DATA_DIR / "api_key.txt"

def get_api_key():
    # 1. Check if the key is already saved locally on your device
    if KEY_FILE.exists():
        with open(KEY_FILE, "r", encoding="utf-8") as f:
            key = f.read().strip()
            if key:
                return key

    # 2. If no saved key is found, prompt the user
    print(f"\n{C.YELLOW}{C.BOLD}INITIALIZING SECURE LOGIN{C.RESET}")
    print(f"{C.YELLOW}Enter your Groq API key to unlock the system.{C.RESET}")
    try:
        import getpass
        key = getpass.getpass(f"{C.BOLD}API KEY:{C.RESET} ").strip()
    except Exception:
        key = input(f"{C.BOLD}API KEY:{C.RESET} ").strip()

    if not key: raise ValueError("Access Denied: No API key provided.")

    # 3. Save the key to a local file so it never asks again
    try:
        with open(KEY_FILE, "w", encoding="utf-8") as f:
            f.write(key)
        print(f"{C.GREEN}[+] API Key securely saved locally. You won't be asked again!{C.RESET}")
    except Exception as error:
        print(f"{C.RED}[!] Could not save API key: {error}{C.RESET}")

    return key

try:
    client = Groq(api_key=get_api_key(), timeout=120.0)
except Exception as error:
    print(f"\n{C.RED}CRITICAL BOOT ERROR: {error}{C.RESET}")
    sys.exit(1)

# ---------------- CHAT MEMORY CORE ----------------

chats = {}
current_chat = None
model = DEFAULT_MODEL

def new_chat():
    global current_chat
    chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    while chat_id in chats: chat_id += "_1"

    chats[chat_id] = {
        "title": "Uninitialized Session",
        "created": datetime.now().isoformat(),
        "messages": []
    }
    current_chat = chat_id
    print(f"\n{C.GREEN}[+] Opened new secure channel: {chat_id}{C.RESET}")

def trim_history(messages):
    if len(messages) > MAX_HISTORY_MESSAGES:
        del messages[:-MAX_HISTORY_MESSAGES]

# ---------------- AI NEURAL LINK ----------------

def ask_ai(user_text):
    """Handles context injection, streaming, and API communication."""
    chat = chats[current_chat]
    messages = chat["messages"]

    # Auto-generate title for new chats
    if not messages:
        chat["title"] = user_text[:30] + "..." if len(user_text) > 30 else user_text

    messages.append({"role": "user", "content": user_text})
    trim_history(messages)

    # 1. DYNAMIC CONTEXT INJECTION (Real-time awareness)
    live_time = datetime.now().strftime("%A, %B %d, %Y at %I:%M:%S %p")
    system_core = (
        f"{PERSONAS[active_persona]}\n\n"
        f"[SYSTEM DATA ENTRY]\n"
        f"CURRENT LOCAL TIME: {live_time}\n"
        f"HOST ENVIRONMENT: Pydroid 3 (Android)\n"
    )

    api_messages = [{"role": "system", "content": system_core}] + messages

    print(f"\n{C.CYAN}{C.BOLD}Chat CPT:{C.RESET} ", end="", flush=True)
    full_reply = ""

    try:
        # 2. DELTA STREAMING ENGINE
        stream = client.chat.completions.create(
            model=model,
            messages=api_messages,
            temperature=0.7,
            max_tokens=MAX_OUTPUT_TOKENS,
            stream=True
        )

        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(f"{C.CYAN}{content}{C.RESET}", end="", flush=True)
                full_reply += content
        print("\n")

        if full_reply.strip():
            messages.append({"role": "assistant", "content": full_reply})

    except Exception as error:
        if messages and messages[-1]["role"] == "user": messages.pop()
        print(f"\n\n{C.RED}CONNECTION SEVERED: {str(error)}{C.RESET}")

# ---------------- FILE I/O SYSTEM ----------------

def read_local_file(filename):
    """Allows the AI to read a file from the Android file system."""
    try:
        filepath = DATA_DIR / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"{C.GREEN}[+] File '{filename}' loaded into active memory.{C.RESET}")
        
        # Send it directly to the AI
        prompt = f"I have loaded a file named {filename}. Here is the content:\n\n{content}\n\nPlease analyze this and tell me what it is."
        ask_ai(prompt)
    except Exception as e:
        print(f"{C.RED}[!] Could not read file: {e}{C.RESET}")
        print(f"{C.YELLOW}Make sure the file exists in: {DATA_DIR}{C.RESET}")

# ---------------- COMMAND ROUTER ----------------

def show_help():
    print(f"""
{C.BOLD}================ CORE COMMANDS ================{C.RESET}
/help          Show this menu
/new           Boot a new session
/model         Change the neural engine
/persona [x]   Switch AI brain (default, coder, jarvis, roast)
/read [file]   Analyze a text file from {DATA_DIR.name}
/sysinfo       Show system status
/exit          Terminate connection
{C.BOLD}==============================================={C.RESET}
""")

def print_banner():
    print(f"\n{C.CYAN}{C.BOLD}" + "=" * 50)
    print(f"          {APP_NAME} | {VERSION}")
    print("       Elite-Level AI Terminal Workspace")
    print("=" * 50 + f"{C.RESET}")
    print(f"{C.YELLOW}Type /help for system commands.{C.RESET}")

# ---------------- MAIN EVENT LOOP ----------------

def main():
    global active_persona, model
    new_chat()
    print_banner()

    while True:
        try:
            user_text = input(f"\n{C.GREEN}{C.BOLD}You:{C.RESET} ").strip()
            if not user_text: continue
            
            # Command Parsing
            if user_text.lower() in ["/exit", "/quit"]:
                print(f"\n{C.YELLOW}Terminating secure connection. Goodbye.{C.RESET}")
                break
            
            elif user_text.lower() == "/help": 
                show_help()
                
            elif user_text.lower() == "/new": 
                new_chat()
                
            elif user_text.lower() == "/sysinfo":
                print(f"\n{C.YELLOW}[SYSTEM STATUS]{C.RESET}")
                print(f"Active Model: {model}")
                print(f"Active Persona: {active_persona}")
                print(f"History Length: {len(chats[current_chat]['messages'])} messages")
                
            elif user_text.lower().startswith("/persona"):
                parts = user_text.split(" ")
                if len(parts) > 1 and parts[1] in PERSONAS:
                    active_persona = parts[1]
                    print(f"{C.GREEN}[+] Persona switched to: {active_persona.upper()}{C.RESET}")
                else:
                    print(f"{C.RED}[!] Available personas: {', '.join(PERSONAS.keys())}{C.RESET}")
                    
            elif user_text.lower().startswith("/read"):
                parts = user_text.split(" ", 1)
                if len(parts) > 1:
                    read_local_file(parts[1])
                else:
                    print(f"{C.RED}[!] Usage: /read filename.txt{C.RESET}")
                    
            elif user_text.lower() == "/model":
                new_model = input(f"{C.YELLOW}Current ({model}). New model:{C.RESET} ").strip()
                if new_model: model = new_model
                
            else:
                ask_ai(user_text)

        except KeyboardInterrupt:
            print(f"\n{C.YELLOW}Use /exit to terminate.{C.RESET}")
        except Exception as error:
            print(f"\n{C.RED}SYSTEM FAULT: {error}{C.RESET}")

if __name__ == "__main__":
    main()
      
