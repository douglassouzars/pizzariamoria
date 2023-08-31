import customtkinter as ctk

options = {
    'Low': ('5', '10'),
    'Medium': ('15', '20'),
    'High': ('25', '30'),
    'Extreme': ('35', '40')
}

def on_combo1_selected(value):
    values = ('Random',)
    if value == 'Random':
        for v in options.values():
            values += v
    else:
        values += options[value]
    combo2.configure(values=values)
    combo2.set('')

root = ctk.CTk()

var1 = ctk.StringVar()
combo1 = ctk.CTkComboBox(root, variable=var1, values=('Random',)+tuple(options.keys()), command=on_combo1_selected)
combo1.pack()

var2 = ctk.StringVar()
combo2 = ctk.CTkComboBox(root, variable=var2)
combo2.pack()

root.mainloop()