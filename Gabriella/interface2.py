from customtkinter import CTkLabel, CTkEntry, CTk, CTkButton, set_appearance_mode, set_default_color_theme
from tkinter import messagebox
from datetime import datetime
import sqlite3

class Home(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")
        self.geometry("800x500")
        self.title("Home")
        largura = self.winfo_screenwidth()
        altura = self.winfo_screenheight()
        cnx = sqlite3.connect("somatoriokcal.db")
        cursor = cnx.cursor()
        data = datetime.now().strftime("%d/%m/%Y")
        self.soma = 0
        x = (largura - 500) // 2
        y = (altura - 400) // 2
        self.geometry(f"500x400+{x}+{y}")
        self.resizable(0, 0)
        self.texto = CTkLabel(self, text="Que refeiçao voce consumiu, e quantas kcal possuia?")
        self.texto.pack(padx=10, pady=10)
        self.refeicao = CTkEntry(self, placeholder_text="Refeição:")
        self.refeicao.pack(padx=10, pady=10)
        self.kcal = CTkEntry(self, placeholder_text="Kcal:")
        self.kcal.pack(padx=10, pady=10)
        self.label = CTkLabel(self, text="Calorias Consumidas= 0")
        self.label.pack()
        self.button = CTkButton(self, text="Enviar", command=self.armazenar)
        self.button.pack()
        r = self.refeicao.get() 
        k = self.kcal.get()
        self.total = cursor.execute(f"SELECT totalcaloria FROM lancamento WHERE Data='{data}'").fetchone()
        print(self.total)
        self.label.config(text=f"Calorias Consumidas= {self.total}")

    def armazenar(self):
        hora= datetime.now().time()
        data = datetime.now().strftime("%d/%m/%Y")
        cnx = sqlite3.connect("somatoriokcal.db")
        cursor = cnx.cursor()
        r = self.refeicao.get() 
        k = self.kcal.get()
        cursor.execute(f"INSERT INTO lancamento ('Data', 'Refeicao', 'calorias', 'id_usuario', 'totalcaloria') VALUES ('{data}', '{r}', {k}, 1, {self.soma})")
        cnx.commit()
        self.soma += float(k)
        cursor.execute(f"UPDATE lancamento SET totalcaloria={self.soma} WHERE Data='{data}'")
        cnx.commit()
        
        self.total = cursor.execute(f"SELECT totalcaloria FROM lancamento WHERE Data='{data}'").fetchone()
        self.label.config(text=f"Calorias Consumidas= {self.total}")
        
            
        messagebox.showinfo("Atenção!", "Salvo com sucesso!")
        cursor.execute("SELECT * FROM lancamento")
        dados = cursor.fetchall()
        for row in dados:
            print(row)
        cnx.close()

if __name__ == "__main__":
    home = Home()
    home.title("")
    home.resizable(0, 0)
    home.mainloop()