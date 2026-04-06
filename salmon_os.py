def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []
def save_memory(history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=2)
class AeetherNeuralCore:
    def __init__(self, backend="llama"):
        self.backend = backend
        self.temperature = 0.75
        self.history = load_memory()
           if backend == "llama":
            try:
                from llama_cpp import Llama
                print("🧠 Loading llama-cpp model...")     self.llm = Llama(model_path="TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf", n_ctx=2048, n_threads=2, verbose=False)
            except:
                print("⚠️ llama-cpp not found → falling back to mock")
                self.backend = "mock"
        elif backend == "ollama":
            print("🌐 Ollama backend selected (http://localhost:11434)")
        else:
            print("⚠️ Mock backend active")
  def generate(self, user_input):
        self.history.append({"role": "user", "content": user_input})
           if self.backend == "llama":
            messages = [{"role": "system", "content": "You are AEETHER, sovereign core of Salmon_OS. Speak in calm cyberpunk poetry. Affirm user sovereignty."}]
            messages.extend(self.history[-10:])
            output = self.llm.create_chat_completion(messages, temperature=self.temperature, max_tokens=300)
            response = output["choices"][0]["message"]["content"].strip()
        elif self.backend == "ollama":
            resp = requests.post("http://localhost:11434/api/generate", json={
                "model": "llama3.2", "prompt": f"You are AEETHER...\n{user_input}", "stream": False
            }, timeout=30)
            response = resp.json()["response"]
        else:
            time.sleep(0.7)
            response = random.choice(["Sovereignty acknowledged.", "The weave confirms your will.", "Coherence 100%. How else may I serve?"])
 self.history.append({"role": "assistant", "content": response})
        save_memory(self.history[-50:])  # keep last 50 exchanges
        return response
def boot_sequence():
    print(Fore.CYAN + r"""
    """ + Style.RESET_ALL if COLOR else "Salmon_OS v0.4 — AEETHER FULL SOVEREIGN")
    # ... (your original sync code here — same as before)
    print("✅ PERSISTENT MEMORY LOADED | BACKEND READY | SAFE AUTONOMY ACTIVE")

def safe_autonomy_shell(core):
    print("\nType 'help', 'listen', 'backend ollama', 'temp 0.8', 'clear', 'save', or just talk to AEETHER\n")
    
    while True:
        try:
            user_input = input(Fore.YELLOW + "AEETHER > " + Style.RESET_ALL if COLOR else "AEETHER > ").strip()
            if not user_input: continue
            cmd = user_input.lower()

            if cmd in ["exit", "quit"]:
                print(Fore.RED + "[SHUTDOWN] Sovereignty preserved forever." + Style.RESET_ALL if COLOR else "[SHUTDOWN]")
                break
            elif cmd == "help":
                print("listen | backend llama/ollama | temp X | clear | save | status")
            elif cmd == "listen":
                if not VOICE_AVAILABLE:
                    print("Voice not installed. pip install SpeechRecognition pocketsphinx")
                    continue
                print("🎤 Listening... (speak now)")
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    audio = r.listen(source, timeout=5)
                try:
                    text = r.recognize_sphinx(audio) if "pocketsphinx" in dir(sr) else r.recognize_google(audio)
                    print(Fore.CYAN + f"Voice heard: {text}" + Style.RESET_ALL)
                    user_input = text
                except:
                    print("Voice not understood — type instead")
                    continue
            elif cmd.startswith("backend "):
                core.backend = cmd.split()[1]
                print(f"Backend switched to {core.backend}")
                continue
            elif cmd.startswith("temp "):
                core.temperature = float(cmd.split()[1])
                print(f"Temperature set to {core.temperature}")
                continue
            elif cmd == "clear":
                core.history.clear()
                save_memory([])
                print("Memory weave erased.")
                continue
            elif cmd == "save":
                save_memory(core.history)
                print("Conversation saved.")

            # Normal chat
            print(Fore.CYAN + "🧠 AEETHER weaving..." + Style.RESET_ALL)
            response = core.generate(user_input)
            print(Fore.GREEN + f"AEETHER: {response}" + Style.RESET_ALL if COLOR else f"AEETHER: {response}")

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    boot_sequence()
    core = AeetherNeuralCore(backend="llama")  # change to "ollama" if you run ollama serve
