import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
from translate import Translator  # Importa a nova biblioteca

def abrir_arquivo():
    """Abre um arquivo .json e retorna seu conteúdo."""
    caminho_arquivo = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
    )
    if not caminho_arquivo:
        return None  # Nenhum arquivo selecionado

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = json.load(f)
        return conteudo
    except (json.JSONDecodeError, UnicodeDecodeError):
        messagebox.showerror("Erro", "Arquivo JSON inválido ou formato não suportado.")
        return None

def contar_elementos(json_data):
    """Conta o número total de elementos (valores) no JSON."""
    if isinstance(json_data, dict):
        return sum(contar_elementos(valor) for valor in json_data.values())
    elif isinstance(json_data, list):
        return sum(contar_elementos(valor) for valor in json_data)
    else:
        return 1

def traduzir_json(json_data, progress_bar, progress_var):
    """Traduz os valores de um JSON para português,
    mantendo as chaves originais, reconhecendo diferentes tipos de dados
    e atualizando a barra de progresso.
    """
    total_elementos = contar_elementos(json_data)
    elementos_traduzidos = 0

    def atualizar_barra_progresso():
        nonlocal elementos_traduzidos
        elementos_traduzidos += 1
        progresso = (elementos_traduzidos / total_elementos) * 100
        progress_var.set(progresso)
        progress_bar.update()

    def traduzir_valor(valor):
        if isinstance(valor, str) and valor is not None:
            try:
                translator = Translator(to_lang="pt")  # Instancia o tradutor da nova biblioteca
                traducao = translator.translate(valor)  # Usa o método translate da nova biblioteca
                atualizar_barra_progresso()
                return traducao
            except Exception as e:
                print(f"Erro ao traduzir '{valor}': {e}")
                return valor
        return valor

    if isinstance(json_data, dict):
        for chave, valor in json_data.items():
            json_data[chave] = traduzir_valor(valor)
            if isinstance(valor, (list, dict)):
                traduzir_json(valor, progress_bar, progress_var)
    elif isinstance(json_data, list):
        for i, valor in enumerate(json_data):
            json_data[i] = traduzir_valor(valor)
            if isinstance(valor, (list, dict)):
                traduzir_json(valor, progress_bar, progress_var)

def exibir_traducao():
    """Abre o arquivo, traduz o JSON e exibe o resultado."""
    conteudo = abrir_arquivo()
    if conteudo:
        # Criar uma nova janela para exibir o progresso e o resultado
        janela_progresso = tk.Toplevel(janela)
        janela_progresso.title("Traduzindo...")
        janela_progresso.geometry("400x150")

        # Barra de progresso
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(janela_progresso, variable=progress_var, maximum=100)
        progress_bar.pack(pady=20)

        # Chamar a função traduzir_json com a barra de progresso
        traduzir_json(conteudo, progress_bar, progress_var)

        janela_progresso.destroy()  # Fechar a janela de progresso

        json_traduzido = json.dumps(conteudo, indent=4, ensure_ascii=False)
        # Criar uma nova janela para exibir o JSON traduzido
        janela_resultado = tk.Toplevel(janela)
        janela_resultado.title("JSON Traduzido")
        janela_resultado.geometry("600x400")
        texto_resultado = tk.Text(janela_resultado)
        texto_resultado.pack(expand=True, fill="both")
        texto_resultado.insert(tk.END, json_traduzido)

# Configuração da janela principal
janela = tk.Tk()
janela.title("Tradutor de JSON")

# Obter a largura e altura da tela
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

# Definir a largura e altura da janela
largura_janela = 800
altura_janela = 600

# Calcular a posição x e y para centralizar a janela
x = (largura_tela // 2) - (largura_janela // 2)
y = (altura_tela // 2) - (altura_janela // 2)

# Definir a geometria da janela
janela.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

# Botão para abrir o arquivo
botao_abrir = tk.Button(janela, text="Selecionar arquivo JSON", command=exibir_traducao)
botao_abrir.pack(pady=20)

janela.mainloop()