import tkinter as tk
import keyboard
import pyperclip
import time
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import sys


english_to_russian = {
    "q": "й", "w": "ц", "e": "у", "r": "к", "t": "е", "y": "н", "u": "г", "i": "ш", "o": "щ",
    "p": "з", "[": "х", "]": "ъ", "'": "э", ";": "ж", "l": "д", "k": "л", "j": "о", "h": "р",
    "g": "п", "f": "а", "d": "в", "s": "ы", "a": "ф", "z": "я", "x": "ч", "c": "с", "v": "м",
    "b": "и", "n": "т", "m": "ь", ",": "б", ".": "ю",
}

russian_to_english = {
    "й": "q", "ц": "w", "у": "е", "к": 'r', "е": 't', "н": 'y', "г": 'u', "ш": 'i', "щ": 'o',
    "з": 'p', "х": '[', "ъ": ']', "ф": 'a', "ы": 's', "в": 'd', "а": 'f', "п": 'g', "р": 'h',
    "о": 'j', "л": 'k', "д": 'l', "ж": ';', "э": '"', "я": 'z', "ч": 'x', "с": 'c', "м": 'v',
    "и": 'b', "т": 'n', "ь": 'm', "б": ',', "ю": '.',
}

english_to_arabic = {
    "q": "ض", "w": "ص", "e": "ث", "r": "ق", "t": "ف", "y": "غ", "u": "ع", "i": "ه", "o": "خ",
    "p": "ح", "[": "ج", "]": "د", "'": "ش", ";": "س", "l": "ب", "k": "ل", "j": "ا", "h": "ر",
    "g": "ة", "f": "و", "d": "ى", "s": "ئ", "a": "ؤ", "z": "ظ", "x": "ط", "c": "ز", "v": "ظ",
    "b": "ي", "n": "ن", "m": "م", ",": "ك", ".": "ط",
}

russian_to_arabic = {
    "й": "ض", "ц": "ص", "у": "ث", "к": 'ق', "е": 'ف', "н": 'غ', "г": 'ع', "ш": 'ه', "щ": 'خ',
    "з": 'ح', "х": 'ج', "ъ": 'د', "ф": 'ش', "ы": 'س', "в": 'ب', "а": 'ل', "п": 'ا', "р": 'ر',
    "о": 'ة', "л": 'و', "д": 'ى', "ж": 'ئ', "э": 'ؤ', "я": 'ظ', "ч": 'ط', "с": 'ز', "м": 'ظ',
    "и": 'ي', "т": 'ن', "ь": 'م', "б": ',', "ю": '.',
}

english_to_bashkir = {
    "q": "ҡ", "w": "ш", "e": "е", "r": "р", "t": "т", "y": "й", "u": "у", "i": "и", "o": "о",
    "p": "п", "[": "ю", "]": "ж", "'": "э", ";": "к", "l": "л", "k": "д", "j": "ж", "h": "г",
    "g": "ф", "f": "а", "d": "в", "s": "ы", "a": "з", "z": "я", "x": "ч", "c": "с", "v": "м",
    "b": "б", "n": "н", "m": "ь", ",": "т", ".": "ю",
}

russian_to_bashkir = {
    "й": "ҡ", "ц": "ш", "у": "е", "к": 'р', "е": 'т', "н": 'й', "г": 'у', "ш": 'и', "щ": 'о',
    "з": 'п', "х": 'ю', "ъ": 'ж', "ф": 'э', "ы": 'к', "в": 'л', "а": 'д', "п": 'ж', "р": 'г',
    "о": 'ф', "л": 'а', "д": 'в', "ж": 'ы', "э": 'з', "я": 'я', "ч": 'ч', "с": 'с', "м": 'м',
    "и": 'и', "т": 'т', "ь": 'ь', "б": 'б', "ю": '.',
}


Symbols = {
    **english_to_russian,
    **russian_to_english,
    **english_to_arabic,
    **russian_to_arabic,
    **english_to_bashkir,
    **russian_to_bashkir,
    " ": " ", "Q": 'Й', "W": 'Ц', "E": 'У', "R": 'К', "T": 'Е', "Y": 'Н', "U": 'Г', "I": 'Ш',
    "O": 'Щ', "P": 'З', "{": 'Х', "}": 'Ъ', "A": 'Ф', "S": 'Ы', "D": 'В', "F": 'А', "G": 'П',
    "H": 'Р', "J": 'О', "K": 'Л', "L": 'Д', ":": 'Ж', "Z": 'Я', "C": 'С', "X": 'Ч', '''"''': 'Э',
    "V": 'М', "B": 'И', "N": 'Т', "M": 'Ь', "<": 'Б', ">": 'Ю', "\r": ' ', "\n": ' ', "—": '—',
    "`": 'ё', "~": 'Ё', "Ё": '~', "ё": '`'
}

