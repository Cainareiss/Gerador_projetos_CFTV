import tkinter as tk


class DropdownMenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dropdown Menu")
        self.root.geometry("400x200")
        self.root.configure(bg="#ECF0F1")

        # Criar o botão principal
        self.main_button = tk.Button(
            root,
            text="Selecionar Idioma",
            font=("Arial", 14),
            bg="#27AE60",
            fg="white",
            command=self.toggle_menu,
        )
        self.main_button.pack(pady=20)

        # Criar o menu suspenso (inicialmente oculto)
        self.menu_frame = tk.Frame(root, bg="#ECF0F1")
        self.menu_frame.pack()

        self.menu_visible = False  # Controla se o menu está visível

        # Adicionar as opções ao menu
        self.add_menu_option("English", "//nwaypro.com/.../en.png", lambda: self.set_language("English"))
        self.add_menu_option("Português", "//nwaypro.com/.../brasil.png", lambda: self.set_language("Português"))
        self.add_menu_option("Spanish", "//nwaypro.com/.../es.png", lambda: self.set_language("Spanish"))

    def add_menu_option(self, text, img_url, command):
        """Adiciona uma opção ao menu."""
        button = tk.Button(
            self.menu_frame,
            text=text,
            font=("Arial", 12),
            bg="white",
            fg="#34495E",
            relief=tk.GROOVE,
            command=command,
        )
        button.pack(fill=tk.X, pady=2)

    def toggle_menu(self):
        """Exibe ou oculta o menu."""
        if self.menu_visible:
            self.menu_frame.pack_forget()
        else:
            self.menu_frame.pack()
        self.menu_visible = not self.menu_visible

    def set_language(self, language):
        """Ação executada ao selecionar um idioma."""
        print(f"Idioma selecionado: {language}")
        self.main_button.config(text=f"Idioma: {language}")
        self.toggle_menu()


# Inicializar a interface
if __name__ == "__main__":
    root = tk.Tk()
    app = DropdownMenuApp(root)
    root.mainloop()
