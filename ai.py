import tkinter as tk
from tkinter import messagebox
import pandas as pd
import pyttsx3
import threading
import google.generativeai as genai

# Load Dataset
dataset_path = r"D:\Sem 4\AI model Trainer\sentiment_dataset.csv"
try:
    df = pd.read_csv("D:\Sem 4\AI model Trainer\sentiment_dataset.csv")
    df_sample = df.sample(5).to_string(index=False)
except Exception as e:
    df_sample = "Could not load dataset: " + str(e)

# Configure Gemini
genai.configure(api_key="AIzaSyAsEgBykX7ESL3fiQK6ITDIIpxdOXGjLM4")  # Replace with your Gemini API Key
model = genai.GenerativeModel("models/gemini-1.5-pro-001")

# TTS Engine
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 160)
tts_engine.setProperty("volume", 0.9)

# State Variables
latest_ai_response = ""
speaking_thread = None
stop_speaking_flag = False

# Ask AI Function
def ask_ai():
    global latest_ai_response

    user_input = user_entry.get()
    if not user_input.strip():
        messagebox.showwarning("Input Required", "Please enter a message.")
        return

    insert_message("You", user_input)

    try:
        full_prompt = (
            "You are an AI trainer assistant. Use the following sample training data to guide your answer.\n\n"
            f"Sample Training Data:\n{df_sample}\n\n"
            f"User Query: {user_input}"
        )

        response = model.generate_content(full_prompt)
        reply = response.text.strip()
        latest_ai_response = reply

        insert_message("Trainer AI", reply)
        user_entry.delete(0, tk.END)
    except Exception as e:
        insert_message("Error", str(e))

def insert_message(sender, message):
    chat_window.config(state=tk.NORMAL)
    if sender == "You":
        chat_window.insert(tk.END, f"\n👤 {sender}: {message}\n", "user")
    elif sender == "Trainer AI":
        chat_window.insert(tk.END, f"\n🤖 {sender}: {message}\n", "ai")
    else:
        chat_window.insert(tk.END, f"\n⚠️ {sender}: {message}\n", "error")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

# Speak Thread Function
def speak_text(text):
    global stop_speaking_flag
    tts_engine.stop()
    tts_engine.say(text)
    tts_engine.runAndWait()
    speak_btn.config(text="🔊 Speak")

# Toggle Speaking
def speak_response():
    global speaking_thread, stop_speaking_flag

    if speak_btn.cget("text") == "🔊 Speak":
        if not latest_ai_response:
            messagebox.showinfo("No Response", "No AI response to speak yet.")
            return

        speak_btn.config(text="⏹ Stop")
        stop_speaking_flag = False
        speaking_thread = threading.Thread(target=speak_text, args=(latest_ai_response,))
        speaking_thread.start()
    else:
        stop_speaking_flag = True
        tts_engine.stop()
        speak_btn.config(text="🔊 Speak")

# GUI Setup
root = tk.Tk()
root.title("💡 AI Model Trainer")
root.geometry("700x600")
root.configure(bg="#121212")

chat_window = tk.Text(root, wrap=tk.WORD, font=("Segoe UI", 12), bg="#1E1E1E", fg="#EEEEEE",
                      insertbackground="white", state=tk.DISABLED, padx=10, pady=10)
chat_window.tag_config("user", foreground="#00BFFF", font=("Segoe UI", 12, "bold"))
chat_window.tag_config("ai", foreground="#00FF7F", font=("Segoe UI", 12))
chat_window.tag_config("error", foreground="#FF6347", font=("Segoe UI", 12, "italic"))
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry_frame = tk.Frame(root, bg="#121212")
entry_frame.pack(fill=tk.X, pady=(0, 20), padx=10)

user_entry = tk.Entry(entry_frame, font=("Segoe UI", 13), bg="#2C2C2C", fg="white", relief=tk.FLAT, insertbackground="white")
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)

send_btn = tk.Button(entry_frame, text="Send 🚀", font=("Segoe UI", 11, "bold"), command=ask_ai,
                     bg="#4CAF50", fg="white", activebackground="#45A049", relief=tk.FLAT, padx=20, pady=6)
send_btn.pack(side=tk.LEFT)

speak_btn = tk.Button(entry_frame, text="🔊 Speak", font=("Segoe UI", 11, "bold"), command=speak_response,
                      bg="#2196F3", fg="white", activebackground="#1E88E5", relief=tk.FLAT, padx=15, pady=6)
speak_btn.pack(side=tk.LEFT, padx=(10, 0))

root.mainloop()