current_language = "English"
current_bind = None
current_layout = "english_to_russian"


def translate(text_in):
    new_text = ""
    layout = eval(current_layout)
    for i in range(len(text_in)):
        sym = layout.get(text_in[i], text_in[i])
        new_text += sym
    return new_text


def launch():
    keyboard.press_and_release("ctrl + x")
    time.sleep(0.1)
    data = str(pyperclip.paste())
    translated = str(translate(data))
    pyperclip.copy(translated)
    keyboard.press_and_release("ctrl + v")
    time.sleep(0.1)


def set_bind():
    global current_bind
    bind = bind_entry.get()
    if current_bind:
        keyboard.remove_hotkey(current_bind)
    keyboard.add_hotkey(str(bind), launch)
    current_bind = bind
    update_status_label()


def clear_bind():
    global current_bind
    if current_bind:
        keyboard.remove_hotkey(str(current_bind))
        current_bind = None
    update_status_label()


def update_status_label():
    if current_bind:
        if current_language == "English":
            status_label.config(text=f"Hotkey set to: {current_bind}")
        elif current_language == "Russian":
            status_label.config(text=f"Бинд установлен: {current_bind}")
        elif current_language == "Arabic":
            status_label.config(text=f"تم تعيين مفتاح: {current_bind}")
        elif current_language == "Bashkir":
            status_label.config(text=f"Бинд белән бөтәлде: {current_bind}")
    else:
        if current_language == "English":
            status_label.config(text="No bind set")
        elif current_language == "Russian":
            status_label.config(text="Бинд не установлен")
        elif current_language == "Arabic":
            status_label.config(text="لم يتم تعيين أي مفتاح")
        elif current_language == "Bashkir":
            status_label.config(text="Бинд бу кирәкле")


def change_language_to_russian():
    global current_language, current_layout
    current_language = "Russian"
    current_layout = "english_to_russian"
    bind_label.config(text="Введите бинд:")
    set_bind_button.config(text="Установить")
    clear_bind_button.config(text="Сбросить бинд")
    update_status_label()
    root.title("Настройки бинда")
    update_menu_items()
    update_language_menu()


def change_language_to_english():
    global current_language, current_layout
    current_language = "English"
    current_layout = "english_to_russian"
    bind_label.config(text="Enter your bind:")
    set_bind_button.config(text="Set Bind")
    clear_bind_button.config(text="Clear Bind")
    update_status_label()
    root.title("Bind Settings")
    update_menu_items()
    update_language_menu()


def change_language_to_arabic():
    global current_language, current_layout
    current_language = "Arabic"
    current_layout = "english_to_arabic"
    bind_label.config(text="أدخل مفتاحك:")
    set_bind_button.config(text="تعيين")
    clear_bind_button.config(text="مسح المفتاح")
    update_status_label()
    root.title("إعدادات المفتاح")
    update_menu_items()
    update_language_menu()


def change_language_to_bashkir():
    global current_language, current_layout
    current_language = "Bashkir"
    current_layout = "english_to_bashkir"
    bind_label.config(text="Байлап беләйү:")
    set_bind_button.config(text="Таныстыру")
    clear_bind_button.config(text="Башлыкты бушату")
    update_status_label()
    root.title("Бинд параметрләре")
    update_menu_items()
    update_language_menu()


def change_layout_to_english_to_russian():
    global current_layout
    current_layout = "english_to_russian"


def change_layout_to_russian_to_english():
    global current_layout
    current_layout = "russian_to_english"


def change_layout_to_english_to_arabic():
    global current_layout
    current_layout = "english_to_arabic"


def change_layout_to_russian_to_arabic():
    global current_layout
    current_layout = "russian_to_arabic"


def change_layout_to_english_to_bashkir():
    global current_layout
    current_layout = "english_to_bashkir"


def change_layout_to_russian_to_bashkir():
    global current_layout
    current_layout = "russian_to_bashkir"


