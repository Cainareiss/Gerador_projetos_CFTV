import tkinter as tk
from tkinter import Toplevel, messagebox
from tkintervideo import TkinterVideo

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicação com Vídeo")
        self.root.geometry("800x600")

        # Inicia o popup com vídeo ao abrir a interface
        self.mostrar_video_popup()

    def mostrar_video_popup(self):
        # Cria a janela secundária (popup)
        popup = Toplevel(self.root)
        popup.title("Vídeo de Boas-Vindas")
        popup.geometry("640x480")
        popup.resizable(False, False)

        # Adiciona o vídeo
        videoplayer = TkinterVideo(master=popup, scaled=True)
        videoplayer.load(r"caminho_para_o_video.mp4")  # Coloque o caminho do vídeo
        videoplayer.pack(expand=True, fill="both")

        # Reproduz o vídeo
        videoplayer.play()

        # Fecha o popup automaticamente ao final do vídeo
        def fechar_popup():
            popup.destroy()

        # Vincula o evento de fim do vídeo
        videoplayer.bind("<<Ended>>", lambda e: fechar_popup())

        # Opcional: Mensagem de boas-vindas após o vídeo
        def mensagem_boas_vindas():
            messagebox.showinfo("Bem-vindo", "Bem-vindo ao sistema!")

        videoplayer.bind("<<Ended>>", lambda e: [fechar_popup(), mensagem_boas_vindas()])


if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
