from tkinter import *
import cmath
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

window = Tk()
window['bg'] = "#D6DBDF"
window.title("Quadratic equation")
window.geometry("350x200")
window.resizable(False, False)
tk_logo = PhotoImage(file='img/logo.png')
window.iconphoto(False, tk_logo)

label = Label(window, text="Введіть дані для квадратичного рівняння:", font=("Arial", 11), bg="#D6DBDF")
label.place(x=2, y=1)

frame_data = Frame(window, bg="#F4F6F6", bd=5)

label1 = Label(frame_data, text="a = ", font=("Arial", 11))
entry1 = Entry(frame_data)

label2 = Label(frame_data, text="b = ", font=("Arial", 11))
entry2 = Entry(frame_data)

label3 = Label(frame_data, text="c = ", font=("Arial", 11))
entry3 = Entry(frame_data)

result_label = Label(text=f"Результат: ", font=("Arial", 11), bg="#D6DBDF")
result_label.place(x=110, y=155)

massage_label = Label(text=f"", font=("Arial", 9), bg="#D6DBDF")
massage_label.place(x=230, y=60)

label1.grid(row=0, column=0, sticky=E, pady=5, padx=5)
label2.grid(row=1, column=0, sticky=E, pady=5, padx=5)
label3.grid(row=2, column=0, sticky=E, pady=5, padx=5)

entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)
entry3.grid(row=2, column=1)

frame_data.place(relx=0.02, rely=0.15, relwidth=0.60, relheight=0.54)


def calculation_quadratic_equation(entry_list):
    a, b, c = entry_list[0], entry_list[1], entry_list[2]
    discriminant = (b ** 2) - (4 * a * c)
    if discriminant > 0:
        x1 = (-b - cmath.sqrt(discriminant)) / (2 * a)
        x2 = (-b + cmath.sqrt(discriminant)) / (2 * a)
        return [x1.real, x2.real]
    elif discriminant == 0:
        x = (-b / (2 * a))
        return [x]
    else:
        return None


def clear_window_func():
    result_label["text"] = "Результат"
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)


def entry_error(line):
    massage_label["text"] = line


def get_data_from_entry():
    list_entry = [entry1.get(), entry2.get(), entry3.get()]
    bad_entry = []
    output_list = []
    for element in list_entry:
        if element.lstrip('-').isdigit():
            value = int(element)
            output_list.append(value)
        else:
            bad_entry.append(element)

    if len(bad_entry) > 0:
        clear_window_func()
        for i in bad_entry:
            if i.strip() == "":
                entry_error("Заповніть всі поля")
            else:
                entry_error(f"Неправильні дані:\n{', '.join(bad_entry)}\n Введіть число")
    print(output_list)
    if len(output_list) == 3 and output_list[0] == 0:
        entry_error(f'"a" не може бути 0')
        clear_window_func()

    if len(output_list) == 3 and output_list[0] != 0:
        massage_label["text"] = ""
        return output_list


def calculate_the_equation():
    data = get_data_from_entry()
    result = None
    if data is not None:
        result = calculation_quadratic_equation(data)
    if result is not None and len(result) == 2:
        x1 = result[0]
        x2 = result[1]
        result_label["text"] = f"x1 ={float('%.2f' % x1)}, x2 = {float('%.2f' % x2)}"
    if result is not None and len(result) == 1:
        result_label["text"] = f"x={float('%.2f' % result[0])}"
    if result is None:
        result_label["text"] = "Розвязку немає"


button_result = Button(text="Розрахувати", font=("Arial", 11), command=calculate_the_equation)
button_result.place(x=6, y=150)


def create_cartesian_plane(entry_list):
    a, b, c = entry_list[0], entry_list[1], entry_list[2]
    x_min, x_max, y_min, y_max = -10, 10, -10, 10
    ticks_frequency = 1
    fig, ax = plt.subplots(figsize=(10, 10))

    # Встановлення ідентичний маштабів для обох осей
    ax.set(xlim=(x_min - 1, x_max + 1), ylim=(y_min - 1, y_max + 1), aspect='equal')

    # Створення декартової системи координат
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Позначки "x" і "y" на осях
    ax.set_xlabel('x', size=14, labelpad=-24, x=1.03)
    ax.set_ylabel('y', size=14, labelpad=-21, y=1.02, rotation=0)

    # Визначення положення точок на осях та їхнього цифрового позначення
    x_ticks = np.arange(x_min, x_max + 1, ticks_frequency)
    y_ticks = np.arange(y_min, y_max + 1, ticks_frequency)
    ax.set_xticks(x_ticks[x_ticks != 0])
    ax.set_yticks(y_ticks[y_ticks != 0])

    # Другорядні лінії сітки
    ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)

    # Встановлення стрілок на кінцях координат
    arrow_fmt = dict(markersize=4, color='black', clip_on=False)
    ax.plot(1, 0, marker='>', transform=ax.get_yaxis_transform(), **arrow_fmt)
    ax.plot(0, 1, marker='^', transform=ax.get_xaxis_transform(), **arrow_fmt)

    x = np.linspace(x_min, x_max, 1000)
    y = a * x ** 2 + b * x + c
    graph_window = Toplevel()
    ax.plot(x, y)
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, graph_window)
    toolbar.update()
    canvas.get_tk_widget().pack()


def make_graph():
    data = get_data_from_entry()
    if data is not None:
        create_cartesian_plane(data)


function_graph = Button(text="Графік", font=("Arial", 11), command=make_graph)
function_graph.place(x=250, y=150)


def clear_window_btn():
    clear_window_func()


clear_window = Button(text="Очистити поля", font=("Arial", 9), command=clear_window_btn)
clear_window.place(x=230, y=31)

if __name__ == '__main__':
    window.mainloop()
