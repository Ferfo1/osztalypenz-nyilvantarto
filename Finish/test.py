import tkinter as tk
from tkinter import messagebox

class Student:
    def __init__(self, name, balance):
        self.name = name
        self.balance = int(balance)

class App:
    def __init__(self, window):
        self.window = window
        self.window.title("OSZTÁLYPÉNZ ALKALMAZÁS")
        self.students = {}

        # Fájlból tanulók betöltése
        self.load_students()

        # GUI elemek
        self.label_name = tk.Label(self.window, text="Név:", font=("Helvetica", 14))
        self.label_name.grid(row=0, column=0)

        self.entry_name = tk.Entry(self.window, font=("Helvetica", 14))
        self.entry_name.grid(row=0, column=1)

        self.label_balance = tk.Label(self.window, text="Egyenleg:", font=("Helvetica", 14))
        self.label_balance.grid(row=1, column=0)

        self.entry_balance = tk.Entry(self.window, font=("Helvetica", 14))
        self.entry_balance.grid(row=1, column=1)

        self.button_add = tk.Button(self.window, text="Tanuló hozzáadása", command=self.add_student, font=("Helvetica", 14))
        self.button_add.grid(row=2, column=0, columnspan=2)

        self.button_delete = tk.Button(self.window, text="Tanuló törlése", command=self.delete_student, font=("Helvetica", 14))
        self.button_delete.grid(row=3, column=0, columnspan=2)

        self.button_save = tk.Button(self.window, text="Tanulók mentése", command=self.save_students, font=("Helvetica", 14))
        self.button_save.grid(row=4, column=0, columnspan=2)

        self.listbox_students = tk.Listbox(self.window, width=40, font=("Helvetica", 14))
        self.listbox_students.grid(row=5, column=0, columnspan=2, sticky="nsew")

        scrollbar = tk.Scrollbar(self.window, command=self.listbox_students.yview)
        scrollbar.grid(row=5, column=2, sticky="nse")

        self.listbox_students.config(yscrollcommand=scrollbar.set)

        # Pénz hozzáadás és kivétel elemek
        self.label_money_action = tk.Label(self.window, text="Pénzmozgás:", font=("Helvetica", 14))
        self.label_money_action.grid(row=6, column=0)

        self.entry_money_action = tk.Entry(self.window, font=("Helvetica", 14))
        self.entry_money_action.grid(row=6, column=1)

        self.button_add_money = tk.Button(self.window, text="Pénz hozzáadása", command=self.add_money, font=("Helvetica", 14))
        self.button_add_money.grid(row=7, column=0, columnspan=2)

        self.button_withdraw_money = tk.Button(self.window, text="Pénz kivétele", command=self.withdraw_money, font=("Helvetica", 14))
        self.button_withdraw_money.grid(row=8, column=0, columnspan=2)

        self.button_add_to_all = tk.Button(self.window, text="Minden tanulóhoz pénz hozzáadása", command=self.add_money_to_all, font=("Helvetica", 14))
        self.button_add_to_all.grid(row=9, column=0, columnspan=2)

        self.button_withdraw_from_all = tk.Button(self.window, text="Minden tanulótól pénz kivétele", command=self.withdraw_money_from_all, font=("Helvetica", 14))
        self.button_withdraw_from_all.grid(row=10, column=0, columnspan=2)

        # Automatikus mentés beállítása minden pénzmozgás után
        self.window.after(300000, self.auto_save)

        # Összesített egyenleg címke
        self.label_total_balance = tk.Label(self.window, text="Összes egyenleg: 0", font=("Helvetica", 14))
        self.label_total_balance.grid(row=11, column=0, columnspan=2)

        self.update_students_listbox()

    def load_students(self):
        try:
            with open("students.txt", "r", encoding="utf-8") as file:
                for line in file:
                    name, balance = line.strip().split(",")
                    self.students[name] = Student(name, float(balance))
        except FileNotFoundError:
            pass


    def save_students(self):
        with open("students.txt", "w", encoding='utf-8') as file:
            for student in self.students.values():
                file.write(f"{student.name},{student.balance}\n")

    def add_student(self):
        name = self.entry_name.get()
        balance = self.entry_balance.get()

        if name in self.students:
            messagebox.showerror("Hiba", "Ilyen nevű tanuló már létezik.")
            return

        self.students[name] = Student(name, int(balance))
        self.save_students()
        self.update_students_listbox()

    def delete_student(self):
        selected_student = self.listbox_students.get(self.listbox_students.curselection())

        if selected_student:
            del self.students[selected_student.split(" - ")[0]]
            self.save_students()
            self.update_students_listbox()

    def add_money(self):
        selected_student = self.listbox_students.get(self.listbox_students.curselection())
        if selected_student:
            try:
                amount = int(self.entry_money_action.get())
                self.students[selected_student.split(" - ")[0]].balance += amount
                self.save_students()
                self.update_students_listbox()
            except ValueError:
                messagebox.showerror("Hiba", "Érvénytelen összeg.")

    def withdraw_money(self):
        selected_student = self.listbox_students.get(self.listbox_students.curselection())
        if selected_student:
            try:
                amount = int(self.entry_money_action.get())
                
                self.students[selected_student.split(" - ")[0]].balance -= amount
                self.save_students()
                self.update_students_listbox()
            except ValueError:
                messagebox.showerror("Hiba", "Érvénytelen összeg.")


    def add_money_to_all(self):
        try:
            amount = int(self.entry_money_action.get())
            for student in self.students.values():
                student.balance += amount
            self.save_students()
            self.update_students_listbox()
        except ValueError:
            messagebox.showerror("Hiba", "Érvénytelen összeg.")

    def withdraw_money_from_all(self):
        try:
            amount = int(self.entry_money_action.get())
            for student in self.students.values():
                if student.balance >= amount:
                    student.balance -= amount
                else:
                    messagebox.showerror("Hiba", f"Nincs elég pénz {student.name} tanulónál!")
            self.save_students()
            self.update_students_listbox()
        except ValueError:
            messagebox.showerror("Hiba", "Érvénytelen összeg.")

    def auto_save(self):
        self.save_students()
        # Újra beállítjuk az időzítőt
        self.window.after(300000, self.auto_save)

    def update_students_listbox(self):
        total_balance = sum(student.balance for student in self.students.values())
        self.label_total_balance.config(text=f"Összes egyenleg: {total_balance}")

        self.listbox_students.delete(0, tk.END)
        for student in self.students.values():
            balance_str = f"{student.balance:.0f}"  # Ne tartalmazzon tizedesjegyeket
            self.listbox_students.insert(tk.END, f"{student.name} - Egyenleg: {balance_str}")


window = tk.Tk()
app = App(window)
window.mainloop()
