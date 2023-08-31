import os
from ssl import CERT_NONE
from tkinter import *
from turtle import update
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime, timedelta
from login import BackEnd
from tkinter import messagebox

root = ctk.CTk()

class App():
    
    
    def __init__(self):
        self.root = root
        
        self.logo()
        self.tela()
        self.frames()
        self.update_time()
        #self.radio_var = ctk.IntVar(value=0)
        self.backend = BackEnd()
       
        

    def tela(self):
        """Definição da tela e sua cor total"""
        self.root.title("PIZZARIA MORIÁ")
        self.root.configure(background='#e8e8e8')
        self.root.geometry("1366x768")
        self.root.resizable(True, True)
        self.root.minsize(850, 600)

    def logo(self):
        logoimg = Image.open("mussarela(1).png")
        self.lg = ImageTk.PhotoImage(logoimg)
        self.lbl = tk.Label(self.root, image=self.lg)
        self.lbl.place(relx=0.0, rely=0.0, relwidth=1.05, relheight=1)
        self.lbl.image = self.lg


    def frames(self):
        """Header preto"""
        self.frame_1 = ctk.CTkFrame(self.root)
        #self.frame_1.configure(background='#000000')
        self.frame_1.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.15)

        """nav lateral"""
        self.frame_2 = ctk.CTkFrame(self.root)
        #self.frame_2.configure(background='#000000')
        self.frame_2.place(relx=0.0, rely=0.15, relwidth=0.055, relheight=1)

        """rodape"""
        self.frame_3 = ctk.CTkFrame(self.root,fg_color='#ff0000')
        #self.frame_3.configure(background='#ff0000')
        self.frame_3.place(relx=0.0, rely=0.95, relwidth=1, relheight=0.05)

        """Caixa CE"""

        logoimg2 = Image.open("2(1).png")
        self.lg2 = ImageTk.PhotoImage(logoimg2)
        self.lbl2 = tk.Label(self.frame_1, image=self.lg2)
        self.lbl2.place(relx=0.08, rely=0.03, relwidth=0.07, relheight=0.95)
        self.lbl2.image = self.lg2

        """tela principal"""
        #self.frame_4 = Frame(self.root)
        #self.frame_4.configure(background='white')
        #self.frame_4.place(relx=0.09, rely=0.2, relwidth=0.875, relheight=0.75)
        
        

        
        def cardapio():
                        
            self.frame_4.pack_forget()
            def select_lista():
                
                self.historico.delete(*self.historico.get_children())
                
                self.backend.conecta_db()
                # Comando SQL para inserir dados na tabela "catalogo" com os valores de produto e preco
                sql = "INSERT INTO catalogo (produto, preco) VALUES (%s, %s)"
                # Executa o comando SQL com os valores de produto e preco
                self.backend.cursor.execute(sql, (self.produto, self.preco))
                # Commit das alterações no banco de dados
                self.backend.conn.commit()
                # Fechar a conexão com o banco de dados
                self.backend.conn.close()

            def salvar_produto():
                self.produto = self.produto_entry.get()
                self.preco = self.preco_entry.get()
                if self.produto == '' or self.preco == '':
                    messagebox.showerror("Falta atributos", f"Preencha o sabor e escolha o tipo")
                else:    
                    self.backend.conecta_db()
                    sql = "INSERT INTO catalogo (produto, preco) VALUES (%s, %s)"
                    self.backend.cursor.execute(sql, (self.produto, self.preco))
                    self.backend.conn.commit()
                    self.backend.conn.close()
                    cardapio()

            def salvar_sabor():
                self.sabor = self.sabor_entry.get().capitalize()
                self.tipo = self.tipo_entry.get().lower()
                print(self.sabor,self.tipo)
                if self.sabor == '' or self.tipo == '':
                    messagebox.showerror("Falta atributos", f"Preencha o sabor e escolha o tipo")
                else:
                    self.backend.conecta_db()
                    sql = f"INSERT INTO {self.tipo} (sabor) VALUES (%s)"
                    self.backend.cursor.execute(sql, (self.sabor,))
                    self.backend.conn.commit()
                    self.backend.conn.close()
                    cardapio()
                       
            def excluir():
                
                item_selecionado_produto = self.historico.selection()
                item_sabor_tradicionais = self.historico_tradicionais.selection()
                item_sabor_doces = self.historico_doces.selection()
                item_sabor_especiais = self.historico_especiais.selection()
                if item_selecionado_produto:
                    item_id = self.historico.item(item_selecionado_produto, "values")[0]
                    try:
                        self.backend = BackEnd()
                        self.backend.conecta_db()
                        sql = "DELETE FROM catalogo WHERE id = %s"
                        self.backend.cursor.execute(sql, (item_id,))
                        self.backend.conn.commit()
                        self.historico.delete(item_selecionado_produto)
                        self.backend.conn.close()   
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao excluir o item: {e}")
                elif item_sabor_tradicionais:
                    item_id = self.historico_tradicionais.item(item_sabor_tradicionais, "values")[0]
                    try:
                        self.backend = BackEnd()
                        self.backend.conecta_db()
                        sql = "DELETE FROM tradicional WHERE idsabor1 = %s"
                        self.backend.cursor.execute(sql, (item_id,))
                        self.backend.conn.commit()
                        self.historico_tradicionais.delete(item_sabor_tradicionais)
                        self.backend.conn.close()   
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao excluir o item: {e}")
                elif item_sabor_doces:
                    item_id = self.historico_doces.item(item_sabor_doces, "values")[0]
                    try:
                        self.backend = BackEnd()
                        self.backend.conecta_db()
                        sql = "DELETE FROM doces WHERE idsabor2 = %s"
                        self.backend.cursor.execute(sql, (item_id,))
                        self.backend.conn.commit()
                        self.historico_doces.delete(item_sabor_doces)
                        self.backend.conn.close()   
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao excluir o item: {e}")  
                elif item_sabor_especiais:
                    item_id = self.historico_especiais.item(item_sabor_especiais, "values")[0]
                    try:
                        self.backend = BackEnd()
                        self.backend.conecta_db()
                        sql = "DELETE FROM especiais WHERE idsabor3 = %s"
                        self.backend.cursor.execute(sql, (item_id,))
                        self.backend.conn.commit()
                        self.historico_especiais.delete(item_sabor_especiais)
                        self.backend.conn.close()   
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao excluir o item: {e}")               
                else:
        # Se nenhum item estiver selecionado, exiba uma mensagem de aviso
                    messagebox.showwarning("Aviso", "Selecione um item para excluir.")
            
            """tela cadastro"""
            self.frame_cadastro = ctk.CTkFrame(self.root, fg_color='white')
            self.frame_cadastro.place(relx=0.09, rely=0.2, relwidth=0.875, relheight=0.75)

            """tela cadastro- LABEL"""
            self.titulo2=ctk.CTkLabel(self.frame_1, text=f"Produtos",font=('Arial', 38))
            self.titulo2.place(relx=0.20, rely=0.10, relwidth=0.55, relheight=1) 
            self.cadastroproduto=ctk.CTkLabel(self.frame_cadastro,text_color="black", text=f"Cadastro de Produtos:",font=('Times New Roman', 28))
            self.cadastroproduto.place(relx=0.01, rely=0.05, relwidth=0.3, relheight=0.07)
            self.nomeproduto=ctk.CTkLabel(self.frame_cadastro,text_color="black", text=f"Produtos:",font=('Times New Roman', 18))
            self.nomeproduto.place(relx=0.01, rely=0.15, relwidth=0.1, relheight=0.07)
            self.precoproduto=ctk.CTkLabel(self.frame_cadastro,text_color="black", text=f"Preço:",font=('Times New Roman', 18))
            self.precoproduto.place(relx=0.01, rely=0.23, relwidth=0.1, relheight=0.07)
            self.cadastroproduto=ctk.CTkLabel(self.frame_cadastro,text_color="black", text=f"Catálogo:",font=('Times New Roman', 28))
            self.cadastroproduto.place(relx=0.01, rely=0.33, relwidth=0.18, relheight=0.07)
            self.nomesabor=ctk.CTkLabel(self.frame_cadastro,text_color="black", text=f"Sabor:",font=('Times New Roman', 18))
            self.nomesabor.place(relx=0.43, rely=0.23, relwidth=0.1, relheight=0.07)
            self.cadastrosabor=ctk.CTkLabel(self.frame_cadastro,text_color="black", text=f"Novo Sabor:",font=('Times New Roman', 28))
            self.cadastrosabor.place(relx=0.38, rely=0.05, relwidth=0.3, relheight=0.07)
            self.nometipo=ctk.CTkLabel(self.frame_cadastro,text_color="black", text=f"Tipo:",font=('Times New Roman', 18))
            self.nometipo.place(relx=0.43, rely=0.15, relwidth=0.1, relheight=0.07)

            """tela cadastro- Entry"""
            self.produto_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="", width=300, font=("Times New Roman",16))
            self.produto_entry.place(relx=0.1, rely=0.15, relwidth=0.25, relheight=0.07)
            self.preco_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="", width=300, font=("Times New Roman",16))
            self.preco_entry.place(relx=0.1, rely=0.23, relwidth=0.10, relheight=0.07)
            self.sabor_entry = ctk.CTkEntry(self.frame_cadastro, placeholder_text="", width=300, font=("Times New Roman",16))
            self.sabor_entry.place(relx=0.51, rely=0.23, relwidth=0.15, relheight=0.07)

            """tela cadastro- BOTOES"""
            self.salvarproduto = ctk.CTkButton(self.frame_cadastro, text='Salvar', fg_color='green', text_color='White',font=("Times New Roman",16),command=salvar_produto)
            self.salvarproduto.place(relx=0.3, rely=0.23, relwidth=0.05, relheight=0.07)
            self.salvarsabor = ctk.CTkButton(self.frame_cadastro, text='Salvar', fg_color='green', text_color='White',font=("Times New Roman",16),command=salvar_sabor)
            self.salvarsabor.place(relx=0.665, rely=0.23, relwidth=0.05, relheight=0.07)           

            self.tipo_entry = ctk.CTkComboBox(self.frame_cadastro,text_color="black",fg_color='#e8e8e8', values=('Tradicional','Doces','Especiais'),font=('Times New Roman', 22),state='readonly')
            self.tipo_entry.place(relx=0.51, rely=0.15, relwidth=0.205, relheight=0.07)

            self.historico = ttk.Treeview(self.frame_cadastro, columns=("id", "produto", "preco"), show="headings")
            style = ttk.Style()
            style.configure("Treeview", font=('Times New Roman', 17))
            self.historico.heading("id", text="ID")
            self.historico.heading("produto", text="Produto")
            self.historico.heading("preco", text="Preço")
            self.historico.column("id", width=50, anchor=tk.CENTER)
            self.historico.column("produto", width=200, anchor=tk.CENTER)
            self.historico.column("preco", width=100, anchor=tk.CENTER)
            self.backend = BackEnd()
            self.backend.conecta_db()
            self.backend.cursor.execute("SELECT id, produto, preco FROM catalogo WHERE id > 0")
            results = self.backend.cursor.fetchall()
            for row in results:
                self.historico.insert("", "end", values=row)       
            #self.backend.conn.close()            
            self.historico.place(relx=0.03, rely=0.43, relwidth=0.3, relheight=0.54)
            self.scroolList = Scrollbar(self.frame_cadastro,orient='vertical')
            self.historico.configure(yscrollcommand=self.scroolList.set)
            self.scroolList.place(relx=0.33, rely=0.43, relwidth=0.02, relheight=0.54)
           
           
            self.backend = BackEnd()
            self.backend.conecta_db()
            self.backend.cursor.execute("SELECT idsabor1, sabor FROM tradicional")
            results2 = self.backend.cursor.fetchall()
            #self.backend.conn.close()
            self.historico_tradicionais = ttk.Treeview(self.frame_cadastro, columns=("id", "sabor"), show="headings")
            style2 = ttk.Style()
            style2.configure("Treeview", font=('Times New Roman', 17))
            self.historico_tradicionais.heading("id", text="ID")  # Substitua "idsabor1" por "id" no heading
            self.historico_tradicionais.heading("sabor", text="TRADICIONAIS")
            self.historico_tradicionais.column("id", width=5, anchor=tk.CENTER)  # Substitua "idsabor1" por "id" no column
            self.historico_tradicionais.column("sabor", width=200, anchor=tk.CENTER)
            for row in results2:
                self.historico_tradicionais.insert("", "end", values=row)
            self.historico_tradicionais.place(relx=0.37, rely=0.43, relwidth=0.15, relheight=0.54)
            self.scroolList_tradicionais = Scrollbar(self.frame_cadastro, orient='vertical')
            self.historico_tradicionais.configure(yscrollcommand=self.scroolList_tradicionais.set)
            self.scroolList_tradicionais.place(relx=0.52, rely=0.43, relwidth=0.02, relheight=0.54)

            self.backend = BackEnd()
            self.backend.conecta_db()
            self.backend.cursor.execute("SELECT idsabor2, sabor FROM doces")
            results3 = self.backend.cursor.fetchall()
            #self.backend.conn.close()
            self.historico_doces = ttk.Treeview(self.frame_cadastro, columns=("id", "sabor"), show="headings")
            style3 = ttk.Style()
            style3.configure("Treeview", font=('Times New Roman', 17))
            self.historico_doces.heading("id", text="ID")  # Substitua "idsabor1" por "id" no heading
            self.historico_doces.heading("sabor", text="DOCES")
            self.historico_doces.column("id", width=20, anchor=tk.CENTER)  # Substitua "idsabor1" por "id" no column
            self.historico_doces.column("sabor", width=200, anchor=tk.CENTER)
            for row in results3:
                self.historico_doces.insert("", "end", values=row)
            self.historico_doces.place(relx=0.55, rely=0.43, relwidth=0.15, relheight=0.54)
            self.scroolList_doces = Scrollbar(self.frame_cadastro, orient='vertical')
            self.historico_doces.configure(yscrollcommand=self.scroolList_doces.set)
            self.scroolList_doces.place(relx=0.70, rely=0.43, relwidth=0.02, relheight=0.54)

            self.backend = BackEnd()
            self.backend.conecta_db()
            self.backend.cursor.execute("SELECT idsabor3, sabor FROM especiais")
            results4 = self.backend.cursor.fetchall()
            #self.backend.conn.close()
            self.historico_especiais = ttk.Treeview(self.frame_cadastro, columns=("id", "sabor"), show="headings")
            style3 = ttk.Style()
            style3.configure("Treeview", font=('Times New Roman', 17))
            self.historico_especiais.heading("id", text="ID")  # Substitua "idsabor1" por "id" no heading
            self.historico_especiais.heading("sabor", text="ESPECIAIS")
            self.historico_especiais.column("id", width=5, anchor=tk.CENTER)  # Substitua "idsabor1" por "id" no column
            self.historico_especiais.column("sabor", width=200, anchor=tk.CENTER)
            for row in results4:
                self.historico_especiais.insert("", "end", values=row)
            self.historico_especiais.place(relx=0.73, rely=0.43, relwidth=0.17, relheight=0.54)
            self.scroolList_especiais = Scrollbar(self.frame_cadastro, orient='vertical')
            self.historico_especiais.configure(yscrollcommand=self.scroolList_especiais.set)
            self.scroolList_especiais.place(relx=0.90, rely=0.43, relwidth=0.02, relheight=0.54)

            self.excluirproduto = ctk.CTkButton(self.frame_cadastro, text='Excluir', fg_color='#FF1616', text_color='White',font=("Times New Roman",16),command=excluir)
            self.excluirproduto.place(relx=0.93, rely=0.75, relwidth=0.06, relheight=0.07)

        """tela menu- PRINCIPAL"""    
        def menu():

            self.frame_4 = ctk.CTkFrame(self.root, fg_color='white')
            self.frame_4.place(relx=0.09, rely=0.2, relwidth=0.875, relheight=0.75)
            titulo=ctk.CTkLabel(self.frame_1,text=f"Qual o pedido?",font=('Arial', 38))
            titulo.place(relx=0.20, rely=0.10, relwidth=0.55, relheight=1)
            self.listra_frame_4 = ctk.CTkFrame(self.root, fg_color='red')
            self.listra_frame_4.place(relx=0.09, rely=0.35, relwidth=0.875, relheight=0.01)
            self.listra2_frame_4 = ctk.CTkFrame(self.root, fg_color='red')
            self.listra2_frame_4.place(relx=0.09, rely=0.5, relwidth=0.875, relheight=0.01)
            self.lista_frame_4 = ctk.CTkFrame(self.root)
            self.lista_frame_4.place(relx=0.4, rely=0.36, relwidth=0.565, relheight=0.59)
            titulo=ctk.CTkLabel(self.frame_1,text=f"Qual o pedido?",font=('Arial', 38))
            titulo.place(relx=0.20, rely=0.10, relwidth=0.55, relheight=1)
            self.itens_selecionados = []
            self.botoes_excluir = []
            self.lista_vendas = ttk.Treeview(self.lista_frame_4, columns=("item","preco",), show="headings", height=10)
            self.lista_vendas.heading("item", text="Item")
            self.lista_vendas.heading("preco", text="Preço")
            self.lista_vendas.place(relx=0.01, rely=0.25, relwidth=0.86, relheight=0.75)
            total_final = total_final = f"Total: R$ {0.0}"
            self.total_lista_itens = ctk.CTkLabel(self.root, text=total_final, text_color="white",font=('Times New Roman', 35))
            self.total_lista_itens.place(relx=0.09, rely=0.7, relwidth=0.31, relheight=0.1)
            def adicionar():
                largura_total = self.lista_vendas.winfo_width()

        # Calcula o tamanho da coluna "item" (70% ou 700, o que for menor)
                largura_item = min(int(largura_total * 0.7), 700)

        # Calcula o tamanho da coluna "preco" (30%)
                largura_preco = int(largura_total * 0.3)

        # Ajusta as larguras das colunas no Treeview
                self.lista_vendas.column("item", width=largura_item)
                self.lista_vendas.column("preco", width=largura_preco,anchor=CENTER)
                # Captura dos valores selecionados nos comboboxes
                pedido = selecionartipo.get()
                sabor = self.selecionarsabor.get()
                variedade = "meia" if radio_var.get() == 1 else "inteira"
                borda = self.selecionarborda.get()
                adicionais = self.selecionaradd.get()   
                bebidas = self.selecionarbebida.get()
                # Impressão dos valores selecionados
                print(f"Pedido: {pedido}")
                print(f"Sabor: {sabor}")
                print(f"Variedade: {variedade}")
                print(f"Borda: {borda}")
                print(f"Adicionais: {adicionais}")
                print(f"bebidas: {bebidas}")

                if variedade and pedido and sabor:
                    print(pedido)
                    self.backend = BackEnd()
                    self.backend.conecta_db()
                    self.backend.cursor.execute("SELECT preco FROM catalogo WHERE produto = %s", (pedido,))
                    resultado = self.backend.cursor.fetchone()  # Recuperar apenas o primeiro resultado (preço)

                    if resultado:
                        preco = float(resultado[0])   # Valor do preço está na primeira posição da tupla
                        item_pizza = f"{variedade}      {pedido}          {sabor}"
                        if variedade == 'meia':
                            preco_meia = preco / 2
                            item_pizza_preco = f"R$ {preco_meia:.2f}"
                        else:
                            item_pizza_preco = f"R$ {preco:.2f}"
                        self.lista_vendas.insert("", "end", values=(item_pizza, item_pizza_preco))
                        if borda:
                            self.backend = BackEnd()
                            self.backend.conecta_db()
                            self.backend.cursor.execute("SELECT preco FROM catalogo WHERE produto = %s", (borda,))
                            resultado2 = self.backend.cursor.fetchone()  # Recuperar apenas o primeiro resultado (preço)
                            if resultado2:
                                preco2 = float(resultado2[0])
                                item_borda_preco= f"R$ {preco2:.2f}"
                                self.lista_vendas.insert("", "end", values=(f"                    + {borda}",item_borda_preco))
                        if adicionais:
                            self.backend = BackEnd()
                            self.backend.conecta_db()
                            self.backend.cursor.execute("SELECT preco FROM catalogo WHERE produto = %s", (adicionais,))
                            resultado3 = self.backend.cursor.fetchone()  # Recuperar apenas o primeiro resultado (preço)
                            if resultado3:
                                preco3 = float(resultado3[0])
                                item_adicionais_preco= f"R$ {preco3:.2f}"
                                self.lista_vendas.insert("", "end", values=(f"                    + {adicionais}",item_adicionais_preco))    
                elif bebidas:
                        self.backend = BackEnd()
                        self.backend.conecta_db()
                        self.backend.cursor.execute("SELECT preco FROM catalogo WHERE produto = %s", (bebidas,))
                        resultado4 = self.backend.cursor.fetchone()  # Recuperar apenas o primeiro resultado (preço)
                        if resultado4:
                            preco4 = float(resultado4[0])
                            item_bebidas_preco= f"R$ {preco4:.2f}"
                            item_selecionado = f"        {bebidas}"
                            self.lista_vendas.insert("", "end", values=(item_selecionado,item_bebidas_preco))
                else:
                    messagebox.showerror(title="Selecione os itens", message="Selecione alguma pizza ou bebida")

                total = calcular_total()
                    
                selecionartipo.set('')
                self.selecionarsabor.set('')
                radio_var.set(0)
                self.selecionarborda.set('')
                self.selecionaradd.set('')
                self.selecionarbebida.set('')              
                #self.itens_selecionados.append(item_selecionado)
            def calcular_total():
                total = 0
                for item_id in self.lista_vendas.get_children():
                    preco_str = self.lista_vendas.item(item_id, "values")[1]
                    preco = float(preco_str.replace("R$", "").replace(",", "."))
                    total += preco
                    total_final=f"Total: R$ {total:.2f}"
                    self.total_lista_itens = ctk.CTkLabel(self.root, text=total_final, text_color="white",font=('Times New Roman', 35))
                    self.total_lista_itens.place(relx=0.09, rely=0.7, relwidth=0.31, relheight=0.1)

    # Agora você tem o total da coluna "preco"
                return total    
            def vender():
                print("vendido")
                informacoes_combinadas = [] 
                agora = datetime.now()
                for item in self.lista_vendas.get_children():
                    values = self.lista_vendas.item(item, "values")
                    nome_produto = values[0].strip()
                    informacoes_combinadas.append(nome_produto.replace(' ', '_'))

                informacao_combinada = '_'.join(informacoes_combinadas)

                if "inteira" in informacao_combinada or "meio" in informacao_combinada:
                    informacao_combinada = f"_{informacao_combinada}"

                
                total = calcular_total()
                total_final = f" {total:.2f}"
                
                self.backend.conecta_db()
                sql = "INSERT INTO vendas (datavenda,valor, vendido) VALUES (%s,%s, %s)"
                self.backend.cursor.execute(sql, (agora, total_final,informacao_combinada))
                # Commit das alterações no banco de dados
                self.backend.conn.commit()
                # Fechar a conexão com o banco de dados
                self.backend.conn.close()
                messagebox.showinfo(title="Vendido", message="Venda realizada com Sucesso!")
                menu()
            def excluir_venda():
                item_para_excluir = self.lista_vendas.selection()
                if item_para_excluir:
        # Remover o item do Treeview
                    self.lista_vendas.delete(item_para_excluir) 
                    for item in self.lista_vendas.get_children():
                        values = self.lista_vendas.item(item, "values")
                        print(values)
                    total = calcular_total()
                    total_final = f"Total: R$ {total:.2f}"
                    
                    if total == 0:
                        self.total_lista_itens = ctk.CTkLabel(self.root, text=total_final, text_color="white",font=('Times New Roman', 35))
                        self.total_lista_itens.place(relx=0.09, rely=0.7, relwidth=0.31, relheight=0.1)
                    
                
            self.titulo_lista_itens_label = ctk.CTkLabel(self.lista_frame_4, text="Vendas", text_color="white",font=('Times New Roman', 28))
            self.titulo_lista_itens_label.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.1)    
            self.excluir = ctk.CTkButton(self.lista_frame_4, text='Excluir', fg_color='#FF1616', text_color='White',font=("Times New Roman",16),command=excluir_venda)
            self.excluir.place(relx=0.88, rely=0.5, relwidth=0.11, relheight=0.07)
            self.vender = ctk.CTkButton(self.lista_frame_4, text='Vender', fg_color='green', text_color='White',font=("Times New Roman",16),command=vender)
            self.vender.place(relx=0.88, rely=0.7, relwidth=0.11, relheight=0.07)
            """escolher o tamanho da pizza"""
            self.backend = BackEnd()
            self.backend.conecta_db()
            self.backend.cursor.execute("SELECT produto FROM catalogo WHERE produto LIKE '%pizza%' OR produto LIKE '%Pizza%'")
            resultados = self.backend.cursor.fetchall()
            valores_de_pizza = tuple(resultado[0] for resultado in resultados)

            def selecionando_tipo(value):
                #values = ('',)
                if 'Doces' in value:
                    
                    self.backend = BackEnd()
                    self.backend.conecta_db()
                    self.backend.cursor.execute("SELECT sabor FROM doces")
                    resultados_doces = self.backend.cursor.fetchall()
                    values = tuple(resultado[0] for resultado in resultados_doces)
                elif 'Tradicional' in value:
                    
                    self.backend = BackEnd()
                    self.backend.conecta_db()
                    self.backend.cursor.execute("SELECT sabor FROM tradicional")
                    resultados_tradicionais = self.backend.cursor.fetchall()
                    values = tuple(resultado[0] for resultado in resultados_tradicionais)    
                elif 'Especiais' in value:
                    
                    self.backend = BackEnd()
                    self.backend.conecta_db()
                    self.backend.cursor.execute("SELECT sabor FROM especiais")
                    resultados_especiais = self.backend.cursor.fetchall()
                    values = tuple(resultado[0] for resultado in resultados_especiais)              
                else:
                    #values += valores_de_pizza[value]
                    values = ''
                self.selecionarsabor.configure(values=values)
                self.selecionarsabor.set('')
            self.nomepedido = ctk.CTkLabel(self.frame_4, text_color="black", text="Pizza:", font=('Times New Roman', 18))
            self.nomepedido.place(relx=0.01, rely=0.04, relwidth=0.15, relheight=0.07)
            var1 = ctk.StringVar()
            selecionartipo = ctk.CTkComboBox(self.frame_4, variable=var1, values=('',) + valores_de_pizza, text_color="black",fg_color='#e8e8e8',command=selecionando_tipo,font=('Times New Roman', 16))
            selecionartipo.place(relx=0.01, rely=0.1, relwidth=0.17, relheight=0.07)
            
            
            """escolher o sabor"""
            self.nomesabor=ctk.CTkLabel(self.frame_4,text_color="black", text=f"Sabor:",font=('Times New Roman', 18))
            self.nomesabor.place(relx=0.2, rely=0.04, relwidth=0.15, relheight=0.07)
            var2 = ctk.StringVar()
            self.selecionarsabor = ctk.CTkComboBox(self.frame_4,text_color="black",fg_color='#e8e8e8', variable=var2,font=('Times New Roman', 16))
            self.selecionarsabor.place(relx=0.2, rely=0.1, relwidth=0.17, relheight=0.07) 

            """escolher inteira ou meia"""
            self.nomevariedade=ctk.CTkLabel(self.frame_4,text_color="black", text=f"Variedade:",font=('Times New Roman', 18))
            self.nomevariedade.place(relx=0.38, rely=0.04, relwidth=0.1, relheight=0.07)
            radio_var = ctk.IntVar(value=0)
            r_1 = ctk.CTkRadioButton(self.frame_4, text="meia", text_color='black', variable= radio_var, value=1)
            r_2 = ctk.CTkRadioButton(self.frame_4, text="inteira",text_color='black', variable= radio_var, value=2)
            r_1.place(relx=0.38, rely=0.1, relwidth=0.05, relheight=0.07)
            r_2.place(relx=0.43, rely=0.1, relwidth=0.07, relheight=0.07)       
            
            """acresentar borda"""
            self.nomeborda=ctk.CTkLabel(self.frame_4,text_color="black", text=f"Borda:",font=('Times New Roman', 18))
            self.nomeborda.place(relx=0.5, rely=0.04, relwidth=0.15, relheight=0.07)
            self.backend = BackEnd()
            self.backend.conecta_db()
            self.backend.cursor.execute("SELECT produto FROM catalogo WHERE produto LIKE '%borda%' OR produto LIKE '%Borda%'")
            resultados = self.backend.cursor.fetchall()
            valores_de_borda = tuple(resultado[0] for resultado in resultados)
            self.selecionarborda = ctk.CTkComboBox(self.frame_4,text_color="black",fg_color='#e8e8e8', values=valores_de_borda,font=('Times New Roman', 16),state='readonly')
            self.selecionarborda.place(relx=0.5, rely=0.1, relwidth=0.17, relheight=0.07)
            
            """acrescentar adicionais"""
            self.nomeadd=ctk.CTkLabel(self.frame_4,text_color="black", text=f"Adicionais:",font=('Times New Roman', 18))
            self.nomeadd.place(relx=0.7, rely=0.04, relwidth=0.15, relheight=0.07)
            self.backend = BackEnd()
            self.backend.conecta_db()
            self.backend.cursor.execute("SELECT produto FROM catalogo WHERE produto LIKE '%Adicionais%'")
            resultados_add = self.backend.cursor.fetchall()
            valores_de_add = tuple(resultado[0] for resultado in resultados_add)
            self.selecionaradd = ctk.CTkComboBox(self.frame_4,text_color="black",fg_color='#e8e8e8', values=valores_de_add,font=('Times New Roman', 16),state='readonly')
            self.selecionaradd.place(relx=0.7, rely=0.1, relwidth=0.17, relheight=0.07)
            self.adicionar_carrinho = ctk.CTkButton(self.frame_4, text='+', fg_color='#FF1616', text_color='White',font=("Times New Roman",22),command=adicionar)
            self.adicionar_carrinho.place(relx=0.89, rely=0.1, relwidth=0.07, relheight=0.07)
            
            """comprar bebida"""
            self.nomebebida=ctk.CTkLabel(self.frame_4,text_color="black", text=f"Bebida:",font=('Times New Roman', 18))
            self.nomebebida.place(relx=0.01, rely=0.22, relwidth=0.15, relheight=0.07)
            self.backend = BackEnd()
            self.backend.conecta_db()
            self.backend.cursor.execute("SELECT produto FROM catalogo WHERE produto NOT LIKE '%pizza%' AND produto NOT LIKE '%Pizza%' AND produto NOT LIKE '%borda%' AND produto NOT LIKE '%Borda%' AND produto NOT LIKE '%Adicionais%'")
            resultados_bebidas = self.backend.cursor.fetchall()
            valores_de_bebidas = tuple(resultado[0] for resultado in resultados_bebidas)
            self.selecionarbebida = ctk.CTkComboBox(self.frame_4,text_color="black",fg_color='#e8e8e8', values=valores_de_bebidas,font=('Times New Roman', 16),state='readonly')
            self.selecionarbebida.place(relx=0.01, rely=0.29, relwidth=0.25, relheight=0.07)
            self.adicionar_bebida_carrinho = ctk.CTkButton(self.frame_4, text='+', fg_color='#FF1616', text_color='White',font=("Times New Roman",22),command=adicionar)
            self.adicionar_bebida_carrinho.place(relx=0.27, rely=0.29, relwidth=0.07, relheight=0.07)
        

            

        def notas():
            self.frame_4.pack_forget()
            self.frame_6 = ctk.CTkFrame(self.root,fg_color='white')
            #self.frame_6.configure(background='red')
            self.frame_6.place(relx=0.09, rely=0.2, relwidth=0.875, relheight=0.75)
            Emitirnotas=ctk.CTkLabel(self.frame_1,text=f"Emitir Notas Fiscais",font=('Arial', 38))
            Emitirnotas.place(relx=0.20, rely=0.10, relwidth=0.55, relheight=1)    


        def historico():
            self.canvas = ctk.CTkCanvas(self.root)
            scrollable_frame = ctk.CTkFrame(self.canvas)
            scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            self.canvas.place(relx=0.09, rely=0.2, relwidth=0.875, relheight=0.75)  # Manter o place para a tabela

            header = ["Ações", "id", "data", "valor", "Vendido","Emitir"]
            

            for x, y in enumerate(header):
                entry = ctk.CTkEntry(scrollable_frame, justify='center')
                entry.insert(0, y)
                entry.configure(state='readonly')
                if y.lower() == 'phone number':
                    entry.grid(row=0, column=x, ipadx=100, pady=5)
                else:
                    entry.grid(row=0, column=x, pady=5)

            for x in range(13):
                entry = ctk.CTkEntry(scrollable_frame, justify='center')
                entry2 = ctk.CTkEntry(scrollable_frame, justify='center')
                entry.insert(0, x)
                entry2.insert(x, 0)
                entry.configure(state='readonly')
                entry2.configure(state='readonly')
                entry.grid(row=x + 3, column=0, ipadx=3, pady=0)
                entry2.grid(row=x + 3, column=5, ipadx=3, pady=0)
                button = ctk.CTkButton(scrollable_frame, text='Apagar', fg_color='red')
                button.grid(row=x + 3, column=0, pady=0)
                button2 = ctk.CTkButton(scrollable_frame, text='Emitir Notas', fg_color='green')
                button2.grid(row=x + 3, column=5, pady=0)
        
        btn_art1 = ctk.CTkButton(self.frame_2, text='Menu', fg_color='#FF1616', text_color='White',font=('Arial', 14),command=menu)
        btn_art1.place(relx=0, rely=0, relwidth=1, relheight=0.08)
        btn_art6 = ctk.CTkButton(self.frame_2, text='Cardápio', fg_color='#FF1616', text_color='White',font=('Arial', 14), command=cardapio)
        btn_art6.place(relx=0, rely=0.085, relwidth=1, relheight=0.08)
        btn_art59 = ctk.CTkButton(self.frame_2, text='Notas', fg_color='#FF1616', text_color='White',font=('Arial', 14),command=notas)
        btn_art59.place(relx=0, rely=0.17, relwidth=1, relheight=0.08)
        btn_art2 = ctk.CTkButton(self.frame_2, text='Vendas', fg_color='#FF1616', text_color='White',font=('Arial', 14))
        btn_art2.place(relx=0, rely=0.255, relwidth=1, relheight=0.08)
        btn_historico = ctk.CTkButton(self.frame_2, text='Historico', fg_color='#FF1616', text_color='White',font=('Arial', 14),command=historico)
        btn_historico.place(relx=0, rely=0.34, relwidth=1, relheight=0.08)

        menu()
        
            # btn_art2 = ctk.CTkButton(self.frame_2, text='Art 2º', fg_color='#01509b', text_color='White',font=('Arial', 14))
            # btn_art2.place(relx=0, rely=0.32, relwidth=1, relheight=0.08)
    def update_time(self):
            current_time = datetime.now().strftime("%H:%M")
            self.lbl.config(text=current_time)
            self.lbl.after(60000, self.update_time)  # Update every minute (60000 milliseconds)
            lbl = ctk.CTkLabel(self.frame_1,text=f"{datetime.now(): %H:%M}",font=('Arial', 45))
            lbl.place(relx=0.80, rely=0.10, relwidth=0.15, relheight=1)



        

App()
root.mainloop()