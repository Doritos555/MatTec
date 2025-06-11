from math import sqrt, log, sin, cos, tan, exp, pi
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import random
import copy
import pandas as pd
import streamlit as st

#-----------------------------#

def imprime_matriz(m, title=" ", m_plot = None, save = False, ):

    if m_plot is None:
        m_fig, m_plot = plt.subplots()

    # Novo colormap mais suave
    colors = ["#ff9999",  # vermelho claro
              "#ffffff",  # branco
              "#9999ff"]  # azul claro

    # Cria o colormap
    light_red_blue = LinearSegmentedColormap.from_list("light_red_blue", colors)
    
    m_plot.imshow(m, cmap=light_red_blue)
    #m_plot.imshow(m, cmap='coolwarm')
    #m_plot.imshow(m, cmap='viridis')

    linhas = range(len(m))
    colunas = range(len(m[0]))

    for i in linhas:
        for j in colunas:
            # arredondando para 2 casas decimais só na visualização
            m_plot.text(j, i, round(m[i][j],2), ha='center', 
                        va='center', color='black', fontsize=8) 
    
    m_plot.set_xticks(colunas)
    m_plot.set_yticks(linhas)

    m_plot.set_xticklabels(colunas)
    m_plot.set_yticklabels(linhas) 

    m_plot.xaxis.tick_top() 

    m_plot.set_title(title)

    if save:
        m_fig.savefig("matriz.png", dpi=300)

def imprime_lista_matrizes(ms, ts, title = "Lista de Matrizes"):

    if len(ms) == 0:    
        print("Lista de matrizes vazia, nada a exibir!")
        return

    fig, ms_plots = plt.subplots(1, len(ms))

    # linha abaixo é para o caso de só ter uma matriz na lista
    ms_plots = [ms_plots] if len(ms) == 1 else ms_plots

    for ms_plot, mi, ti in zip(ms_plots, ms, ts):
        imprime_matriz(mi, m_plot=ms_plot, title=ti)
    
    fig.suptitle(title, fontsize=16)
    plt.tight_layout(w_pad = 1.5, # distância entre os subplots
                     rect = [0, 0, 1, 0.95]) # espaço para o título

    return fig

def recebe_matriz_manual(n, k):
   
    m = []
    linhas = range(n)
    colunas = range(k)
    
    for i in linhas:
        linha = []
        for j in colunas:
            elemento = input(f"Elemento [{i}][{j}]: ")
            linha.append(float(elemento)) # admite float
        m.append(linha)
    
    return m

def recebe_matriz_aleatoria(n, k):
    m = []
    linhas = range(n)
    colunas = range(k)

    for i in linhas:
        linha = []
        for j in colunas:
            num = random.randint(-10, 10)
            linha.append(int(num))
        m.append(linha)

    return(m)

def multiplica_escalar_np(m, escalar):

    aux = np.array(m)
    aux = aux * escalar
    aux = aux.tolist()
    return aux

def inversa_matriz_np(m):

    aux = np.array(m)
    aux = np.linalg.inv(aux)
    aux = aux.tolist()
    return aux

def produto_2_matrizes_np(ms):

    aux1 = np.array(ms[0])
    aux2 = np.array(ms[1])
    aux = np.dot(aux1, aux2)
    aux = aux.tolist()
    return aux

def transposta_matriz_np(m):
    
    aux = np.array(m)
    aux = np.transpose(aux)
    aux = aux.tolist()
    return aux

#-----------------------------#

def menu():
    
    st.title("Mini-App de Matrizes")
    st.write("""
             Minha primeira App Web! Tão Feliz
             TAJADOR
              """)

    if 'ms' not in st.session_state:
        st.session_state.ms = []
        st.session_state.ts = []
        st.session_state.r = 0

    st.sidebar.header("MENU")

    st.image("Tajador.wepb")

    opcao = st.sidebar.selectbox(
        "SELECIONE A FUNÇÃO:",
        options=[
            "recebe matriz aleatória",
            "inversa matriz",
            "transposta matriz",
            "produto de 2 matrizes",
            "limpar matrizes"
        ]
    )

    if opcao == "recebe matriz aleatória":
        n = st.sidebar.number_input("Número de linhas (n):", min_value=1, value=3, step=1)
        k = st.sidebar.number_input("Número de colunas (k):", min_value=1, value=3, step=1)

        if st.sidebar.button("Executar"):
            m = recebe_matriz_aleatoria(n=n, k=k)
            st.session_state.ms.append(m)
            st.session_state.r += 1
            st.session_state.ts.append(f"m{st.session_state.r}")

    elif opcao == "inversa matriz":
        if st.session_state.ms:
            idx = st.sidebar.selectbox("Escolha a matriz:", range(len(st.session_state.ms)), format_func=lambda i: st.session_state.ts[i])
            if st.sidebar.button("Calcular Inversa"):
                inv = inversa_matriz_np(st.session_state.ms[idx])
                if inv:
                    st.session_state.r += 1
                    st.session_state.ms.append(inv)
                    st.session_state.ts.append(f"Inversa de {st.session_state.ts[idx]}")
        else:
            st.warning("Nenhuma matriz disponível.")

    elif opcao == "transposta matriz":
        if st.session_state.ms:
            idx = st.sidebar.selectbox("Escolha a matriz:", range(len(st.session_state.ms)), format_func=lambda i: st.session_state.ts[i])
            if st.sidebar.button("Calcular Transposta"):
                trans = transposta_matriz_np(st.session_state.ms[idx])
                st.session_state.r += 1
                st.session_state.ms.append(trans)
                st.session_state.ts.append(f"Transposta de {st.session_state.ts[idx]}")
        else:
            st.warning("Nenhuma matriz disponível.")

    elif opcao == "produto de 2 matrizes":
        if len(st.session_state.ms) >= 2:
            idx1 = st.sidebar.selectbox("Matriz 1:", range(len(st.session_state.ms)), format_func=lambda i: st.session_state.ts[i], key="m1")
            idx2 = st.sidebar.selectbox("Matriz 2:", range(len(st.session_state.ms)), format_func=lambda i: st.session_state.ts[i], key="m2")
            if st.sidebar.button("Multiplicar"):
                ms_selecionadas = [st.session_state.ms[idx1], st.session_state.ms[idx2]]
                resultado = produto_2_matrizes_np(ms_selecionadas)
                if resultado:
                    st.session_state.r += 1
                    st.session_state.ms.append(resultado)
                    st.session_state.ts.append(f"{st.session_state.ts[idx1]} x {st.session_state.ts[idx2]}")
        else:
            st.warning("É necessário pelo menos duas matrizes.")


    elif opcao == "limpar matrizes":
        if st.sidebar.button("Confirmar Limpeza"):
            st.session_state.ms.clear()
            st.session_state.ts.clear()
            st.session_state.r = 0
            st.success("Matrizes apagadas com sucesso!")

    fig = imprime_lista_matrizes(st.session_state.ms, st.session_state.ts)
    if fig is not None:
        st.pyplot(fig)


if __name__ == '__main__':
    menu()
