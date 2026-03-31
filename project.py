import pyautogui
import time
import random

def auto_clicker(clicks_count, delay_range):
    print("У тебя есть 5 секунд, чтобы переключиться на окно Roblox...")
    time.sleep(5)
    
    for i in range(clicks_count):
        # Делаем клик
        pyautogui.click()
        
        # Генерируем случайную задержку (например, от 0.1 до 0.3 сек)
        wait_time = random.uniform(delay_range[0], delay_range[1])
        print(f"Клик {i+1} выполнен. Жду {wait_time:.3f} сек.")
        time.sleep(wait_time)

    print("Работа завершена!")

# Настройки: 100 кликов, задержка от 0.1 до 0.5 секунды
auto_clicker(100, (0.1, 0.5))
