import customtkinter
from tkinter import messagebox
import sqlite3 

cnx = sqlite3.connect("somatoriokcal.db")
cursor = cnx.cursor()

def dados():
    global cnx
    _nome = nome.get()
    _email = email.get()
    _idade = idade.get()
    _genero = genero.get()
    _peso = peso.get()
    _altura = altura.get()
    lista =[_nome,_email,_idade,_genero,_peso,_altura]
    cursor.execute(f"INSERT INTO usuario (nome, email, idade, genero, peso, altura) VALUES ('{lista[0]}', '{lista[1]}', {lista[2]}, '{lista[3]}', {lista[4]}, {lista[5]})")
    cnx.commit()

    messagebox.showinfo("Atenção!","Salvo com sucesso!")


janela = customtkinter.CTk()
janela.geometry ('800x500')

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

texto = customtkinter.CTkLabel(janela,text= "Faça seu perfil")
texto.pack(padx=10, pady=10)

nome= customtkinter.CTkEntry(janela,placeholder_text="Digite seu nome")
nome.pack(padx=10, pady=10)
email= customtkinter.CTkEntry(janela,placeholder_text="Digite seu email")
email.pack(padx=10, pady=10)
idade= customtkinter.CTkEntry(janela,placeholder_text="Digite seu idade")
idade.pack(padx=10, pady=10)
genero= customtkinter.CTkEntry(janela,placeholder_text="Digite seu gênero")
genero.pack(padx=10, pady=10)
peso= customtkinter.CTkEntry(janela,placeholder_text="Digite seu peso")
peso.pack(padx=10, pady=10)
altura= customtkinter.CTkEntry(janela,placeholder_text="Digite sua altura")
altura.pack(padx=10, pady=10)
bttn =  customtkinter.CTkButton(janela, text= "salvar", command= dados)
bttn.pack()






janela.mainloop()
cnx.close()
