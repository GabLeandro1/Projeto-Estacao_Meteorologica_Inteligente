import csv
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==========================================================
# CONFIGURAÇÃO DO ARQUIVO
# ==========================================================

nome_arquivo = r'C:\Users\gabri\Downloads\Projeto\Projeto\dados_estacao_meteorologica_set_out_2026.csv'


# ==========================================================
# LISTAS QUE ARMAZENAM OS DADOS
# ==========================================================

datas = []
temperaturas = []
umidades = []
pressoes = []
luminosidades = []
chuvas = []


# ==========================================================
# FUNÇÃO PARA LER O ARQUIVO E CARREGAR OS DADOS
# ==========================================================

def carregar_dados():
    datas.clear()
    temperaturas.clear()
    umidades.clear()
    pressoes.clear()
    luminosidades.clear()
    chuvas.clear()
    total_registros = 0

    try:
        with open(nome_arquivo, 'r', encoding='utf-8-sig', newline='') as arquivo:
            leitor = csv.reader(arquivo, delimiter=';')

            # Lê o cabeçalho
            cabecalho = next(leitor, None)

            if cabecalho is None:
                messagebox.showwarning(
                    'Aviso',
                    'O arquivo CSV está vazio.'
                )
                return

            # Percorre as linhas do arquivo
            for linha in leitor:

                # Ignora linhas vazias ou incompletas
                if not linha or len(linha) < 6:
                    continue

                try:
                    # A data e a hora estão na mesma coluna
                    data_hora_completa = linha[0].strip()

                    temp_str = linha[1].strip()
                    umidade_str = linha[2].strip()
                    pressao_str = linha[3].strip()
                    luminosidade_str = linha[4].strip()
                    chuva_str = linha[5].strip()

                    # Converte a data e a hora para o formato datetime.
                    # Aceita data com vírgula ou sem vírgula.
                    data_hora_completa = data_hora_completa.strip()

                    try:
                        data_convertida = datetime.strptime(
                            data_hora_completa,
                            '%d/%m/%Y, %H:%M:%S'
                        )
                    except ValueError:
                        data_convertida = datetime.strptime(
                            data_hora_completa,
                            '%d/%m/%Y %H:%M:%S'
                        )

                    # Trata e converte a temperatura
                    temperatura_num = float(
                        temp_str.replace('°C', '').strip().replace(',', '.')
                    )

                    # Trata a umidade
                    umidade_num = float(
                        umidade_str.replace('%', '').strip().replace(',', '.')
                    )

                    # Trata a pressão
                    pressao_num = float(
                        pressao_str.replace('hPa', '').strip().replace(',', '.')
                    )

                    # Trata a luminosidade
                    luminosidade_num = float(
                        luminosidade_str.strip().replace(',', '.')
                    )

                    # Trata o indicador de chuva
                    chuva_num = float(
                        chuva_str.strip().replace(',', '.')
                    )

                    # Guarda os dados nas listas
                    datas.append(data_convertida)
                    temperaturas.append(temperatura_num)
                    umidades.append(umidade_num)
                    pressoes.append(pressao_num)
                    luminosidades.append(luminosidade_num)
                    chuvas.append(chuva_num)
                    total_registros += 1

                except (ValueError, IndexError) as erro:
                    print(
                        f'Linha ignorada por erro de formato: {linha}\n'
                        f'Detalhes: {erro}'
                    )
                    continue

        if total_registros == 0:
            messagebox.showwarning(
                'Aviso',
                'Nenhum dado válido encontrado. Verifique o formato do CSV.'
            )
            return
        # Atualiza a quantidade de registros
        label_registros.config(
            text=f'Registros carregados: {total_registros}'
        )

        # Exibe inicialmente o gráfico de temperatura
        mostrar_grafico('Temperatura')

    except FileNotFoundError:
        messagebox.showerror(
            'Erro',
            f'Arquivo não encontrado:\n{nome_arquivo}'
        )

    except UnicodeDecodeError:
        messagebox.showerror(
            'Erro de codificação',
            'Não foi possível ler o arquivo como UTF-8. '
            'Salve o CSV usando a codificação UTF-8.'
        )

    except Exception as erro:
        messagebox.showerror(
            'Erro',
            f'Ocorreu um erro inesperado:\n{erro}'
        )


# ==========================================================
# FUNÇÃO PARA ALTERNAR ENTRE OS GRÁFICOS
# ==========================================================

