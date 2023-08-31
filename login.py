from distutils import command
from email import message
import os
from tkinter import *

import customtkinter as ctk
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import mysql.connector
from tkinter import messagebox



class BackEnd():
    def __init__(self):
        self.conn = None
        self.cursor = None
    def conecta_db(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="senhateste",
            db="pizzaria"
        )
        self.cursor = self.conn.cursor()
        #print("Banco de dados conectado")

    def desconecta_db(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        #print("Banco de dados desconectado")
   


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
class App():
    def __init__(self):
        self.root = root
        self.tela()
        self.frames()
        self.backend = BackEnd()


    def tela(self):
        """Definição da tela e sua cor total"""
        self.root.title("Sistema Moriá")
        self.root.configure(background='#e8e8e8')
        self.root.geometry("700x400")
        self.root.resizable(False, False)

    def frames(self):
        """Imagem de login"""
        logoimg2 = Image.open("2.png")
        self.lg2 = ImageTk.PhotoImage(logoimg2)
        self.lbl2 = tk.Label(self.root, image=self.lg2)
        self.lbl2.place(relx=0.1, rely=0.25, relwidth=0.28, relheight=0.5)
        self.lbl2.image = self.lg2
        """Login"""
        self.frame_1 = ctk.CTkFrame(self.root, width=350,height=396)
        self.frame_1.pack(side=RIGHT)

        def tela_menu():
            
            pass
        """widgets"""
        self.titulo = ctk.CTkLabel(self.frame_1, text="Sistema de Login", font=("Times New Roman",24,"bold"))
        self.titulo.place(relx=0.05, rely=0.02, relwidth=0.9, relheight=0.07)
        self.nome = ctk.CTkEntry(self.frame_1, placeholder_text="nome", width=300, font=("Times New Roman",16))
        self.nome.place(relx=0.1, rely=0.32, relwidth=0.8, relheight=0.07)
        self.nome_aviso = ctk.CTkLabel(self.frame_1, text="O nome é obrigatório", width=300, text_color="red",font=("Times New Roman", 10))
        self.nome_aviso.place(relx=0.1, rely=0.39, relwidth=0.8, relheight=0.07)
        self.senha = ctk.CTkEntry(self.frame_1, placeholder_text="senha", width=300, font=("Times New Roman",16))
        self.senha.place(relx=0.1, rely=0.46, relwidth=0.8, relheight=0.07)
        self.senha_aviso = ctk.CTkLabel(self.frame_1,text="A senha é obrigatório", width=300, text_color="red",font=("Times New Roman",10))
        self.senha_aviso.place(relx=0.1, rely=0.53, relwidth=0.8, relheight=0.07)
        self.button = ctk.CTkButton(self.frame_1, fg_color='#FF1616', text_color='White',text="LOGIN",width=300, command=self.verificando)
        self.button.place(relx=0.1, rely=0.75, relwidth=0.8, relheight=0.07)

    #def conecta_db(self):
     #   self.backend.conecta_db()

    #def desconecta_db(self):
    #    self.backend.desconecta_db()    

    def verificando(self):
        self.nome_login = self.nome.get()
        self.senha_login = self.senha.get()
        print(self.nome_login,self.senha_login)
        self.limpar_dados()
        
        self.backend.conecta_db()
        self.backend.cursor.execute("""SELECT * FROM login WHERE (username=%s and password=%s)""",(self.nome_login, self.senha_login))

        self.verificando = self.backend.cursor.fetchone()
        try:
            if(self.nome_login in self.verificando and self.senha_login in self.verificando):
                messagebox.showinfo(title='Sistema de Login',message='Acesso Liberado')
                root.destroy()
                import main
                app = main.App()  # Instancie a classe App para exibir a tela principal
                app.run()  # Chame um método ou função para exibir a tela principal
                self.backend.desconecta_db()
                
        except:
            print("desconectado")
            #messagebox.showinfo(title='Erro no Sistema de Login',message='Acesso Negado')

    def limpar_dados(self):
        self.nome.delete(0,END)
        self.senha.delete(0,END)    
App()
root.mainloop()