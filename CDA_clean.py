import tkinter as tk
from tkinter import PhotoImage, messagebox, scrolledtext, TclError
import os
import json
import logging
from tkinter import ttk

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Interface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gerador de Projetos")
        self.window.geometry("1080x720")
        self.window.configure(bg="#F5F6F5")
        self.window.resizable(True, True)  # Janela redimensionável

        # Definindo caminhos base
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.logo_dir = os.path.join(self.base_dir, "PROJETO-SISTEMA", "produtos_logos")
        if not os.path.exists(self.logo_dir):
            os.makedirs(self.logo_dir, exist_ok=True)
            logging.warning(f"Diretório de logotipos criado: {self.logo_dir}")

        # Carregar configuração
        try:
            with open(os.path.join(self.base_dir, "config.json"), "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            logging.error("Arquivo config.json não encontrado.")
            messagebox.showerror("Erro", "Arquivo de configuração (config.json) não encontrado.")
            self.window.destroy()
            return

        # Dicionário de strings para internacionalização
        self.strings = {
            "pt": {
                "title": "Gerador de Projetos",
                "menu": "Menu",
                "consultation": "Consulta",
                "cctv": "CFTV",
                "access_control": "Controle de Acesso",
                "chatbot": "Chatbot",
                "company_name": "Nome da Empresa:",
                "enter_company_name": "Digite o nome da empresa",
                "footer": "Created by Reis ~ Beta 6.6",
                "confirm_cctv": "Confirmar CFTV",
                "confirm_access_control": "Confirmar Controle de Acesso",
                "select_model": "Selecione um modelo",
                "no_logo": "Logotipo não encontrado",
                "file_generated": "FOI GERADO UM ARQUIVO DE PROJETO",
                "warning_company_name": "Por favor, preencha o nome da empresa antes de confirmar os itens.",
                "invalid_quantity": "Quantidade inválida para {item}.",
                "no_model_selected": "Por favor, selecione um modelo para {item}.",
            }
        }
        self.lang = "pt"

        # Fontes
        self.fonte_titulo = ("Arial", 24, "bold")
        self.fonte_label = ("Arial", 14, "bold")
        self.fonte_pequena = ("Arial", 12)
        self.fonte_botao = ("Arial", 12, "bold")
        self.fonte_rodape = ("Arial", 10, "italic")

        # Dicionários para armazenar dados
        self.modelos_cctv = {}
        self.modelos_controle_acesso = {}
        self.checkboxes_controle_acesso = {}
        self.quantidades_controle_acesso = {}
        self.checkboxes_cctv = {}
        self.quantidades_cctv = {}

        # Variáveis de controle
        self.controle_acesso_visivel = False
        self.cctv_visivel = False
        self.chatbot_visivel = False
        self.consulta_visivel = False
        self.consulta_container = None

        # Layout Principal
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        # Sidebar
        self.sidebar_frame = tk.Frame(self.window, bg="#2B2D42", width=200)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")

        tk.Label(
            self.sidebar_frame, text=self.strings[self.lang]["menu"],
            font=self.fonte_label, fg="white", bg="#2B2D42", pady=20
        ).pack(anchor="n")

        self.consulta_botao = tk.Button(
            self.sidebar_frame, text=self.strings[self.lang]["consultation"],
            command=self.toggle_consulta, font=self.fonte_botao, fg="white",
            bg="#8D99AE", relief="flat", width=15, height=2
        )
        self.consulta_botao.pack(pady=10)

        self.cctv_botao = tk.Button(
            self.sidebar_frame, text=self.strings[self.lang]["cctv"],
            command=self.toggle_lista_cctv, font=self.fonte_botao, fg="white",
            bg="#8D99AE", relief="flat", width=15, height=2
        )
        self.cctv_botao.pack(pady=10)

        self.controle_acesso_botao = tk.Button(
            self.sidebar_frame, text=self.strings[self.lang]["access_control"],
            command=self.toggle_lista_controle_acesso, font=self.fonte_botao, fg="white",
            bg="#8D99AE", relief="flat", width=15, height=2
        )
        self.controle_acesso_botao.pack(pady=10)

        self.chatbot_botao = tk.Button(
            self.sidebar_frame, text=self.strings[self.lang]["chatbot"],
            command=self.toggle_lista_chatbot, font=self.fonte_botao, fg="white",
            bg="#8D99AE", relief="flat", width=15, height=2
        )
        self.chatbot_botao.pack(pady=10)

        # Área Principal
        self.main_frame = tk.Frame(self.window, bg="#F5F6F5")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.header_frame = tk.Frame(self.main_frame, bg="#F5F6F5")
        self.header_frame.grid(row=0, column=0, sticky="ew")

        tk.Label(
            self.header_frame, text=self.strings[self.lang]["title"],
            font=self.fonte_titulo, fg="#2B2D42", bg="#F5F6F5"
        ).pack(anchor="w", pady=10)

        self.nome_label, self.nome_entry = self.criar_campo_cliente(self.strings[self.lang]["company_name"])

        self.content_frame = tk.Frame(self.main_frame, bg="#F5F6F5")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.controle_acesso_frame = tk.Frame(self.content_frame, bg="#F5F6F5")
        self.cctv_frame = tk.Frame(self.content_frame, bg="#F5F6F5")
        self.chatbot_frame = tk.Frame(self.content_frame, bg="#F5F6F5")

        self.footer_frame = tk.Frame(self.main_frame, bg="#F5F6F5")
        self.footer_frame.grid(row=2, column=0, sticky="ew")

        tk.Label(
            self.footer_frame, text=self.strings[self.lang]["footer"],
            font=self.fonte_rodape, fg="#8D99AE", bg="#F5F6F5", anchor="e"
        ).pack(side=tk.RIGHT, padx=20)

        self.chatbot_text = None
        self.chatbot_buttons_frame = None

    def criar_campo_cliente(self, label_text):
        frame = tk.Frame(self.main_frame, bg="#F5F6F5")
        frame.grid(sticky="ew", pady=10)

        label = tk.Label(frame, text=label_text, font=self.fonte_label, bg="#F5F6F5", fg="#2B2D42")
        label.pack(anchor="w")

        entry = tk.Entry(frame, font=self.fonte_pequena, bg="#FFFFFF", fg="#2B2D42", bd=1, relief="solid", width=50)
        entry.insert(0, self.strings[self.lang]["enter_company_name"])
        entry.bind("<FocusIn>", lambda event: entry.delete(0, tk.END) if entry.get() == self.strings[self.lang]["enter_company_name"] else None)
        entry.pack(anchor="w", pady=5)
        return label, entry

    def atualizar_logo(self, modelo_selecionado, modelos, logos, label):
        try:
            index = modelos.index(modelo_selecionado)
            logo_file = logos[index]
            logo_path = os.path.join(self.logo_dir, logo_file)
            if os.path.exists(logo_path):
                logo = PhotoImage(file=logo_path)
                label.config(image=logo, text="")
                label.image = logo
            else:
                label.config(image="", text=self.strings[self.lang]["no_logo"])
                label.image = None
                logging.warning(f"Logo não encontrado: {logo_path}")
        except (ValueError, TclError) as e:
            label.config(image="", text=self.strings[self.lang]["no_logo"])
            label.image = None
            logging.error(f"Erro ao carregar logo: {e}")

    def toggle_lista_controle_acesso(self):
        if self.cctv_visivel:
            for widget in self.cctv_frame.winfo_children():
                widget.destroy()
            self.cctv_frame.grid_forget()
            self.quantidades_cctv.clear()
            self.cctv_visivel = False

        if self.chatbot_visivel:
            self.toggle_lista_chatbot()

        if self.consulta_visivel:
            self.toggle_consulta()

        if self.controle_acesso_visivel:
            for widget in self.controle_acesso_frame.winfo_children():
                widget.destroy()
            self.controle_acesso_frame.grid_forget()
            self.quantidades_controle_acesso.clear()
            self.controle_acesso_visivel = False
        else:
            self.mostrar_lista_controle_acesso()
            self.controle_acesso_visivel = True

    def mostrar_lista_controle_acesso(self):
        for widget in self.controle_acesso_frame.winfo_children():
            widget.destroy()

        self.controle_acesso_frame.grid(row=0, column=0, sticky="nsew", padx=(5, 10), pady=(5, 10))

        container = tk.Frame(self.controle_acesso_frame, bg="#FFFFFF", bd=1, relief="solid")
        container.grid(sticky="nsew", padx=(0, 200), pady=(5, 20))
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        tk.Label(
            container, text=self.strings[self.lang]["access_control"],
            font=self.fonte_label, bg="#FFFFFF", fg="#2B2D42"
        ).grid(row=0, column=0, sticky="w", pady=10)

        self.checkboxes_controle_acesso = {}
        self.quantidades_controle_acesso = {}
        itens_controle_acesso = self.config["controle_acesso"].keys()

        row = 1
        for item in itens_controle_acesso:
            frame_item = tk.Frame(container, bg="#FFFFFF")
            frame_item.grid(row=row, column=0, sticky="ew", pady=5)

            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(
                frame_item, text=item, variable=var, font=self.fonte_pequena,
                bg="#FFFFFF", fg="#2B2D42", anchor="w", selectcolor="#8D99AE"
            )
            checkbox.pack(side=tk.LEFT, padx=10)
            self.checkboxes_controle_acesso[item] = var

            validate_cmd = self.window.register(self.validate_spinbox)
            spinbox = tk.Spinbox(
                frame_item, from_=0, to=100, font=self.fonte_pequena, width=5,
                justify="center", bg="#FFFFFF", fg="#2B2D42", bd=1, relief="solid",
                validate="key", validatecommand=(validate_cmd, "%P")
            )
            spinbox.pack(side=tk.RIGHT, padx=10)
            self.quantidades_controle_acesso[item] = spinbox

            modelos = self.config["controle_acesso"][item]["modelos"]
            logos = self.config["controle_acesso"][item]["logos"]
            logo_label = tk.Label(frame_item, bg="#FFFFFF")
            logo_label.pack(side=tk.LEFT, padx=10)

            if modelos:
                var_modelo = tk.StringVar(value=self.strings[self.lang]["select_model"])
                dropdown = tk.OptionMenu(
                    frame_item, var_modelo, *modelos,
                    command=lambda selected, m=modelos, l=logos, lbl=logo_label: self.atualizar_logo(selected, m, l, lbl)
                )
                dropdown.config(font=self.fonte_pequena, bg="#FFFFFF", fg="#2B2D42")
                dropdown.pack(side=tk.RIGHT, padx=10)
                self.modelos_controle_acesso[item] = var_modelo

            row += 1

        tk.Button(
            container, text=self.strings[self.lang]["confirm_access_control"],
            command=self.confirmar_conclusao_controle_acesso, font=self.fonte_pequena,
            fg="white", bg="#2B2D42", relief="flat", width=20
        ).grid(row=row, column=0, sticky="e", pady=10)

    def validate_spinbox(self, value):
        if value == "":
            return True
        try:
            int_value = int(value)
            return 0 <= int_value <= 100
        except ValueError:
            return False

    def mostrar_lista_cctv(self):
        for widget in self.cctv_frame.winfo_children():
            widget.destroy()

        self.cctv_frame.grid(row=0, column=0, sticky="nsew", padx=(5, 10), pady=(5, 10))

        container = tk.Frame(self.cctv_frame, bg="#FFFFFF", bd=1, relief="solid")
        container.grid(sticky="nsew", padx=(0, 200), pady=(5, 20))
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        tk.Label(
            container, text=self.strings[self.lang]["cctv"],
            font=self.fonte_label, bg="#FFFFFF", fg="#2B2D42"
        ).grid(row=0, column=0, sticky="w", pady=10)

        self.checkboxes_cctv = {}
        self.quantidades_cctv = {}
        itens_cctv = self.config["cctv"].keys()

        row = 1
        for item in itens_cctv:
            frame_item = tk.Frame(container, bg="#FFFFFF")
            frame_item.grid(row=row, column=0, sticky="ew", pady=5)

            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(
                frame_item, text=item, variable=var, font=self.fonte_pequena,
                bg="#FFFFFF", fg="#2B2D42", anchor="w", selectcolor="#8D99AE"
            )
            checkbox.pack(side=tk.LEFT, padx=10)
            self.checkboxes_cctv[item] = var

            validate_cmd = self.window.register(self.validate_spinbox)
            spinbox = tk.Spinbox(
                frame_item, from_=0, to=100, font=self.fonte_pequena, width=5,
                justify="center", bg="#FFFFFF", fg="#2B2D42", bd=1, relief="solid",
                validate="key", validatecommand=(validate_cmd, "%P")
            )
            spinbox.pack(side=tk.RIGHT, padx=10)
            self.quantidades_cctv[item] = spinbox

            modelos = self.config["cctv"][item]["modelos"]
            logos = self.config["cctv"][item]["logos"]
            logo_label = tk.Label(frame_item, bg="#FFFFFF")
            logo_label.pack(side=tk.LEFT, padx=10)

            if modelos:
                var_modelo = tk.StringVar(value=self.strings[self.lang]["select_model"])
                dropdown = tk.OptionMenu(
                    frame_item, var_modelo, *modelos,
                    command=lambda selected, m=modelos, l=logos, lbl=logo_label: self.atualizar_logo(selected, m, l, lbl)
                )
                dropdown.config(font=self.fonte_pequena, bg="#FFFFFF", fg="#2B2D42")
                dropdown.pack(side=tk.RIGHT, padx=10)
                self.modelos_cctv[item] = var_modelo

            row += 1

        tk.Button(
            container, text=self.strings[self.lang]["confirm_cctv"],
            command=self.confirmar_conclusao_cctv, font=self.fonte_pequena,
            fg="white", bg="#2B2D42", relief="flat", width=20
        ).grid(row=row, column=0, sticky="e", pady=10)

    def toggle_lista_cctv(self):
        if self.controle_acesso_visivel:
            for widget in self.controle_acesso_frame.winfo_children():
                widget.destroy()
            self.controle_acesso_frame.grid_forget()
            self.quantidades_controle_acesso.clear()
            self.controle_acesso_visivel = False

        if self.chatbot_visivel:
            self.toggle_lista_chatbot()

        if self.consulta_visivel:
            self.toggle_consulta()

        if self.cctv_visivel:
            for widget in self.cctv_frame.winfo_children():
                widget.destroy()
            self.cctv_frame.grid_forget()
            self.quantidades_cctv.clear()
            self.cctv_visivel = False
        else:
            self.mostrar_lista_cctv()
            self.cctv_visivel = True

    def toggle_lista_chatbot(self):
        if self.controle_acesso_visivel:
            self.toggle_lista_controle_acesso()

        if self.cctv_visivel:
            self.toggle_lista_cctv()

        if self.consulta_visivel:
            self.toggle_consulta()

        if self.chatbot_visivel:
            for widget in self.chatbot_frame.winfo_children():
                widget.destroy()
            self.chatbot_frame.grid_forget()
            self.chatbot_visivel = False
        else:
            self.mostrar_lista_chatbot()
            self.chatbot_visivel = True

    def mostrar_lista_chatbot(self):
        for widget in self.chatbot_frame.winfo_children():
            widget.destroy()

        self.chatbot_frame.grid(row=0, column=0, sticky="nsew", padx=(5, 10), pady=(5, 10))

        container = tk.Frame(self.chatbot_frame, bg="#FFFFFF", bd=1, relief="solid")
        container.grid(sticky="nsew", padx=(0, 200), pady=(5, 20))
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)

        tk.Label(
            container, text=self.strings[self.lang]["chatbot"],
            font=self.fonte_label, bg="#FFFFFF", fg="#2B2D42"
        ).grid(row=0, column=0, sticky="w", pady=10)

        chat_frame = tk.Frame(container, bg="#FFFFFF")
        chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        self.chatbot_text = scrolledtext.ScrolledText(
            chat_frame, height=20, font=self.fonte_pequena, bg="#F0F0F0",
            fg="#2B2D42", bd=1, relief="solid", wrap=tk.WORD
        )
        self.chatbot_text.pack(fill=tk.BOTH, expand=True)
        self.chatbot_text.config(state=tk.DISABLED)

        self.chatbot_buttons_frame = tk.Frame(container, bg="#FFFFFF")
        self.chatbot_buttons_frame.grid(row=2, column=0, sticky="ew", pady=10)

        self.iniciar_conversa_chatbot()

    def iniciar_conversa_chatbot(self):
        self.exibir_mensagem_chatbot("Olá! Eu sou o Assistente de Projetos. Como posso ajudar você hoje?\n")
        self.exibir_mensagem_chatbot("Escolha uma opção abaixo:\n")
        self.exibir_opcoes_chatbot([
            ("Preciso de ajuda com CFTV", self.opcao_cctv),
            ("Preciso de ajuda com Controle de Acesso", self.opcao_controle_acesso),
            ("Quero saber mais sobre o programa", self.opcao_sobre_programa),
            ("Sair do chat", self.opcao_sair)
        ])

    def exibir_mensagem_chatbot(self, mensagem):
        self.chatbot_text.config(state=tk.NORMAL)
        self.chatbot_text.insert(tk.END, mensagem)
        self.chatbot_text.config(state=tk.DISABLED)
        self.chatbot_text.see(tk.END)

    def exibir_opcoes_chatbot(self, opcoes):
        for widget in self.chatbot_buttons_frame.winfo_children():
            widget.destroy()

        for texto, comando in opcoes:
            btn = tk.Button(
                self.chatbot_buttons_frame, text=texto, command=comando,
                font=self.fonte_pequena, fg="white", bg="#2B2D42", relief="flat", width=30
            )
            btn.pack(pady=5)

    def opcao_cctv(self):
        self.exibir_mensagem_chatbot("\nVocê escolheu CFTV!\n")
        self.exibir_mensagem_chatbot("Eu posso ajudar com a escolha de câmeras, NVRs, DVRs e mais. Sobre o que você gostaria de falar?\n")
        self.exibir_opcoes_chatbot([
            ("Câmeras", self.opcao_cctv_cameras),
            ("NVR ou DVR", self.opcao_cctv_nvr_dvr),
            ("Outros equipamentos", self.opcao_cctv_outros),
            ("Voltar", self.iniciar_conversa_chatbot)
        ])

    def opcao_cctv_cameras(self):
        self.exibir_mensagem_chatbot("\nSobre câmeras:\n")
        self.exibir_mensagem_chatbot(
            "Temos modelos como DS-2CD2047G2-LU (4MP, visão noturna colorida, ideal para exteriores), "
            "DS-2CD1143G0-I (4MP, compacto, ideal para interiores) e DS-2CD1023G0E (2MP, ótimo para monitoramento básico).\n"
        )
        self.exibir_mensagem_chatbot("Você gostaria de mais detalhes sobre algum modelo?\n")
        self.exibir_opcoes_chatbot([
            ("Sim, sobre DS-2CD2047G2-LU", lambda: self.exibir_mensagem_chatbot(
                "\nO modelo DS-2CD2047G2-LU tem resolução de 4MP, visão noturna colorida, lente de 2.8mm e proteção IP67. É da Hikvision.\n")),
            ("Sim, sobre DS-2CD1143G0-I", lambda: self.exibir_mensagem_chatbot(
                "\nO modelo DS-2CD1143G0-I tem resolução de 4MP, design compacto, lente de 2.8mm e é ideal para escritórios. É da Hikvision.\n")),
            ("Sim, sobre DS-2CD1023G0E", lambda: self.exibir_mensagem_chatbot(
                "\nO modelo DS-2CD1023G0E tem resolução de 2MP, lente de 2.8mm, visão noturna IR até 30m, ideal para monitoramento básico. É da Hikvision.\n")),
            ("Não, voltar", self.opcao_cctv)
        ])

    def opcao_cctv_nvr_dvr(self):
        self.exibir_mensagem_chatbot("\nSobre NVRs e DVRs:\n")
        self.exibir_mensagem_chatbot("Os NVRs como o DS-7608NI-K1 suportam até 8 canais, enquanto o DS-7732NI-K4 suporta até 32 canais.\n")
        self.exibir_mensagem_chatbot("Você precisa de ajuda para escolher um modelo?\n")
        self.exibir_opcoes_chatbot([
            ("Sim, para 8 canais", lambda: self.exibir_mensagem_chatbot(
                "\nRecomendo o DS-7608NI-K1. Ele suporta 8 canais, resolução até 8MP e é da Hikvision.\n")),
            ("Sim, para mais canais", lambda: self.exibir_mensagem_chatbot(
                "\nO DS-7732NI-K4 suporta até 32 canais, resolução até 12MP e é ideal para projetos maiores. É da Hikvision.\n")),
            ("Não, voltar", self.opcao_cctv)
        ])

    def opcao_cctv_outros(self):
        self.exibir_mensagem_chatbot("\nOutros equipamentos de CFTV:\n")
        self.exibir_mensagem_chatbot("Temos cabos, conectores RJ45, switches PoE, e HDDs para armazenamento.\n")
        self.exibir_mensagem_chatbot("Qual item você gostaria de saber mais?\n")
        self.exibir_opcoes_chatbot([
            ("HDDs", lambda: self.exibir_mensagem_chatbot(
                "\nOferecemos HDDs de 1TB a 4TB, ideais para gravação de vídeo, compatíveis com NVRs e DVRs.\n")),
            ("Switches PoE", lambda: self.exibir_mensagem_chatbot(
                "\nO DS-3E0105P-E é um switch PoE com 5 portas, suporta até 60W, ótimo para pequenas instalações.\n")),
            ("Voltar", self.opcao_cctv)
        ])

    def opcao_controle_acesso(self):
        self.exibir_mensagem_chatbot("\nVocê escolheu Controle de Acesso!\n")
        self.exibir_mensagem_chatbot("Posso ajudar com leitores faciais, catracas, eletroímãs e mais. Sobre o que você gostaria de falar?\n")
        self.exibir_opcoes_chatbot([
            ("Leitores Faciais", self.opcao_controle_acesso_leitores),
            ("Catracas", self.opcao_controle_acesso_catracas),
            ("Outros equipamentos", self.opcao_controle_acesso_outros),
            ("Voltar", self.iniciar_conversa_chatbot)
        ])

    def opcao_controle_acesso_leitores(self):
        self.exibir_mensagem_chatbot("\nSobre Leitores Faciais:\n")
        self.exibir_mensagem_chatbot("Temos modelos como DS-K1T341 da Hikvision e ID-FACE da Control iD.\n")
        self.exibir_mensagem_chatbot("Você gostaria de mais detalhes sobre algum modelo?\n")
        self.exibir_opcoes_chatbot([
            ("Sim, sobre DS-K1T341", lambda: self.exibir_mensagem_chatbot(
                "\nO DS-K1T341 é um leitor facial com tela de 4.3 polegadas, suporta até 1.500 faces e tem proteção IP65.\n")),
            ("Sim, sobre ID-FACE", lambda: self.exibir_mensagem_chatbot(
                "\nO ID-FACE da Control iD é compacto, suporta até 10.000 faces e integra com sistemas de controle.\n")),
            ("Não, voltar", self.opcao_controle_acesso)
        ])

    def opcao_controle_acesso_catracas(self):
        self.exibir_mensagem_chatbot("\nSobre Catracas:\n")
        self.exibir_mensagem_chatbot("Temos modelos como IDBLOCK NEXT FACIAL da Control iD e Ds-k3g411 da Hikvision.\n")
        self.exibir_mensagem_chatbot("Você gostaria de mais detalhes sobre algum modelo?\n")
        self.exibir_opcoes_chatbot([
            ("Sim, sobre IDBLOCK NEXT FACIAL", lambda: self.exibir_mensagem_chatbot(
                "\nA IDBLOCK NEXT FACIAL suporta reconhecimento facial, capacidade para 10.000 usuários, ideal para controle de pedestres.\n")),
            ("Sim, sobre Ds-k3g411", lambda: self.exibir_mensagem_chatbot(
                "\nA Ds-k3g411 da Hikvision é robusta, suporta integração com leitores e tem design modular.\n")),
            ("Não, voltar", self.opcao_controle_acesso)
        ])

    def opcao_controle_acesso_outros(self):
        self.exibir_mensagem_chatbot("\nOutros equipamentos de Controle de Acesso:\n")
        self.exibir_mensagem_chatbot("Temos eletroímãs, fontes, fechaduras, botoeiras e controladoras.\n")
        self.exibir_mensagem_chatbot("Qual item você gostaria de saber mais?\n")
        self.exibir_opcoes_chatbot([
            ("Eletroímãs", lambda: self.exibir_mensagem_chatbot(
                "\nO FE 20150 da Intelbras é um eletroímã robusto, suporta até 150kg de força, ideal para portas.\n")),
            ("Controladoras", lambda: self.exibir_mensagem_chatbot(
                "\nA DS-K2602T da Hikvision suporta até 4 portas, integração com leitores e protocolo TCP/IP.\n")),
            ("Voltar", self.opcao_controle_acesso)
        ])

    def opcao_sobre_programa(self):
        self.exibir_mensagem_chatbot("\nSobre o Programa:\n")
        self.exibir_mensagem_chatbot("Este é o Gerador de Projetos, criado para ajudar na elaboração de projetos de CFTV e Controle de Acesso.\n")
        self.exibir_mensagem_chatbot("Você pode usar as abas CFTV e Controle de Acesso para montar seu projeto, ou a aba Consulta para obter informações rápidas.\n")
        self.exibir_mensagem_chatbot("Gostaria de voltar ao menu principal?\n")
        self.exibir_opcoes_chatbot([
            ("Sim", self.iniciar_conversa_chatbot),
            ("Sair do chat", self.opcao_sair)
        ])

    def opcao_sair(self):
        self.exibir_mensagem_chatbot("\nObrigado por usar o Chatbot! Até a próxima! 😊\n")
        self.exibir_opcoes_chatbot([
            ("Reiniciar conversa", self.iniciar_conversa_chatbot)
        ])

    def toggle_consulta(self):
        if self.controle_acesso_visivel:
            self.toggle_lista_controle_acesso()
        if self.cctv_visivel:
            self.toggle_lista_cctv()
        if self.chatbot_visivel:
            self.toggle_lista_chatbot()

        if self.consulta_visivel:
            if self.consulta_container:
                self.consulta_container.destroy()
            self.consulta_visivel = False
        else:
            self.consulta_container = tk.Frame(self.content_frame, bg="#F5F6F5")
            self.consulta_container.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

            tk.Label(
                self.consulta_container, text=self.strings[self.lang]["consultation"],
                font=self.fonte_label, bg="#F5F6F5", fg="#2B2D42"
            ).pack(anchor="w", pady=5)

            btn_frame = tk.Frame(self.consulta_container, bg="#F5F6F5")
            btn_frame.pack(anchor="w", pady=10)

            self.porta_botao = tk.Button(
                btn_frame, text="Porta", command=self.mostrar_menu_porta,
                font=self.fonte_botao, fg="white", bg="#8D99AE", relief="flat",
                width=15, height=2
            )
            self.porta_botao.pack(side=tk.LEFT, padx=5)

            self.pedestre_botao = tk.Button(
                btn_frame, text="Pedestre", command=self.mostrar_menu_pedestre,
                font=self.fonte_botao, fg="white", bg="#8D99AE", relief="flat",
                width=15, height=2
            )
            self.pedestre_botao.pack(side=tk.LEFT, padx=5)

            self.veicular_botao = tk.Button(
                btn_frame, text="Veicular", command=self.mostrar_menu_veicular,
                font=self.fonte_botao, fg="white", bg="#8D99AE", relief="flat",
                width=15, height=2
            )
            self.veicular_botao.pack(side=tk.LEFT, padx=5)

            self.consulta_visivel = True

    def mostrar_menu_porta(self):
        menu_porta = tk.Menu(self.window, tearoff=0)
        menu_porta.add_command(label="Vidro/Vidro", command=self.mostrar_popup_vidro_vidro)
        menu_porta.add_command(label="Vidro/Parede", command=self.mostrar_popup_vidro_parede)
        menu_porta.add_command(label="Porta Comum", command=self.mostrar_popup_porta_comum)
        menu_porta.post(
            self.porta_botao.winfo_rootx(),
            self.porta_botao.winfo_rooty() + self.porta_botao.winfo_height())

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
            "• Fechadura AGL fail safe para vidro e porta a paredes\n\n"
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

    def mostrar_menu_pedestre(self):
        menu_pedestre = tk.Menu(self.window, tearoff=0)
        menu_pedestre.add_command(label="Torniquete", command=self.mostrar_popup_torniquete_pedestre)
        menu_pedestre.add_command(label="Catraca", command=self.mostrar_popup_catraca_pedestre)
        menu_pedestre.post(
            self.pedestre_botao.winfo_rootx(),
            self.pedestre_botao.winfo_rooty() + self.pedestre_botao.winfo_height())

    def mostrar_popup_torniquete_pedestre(self):
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

    def mostrar_popup_catraca_pedestre(self):
        mensagem = (
            "##################################\n"
            "       CATRACA\n"
            "##################################\n\n"
            "• Catraca/ verificar modelo.\n\n"
            "• Terminal Facial/ verificar modelo.\n\n"
            "• Suporte para facial."
        )
        messagebox.showinfo("Catraca", mensagem)

    def mostrar_menu_veicular(self):
        menu_veicular = tk.Menu(self.window, tearoff=0)
        menu_veicular.add_command(label="Totem", command=self.mostrar_popup_totem_veicular)
        menu_veicular.add_command(label="Lpr", command=self.mostrar_popup_lpr_veicular)
        menu_veicular.add_command(label="Antena", command=self.mostrar_popup_antena_veicular)
        menu_veicular.post(
            self.veicular_botao.winfo_rootx(),
            self.veicular_botao.winfo_rooty() + self.veicular_botao.winfo_height())

    def mostrar_popup_totem_veicular(self):
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

    def mostrar_popup_lpr_veicular(self):
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

    def mostrar_popup_antena_veicular(self):
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

    def confirmar_conclusao_controle_acesso(self):
        nome_empresa = self.nome_entry.get().strip()
        if not nome_empresa or nome_empresa == self.strings[self.lang]["enter_company_name"]:
            messagebox.showwarning("Atenção", self.strings[self.lang]["warning_company_name"])
            return

        selecionados = []
        for item, var in self.checkboxes_controle_acesso.items():
            if var.get():
                spinbox = self.quantidades_controle_acesso[item]
                try:
                    quantidade_valor = int(spinbox.get())
                    if quantidade_valor < 0:
                        raise ValueError
                except ValueError:
                    messagebox.showwarning("Erro", self.strings[self.lang]["invalid_quantity"].format(item=item))
                    return

                if quantidade_valor > 0:
                    if item in self.modelos_controle_acesso:
                        modelo = self.modelos_controle_acesso[item].get()
                        if modelo == self.strings[self.lang]["select_model"]:
                            messagebox.showwarning("Erro", self.strings[self.lang]["no_model_selected"].format(item=item))
                            return
                        selecionados.append(f"Controle de Acesso: {item} - Modelo: {modelo} - Quantidade: {quantidade_valor}")
                    else:
                        selecionados.append(f"Controle de Acesso: {item} - Quantidade: {quantidade_valor}")

        if selecionados:
            nome_arquivo = f"{nome_empresa}_Controle_Acesso.txt"
            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write("Itens Selecionados (Controle de Acesso):\n")
                arquivo.write("\n".join(selecionados))
            logging.info(f"Arquivo '{nome_arquivo}' criado com sucesso.")
            messagebox.showinfo("Sucesso", self.strings[self.lang]["file_generated"])

    def confirmar_conclusao_cctv(self):
        nome_empresa = self.nome_entry.get().strip()
        if not nome_empresa or nome_empresa == self.strings[self.lang]["enter_company_name"]:
            messagebox.showwarning("Atenção", self.stringsaliases[self.lang]["warning_company_name"])
            return

        selecionados = []
        for item, var in self.checkboxes_cctv.items():
            if var.get():
                spinbox = self.quantidades_cctv[item]
                try:
                    quantidade_valor = int(spinbox.get())
                    if quantidade_valor < 0:
                        raise ValueError
                except ValueError:
                    messagebox.showwarning("Erro", self.strings[self.lang]["invalid_quantity"].format(item=item))
                    return

                if quantidade_valor > 0:
                    if item in self.modelos_cctv:
                        modelo = self.modelos_cctv[item].get()
                        if modelo == self.strings[self.lang]["select_model"]:
                            messagebox.showwarning("Erro", self.strings[self.lang]["no_model_selected"].format(item=item))
                            return
                        selecionados.append(f"CCTV: {item} - Modelo: {modelo} - Quantidade: {quantidade_valor}")
                    else:
                        selecionados.append(f"CCTV: {item} - Quantidade: {quantidade_valor}")

        if selecionados:
            nome_arquivo = f"{nome_empresa}_CCTV.txt"
            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write("Itens Selecionados (CCTV):\n")
                arquivo.write("\n".join(selecionados))
            logging.info(f"Arquivo '{nome_arquivo}' criado com sucesso.")
            messagebox.showinfo("Sucesso", self.strings[self.lang]["file_generated"])

    def iniciar(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = Interface()
    app.iniciar()