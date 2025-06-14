import speech_recognition as sr
from tkinter import *
import random
import pyautogui
import time
from tkinter.simpledialog import askstring

class OnScreenKeyboard:
    def __init__(self, root):
        self.root = root
        self.root.title("On-Screen Keyboard")
        self.root.geometry("1024x800")
        self.root.configure(bg="#2C2F33")

        self.entry_frame = Frame(root, bg="white")
        self.entry_frame.pack(pady=10, padx=10, fill="x")

        self.entry_var = StringVar()
        self.real_input = ""
        self.fake_input = ""

        self.entry = Entry(self.entry_frame, textvariable=self.entry_var, font=("Arial", 16), show="*", bg="white", fg="black", insertwidth=0)
        self.entry.pack(side="left", expand=True, fill="x")

        self.eye_label = Label(self.entry_frame, text="👁", font=("Arial", 14), bg="white", fg="black", cursor="hand2")
        self.eye_label.pack(side="right", padx=5)
        self.eye_label.bind("<Button-1>", self.authenticate_and_reveal)

        self.create_keyboard()

        self.clear_btn = Button(root, text="Clear", command=self.clear_input, font=("Arial", 12, "bold"),
                                bg="#99AAB5", fg="black", relief="raised")
        self.clear_btn.pack(pady=10)

        self.submit_btn = Button(root, text="Submit", command=self.submit_input, font=("Arial", 12, "bold"),
                                 bg="#77DD77", fg="black", relief="raised")
        self.submit_btn.pack(pady=5)

        self.voice_btn = Button(root, text="Voice Input", command=self.voice_typing, font=("Arial", 12, "bold"),
                                bg="#99AAB5", fg="black", relief="raised")
        self.voice_btn.pack(pady=5)

    def authenticate_and_reveal(self, event):
        pin = askstring("Authentication", "Enter 4-digit PIN:", show="*")
        if pin == "1234":
            self.entry.config(show="")
            self.root.after(3000, lambda: self.entry.config(show="*"))
        else:
            self.entry_var.set("Wrong PIN!")

    def secure_key_press(self, key):
        self.real_input += key
        self.entry_var.set(self.real_input)

        all_keys = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:',.<>?/`~\"\\")
        fake_chars = "".join(random.choices(all_keys, k=random.randint(2, 5)))
        self.fake_input += fake_chars + key + "".join(random.choices(all_keys, k=2))

        time.sleep(random.uniform(0.05, 0.2))
        pyautogui.write(fake_chars, interval=0.05)
        pyautogui.write(key, interval=0.1)
        pyautogui.write("".join(random.choices(all_keys, k=2)), interval=0.05)

    def submit_input(self):
        with open("real_keystrokes.txt", "a") as file:
            file.write(self.real_input + "\n")
        with open("fake_keystrokes.txt", "a") as file:
            file.write(self.fake_input + "\n")
        self.real_input = ""
        self.fake_input = ""
        self.entry_var.set("")

    def clear_input(self):
        self.entry_var.set("")
        self.real_input = ""
        self.fake_input = ""

    def voice_typing(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.voice_btn.config(text="Listening...", fg="blue")
            self.root.update()
            try:
                audio = recognizer.listen(source, timeout=10)
                text = recognizer.recognize_google(audio)
                self.real_input += text
                all_keys = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+[]{}|;:',.<>?/`~\"\\")
                fake_chars = "".join(random.choices(all_keys, k=5))
                self.fake_input += text + fake_chars
                self.entry_var.set(self.real_input)
                pyautogui.write(fake_chars, interval=0.05)
                pyautogui.write(text, interval=0.1)
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
                pass
            finally:
                self.voice_btn.config(text="Voice Input", fg="black")

    def create_keyboard(self):
        # Block 1: Numbers (10 keys)
        number_keys = list("0123456789")
        random.shuffle(number_keys)
        self.add_row(number_keys)

        # Spacer after numbers
        Frame(self.root, height=20, bg="#2C2F33").pack()

        # Block 2: Letters (3 rows: 9, 9, 8)
        letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        random.shuffle(letters)
        self.add_row(letters[:9])
        self.add_row(letters[9:18])
        self.add_row(letters[18:])

        # Spacer after letters
        Frame(self.root, height=20, bg="#2C2F33").pack()

        # Block 3: Symbols (3 rows: 11, 11, 10)
        symbols = list("!@#$%^&*()-_=+[]{}|;:',.<>?/`~\"\\")
        random.shuffle(symbols)
        self.add_row(symbols[:11])
        self.add_row(symbols[11:22])
        self.add_row(symbols[22:])

    def add_row(self, keys):
        row_frame = Frame(self.root, bg="#2C2F33")
        row_frame.pack()
        for i, key in enumerate(keys):
            Button(
                row_frame, text=key, width=4, height=2, font=("Arial", 12, "bold"),
                bg="#7289DA", fg="white", relief="raised",
                command=lambda k=key: self.secure_key_press(k),
                takefocus=False, highlightthickness=0, bd=0,
                activebackground="#7289DA"
            ).grid(row=0, column=i, padx=3, pady=3)

if __name__ == "__main__":
    root = Tk()
    app = OnScreenKeyboard(root)
    root.mainloop()
