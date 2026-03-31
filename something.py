import pyautogui
import threading
import keyboard
import time
import random
import customtkinter as ctk

# Настройки окна
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ClickerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pro Clicker v1.0")
        self.geometry("300x250")
        self.clicking = False

        # Поле ввода скорости
        self.label = ctk.CTkLabel(self, text="Задержка (сек):")
        self.label.pack(pady=10)
        self.entry = ctk.CTkEntry(self, placeholder_text="0.1")
        self.entry.insert(0, "0.1")
        self.entry.pack(pady=10)

        # Кнопка старта
        self.status_label = ctk.CTkLabel(self, text="Нажми F4 для запуска", text_color="yellow")
        self.status_label.pack(pady=20)

        # Запуск прослушки клавиатуры в отдельном потоке
        threading.Thread(target=self.check_hotkey, daemon=True).start()

    def check_hotkey(self):
        while True:
            if keyboard.is_pressed('f4'): # Горячая клавиша F4
                self.clicking = not self.clicking
                color = "green" if self.clicking else "yellow"
                text = "РАБОТАЕТ (F4 - Стоп)" if self.clicking else "ПАУЗА (F4 - Старт)"
                self.status_label.configure(text=text, text_color=color)
                
                if self.clicking:
                    threading.Thread(target=self.run_clicker).start()
                time.sleep(0.3) # Защита от дребезга клавиши

    def run_clicker(self):
        while self.clicking:
            delay = float(self.entry.get())
            # "Человеческий" рандом: добавляем +/- 5% к задержке
            actual_delay = delay + random.uniform(-delay*0.05, delay*0.05)
            
            pyautogui.click()
            time.sleep(actual_delay)

if __name__ == "__main__":
    app = ClickerApp()
    app.mainloop()
