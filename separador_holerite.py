import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pdfplumber
import PyPDF2
import os

def separar_holerites():
    arquivo_pdf = filedialog.askopenfilename(
        title="Selecione o PDF de holerites",
        filetypes=[("PDF", "*.pdf")]
    )
    if not arquivo_pdf:
        return

    pasta_saida = os.path.join(os.path.dirname(arquivo_pdf), "Holerites Separados")
    os.makedirs(pasta_saida, exist_ok=True)

    with open(arquivo_pdf, "rb") as f:
        leitor = PyPDF2.PdfReader(f)

        with pdfplumber.open(arquivo_pdf) as pdf:
            total_paginas = len(pdf.pages)
            progresso["maximum"] = total_paginas

            for i, page in enumerate(pdf.pages):
                texto = page.extract_text() or ""

                nome = f"Funcionario_{i+1}"  # fallback
                for linha in texto.split("\n"):
                    if "Nome:" in linha:
                        nome = linha.replace("Nome:", "").strip()
                        break

                escritor = PyPDF2.PdfWriter()
                escritor.add_page(leitor.pages[i])

                nome_arquivo = os.path.join(pasta_saida, f"Extrato-{nome}.pdf")
                with open(nome_arquivo, "wb") as saida:
                    escritor.write(saida)

                progresso["value"] = i + 1
                root.update_idletasks()

    messagebox.showinfo("Concluído", f"Todos os holerites foram separados em:\n{pasta_saida}")
    progresso["value"] = 0

root = tk.Tk()
root.title("Separador de Holerites")
root.geometry("400x180")
root.resizable(False, False)

label = tk.Label(root, text="Clique no botão para separar os holerites por página", pady=20)
label.pack()

btn = tk.Button(root, text="Selecionar PDF", command=separar_holerites, width=20)
btn.pack(pady=10)

progresso = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progresso.pack(pady=20)

root.mainloop()
