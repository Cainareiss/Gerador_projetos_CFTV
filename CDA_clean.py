import tkinter as tk
from tkinter import PhotoImage, messagebox, scrolledtext
import os

class Interface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("GERADOR DE PROJETOS")
        self.window.geometry("1080x720")
        self.window.configure(bg="#F5F6F5")

        # Definindo caminhos base para logotipos
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.logo_dir = os.path.join(self.base_dir, "PROJETO-SISTEMA", "produtos_logos")
        os.makedirs(self.logo_dir, exist_ok=True)

        # Fontes (corrigindo "Ariel" para "Arial")
        self.fonte_titulo = ("Arial", 24, "bold")
        self.fonte_label = ("Arial", 14, "bold")
        self.fonte_pequena = ("Arial", 12)
        self.fonte_botao = ("Arial", 12, "bold")
        self.fonte_rodape = ("Arial", 10, "italic")

        # Dicionários para armazenar dados
        self.modelos_cftv = {}
        self.modelos_cda = {}
        self.checkboxes_cda = {}
        self.quantidades_cda = {}
        self.checkboxes_cftv = {}
        self.quantidades_cftv = {}

        # Variáveis de controle
        self.cda_visivel = False
        self.cftv_visivel = False
        self.chatbot_visivel = False
        self.tipo_cda_visivel = False
        self.consulta_container = None

        # Layout Principal: Divisão em Sidebar e Área de Conteúdo
        # Sidebar (à esquerda)
        self.sidebar_frame = tk.Frame(self.window, bg="#2B2D42", width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Título na Sidebar
        tk.Label(
            self.sidebar_frame, text="Menu", font=self.fonte_label, fg="white", bg="#2B2D42",
            pady=20
        ).pack(anchor="n")

        # Botões na Sidebar
        self.consulta_botao = tk.Button(
            self.sidebar_frame, text="Consulta", command=self.toggle_lista_tipos_cda,
            font=self.fonte_botao, fg="white", bg="#8D99AE", relief="flat",
            width=15, height=2
        )
        self.consulta_botao.pack(pady=10)

        self.cftv_botao = tk.Button(
            self.sidebar_frame, text="CFTV", command=self.toggle_lista_cftv,
            font=self.fonte_botao, fg="white", bg="#8D99AE", relief="flat",
            width=15, height=2
        )
        self.cftv_botao.pack(pady=10)

        self.cda_botao = tk.Button(
            self.sidebar_frame, text="Controle de Acesso", command=self.toggle_lista_cda,
            font=self.fonte_botao, fg="white", bg="#8D99AE", relief="flat",
            width=15, height=2
        )
        self.cda_botao.pack(pady=10)

        # Botão para Chatbot
        self.chatbot_botao = tk.Button(
            self.sidebar_frame, text="Chatbot", command=self.toggle_lista_chatbot,
            font=self.fonte_botao, fg="white", bg="#8D99AE", relief="flat",
            width=15, height=2
        )
        self.chatbot_botao.pack(pady=10)

        # Área Principal (à direita da Sidebar)
        self.main_frame = tk.Frame(self.window, bg="#F5F6F5")
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Cabeçalho na Área Principal
        self.header_frame = tk.Frame(self.main_frame, bg="#F5F6F5")
        self.header_frame.pack(fill=tk.X)

        tk.Label(
            self.header_frame, text="Gerador de Projetos", font=self.fonte_titulo, fg="#2B2D42", bg="#F5F6F5"
        ).pack(anchor="w", pady=10)

        # Campo de Entrada para Nome da Empresa
        self.nome_label, self.nome_entry = self.criar_campo_cliente("Nome da Empresa:")

        # Frame para Conteúdo Dinâmico (listas CDA, CFTV, Chatbot, botões de consulta)
        self.content_frame = tk.Frame(self.main_frame, bg="#F5F6F5")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Frames para Listas CDA, CFTV e Chatbot
        self.cda_frame = tk.Frame(self.content_frame, bg="#F5F6F5")
        self.cftv_frame = tk.Frame(self.content_frame, bg="#F5F6F5")
        self.chatbot_frame = tk.Frame(self.content_frame, bg="#F5F6F5")

        # Rodapé
        self.footer_frame = tk.Frame(self.main_frame, bg="#F5F6F5")
        self.footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Label(
            self.footer_frame, text="Created by Reis ~ Beta 6.5", font=self.fonte_rodape,
            fg="#8D99AE", bg="#F5F6F5", anchor="e"
        ).pack(side=tk.RIGHT, padx=20)

        # Variáveis para o Chatbot
        self.chatbot_text = None
        self.chatbot_buttons_frame = None

    def criar_campo_cliente(self, label_text):
        frame = tk.Frame(self.main_frame, bg="#F5F6F5")
        frame.pack(fill=tk.X, pady=10)

        label = tk.Label(frame, text=label_text, font=self.fonte_label, bg="#F5F6F5", fg="#2B2D42")
        label.pack(anchor="w")

        entry = tk.Entry(frame, font=self.fonte_pequena, bg="#FFFFFF", fg="#2B2D42", bd=1, relief="solid", width=50)
        entry.insert(0, "Digite o nome da empresa")
        entry.bind("<FocusIn>", lambda event: entry.delete(0, tk.END) if entry.get() == "Digite o nome da empresa" else None)
        entry.pack(anchor="w", pady=5)
        return label, entry

    def toggle_lista_cda(self):
        if self.cftv_visivel:
            for widget in self.cftv_frame.winfo_children():
                widget.destroy()
            self.cftv_frame.pack_forget()
            self.quantidades_cftv.clear()
            self.cftv_visivel = False

        if self.chatbot_visivel:
            self.toggle_lista_chatbot()

        if self.tipo_cda_visivel:
            self.toggle_lista_tipos_cda()

        if self.cda_visivel:
            for widget in self.cda_frame.winfo_children():
                widget.destroy()
            self.cda_frame.pack_forget()
            self.quantidades_cda.clear()
            self.cda_visivel = False
        else:
            self.mostrar_lista_cda()
            self.cda_visivel = True

    def atualizar_logo(self, modelo_selecionado, modelos, logos, label):
        try:
            index = modelos.index(modelo_selecionado)
            logo_file = logos[index]
            logo_path = os.path.join(self.logo_dir, logo_file)
            if os.path.exists(logo_path):
                logo = PhotoImage(file=logo_path)
                label.config(image=logo)
                label.image = logo
            else:
                label.config(image="")
                label.image = None
                print(f"Logo não encontrado: {logo_path}")
        except (ValueError, tk.TclError) as e:
            label.config(image="")
            label.image = None
            print(f"Erro ao carregar logo: {e}")

    def mostrar_lista_cda(self):
        for widget in self.cda_frame.winfo_children():
            widget.destroy()

        self.cda_frame.pack(fill=tk.BOTH, expand=True, padx=(5, 10), pady=(5, 10))

        container = tk.Frame(self.cda_frame, bg="#FFFFFF", bd=1, relief="solid")
        container.pack(fill=tk.BOTH, expand=True, padx=(0, 200), pady=(5, 20), anchor="w")

        tk.Label(
            container, text="Controle de Acesso", font=self.fonte_label, bg="#FFFFFF", fg="#2B2D42"
        ).pack(anchor="w", pady=10)

        self.checkboxes_cda = {}
        self.quantidades_cda = {}
        itens_cda = ["Leitor Facial", "Catraca", "Eletroímã", "Fonte", "Fonte com bateria", "Fechadura", "Botoeira", "Controladora"]

        for item in itens_cda:
            frame_item = tk.Frame(container, bg="#FFFFFF")
            frame_item.pack(fill=tk.X, pady=5)

            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(
                frame_item, text=item, variable=var, font=self.fonte_pequena,
                bg="#FFFFFF", fg="#2B2D42", anchor="w", selectcolor="#8D99AE"
            )
            checkbox.pack(side=tk.LEFT, padx=10)
            self.checkboxes_cda[item] = var

            spinbox = tk.Spinbox(
                frame_item, from_=0, to=100, font=self.fonte_pequena, width=5,
                justify="center", bg="#FFFFFF", fg="#2B2D42", bd=1, relief="solid"
            )
            spinbox.pack(side=tk.RIGHT, padx=10)
            self.quantidades_cda[item] = spinbox

            modelos, logos = self.get_modelos_logos_cda(item)
            logo_label = tk.Label(frame_item, bg="#FFFFFF")
            logo_label.pack(side=tk.LEFT, padx=10)

            if modelos:
                var_modelo = tk.StringVar(value="Selecione um modelo")
                dropdown = tk.OptionMenu(
                    frame_item, var_modelo, *modelos,
                    command=lambda selected, m=modelos, l=logos, lbl=logo_label: self.atualizar_logo(selected, m, l, lbl)
                )
                dropdown.config(font=self.fonte_pequena, bg="#FFFFFF", fg="#2B2D42")
                dropdown.pack(side=tk.RIGHT, padx=10)
                self.modelos_cda[item] = var_modelo

        tk.Button(
            container, text="Confirmar CDA", command=self.confirmar_conclusao_cda,
            font=self.fonte_pequena, fg="white", bg="#2B2D42", relief="flat", width=20
        ).pack(anchor="e", pady=10)

    def get_modelos_logos_cda(self, item):
        modelos_logos = {
            "Leitor Facial": (["DS-K1T341", "DS-K1T343", "DS-K1T671", "DS-K1T673", "ID-FACE", "ID-FACE MAX"],
                              ["hikvision_logo.png", "hikvision_logo.png", "hikvision_logo.png", "hikvision_logo.png", "controlid_logo.png", "controlid_logo.png"]),
            "Catraca": (["IDBLOCK NEXT FACIAL", "IDBLOCK NEXT", "Ds-k3g411"],
                        ["controlid_logo.png", "controlid_logo.png", "hikvision_logo.png"]),
            "Eletroímã": (["FE 20150", "DS-K4H258", "AGL-150"],
                          ["intelbras_logo.png", "hikvision_logo.png", "agl_logo.png"]),
            "Fonte": (["Fonte 12V", "Fonte 24V", "Fonte 5V"], ["sem_marca.png"] * 3),
            "Fonte com bateria": (["Fonte 12V", "Fonte 24V", "Fonte 5V"], ["sem_marca.png"] * 3),
            "Fechadura": (["Fail Safe P/ Vidro Fs 3010 V", "Fail Safe Porta Vidro Fs 2010"],
                          ["intelbras_logo.png", "intelbras_logo.png"]),
            "Botoeira": (["DS-K7P02", "BT-3000 IN", "BT-INOX AGL"],
                         ["hikvision_logo.png", "intelbras_logo.png", "agl_logo.png"]),
            "Controladora": (["DS-K2602T", "IDBOX", "CT 3000 2PB"],
                             ["hikvision_logo.png", "controlid_logo.png", "intelbras_logo.png"])
        }
        return modelos_logos.get(item, ([], []))

    def mostrar_lista_cftv(self):
        for widget in self.cftv_frame.winfo_children():
            widget.destroy()

        self.cftv_frame.pack(fill=tk.BOTH, expand=True, padx=(5, 10), pady=(5, 10))

        container = tk.Frame(self.cftv_frame, bg="#FFFFFF", bd=1, relief="solid")
        container.pack(fill=tk.BOTH, expand=True, padx=(0, 200), pady=(5, 20), anchor="w")

        tk.Label(
            container, text="CFTV", font=self.fonte_label, bg="#FFFFFF", fg="#2B2D42"
        ).pack(anchor="w", pady=10)

        self.checkboxes_cftv = {}
        self.quantidades_cftv = {}
        itens_cftv = ["Câmera", "Camera LPR", "NVR", "DVR", "HDD", "Cabos", "Conector RJ45", "Switch PoE"]

        for item in itens_cftv:
            frame_item = tk.Frame(container, bg="#FFFFFF")
            frame_item.pack(fill=tk.X, pady=5)

            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(
                frame_item, text=item, variable=var, font=self.fonte_pequena,
                bg="#FFFFFF", fg="#2B2D42", anchor="w", selectcolor="#8D99AE"
            )
            checkbox.pack(side=tk.LEFT, padx=10)
            self.checkboxes_cftv[item] = var

            spinbox = tk.Spinbox(
                frame_item, from_=0, to=100, font=self.fonte_pequena, width=5,
                justify="center", bg="#FFFFFF", fg="#2B2D42", bd=1, relief="solid"
            )
            spinbox.pack(side=tk.RIGHT, padx=10)
            self.quantidades_cftv[item] = spinbox

            modelos, logos = self.get_modelos_logos_cftv(item)
            logo_label = tk.Label(frame_item, bg="#FFFFFF")
            logo_label.pack(side=tk.LEFT, padx=10)

            if modelos:
                var_modelo = tk.StringVar(value="Selecione um modelo")
                dropdown = tk.OptionMenu(
                    frame_item, var_modelo, *modelos,
                    command=lambda selected, m=modelos, l=logos, lbl=logo_label: self.atualizar_logo(selected, m, l, lbl)
                )
                dropdown.config(font=self.fonte_pequena, bg="#FFFFFF", fg="#2B2D42")
                dropdown.pack(side=tk.RIGHT, padx=10)
                self.modelos_cftv[item] = var_modelo

        tk.Button(
            container, text="Confirmar CFTV", command=self.confirmar_conclusao_cftv,
            font=self.fonte_pequena, fg="white", bg="#2B2D42", relief="flat", width=20
        ).pack(anchor="e", pady=10)

    def get_modelos_logos_cftv(self, item):
        modelos_logos = {
            "Câmera": (["DS-2CD2047G2-LU", "DS-2CD1143G0-I", "DS-2CD1023G0E"],
                       ["hikvision_logo.png"] * 3),
            "Camera LPR": (["DS-2CD7A26G0/P-IZHS", "DS-2CD4A26FWD-IZHS/P", "iDS-2CD7A46G0/P-IZHSY",
                            "VIP 7280 LPR", "VIP 7230 LPR", "VIP 7225 LPR G2"],
                           ["hikvision_logo.png", "hikvision_logo.png", "hikvision_logo.png",
                            "intelbras_logo.png", "intelbras_logo.png", "intelbras_logo.png"]),
            "NVR": (["DS-7608NI-K1", "DS-7616NI-K2", "DS-7732NI-K4"],
                    ["hikvision_logo.png"] * 3),
            "DVR": (["DS-7104HGHI-K1", "DS-7208HUHI-K2", "DS-7216HUHI-K4"],
                    ["hikvision_logo.png"] * 3),
            "HDD": (["1TB", "2TB", "3TB", "4TB"],
                    ["seagate_logo.png"] * 4),
            "Cabos": (["Cabo Utp", "Cabo coaxial", "Cabo de fibra optica"],
                      ["caboutp_logo.png", "cabocoaxial_logo.png", "cabofibraotica_logo.png"]),
            "Conector RJ45": (["RJ45 CAT5", "RJ45 CAT6"],
                             ["rj45cat6_logo.png", "rj45cat6_logo.png"]),
            "Switch PoE": (["DS-3E0105P-E", "DS-3E0310P-E", "DS-3E0526P-E"],
                           ["hikvision_logo.png"] * 3)
        }
        return modelos_logos.get(item, ([], []))

    def toggle_lista_cftv(self):
        if self.cda_visivel:
            for widget in self.cda_frame.winfo_children():
                widget.destroy()
            self.cda_frame.pack_forget()
            self.quantidades_cda.clear()
            self.cda_visivel = False

        if self.chatbot_visivel:
            self.toggle_lista_chatbot()

        if self.tipo_cda_visivel:
            self.toggle_lista_tipos_cda()

        if self.cftv_visivel:
            for widget in self.cftv_frame.winfo_children():
                widget.destroy()
            self.cftv_frame.pack_forget()
            self.quantidades_cftv.clear()
            self.cftv_visivel = False
        else:
            self.mostrar_lista_cftv()
            self.cftv_visivel = True

    def toggle_lista_chatbot(self):
        if self.cda_visivel:
            self.toggle_lista_cda()

        if self.cftv_visivel:
            self.toggle_lista_cftv()

        if self.tipo_cda_visivel:
            self.toggle_lista_tipos_cda()

        if self.chatbot_visivel:
            for widget in self.chatbot_frame.winfo_children():
                widget.destroy()
            self.chatbot_frame.pack_forget()
            self.chatbot_visivel = False
        else:
            self.mostrar_lista_chatbot()
            self.chatbot_visivel = True

    def mostrar_lista_chatbot(self):
        for widget in self.chatbot_frame.winfo_children():
            widget.destroy()

        self.chatbot_frame.pack(fill=tk.BOTH, expand=True, padx=(5, 10), pady=(5, 10))

        container = tk.Frame(self.chatbot_frame, bg="#FFFFFF", bd=1, relief="solid")
        container.pack(fill=tk.BOTH, expand=True, padx=(0, 200), pady=(5, 20), anchor="w")

        tk.Label(
            container, text="Chatbot", font=self.fonte_label, bg="#FFFFFF", fg="#2B2D42"
        ).pack(anchor="w", pady=10)

        # Área de exibição do chat com barra de rolagem
        chat_frame = tk.Frame(container, bg="#FFFFFF")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.chatbot_text = scrolledtext.ScrolledText(
            chat_frame, height=20, font=self.fonte_pequena, bg="#F0F0F0", fg="#2B2D42", bd=1, relief="solid", wrap=tk.WORD
        )
        self.chatbot_text.pack(fill=tk.BOTH, expand=True)
        self.chatbot_text.config(state=tk.DISABLED)  # Tornar o texto somente leitura

        # Frame para os botões de opções
        self.chatbot_buttons_frame = tk.Frame(container, bg="#FFFFFF")
        self.chatbot_buttons_frame.pack(fill=tk.X, pady=10)

        # Iniciar a conversa
        self.iniciar_conversa_chatbot()

    def iniciar_conversa_chatbot(self):
        # Mensagem inicial do bot
        self.exibir_mensagem_chatbot("Olá! Eu sou o Assistente de Projetos. Como posso ajudar você hoje?\n")
        self.exibir_mensagem_chatbot("Escolha uma opção abaixo:\n")
        
        # Opções iniciais
        self.exibir_opcoes_chatbot([
            ("Preciso de ajuda com CFTV", self.opcao_cftv),
            ("Preciso de ajuda com Controle de Acesso", self.opcao_cda),
            ("Quero saber mais sobre o programa", self.opcao_sobre_programa),
            ("Sair do chat", self.opcao_sair)
        ])

    def exibir_mensagem_chatbot(self, mensagem):
        self.chatbot_text.config(state=tk.NORMAL)
        self.chatbot_text.insert(tk.END, mensagem)
        self.chatbot_text.config(state=tk.DISABLED)
        self.chatbot_text.see(tk.END)  # Rolar automaticamente para o final

    def exibir_opcoes_chatbot(self, opcoes):
        # Limpar botões anteriores
        for widget in self.chatbot_buttons_frame.winfo_children():
            widget.destroy()

        # Adicionar novos botões de opções
        for texto, comando in opcoes:
            btn = tk.Button(
                self.chatbot_buttons_frame, text=texto, command=comando,
                font=self.fonte_pequena, fg="white", bg="#2B2D42", relief="flat", width=30
            )
            btn.pack(pady=5)

    def opcao_cftv(self):
        self.exibir_mensagem_chatbot("\nVocê escolheu CFTV!\n")
        self.exibir_mensagem_chatbot("Eu posso ajudar com a escolha de câmeras, NVRs, DVRs e mais. Sobre o que você gostaria de falar?\n")
        self.exibir_opcoes_chatbot([
            ("Câmeras", self.opcao_cftv_cameras),
            ("NVR ou DVR", self.opcao_cftv_nvr_dvr),
            ("Outros equipamentos", self.opcao_cftv_outros),
            ("Voltar", self.iniciar_conversa_chatbot)
        ])

    def opcao_cftv_cameras(self):
        self.exibir_mensagem_chatbot("\nSobre câmeras:\n")
        self.exibir_mensagem_chatbot("Temos modelos como DS-2CD2047G2-LU, que é ótimo para ambientes externos, e DS-2CD1143G0-I, ideal para áreas internas.\n")
        self.exibir_mensagem_chatbot("Você gostaria de mais detalhes sobre algum modelo?\n")
        self.exibir_opcoes_chatbot([
            ("Sim, sobre DS-2CD2047G2-LU", lambda: self.exibir_mensagem_chatbot("\nO modelo DS-2CD2047G2-LU tem resolução de 4MP e visão noturna colorida. É da Hikvision.\n")),
            ("Sim, sobre DS-2CD1143G0-I", lambda: self.exibir_mensagem_chatbot("\nO modelo DS-2CD1143G0-I tem resolução de 4MP e é mais compacto, ideal para escritórios. É da Hikvision.\n")),
            ("Não, voltar", self.opcao_cftv)
        ])

    def opcao_cftv_nvr_dvr(self):
        self.exibir_mensagem_chatbot("\nSobre NVRs e DVRs:\n")
        self.exibir_mensagem_chatbot("Os NVRs como o DS-7608NI-K1 suportam até 8 canais, enquanto o DS-7732NI-K4 suporta até 32 canais.\n")
        self.exibir_mensagem_chatbot("Você precisa de ajuda para escolher um modelo?\n")
        self.exibir_opcoes_chatbot([
            ("Sim, para 8 canais", lambda: self.exibir_mensagem_chatbot("\nRecomendo o DS-7608NI-K1. Ele suporta 8 canais e é da Hikvision.\n")),
            ("Sim, para mais canais", lambda: self.exibir_mensagem_chatbot("\nO DS-7732NI-K4 suporta até 32 canais e é ideal para projetos maiores. É da Hikvision.\n")),
            ("Não, voltar", self.opcao_cftv)
        ])

    def opcao_cftv_outros(self):
        self.exibir_mensagem_chatbot("\nOutros equipamentos de CFTV:\n")
        self.exibir_mensagem_chatbot("Temos cabos, conectores RJ45, switches PoE, e HDDs para armazenamento.\n")
        self.exibir_mensagem_chatbot("Qual item você gostaria de saber mais?\n")
        self.exibir_opcoes_chatbot([
            ("HDDs", lambda: self.exibir_mensagem_chatbot("\nOferecemos HDDs de 1TB a 4TB, ideais para gravação de vídeo.\n")),
            ("Switches PoE", lambda: self.exibir_mensagem_chatbot("\nO DS-3E0105P-E é um switch PoE com 5 portas, ótimo para pequenas instalações.\n")),
            ("Voltar", self.opcao_cftv)
        ])

    def opcao_cda(self):
        self.exibir_mensagem_chatbot("\nVocê escolheu Controle de Acesso!\n")
        self.exibir_mensagem_chatbot("Posso ajudar com leitores faciais, catracas, eletroímãs e mais. Sobre o que você gostaria de falar?\n")
        self.exibir_opcoes_chatbot([
            ("Leitores Faciais", self.opcao_cda_leitores),
            ("Catracas", self.opcao_cda_catracas),
            ("Outros equipamentos", self.opcao_cda_outros),
            ("Voltar", self.iniciar_conversa_chatbot)
        ])

    def opcao_cda_leitores(self):
        self.exibir_mensagem_chatbot("\nSobre Leitores Faciais:\n")
        self.exibir_mensagem_chatbot("Temos modelos como DS-K1T341 da Hikvision e ID-FACE da Control iD.\n")
        self.exibir_mensagem_chatbot("Você gostaria de mais detalhes sobre algum modelo?\n")
        self.exibir_opcoes_chatbot([
            ("Sim, sobre DS-K1T341", lambda: self.exibir_mensagem_chatbot("\nO DS-K1T341 é um leitor facial com tela de 4.3 polegadas e suporta até 1.500 faces.\n")),
            ("Sim, sobre ID-FACE", lambda: self.exibir_mensagem_chatbot("\nO ID-FACE da Control iD é compacto e suporta até 10.000 faces.\n")),
            ("Não, voltar", self.opcao_cda)
        ])

    def opcao_cda_catracas(self):
        self.exibir_mensagem_chatbot("\nSobre Catracas:\n")
        self.exibir_mensagem_chatbot("Temos modelos como IDBLOCK NEXT FACIAL da Control iD e Ds-k3g411 da Hikvision.\n")
        self.exibir_mensagem_chatbot("Você gostaria de mais detalhes sobre algum modelo?\n")
        self.exibir_opcoes_chatbot([
            ("Sim, sobre IDBLOCK NEXT FACIAL", lambda: self.exibir_mensagem_chatbot("\nA IDBLOCK NEXT FACIAL suporta reconhecimento facial e é ideal para controle de pedestres.\n")),
            ("Sim, sobre Ds-k3g411", lambda: self.exibir_mensagem_chatbot("\nA Ds-k3g411 da Hikvision é robusta e suporta integração com leitores.\n")),
            ("Não, voltar", self.opcao_cda)
        ])

    def opcao_cda_outros(self):
        self.exibir_mensagem_chatbot("\nOutros equipamentos de Controle de Acesso:\n")
        self.exibir_mensagem_chatbot("Temos eletroímãs, fontes, fechaduras, botoeiras e controladoras.\n")
        self.exibir_mensagem_chatbot("Qual item você gostaria de saber mais?\n")
        self.exibir_opcoes_chatbot([
            ("Eletroímãs", lambda: self.exibir_mensagem_chatbot("\nO FE 20150 da Intelbras é um eletroímã robusto para portas.\n")),
            ("Controladoras", lambda: self.exibir_mensagem_chatbot("\nA DS-K2602T da Hikvision suporta até 4 portas.\n")),
            ("Voltar", self.opcao_cda)
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

    def toggle_lista_tipos_cda(self):
        if self.cda_visivel:
            self.toggle_lista_cda()
        if self.cftv_visivel:
            self.toggle_lista_cftv()
        if self.chatbot_visivel:
            self.toggle_lista_chatbot()

        if self.tipo_cda_visivel:
            if self.consulta_container:
                self.consulta_container.destroy()
            self.tipo_cda_visivel = False
        else:
            self.consulta_container = tk.Frame(self.content_frame, bg="#F5F6F5")
            self.consulta_container.pack(fill=tk.X, padx=10, pady=10)

            tk.Label(
                self.consulta_container, text="Consulta", font=self.fonte_label, bg="#F5F6F5", fg="#2B2D42"
            ).pack(anchor="w", pady=5)

            btn_frame = tk.Frame(self.consulta_container, bg="#F5F6F5")
            btn_frame.pack(anchor="w", pady=10)

            self.tipo_cda_botao = tk.Button(
                btn_frame, text="Porta", command=self.mostrar_menu_porta,
                font=self.fonte_botao, fg="white", bg="#8D99AE", relief="flat",
                width=15, height=2
            )
            self.tipo_cda_botao.pack(side=tk.LEFT, padx=5)

            self.botao_pedestre = tk.Button(
                btn_frame, text="Pedestre", command=self.mostrar_menu_pedestre,
                font=self.fonte_botao, fg="white", bg="#8D99AE", relief="flat",
                width=15, height=2
            )
            self.botao_pedestre.pack(side=tk.LEFT, padx=5)

            self.botao_Veicular = tk.Button(
                btn_frame, text="Veicular", command=self.mostrar_menu_Veicular,
                font=self.fonte_botao, fg="white", bg="#8D99AE", relief="flat",
                width=15, height=2
            )
            self.botao_Veicular.pack(side=tk.LEFT, padx=5)

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
            "• Catraca/ verificar modelo.\n\n"
            "• Terminal Facial/ verificar modelo.\n\n"
            "• Suporte para facial."
        )
        messagebox.showinfo("Catraca", mensagem)

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

    def confirmar_conclusao_cda(self):
        nome_empresa = self.nome_entry.get()
        if not nome_empresa:
            messagebox.showwarning("Atenção", "Por favor, preencha o nome da empresa antes de confirmar os itens.")
            return

        selecionados = []
        for item, var in self.checkboxes_cda.items():
            if var.get():
                quantidade = self.quantidades_cda.get(item, None)
                quantidade_valor = quantidade.get() if quantidade else "N/A"

                if item in self.modelos_cda:
                    modelo = self.modelos_cda[item].get()
                    selecionados.append(f"CDA: {item} - Modelo: {modelo} - Quantidade: {quantidade_valor}")
                else:
                    selecionados.append(f"CDA: {item} - Quantidade: {quantidade_valor}")

        if selecionados:
            nome_arquivo = f"{nome_empresa}_CDA.txt"
            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write("Itens Selecionados (CDA):\n")
                arquivo.write("\n".join(selecionados))
            print(f"Arquivo '{nome_arquivo}' criado com sucesso.")

        messagebox.showinfo("Arquivo Gerado", "FOI GERADO UM ARQUIVO DE PROJETO")

    def confirmar_conclusao_cftv(self):
        nome_empresa = self.nome_entry.get()
        if not nome_empresa:
            messagebox.showwarning("Atenção", "Por favor, preencha o nome da empresa antes de confirmar os itens.")
            return

        selecionados = []
        for item, var in self.checkboxes_cftv.items():
            if var.get():
                spinbox = self.quantidades_cftv[item]
                quantidade_valor = int(spinbox.get())

                if quantidade_valor > 0:
                    modelo = self.modelos_cftv.get(item, tk.StringVar()).get()
                    if modelo and modelo != "Selecione um modelo":
                        selecionados.append(f"CFTV: {item} - Modelo: {modelo} - Quantidade: {quantidade_valor}")
                    else:
                        selecionados.append(f"CFTV: {item} - Quantidade: {quantidade_valor}")

        if selecionados:
            nome_arquivo = f"{nome_empresa}_CFTV.txt"
            with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
                arquivo.write("Itens Selecionados (CFTV):\n")
                arquivo.write("\n".join(selecionados))
            print(f"Arquivo '{nome_arquivo}' criado com sucesso.")

        messagebox.showinfo("Arquivo Gerado", "FOI GERADO UM ARQUIVO DE PROJETO")

    def iniciar(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = Interface()
    app.iniciar()