def update_language_menu():
    global menu_items, current_language
    if current_language == "English":
        menu_items[1].items = (
            MenuItem('Russian', change_language_to_russian),
            MenuItem('English', change_language_to_english),
            MenuItem('Arabic', change_language_to_arabic),
            MenuItem('Bashkir', change_language_to_bashkir)
        )
    if current_language == "Russian":
        menu_items[1].items = (
            MenuItem('Русский', change_language_to_russian),
            MenuItem('Английский', change_language_to_english),
            MenuItem('Арабский', change_language_to_arabic),
            MenuItem('Башкирский', change_language_to_bashkir)
        )
    if current_language == "Arabic":
        menu_items[1].items = (
            MenuItem('الروسية', change_language_to_russian),
            MenuItem('إنجليزي', change_language_to_english),
            MenuItem('عرب', change_language_to_arabic),
            MenuItem('بشكير', change_language_to_bashkir)
        )
    if current_language == "Bashkir":
        menu_items[1].items = (
            MenuItem('Урыҫ', change_language_to_russian),
            MenuItem('Инглиз', change_language_to_english),
            MenuItem('Ғәрәп', change_language_to_arabic),
            MenuItem('Башҡортса', change_language_to_bashkir)
        )


def update_menu_items():
    global menu_items
    menu_items = (
        MenuItem('Bind Settings', show_window),
        MenuItem('Language', Menu(
            MenuItem('Русский', change_language_to_russian),
            MenuItem('English', change_language_to_english),
            MenuItem('العربية', change_language_to_arabic),
            MenuItem('Башҡортса', change_language_to_bashkir)
        )),
        MenuItem('Layout profile', Menu(
            MenuItem('English to russian', change_layout_to_english_to_russian),
            MenuItem('Russian to english', change_layout_to_russian_to_english),
            MenuItem('English to arabic', change_layout_to_english_to_arabic),
            MenuItem('Russian to arabic', change_layout_to_russian_to_arabic),
            MenuItem('English to bashkir', change_layout_to_english_to_bashkir),
            MenuItem('Russian to bashkir', change_layout_to_russian_to_bashkir)
        )),
        MenuItem('Quit', on_quit)
    )
    update_language_menu()
    icon_tray.menu = Menu(*menu_items)
    icon_tray.update_menu()


def on_quit(icon):
    icon.stop()
    root.quit()
    root.destroy()
    sys.exit()


def create_image(path):
    return Image.open(path)


def show_window():
    root.deiconify()


def hide_window():
    root.withdraw()


def setup_tray():
    global icon_tray, menu_items
    icon_tray = Icon('test', create_image("icon.ico"), 'Translator', Menu(*menu_items))
    icon_tray.run()


root = tk.Tk()
root.title("Bind Settings")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

bind_label = tk.Label(frame, text="Enter your bind:")
bind_label.grid(row=0, column=0, padx=5, pady=5)

bind_entry = tk.Entry(frame)
bind_entry.grid(row=0, column=1, padx=5, pady=5)

set_bind_button = tk.Button(frame, text="Set Bind", command=set_bind)
set_bind_button.grid(row=0, column=2, padx=5, pady=5)

clear_bind_button = tk.Button(frame, text="Clear Bind", command=clear_bind)
clear_bind_button.grid(row=3, column=1, padx=5, pady=5)

status_label = tk.Label(frame, text="No bind set")
status_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

root.protocol("WM_DELETE_WINDOW", hide_window)
root.withdraw()

menu_items = (
    MenuItem('Bind Settings', show_window),
    MenuItem('Language', Menu(
        MenuItem('Русский', change_language_to_russian),
        MenuItem('English', change_language_to_english),
        MenuItem('العربية', change_language_to_arabic),
        MenuItem('Башҡортса', change_language_to_bashkir)
    )),
    MenuItem('Layout profile', Menu(
        MenuItem('English to russian', change_layout_to_english_to_russian),
        MenuItem('Russian to english', change_layout_to_russian_to_english),
        MenuItem('English to arabic', change_layout_to_english_to_arabic),
        MenuItem('Russian to arabic', change_layout_to_russian_to_arabic),
        MenuItem('English to bashkir', change_layout_to_english_to_bashkir),
        MenuItem('Russian to bashkir', change_layout_to_russian_to_bashkir)
    )),
    MenuItem('Quit', on_quit)
)

threading.Thread(target=setup_tray).start()

root.mainloop()