def mostrar_grafico(coluna):

    if not datas:
        messagebox.showwarning(
            'Aviso',
            'Primeiro, carregue os dados do arquivo CSV.'
        )
        return

    # Seleciona os valores de acordo com o botão
    unidade = ""
    if coluna == 'Temperatura':
        valores = temperaturas
        titulo = 'Evolução da Temperatura ao Longo do Tempo'
        eixo_y = 'Temperatura (°C)'
        media = sum(temperaturas) / len(temperaturas)
        unidade = "°C"

    elif coluna == 'Umidade':
        valores = umidades
        titulo = 'Evolução da Umidade ao Longo do Tempo'
        eixo_y = 'Umidade (%)'
        media = sum(umidades) / len(umidades)
        unidade = "%"

    elif coluna == 'Pressão':
        valores = pressoes
        titulo = 'Evolução da Pressão Atmosférica ao Longo do Tempo'
        eixo_y = 'Pressão (hPa)'
        media = sum(pressoes) / len(pressoes)
        unidade = "hPa"

    elif coluna == 'Luminosidade':
        valores = luminosidades
        titulo = 'Evolução da Luminosidade ao Longo do Tempo'
        eixo_y = 'Luminosidade'
        media = sum(luminosidades) / len(luminosidades)

    elif coluna == 'Chuva':
        valores = chuvas
        titulo = 'Evolução da Chuva ao Longo do Tempo'
        eixo_y = 'Chuva'
        media = sum(chuvas) / len(chuvas)
    else:
        return

    # Limpa o gráfico anterior
    fig.clear()
    ax = fig.add_subplot(111)
    if coluna == 'Temperatura' or coluna == 'Pressão' or coluna == 'Umidade':
      ax.axhline(
            y=media,
            color='red',
            linestyle='--',
            linewidth=2,
            zorder=3,
            label=f'Média: {media:.2f} {unidade}'
      )
      ax.legend()
          
    # No gráfico de chuva, usa marcadores para destacar os registros
    if coluna == 'Chuva':
        ax.plot(
            datas,
            valores,
            marker='s',
            linestyle='-',
            linewidth=1.5
        )
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['Sem chuva', 'Chuva'])

    else:
        ax.plot(
            datas,
            valores,
            zorder=2,
            marker='o',
            linestyle='-',
            linewidth=1.5
        )

    ax.set_title(titulo)
    ax.set_xlabel('Data')
    ax.set_ylabel(eixo_y)

    # Formata os horários do eixo horizontal
    fig.autofmt_xdate(rotation=45)

    # Ajusta os espaços do gráfico
    fig.tight_layout()

    # Atualiza a interface
    canvas.draw()


# ==========================================================
# CONSTRUÇÃO DA INTERFACE GRÁFICA
# ==========================================================

janela = tk.Tk()
janela.title('Dashboard Meteorológico')
janela.geometry('1100x750')
janela.minsize(800, 550)

# Título
titulo_label = tk.Label(
    janela,
    text='Dashboard Meteorológico',
    font=('Arial', 18, 'bold')
)
titulo_label.pack(pady=(10, 5))

# Informações sobre os dados
label_registros = tk.Label(
    janela,
    text='Registros carregados: 0',
    font=('Arial', 10)
)
label_registros.pack(pady=2)


# ==========================================================
# BOTÕES PARA SELECIONAR O GRÁFICO
# ==========================================================

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

variaveis = [
    'Temperatura',
    'Umidade',
    'Pressão',
    'Luminosidade',
    'Chuva'
]

for variavel in variaveis:
    botao = tk.Button(
        frame_botoes,
        text=variavel,
        command=lambda v=variavel: mostrar_grafico(v),
        width=14,
        font=('Arial', 10)
    )
    botao.pack(side=tk.LEFT, padx=4)


# ==========================================================
# BOTÃO PARA CARREGAR O CSV
# ==========================================================

botao_carregar = tk.Button(
    janela,
    text='Carregar Dados e Gerar Gráficos',
    command=carregar_dados,
    bg='#2196F3',
    fg='white',
    font=('Arial', 10, 'bold')
)
botao_carregar.pack(pady=5)


# ==========================================================
# ÁREA DO GRÁFICO
# ==========================================================

fig = plt.Figure(figsize=(10, 5), dpi=100)

canvas = FigureCanvasTkAgg(fig, master=janela)
canvas.get_tk_widget().pack(
    padx=10,
    pady=10,
    fill=tk.BOTH,
    expand=True
)


# Mensagem inicial
mensagem_inicial = fig.add_subplot(111)
mensagem_inicial.text(
    0.5,
    0.5,
    'Clique em "Carregar Dados e Gerar Gráficos".',
    horizontalalignment='center',
    verticalalignment='center',
    transform=mensagem_inicial.transAxes
)
mensagem_inicial.set_axis_off()
canvas.draw()


# ==========================================================
# INICIA A APLICAÇÃO
# ==========================================================

janela.mainloop()