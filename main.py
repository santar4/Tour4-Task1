import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt


# Функція для завантаження даних
def load_data(file_path, chunksize=100000):
    """Завантажує великі дані з CSV файлів по частинах"""
    chunks = pd.read_csv(file_path, chunksize=chunksize)
    data = pd.concat(chunks, ignore_index=True)
    return data


# Функція для обчислення статистики
def calculate_statistics(data, column):
    """Обчислює середнє, мінімум, максимум для заданого стовпця"""
    try:
        mean = data[column].mean()
        min_val = data[column].min()
        max_val = data[column].max()
        return mean, min_val, max_val
    except Exception as e:
        return None, None, None


# Функція для фільтрації даних
def filter_data(data, column, condition, value):
    """Фільтрує дані за умови: більше, менше, дорівнює"""
    if column not in data.columns:
        return pd.DataFrame()  # Повертає порожній DataFrame, якщо стовпець не знайдений

    if condition == 'більше':
        filtered_data = data[data[column] > value]
    elif condition == 'менше':
        filtered_data = data[data[column] < value]
    elif condition == 'дорівнює':
        filtered_data = data[data[column] == value]
    else:
        filtered_data = data
    return filtered_data


# Функція для побудови графіків
def plot_data(data, column):
    """Побудова графіка для візуалізації даних"""
    plt.figure(figsize=(10, 6))
    plt.hist(data[column], bins=30, color='blue', edgecolor='black')
    plt.title(f'Розподіл значень {column}')
    plt.xlabel(column)
    plt.ylabel('Частота')
    plt.show()


# Функція для збереження фільтрованих даних у новий CSV файл
def save_filtered_data(filtered_data, output_path):
    filtered_data.to_csv(output_path, index=False)


# Створення графічного інтерфейсу за допомогою tkinter
class DataAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Аналізатор даних")

        self.file_path = None
        self.data = None

        # Кнопка для вибору файлу
        self.load_button = tk.Button(root, text="Завантажити CSV файл", command=self.load_file)
        self.load_button.pack(pady=20)

        # Вибір стовпця для статистики
        self.column_label = tk.Label(root, text="Виберіть стовпець для статистики(Значення має починатися з маленької літери):")
        self.column_label.pack(pady=10)

        self.column_entry = tk.Entry(root)
        self.column_entry.pack(pady=10)

        # Кнопка для обчислення статистики
        self.stat_button = tk.Button(root, text="Обчислити статистику", command=self.show_statistics)
        self.stat_button.pack(pady=10)

        # Вибір умови фільтрації
        self.filter_label = tk.Label(root, text="Виберіть умову фільтрації:")
        self.filter_label.pack(pady=10)

        self.filter_condition = tk.StringVar(value="більше")
        self.filter_condition_menu = tk.OptionMenu(root, self.filter_condition, "більше", "менше", "дорівнює")
        self.filter_condition_menu.pack(pady=10)

        self.filter_value_label = tk.Label(root, text="Введіть значення для фільтрації:")
        self.filter_value_label.pack(pady=10)

        self.filter_value_entry = tk.Entry(root)
        self.filter_value_entry.pack(pady=10)

        # Кнопка для фільтрації даних
        self.filter_button = tk.Button(root, text="Застосувати фільтр", command=self.filter_and_plot)
        self.filter_button.pack(pady=10)

    def load_file(self):
        """Завантажує файл CSV через діалогове вікно"""
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.file_path:
            try:
                self.data = load_data(self.file_path)
                messagebox.showinfo("Успіх", "Файл завантажено успішно.")
            except Exception as e:
                messagebox.showerror("Помилка", f"Не вдалося завантажити файл: {e}")

    def show_statistics(self):
        """Показує статистику для вибраного стовпця"""
        column = self.column_entry.get()
        if column and column in self.data.columns:
            mean, min_val, max_val = calculate_statistics(self.data, column)
            if mean is not None:
                result = f"Середнє: {mean}\nМінімум: {min_val}\nМаксимум: {max_val}"
                messagebox.showinfo("Статистика", result)
            else:
                messagebox.showerror("Помилка", "Не вдалося обчислити статистику для цього стовпця.")
        else:
            messagebox.showerror("Помилка", "Стовпець не знайдений.")

    def filter_and_plot(self):
        """Фільтрує дані та будує графік"""
        column = self.column_entry.get()
        condition = self.filter_condition.get()
        try:
            value = float(self.filter_value_entry.get())
            filtered_data = filter_data(self.data, column, condition, value)
            if filtered_data.empty:
                messagebox.showerror("Помилка", "Не знайдено даних після фільтрації.")
            else:
                plot_data(filtered_data, column)
        except ValueError:
            messagebox.showerror("Помилка", "Невірне значення для фільтрації.")


# Запуск програми
if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalyzerApp(root)
    root.mainloop()

