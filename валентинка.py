import tkinter as tk
from tkinter import messagebox
import webbrowser

root = tk.Tk()
root.geometry('400x200')
root.config(bg='pink')
root.title("Валентинка")

click_count = 0  # лічильник натискань

def photo():
    global click_count
    click_count += 1

    if click_count == 1:
        webbrowser.open('4.jpg')
    elif click_count == 2:
        messagebox.showinfo("Повідомлення", "ХА ти самотній")

btn = tk.Button(
    root,
    fg='pink',
    bg='black',
    text='Отримати валентинку',
    font=('Arial', 14),
    padx=10,
    pady=10,
    command=photo
)

btn.pack(expand=True)

root.mainloop()
