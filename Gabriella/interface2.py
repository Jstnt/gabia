from customtkinter import CTkLabel, CTkEntry, CTk, CTkFont, CTkButton, set_appearance_mode, set_default_color_theme, CTkToplevel
from tkinter import messagebox, ttk
from datetime import datetime
import sqlite3

idusuario = None

class Home(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        global idusuario
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")
        self.geometry("800x500")
        self.title("app")
        largura = self.winfo_screenwidth()
        altura = self.winfo_screenheight()
        cnx = sqlite3.connect("somatoriokcal.db")
        cursor = cnx.cursor()
        self.cursor = cnx.cursor()
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
        self.total = cursor.execute(f"SELECT totalcaloria FROM lancamento WHERE Data='{data}' and id_usuario='{idusuario}'").fetchone()
        print(self.total)
        self.label.configure(text=f"Calorias Consumidas= {self.total}")
        colunas = ('data','refeição', 'kcal', )
        self.tree = ttk.Treeview(self, columns=colunas, show='headings')
        self.tree.heading('data', text='Data', anchor='w')
        self.tree.column('data', width=100)
        self.tree.heading('refeição', text='Refeição', anchor='w')
        self.tree.column('refeição', width=200)
        self.tree.heading('kcal', text='Kcal', anchor='w')
        self.tree.column('kcal', width=160)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(pady= 5)
        # Chama resultadoT para exibir os resultados iniciais
        self.resultadoT()
    def resultadoT(self):
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute(f"SELECT Data, Refeicao, calorias FROM lancamento WHERE id_usuario='{idusuario}'")
        
       
        resultados = self.cursor.fetchall()

        for resultado in resultados:
            self.tree.insert("", "end", values=(resultado[0], resultado[1], resultado[2]))

    def armazenar(self):
        
        hora= datetime.now().time()
        data = datetime.now().strftime("%d/%m/%Y")
        cnx = sqlite3.connect("somatoriokcal.db")
        cursor = cnx.cursor()
        r = self.refeicao.get() 
        k = self.kcal.get()

        cursor.execute(f"INSERT INTO lancamento ('Data', 'Refeicao', 'calorias', 'id_usuario', 'totalcaloria') VALUES ('{data}', '{r}', {k}, {idusuario}, {self.soma})")
        cnx.commit()
        comando = f"SELECT totalcaloria FROM lancamento WHERE id_usuario = '{idusuario}' ORDER BY Data DESC LIMIT 1;"
        resultado = cursor.execute(comando).fetchone()
        self.soma = resultado[0] + float(k)
        cursor.execute(f"UPDATE lancamento SET totalcaloria={self.soma} WHERE Data='{data}' and id_usuario='{idusuario}'")
        cnx.commit()
        
        self.total = cursor.execute(f"SELECT totalcaloria FROM lancamento WHERE Data='{data}' and id_usuario='{idusuario}'").fetchone()
        self.label.configure(text=f"Calorias Consumidas= {self.total}")
        
            
        messagebox.showinfo("Atenção!", "Salvo com sucesso!")
        cursor.execute("SELECT * FROM lancamento")
        dados = cursor.fetchall()
        for row in dados:
            print(row)
        cnx.close()
        self.refeicao.delete(0, "end")
        self.kcal.delete(0, "end")
        self.resultadoT()

class Cadastro(CTkToplevel):
    def __init__(self):
        super().__init__()
        
        largura = self.winfo_screenwidth()
        altura = self.winfo_screenheight()
        x = (largura - 750) // 2
        y = (altura - 600) // 2
        self.geometry(f"750x600+{x}+{y}")
        self.title("")
        self.resizable(0,0)


        texto = CTkLabel(self,text= "Faça seu perfil")
        texto.pack(padx=10, pady=10)

        self.nome= CTkEntry(self,placeholder_text="Digite seu nome")
        self.nome.pack(padx=10, pady=10)
        self.email= CTkEntry(self,placeholder_text="Digite seu email")
        self.email.pack(padx=10, pady=10)
        self.idade= CTkEntry(self,placeholder_text="Digite seu idade")
        self.idade.pack(padx=10, pady=10)
        self.genero= CTkEntry(self,placeholder_text="Digite seu gênero")
        self.genero.pack(padx=10, pady=10)
        self.peso= CTkEntry(self,placeholder_text="Digite seu peso")
        self.peso.pack(padx=10, pady=10)
        self.altura= CTkEntry(self,placeholder_text="Digite sua altura")
        self.altura.pack(padx=10, pady=10)
        self.bttn =  CTkButton(self, text= "salvar", command= self.dados)
        self.bttn.pack()

    def dados(self):
        cnx = sqlite3.connect("somatoriokcal.db")
        cursor = cnx.cursor()
        _nome = self.nome.get()
        _email = self.email.get()
        _idade = self.idade.get()
        _genero = self.genero.get()
        _peso = self.peso.get()
        _altura = self.altura.get()
        lista =[_nome,_email,_idade,_genero,_peso,_altura]
        cursor.execute(f"INSERT INTO usuario (nome, email, idade, genero, peso, altura) VALUES ('{lista[0]}', '{lista[1]}', {lista[2]}, '{lista[3]}', {lista[4]}, {lista[5]})")
        cnx.commit()
        cnx.close()


        messagebox.showinfo("Atenção!","Salvo com sucesso!")

class Login(CTk):
    def __init__(self):
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")
        print("Construtor de Cadastro chamado")
        super().__init__()
        FonteN = CTkFont(weight="bold", size= 14)
        CTkLabel(self, text="Faça seu Login", font = FonteN).pack()
        self.user = CTkEntry(self, placeholder_text="Insira o nome")
        self.user.pack(pady = 8)
        self.email = CTkEntry(self, placeholder_text="Insira seu email")
        self.email.pack(pady = 8)
        ok = CTkButton(self, text="ok",font = FonteN, command= self.show_error)
        ok.pack(pady = 8)
        bttncadastro = CTkButton(self, text="Criar Perfil",font = FonteN, command= self.InitCadastro, text_color= "blue",fg_color="transparent", width=10, height=5)
        bttncadastro.pack()
        self.cadastro = None
    def show_error(self):
        email = self.email.get()
        nome = self.user.get()
        cnx = sqlite3.connect("somatoriokcal.db")
        cursor = cnx.cursor()

        # Consulta para verificar se o e-mail e o nome correspondem
        comando = f"SELECT nome FROM usuario WHERE email='{email}'"
        resultado = cursor.execute(comando).fetchone()

        if resultado and resultado[0] == nome:
            global idusuario
            idusuario = cursor.execute(f"SELECT id FROM usuario WHERE email='{email}'").fetchone()[0]
            print("Login realizado")
            self.destroy()  # Use self.destroy() para fechar a janela de login
            initHome()
        else:
            # Mostrar mensagem de erro
            messagebox.showerror("Erro de Login", "Usuário Inexistente no banco de dados")

        cnx.close()

    def InitCadastro(self):
        if self.cadastro is None or not self.cadastro.winfo_exists():
            print("Criando instância de Cadastro")
            self.cadastro = Cadastro()
            self.cadastro.grab_set()
            self.cadastro.update()
            self.cadastro.mainloop()
        else:
            self.cadastro.grab_set()       



def initHome():
    home = Home()
    largura = home.winfo_screenwidth()
    altura = home.winfo_screenheight()
    x = (largura - 750) // 2
    y = (altura - 600) // 2
    home.geometry(f"750x600+{x}+{y}")
    home.title("")
    home.resizable(0,0)
    home.mainloop()   

if __name__ == "__main__":
    app = Login()
    largura = app.winfo_screenwidth()
    altura = app.winfo_screenheight()
    x = (largura - 200) // 2
    y = (altura - 200) // 2
    app.geometry(f"200x180+{x}+{y}")
    app.title("")
    app.resizable(0,0)
    app.mainloop()