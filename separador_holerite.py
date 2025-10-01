import PyPDF2
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os

def separar_pdf():
    # Abre janela para escolher o PDF
    arquivo_pdf = filedialog.askopenfilename(
        title="Selecione o PDF de Holerites",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )

    if not arquivo_pdf:
        return

    # Cria pasta de saída na mesma pasta do PDF
    pasta_saida = os.path.join(os.path.dirname(arquivo_pdf), "Holerites Separados")
    os.makedirs(pasta_saida, exist_ok=True)

    # Abre PDF
    with open(arquivo_pdf, "rb") as pdf_file:
        leitor = PyPDF2.PdfReader(pdf_file)

        for num_pagina in range(len(leitor.pages)):
            # Pede o nome para cada página
            nome = simpledialog.askstring(
                "Nome da Pessoa",
                f"Digite o nome para a página {num_pagina + 1}:"
            )

            if not nome:
                nome = f"Pessoa_{num_pagina+1}"  # fallback se não digitar nada

            escritor = PyPDF2.PdfWriter()
            escritor.add_page(leitor.pages[num_pagina])

            nome_arquivo = os.path.join(pasta_saida, f"Holerite - {nome}.pdf")

            with open(nome_arquivo, "wb") as saida:
                escritor.write(saida)

            print(f"✅ Criado: {nome_arquivo}")

    messagebox.showinfo("Concluído", f"Holerites separados em:\n{pasta_saida}")

# Interface gráfica simples
root = tk.Tk()
root.title("Separador de Holerites")
root.geometry("300x150")

label = tk.Label(root, text="Clique no botão para separar o PDF", pady=20)
label.pack()

botao = tk.Button(root, text="Selecionar PDF", command=separar_pdf)
botao.pack(pady=10)

root.mainloop()
