import tkinter as tk
from tkinter import PhotoImage, messagebox
class Interface:
    
    def __init__(self):
        self.window = tk.Tk()  # Inicializando a janela principal

        self.window.title("GERADOR DE PROJETOS")
        self.window.geometry("1080x720")
        self.window.configure(bg="#ECF0F1")

        self.fonte_grande = ("Arial", 20, "bold")
        self.fonte_pequena = ("Arial", 12)
        self.fonte_botao = ("Arial", 12, "bold")
        #ira amarzenar dados dos itens 
        self.modelos_cftv = {}
        self.modelos_cda = {}
        # Frames de controle
        

        self.cda_frame = tk.Frame(self.window, bg="#ECF0F1")
        self.cda_frame.pack(fill=tk.X)
        self.cda_visivel = False

        self.cftv_frame = tk.Frame(self.window, bg="#ECF0F1")
        self.cftv_frame.pack(fill=tk.X)
        self.cftv_visivel = False

        # Variáveis de controle
        self.tipo_cda_visivel = False
        self.tipo_cda_botao = None
        self.botao_pedestre = None
        self.botao_Veicular = None

     # Iniciando o loop principal da interface

        # Cabeçalho
        self.header_frame = tk.Frame(self.window, bg="#2C3E50", pady=1)
        self.header_frame.pack(fill=tk.X)

        #self.logo_path = r"C:\Users\PreVenda ProtekSeg\Desktop\PROJETO-SISTEMA\logo-1.png"  # Atualize o caminho da logomarca
        #try:
            #self.logo_image = PhotoImage(file=self.logo_path)
            #self.logo_label = tk.Label(self.header_frame, image=self.logo_image, bg="#2C3E50")
            #self.logo_label.pack(pady=1)
        #except Exception as e:
            #print(f"Erro ao carregar a logomarca: {e}")

        self.header_label = tk.Label(
            self.header_frame, text="GERADOR DE PROJETOS", font=self.fonte_grande, fg="white", bg="#2C3E50"
        )
        self.header_label.pack()

        # Campo de entrada para o nome da empresa
        self.nome_label, self.nome_entry = self.criar_campo_cliente("Nome da Empresa:")

        # Seção para Diagramas de Projetos
        self.produtos_frame = tk.Frame(self.window, bg="#ECF0F1", pady=20)
        self.produtos_frame.pack(fill=tk.X)

        tk.Label(
            self.produtos_frame, text="DIAGRAMAS DE PROJETOS", font=self.fonte_grande, fg="#34495E", bg="#ECF0F1"
        ).pack(pady=10)

        # Botões modernos com bordas
        self.cda_botao = tk.Button(
            self.produtos_frame, text="Controle de Acesso", command=self.toggle_lista_cda,
            font=self.fonte_botao, fg="white", bg="#27AE60", relief="solid", bd=3,
            highlightthickness=2, highlightbackground="#2C3E50", width=38
        )
        self.cda_botao.place(x=700, y=50)

        self.Cftv_botao = tk.Button(
          self.produtos_frame, text="CFTV", command=self.toggle_lista_cftv,
          font=self.fonte_botao, fg="white", bg="#27AE69", relief="solid", bd=3,
          highlightthickness=2, highlightbackground="#2C3E50", width=38


        )
        self.Cftv_botao.place(x=270, y=50)  # Ajuste a posição para não sobrepor

        self.consulta_botao = tk.Button(
            self.produtos_frame, text="Consulta", command=self.toggle_lista_tipos_cda,
            font=self.fonte_botao, fg="white", bg="#E74C3C", relief="solid", bd=2,
            highlightthickness=2, highlightbackground="#2C3E50", height=5, width=10
        )
        self.consulta_botao.place(x=60, y=0)

        # Rodapé com mensagem
        self.footer_frame = tk.Frame(self.window, bg="#ECF0F1")
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        self.footer_label = tk.Label(
            self.footer_frame, text="Create by Reis~ Beta 5.5", font=("Arial", 10, "bold"),
            fg="#95A5A6", bg="#ECF0F1", anchor="e"
        )
        self.footer_label.pack(side=tk.RIGHT, padx=20)

    def criar_campo_cliente(self, label_text):
        label = tk.Label(self.window, text=label_text, font=self.fonte_grande, bg="#ECF0F1", fg="#2C3E50")
        label.pack(pady=5)
        entry = tk.Entry(self.window, font=self.fonte_pequena, bg="#FFFFFF", fg="#2C3E50", bd=2, relief="solid", width=40)
        entry.pack(pady=10)
        return label, entry

    def toggle_lista_cda(self):
        if self.cftv_visivel:
        # Esconde todos os widgets da lista de CFTV
            for widget in self.cftv_frame.winfo_children():
                widget.destroy()
            self.quantidades_cftv.clear()  # Limpar dicionário CFTV
            self.cftv_visivel = False

        if self.cda_visivel:
           for widget in self.cda_frame.winfo_children():
               widget.destroy()
           self.quantidades_cda.clear()  # Limpar dicionário CDA
           self.cda_visivel = False
        else:
        # Exibe a lista de itens de CDA
           self.mostrar_lista_cda()
           self.cda_visivel = True


    def mostrar_lista_cda(self):
        for widget in self.cda_frame.winfo_children():
            widget.destroy()

    # Obtém a posição do botão "Controle de Acesso"
        x, y = self.cda_botao.winfo_x(), self.cda_botao.winfo_y() + self.cda_botao.winfo_height()
    
    # Coloca o frame na posição correta
        self.cda_frame.place(x=690, y=230)

        container = tk.Frame(self.cda_frame, bg="#ECF0F1")
        container.pack(pady=1, anchor="center")

        tk.Label(
            container, text="Itens de Controle de Acesso:", font=self.fonte_grande, bg="#ECF0F1", fg="#2C3E50"
        ).pack(pady=5)

        self.checkboxes_cda = {}
        self.quantidades_cda = {}
        itens_cda = ["Leitor Facial", "Catraca", "Eletroímã", "Fonte", "Fonte com bateria", "Fechadura" , "Botoeira", "Controladora"]

        for item in itens_cda:
            frame_item = tk.Frame(container, bg="#ECF0F1")
            frame_item.pack(anchor="w", pady=1, fill=tk.X)

            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(
                frame_item, text=item, variable=var, font=self.fonte_pequena,
                bg="#ECF0F1", fg="#2C3E50", anchor="w", selectcolor="#16A085"
        )
            checkbox.pack(side=tk.LEFT, padx=5)
            self.checkboxes_cda[item] = var

        # Spinbox para quantidade
            spinbox = tk.Spinbox(
                frame_item, from_=0, to=100, font=self.fonte_pequena, width=5,
                justify="center", bg="#FFFFFF", fg="#2C3E50", bd=1, relief="solid"
        )
            spinbox.pack(side=tk.RIGHT, padx=5)
            self.quantidades_cda[item] = spinbox

        # Dropdown para selecionar modelos (somente para itens específicos)
            if item == "Leitor Facial":
               modelos = ["DS-K1T341", "DS-K1T343", "DS-K1T671", "DS-K1T673"]
               var_modelo = tk.StringVar()
               var_modelo.set("Selecione um modelo")
               dropdown = tk.OptionMenu(
                   frame_item, var_modelo, *modelos
            )
               dropdown.config(font=self.fonte_pequena, bg="#6c6e71", fg="#d71820")
               dropdown.pack(side=tk.RIGHT, padx=5)
               self.modelos_cda[item] = var_modelo

            elif item == "Catraca":
                modelos = ["Catraca X", "Catraca Y", "Catraca Z"]
                var_modelo = tk.StringVar()
                var_modelo.set("Selecione um modelo")
                dropdown = tk.OptionMenu(
                    frame_item, var_modelo, *modelos
            )
                dropdown.config(font=self.fonte_pequena, bg="#FFFFFF", fg="#2C3E50")
                dropdown.pack(side=tk.RIGHT, padx=5)
                self.modelos_cda[item] = var_modelo

            elif item == "Eletroímã":
                modelos = ["FE 20150", "DS-K4H258", "Eletroímã C"]
                var_modelo = tk.StringVar()
                var_modelo.set("Selecione um modelo")
                dropdown = tk.OptionMenu(
                    frame_item, var_modelo, *modelos
            )
                dropdown.config(font=self.fonte_pequena, bg="#FFFFFF", fg="#2C3E50")
                dropdown.pack(side=tk.RIGHT, padx=5)
                self.modelos_cda[item] = var_modelo

            elif item == "Fonte":
                modelos = ["Fonte 12V", "Fonte 24V", "Fonte 5V"]
                var_modelo = tk.StringVar()
                var_modelo.set("Selecione um modelo")
                dropdown = tk.OptionMenu(
                    frame_item, var_modelo, *modelos
            )
                dropdown.config(font=self.fonte_pequena, bg="#FFFFFF", fg="#2C3E50")
                dropdown.pack(side=tk.RIGHT, padx=5)
                self.modelos_cda[item] = var_modelo

            elif item == "Fonte com bateria":
                modelos = ["Fonte 12V", "Fonte 24V", "Fonte 5V"]
                var_modelo = tk.StringVar()
                var_modelo.set("Selecione um modelo")
                dropdown = tk.OptionMenu(
                    frame_item, var_modelo, *modelos
            )
                dropdown.config(font=self.fonte_pequena, bg="#FFFFFF", fg="#2C3E50")
                dropdown.pack(side=tk.RIGHT, padx=5)
                self.modelos_cda[item] = var_modelo

            elif item == "Fechadura":
                modelos = ["Fail Safe P/ Vidro Fs 3010 V ", " Fail Safe Porta Vidro Fs 2010"]
                var_modelo = tk.StringVar()
                var_modelo.set("Selecione um modelo")
                dropdown = tk.OptionMenu(
                    frame_item, var_modelo, *modelos
            )
                dropdown.config(font=self.fonte_pequena, bg="#FFFFFF", fg="#2C3E50")
                dropdown.pack(side=tk.RIGHT, padx=5)
                self.modelos_cda[item] = var_modelo

            elif item == "Botoeira":
                modelos = ["DS-K7P02", "BT-3000 IN", "BT-INOX AGL"]

                var_modelo = tk.StringVar()
                var_modelo.set("Selecione um modelo")
                dropdown = tk.OptionMenu(
                    frame_item, var_modelo, *modelos
            )
                dropdown.config(font=self.fonte_pequena, bg="#FFFFFF", fg="#2C3E50")
                dropdown.pack(side=tk.RIGHT, padx=5)
                self.modelos_cda[item] = var_modelo
            elif item == "Controladora":
                modelos = ["DS-K2602T", "IDBOX", "CT 3000 2PB"]
                var_modelo = tk.StringVar()
                var_modelo.set("Selecione um modelo")
                dropdown = tk.OptionMenu(
                    frame_item, var_modelo, *modelos
            )
                dropdown.config(font=self.fonte_pequena, bg="#FFFFFF", fg="#2C3E50")
                dropdown.pack(side=tk.RIGHT, padx=5)
                self.modelos_cda[item] = var_modelo
        tk.Button(
            container, text="Confirmar CDA", command=self.confirmar_conclusao_cda,
            font=self.fonte_pequena, fg="white", bg="#2980B9", relief="solid", bd=2, width=20
        ).pack(pady=5)


    def toggle_lista_cftv(self):
        
       if self.cda_visivel:
        # Esconde todos os widgets da lista de CDA
           for widget in self.cda_frame.winfo_children():
               widget.destroy()
           self.quantidades_cda.clear()  # Limpar dicionário CDA
           self.cda_visivel = False

       if self.cftv_visivel:
           for widget in self.cftv_frame.winfo_children():
               widget.destroy()
           self.quantidades_cftv.clear()  # Limpar dicionário CFTV
           self.cftv_visivel = False
       else:
        # Exibe a lista de itens de CFTV
           self.mostrar_lista_cftv()
           self.cftv_visivel = True


    def mostrar_lista_cftv(self):
       for widget in self.cftv_frame.winfo_children():
           widget.destroy()

    # Obtém a posição do botão "CFTV"
       x, y = self.Cftv_botao.winfo_x(), self.Cftv_botao.winfo_y() + self.Cftv_botao.winfo_height()

    # Coloca o frame na posição correta
       self.cftv_frame.place(x=270, y=230)

       container = tk.Frame(self.cftv_frame, bg="#ECF0F1")
       container.pack(pady=10, anchor="center")

       tk.Label(
       container, text="Itens de CFTV:", font=self.fonte_grande, bg="#ECF0F1", fg="#2C3E50"
       ).pack(pady=5)

       self.checkboxes_cftv = {}
       self.quantidades_cftv = {}
       itens_cftv = ["Câmera","Camera LPR", "NVR", "DVR","HDD", "Switch PoE"]

       for item in itens_cftv:
           frame_item = tk.Frame(container, bg="#ECF0F1")
           frame_item.pack(anchor="w", pady=5, fill=tk.X)

           var = tk.BooleanVar()
           checkbox = tk.Checkbutton(
           frame_item, text=item, variable=var, font=self.fonte_pequena,
           bg="#ECF0F1", fg="#2C3E50", anchor="w", selectcolor="#16A085"
        )
           checkbox.pack(side=tk.LEFT, padx=5)
           self.checkboxes_cftv[item] = var

        # Spinbox para quantidade
           spinbox = tk.Spinbox(
               frame_item, from_=0, to=100, font=self.fonte_pequena, width=5,
               justify="center", bg="#FFFFFF", fg="#2C3E50", bd=1, relief="solid"
        )
           spinbox.pack(side=tk.RIGHT, padx=5)
           self.quantidades_cftv[item] = spinbox

        # Dropdown para selecionar modelos
           if item == "Câmera":
              modelos = ["DS-2CD2047G2-LU", "DS-2CD1143G0-I", "DS-2CD1023G0E"]

           elif item == "Camera LPR":
              modelos = ["DS-2CD7A26G0/P-IZHS", "DS-2CD4A26FWD-IZHS/P", "iDS-2CD7A46G0/P-IZHSY", 
               "VIP 7280 LPR", "VIP 7230 LPR", "VIP 7225 LPR G2"]

           elif item == "NVR":
                modelos = ["DS-7608NI-K1", "DS-7616NI-K2", "DS-7732NI-K4"]
           elif item == "DVR":
                modelos = ["DS-7104HGHI-K1", "DS-7208HUHI-K2", "DS-7216HUHI-K4"]

           elif item == "HDD":
                modelos = ["1TB", "2TB", "3TB","4TB"]
           elif item == "Switch PoE":
                modelos = ["DS-3E0105P-E", "DS-3E0310P-E", "DS-3E0526P-E"]
           else:
              modelos = []

           if modelos:
              var_modelo = tk.StringVar()
              var_modelo.set("Selecione um modelo")
              dropdown = tk.OptionMenu(
                 frame_item, var_modelo, *modelos
            )
              dropdown.config(font=self.fonte_pequena, bg="#FFFFFF", fg="#2C3E50")
              dropdown.pack(side=tk.RIGHT, padx=5)
              self.modelos_cftv[item] = var_modelo
       btn_confirmar_cftv = tk.Button(
        container, text="Confirmar cftv", command=self.confirmar_conclusao_cftv,
        font=self.fonte_pequena, fg="white", bg="#2980B9", relief="solid", bd=2, width=20
        )
       btn_confirmar_cftv.pack(pady=5)
 
    def toggle_lista_tipos_cda(self):
        self.cda_frame.pack(side="top", padx=100, pady=5)

    # Verifica se a lista de tipos de CDA está visível
        if self.tipo_cda_visivel:
        # Se já estiver visível, remove os widgets e define a variável de controle como False
            if hasattr(self, "botao_pedestre"):
                self.botao_pedestre.pack_forget()
            if hasattr(self, "botao_Veicular"):
                self.botao_Veicular.pack_forget()
            if hasattr(self, "tipo_cda_botao"):
                self.tipo_cda_botao.pack_forget()
            if hasattr(self, "frame_porta"):
               self.frame_porta.destroy()
            if hasattr(self, "frame_pedestre"):
               self.frame_pedestre.destroy()
            if hasattr(self, "frame_veicular"):
               self.frame_veicular.destroy()

            self.tipo_cda_visivel = False
        else:
        # Cria frames para organizar os botões
            self.frame_porta = tk.Frame(self.cda_frame)
            self.frame_porta.pack(side="right", fill="x", padx=180, pady=5)

            self.frame_pedestre = tk.Frame(self.cda_frame)
            self.frame_pedestre.pack(side="right", fill="x", padx=182, pady=5)

            self.frame_veicular = tk.Frame(self.cda_frame)
            self.frame_veicular.pack(side="right", fill="x", padx=135, pady=5)

        # Botão Porta
            self.tipo_cda_botao = tk.Button(
                self.cda_frame,
                text="Porta",
                command=self.mostrar_menu_porta,  # Chamando diretamente a função
                font=self.fonte_botao,
                fg="white",
                bg="#3fb79f",
                relief="solid",
                bd=2,
                highlightthickness=2,
                highlightbackground="#2C3E50",
                width=20
        )
            self.tipo_cda_botao.pack(side="top", padx=1, pady=5)

        # Botões específicos para Pedestre e Veicular
            self.botao_pedestre = tk.Button(
                 self.cda_frame,
                 text="Pedestre",
                 command=self.mostrar_menu_pedestre,
                 font=self.fonte_botao,
                 fg="white",
                 bg="#cb84d2",
                 relief="solid",
                 bd=2,
                 highlightthickness=2,
                 highlightbackground="#2C3E50",
                 width=20
        )
            self.botao_pedestre.pack(side="top", padx=1, pady=5)

            self.botao_Veicular = tk.Button(
                self.cda_frame,
                text="Veicular",
                command=self.mostrar_menu_Veicular,
                font=self.fonte_botao,
                fg="white",
                bg="#ed9e4e",
                relief="solid",
                bd=2,
                highlightthickness=2,
                highlightbackground="#2C3E50",
                width=20
        )
            self.botao_Veicular.pack(side="top", padx=1, pady=5)

        # Torna os elementos visíveis
            self.tipo_cda_visivel = True

    def mostrar_menu_porta(self):
        menu_porta = tk.Menu(self.window, tearoff=0)
        menu_porta.add_command(label="Vidro/Vidro", command=self.mostrar_popup_vidro_vidro)
        menu_porta.add_command(label="Vidro/Parede", command=self.mostrar_popup_vidro_parede)
        menu_porta.add_command(label="Porta Comum", command=self.mostrar_popup_porta_comum)
        menu_porta.post(
            self.tipo_cda_botao.winfo_rootx(),
            self.tipo_cda_botao.winfo_rooty() + self.tipo_cda_botao.winfo_height())

    def mostrar_popup_vidro_vidro(self):
        mensagem = (
            "##################################\n"
            "   PORTA VIDRO/VIDRO \n"
            "##################################\n\n"
            "• Fechadura fail safe vidro/vidro fs 3010 V intelbras\n\n"
            "• Fechadura Elétrica Para Porta De Vidro Agl - Modelo Pvr1i\n\n"
            "• Fonte De Alimentação 12v 5a C/ Função Nobreak Power 512 Plus com bateria\n\n"
            "• Botoeira inox"
        )
        messagebox.showinfo("Informações da Porta Vidro/vidro", mensagem)

    def mostrar_popup_vidro_parede(self):
        mensagem = (
            "##################################\n"
            "   PORTA VIDRO/PAREDE \n"
            "##################################\n\n"
            "• Fechadura AGL fail safe para vidro e porta a parede\n\n"
            "• Fonte com bateria nobreak\n\n"
            "• Conectores"
        )
        messagebox.showinfo("Informações da Porta Vidro/parede", mensagem)

    def mostrar_popup_porta_comum(self):
        mensagem = (
            "##################################\n"
            "   PORTA COMUM\n"
            "##################################\n\n"
            "• Eletroímã ou Fecho Magnético para portas convencionais\n\n"
            "• Fonte com bateria nobreak\n\n"
            "• Botoeira"
        )
        messagebox.showinfo("Informações da Porta Comum", mensagem)
    
    def acao_porta(self):
        
        self.mostrar_menu_porta()    


    def mostrar_menu_pedestre(self):
        menu_pedestre = tk.Menu(self.window, tearoff=0)
        menu_pedestre.add_command(label="Torniquete", command=self.mostrar_popup_Torniquete_pedestre)
        menu_pedestre.add_command(label="Catraca", command=self.mostrar_popup_Catraca_pedestre)
        menu_pedestre.post(self.botao_pedestre.winfo_rootx(), self.botao_pedestre.winfo_rooty() + self.botao_pedestre.winfo_height())
    def mostrar_popup_Torniquete_pedestre(self):
        mensagem = (
            "##################################\n"
            "   TORNIQUETE\n"
            "##################################\n\n"
            "• Torniquete verificar modelo.\n\n"
            "• Controlador de acesso compatível (Exemplo: Facial HIK).\n\n"
            "• Fonte colmeia.\n\n"
            "• Licença nwaypro."
        )
        messagebox.showinfo("Torniquete", mensagem)

    def mostrar_popup_Catraca_pedestre(self):
        mensagem = (
            "##################################\n"
            "       CATRACA\n"
            "##################################\n\n"
            "• Catraca/ virificar modelo.\n\n"
            "• Terminal Facial/ verificar modelo.\n\n"
            "• Suporte para facial."
        )
        messagebox.showinfo("Catraca", mensagem)


    def acao_pedestre(self):
        self.mostrar_menu_pedestre()

    def mostrar_menu_Veicular(self):
        menu_Veicular = tk.Menu(self.window, tearoff=0)
        menu_Veicular.add_command(label="Totem", command=self.mostrar_popup_Totem_Veicular)
        menu_Veicular.add_command(label="Lpr", command=self.mostrar_popup_Lpr_Veicular)
        menu_Veicular.add_command(label="Antena", command=self.mostrar_popup_Antena_Veicular)
        menu_Veicular.post(self.botao_Veicular.winfo_rootx(), self.botao_Veicular.winfo_rooty() + self.botao_Veicular.winfo_height())

    def mostrar_popup_Totem_Veicular(self):
        mensagem = (
           "##################################\n"
           "        TOTEM VEICULAR\n"
           "##################################\n\n"
           "• Totem de acesso veicular.\n\n"
           "• Controlador de acesso compatível (Exemplo: Facial HIK ou RFID).\n\n"
           "• Fonte colmeia 12V.\n\n"
           "• Licença nwaypro (se aplicável)."
        )
        messagebox.showinfo("Totem", mensagem)

    def mostrar_popup_Lpr_Veicular(self):
        mensagem = (
             "##################################\n"
             "       CÂMERAS LPR\n"
             "##################################\n\n"
             "• Câmeras LPR para leitura de placas.\n\n"
             "• NVR compatível com gravação.\n\n"
             "• Configuração de alcance (exemplo: 20 a 50 metros).\n\n"
             "• Licença nwaypro (se aplicável)."
        )
        messagebox.showinfo("Cameras Lpr", mensagem)

    def mostrar_popup_Antena_Veicular(self):
        mensagem = (
           "##################################\n"
           "       ANTENA VEICULAR\n"
           "##################################\n\n"
           "• Antena para identificação de veículos (UHF ou RFID).\n\n"
           "• Controlador de acesso compatível.\n\n"
           "• Tag para veículos.\n\n"
           "• Configuração de alcance da antena."
        )
        messagebox.showinfo("Antena", mensagem)

    def acao_Veicular(self):
        
        self.mostrar_menu_Veicular()    
    


    def confirmar_conclusao_cda(self):
        nome_empresa = self.nome_entry.get()  # Captura o nome da empresa
        if not nome_empresa:  # Verifica se o nome da empresa foi preenchido
            messagebox.showwarning("Atenção", "Por favor, preencha o nome da empresa antes de confirmar os itens.")
            return  # Sai da função se o nome não for preenchido

        selecionados = []
        for item, var in self.checkboxes_cda.items():
            if var.get():  # Verifica se o item foi selecionado
                quantidade = self.quantidades_cda.get(item, None)
                quantidade_valor = quantidade.get() if quantidade else "N/A"

                if item in self.modelos_cda:  # Verifica se o item tem modelo
                    modelo = self.modelos_cda[item].get()
                    selecionados.append(f"CDA: {item} - Modelo: {modelo} - Quantidade: {quantidade_valor}")
                else:
                    selecionados.append(f"CDA: {item} - Quantidade: {quantidade_valor}")

        if selecionados:  # Criação do arquivo se houver itens selecionados
            nome_arquivo = f"{nome_empresa}_CDA.txt"
            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write("Itens Selecionados (CDA):\n")
                arquivo.write("\n".join(selecionados))
            print(f"Arquivo '{nome_arquivo}' criado com sucesso.")

        # Único pop-up informando que o arquivo foi gerado
        messagebox.showinfo("Arquivo Gerado", "FOI GERADO UM ARQUIVO DE PROJETO")

    def confirmar_conclusao_cftv(self):
        nome_empresa = self.nome_entry.get()  # Captura o nome da empresa
        if not nome_empresa:  # Verifica se o nome da empresa foi preenchido
            messagebox.showwarning("Atenção", "Por favor, preencha o nome da empresa antes de confirmar os itens.")
            return  # Sai da função se o nome não for preenchido

        selecionados = []  # Lista para armazenar os itens selecionados
        for item, var in self.checkboxes_cftv.items():
            if var.get():  # Verifica se o checkbox foi marcado
                spinbox = self.quantidades_cftv[item]
                quantidade_valor = int(spinbox.get())  # Captura a quantidade como inteiro

                if quantidade_valor > 0:  # Só adiciona se a quantidade for maior que 0
                    modelo = self.modelos_cftv.get(item, tk.StringVar()).get()
                    if modelo and modelo != "Selecione um modelo":  # Verifica se um modelo válido foi escolhido
                        selecionados.append(f"CFTV: {item} - Modelo: {modelo} - Quantidade: {quantidade_valor}")
                    else:
                        selecionados.append(f"CFTV: {item} - Quantidade: {quantidade_valor}")

        if selecionados:  # Criação do arquivo se houver itens selecionados
            nome_arquivo = f"{nome_empresa}_CFTV.txt"
            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write("Itens Selecionados (CFTV):\n")
                arquivo.write("\n".join(selecionados))
            print(f"Arquivo '{nome_arquivo}' criado com sucesso.")

        # Único pop-up informando que o arquivo foi gerado
        messagebox.showinfo("Arquivo Gerado", "FOI GERADO UM ARQUIVO DE PROJETO")
    def iniciar(self):
        self.window.mainloop()

# Executar o programa
if __name__ == "__main__":
    root = tk.Tk
    app = Interface()
    app.iniciar()