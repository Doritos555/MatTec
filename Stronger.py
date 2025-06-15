from math import sqrt, log, sin, cos, tan, exp, pi
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import random
import copy
import pandas as pd
import streamlit as st
from PIL import Image
import random
import streamlit.components.v1 as components 

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
        st.write("Lista de matrizes vazia, nada a exibir!")
        return None

    fig, ms_plots = plt.subplots(1, len(ms))

    # linha abaixo é para o caso de só ter uma matriz na lista
    ms_plots = [ms_plots] if len(ms) == 1 else ms_plots

    for ms_plot, mi, ti in zip(ms_plots, ms, ts):
        imprime_matriz(mi, m_plot=ms_plot, title=ti)
    
    fig.suptitle(title, fontsize=16)
    plt.tight_layout(w_pad = 1.5, # distância entre os subplots
                     rect = [0, 0, 1, 0.95]) # espaço para o título

    return fig

def recebe_matriz_manual_streamlit(n, k):
    matriz = []
    st.write("Insira os valores da matriz:")
    for i in range(n):
        linha = []
        cols = st.columns(k)
        for j in range(k):
            valor = cols[j].number_input(f"[{i}][{j}]", key=f"manual_{i}_{j}")
            linha.append(valor)
        matriz.append(linha)
    return matriz

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

    return m

def soma_matrizes_np(m1, m2):
    try:
        a = np.array(m1)
        b = np.array(m2)
        if a.shape != b.shape:
            st.error("As matrizes devem ter as mesmas dimensões para soma.")
            st.image("Aqua.gif")
            return None
        soma = np.add(a, b)
        return soma.tolist()
    except Exception as e:
        st.error(f"Erro ao somar matrizes: {e}")
        st.image("Fing.gif")
        return None

def multiplica_escalar_np(m, escalar):
    aux = np.array(m)
    aux = aux * escalar
    aux = aux.tolist()
    return aux

def inversa_matriz_np(m):
    aux = np.array(m)
    try:
        aux = np.linalg.inv(aux)
    except np.linalg.LinAlgError:
        st.error("Matriz singular, não é possível calcular a inversa.")
        st.image("Jack.gif")
        return None
    aux = aux.tolist()
    return aux

def produto_2_matrizes_np(ms):
    aux1 = np.array(ms[0])
    aux2 = np.array(ms[1])
    try:
        aux = np.dot(aux1, aux2)
    except ValueError:
        st.error("Dimensões incompatíveis para multiplicação.")
        return None
    aux = aux.tolist()
    return aux

def transposta_matriz_np(m):
    aux = np.array(m)
    aux = np.transpose(aux)
    aux = aux.tolist()
    return aux

def determinante_matriz_np(m):
    try:
        return float(np.linalg.det(np.array(m)))
    except:
        st.error("Erro ao calcular determinante.")
        st.image("teto2.gif")
        st.audio("Sad.mp3")
        return None

def salvar_matriz_especifica_csv(idx):
    m = st.session_state.ms[idx]
    df = pd.DataFrame(m)
    return df.to_csv(index=False).encode('utf-8')

def carregar_matriz_csv(arquivo):
    try:
        df = pd.read_csv(arquivo)
        return df.values.tolist()
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return None

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
        st.session_state.exibir_matrizes = True

    st.sidebar.header("MENU")

    st.image("Tajador.webp")

    opcao = st.sidebar.selectbox(
        "SELECIONE A FUNÇÃO:",
        options=[
            "recebe matriz manual",
            "recebe matriz aleatória",
            "inversa matriz",
            "transposta matriz",
            "produto de 2 matrizes",
            "multiplica por escalar",
            "soma de 2 matrizes",
            "determinante de matriz",
            "salvar matrizes em CSV",
            "carregar matriz de CSV",
            "jogar Doom 🎮",
            "lutar contra Sans 💀",
            "limpar matrizes"
        ]
    )

    if opcao == "recebe matriz manual":
        n = st.sidebar.number_input("Número de linhas (n):", min_value=1, value=3, step=1, key="linhas_manual")
        k = st.sidebar.number_input("Número de colunas (k):", min_value=1, value=3, step=1, key="colunas_manual")

        with st.form("form_matriz_manual"):
            matriz = recebe_matriz_manual_streamlit(n, k)
            submitted = st.form_submit_button("Salvar matriz")
            if submitted:
                st.session_state.ms.append(matriz)
                st.session_state.r += 1
                st.session_state.ts.append(f"m{st.session_state.r}")

    elif opcao == "recebe matriz aleatória":
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
                if inv is not None:
                    st.session_state.r += 1
                    st.session_state.ms.append(inv)
                    st.session_state.ts.append(f"Inversa de {st.session_state.ts[idx]}")
        else:
            st.warning("Nenhuma matriz disponível.")
            st.image("Cry.gif")

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
            st.image("Neko.gif")

    elif opcao == "produto de 2 matrizes":
        if len(st.session_state.ms) >= 2:
            idx1 = st.sidebar.selectbox("Matriz 1:", range(len(st.session_state.ms)), format_func=lambda i: st.session_state.ts[i], key="m1")
            idx2 = st.sidebar.selectbox("Matriz 2:", range(len(st.session_state.ms)), format_func=lambda i: st.session_state.ts[i], key="m2")
            if st.sidebar.button("Multiplicar"):
                ms_selecionadas = [st.session_state.ms[idx1], st.session_state.ms[idx2]]
                resultado = produto_2_matrizes_np(ms_selecionadas)
                if resultado is not None:
                    st.session_state.r += 1
                    st.session_state.ms.append(resultado)
                    st.session_state.ts.append(f"{st.session_state.ts[idx1]} x {st.session_state.ts[idx2]}")
        else:
            st.warning("É necessário pelo menos duas matrizes.")
            st.image("teto.gif")

    elif opcao == "multiplica por escalar":
        if st.session_state.ms:
            idx = st.sidebar.selectbox("Matriz:", range(len(st.session_state.ms)), format_func=lambda i: st.session_state.ts[i])
            escalar = st.sidebar.number_input("Escalar:", value=2.0)
            if st.sidebar.button("Multiplicar"):
                resultado = multiplica_escalar_np(st.session_state.ms[idx], escalar)
                st.session_state.ms.append(resultado)
                st.session_state.r += 1
                st.session_state.ts.append(f"{escalar} x {st.session_state.ts[idx]}")

    elif opcao == "soma de 2 matrizes":
        if len(st.session_state.ms) >= 2:
            idx1 = st.sidebar.selectbox("Matriz 1:", range(len(st.session_state.ms)), format_func=lambda i: st.session_state.ts[i], key="soma1")
            idx2 = st.sidebar.selectbox("Matriz 2:", range(len(st.session_state.ms)), format_func=lambda i: st.session_state.ts[i], key="soma2")
            if st.sidebar.button("Somar"):
                m1 = st.session_state.ms[idx1]
                m2 = st.session_state.ms[idx2]
                resultado = soma_matrizes_np(m1, m2)
                if resultado is not None:
                    st.session_state.r += 1
                    st.session_state.ms.append(resultado)
                    st.session_state.ts.append(f"{st.session_state.ts[idx1]} + {st.session_state.ts[idx2]}")
        else:
            st.warning("É necessário pelo menos duas matrizes.")
            st.image("Fing.gif")


    elif opcao == "determinante de matriz":
        if st.session_state.ms:
            idx = st.sidebar.selectbox("Matriz:", range(len(st.session_state.ms)), format_func=lambda i: st.session_state.ts[i])
            if st.sidebar.button("Calcular Determinante"):
                det = determinante_matriz_np(st.session_state.ms[idx])
                if det is not None:
                    st.image("Deltarune.gif", use_container_width=True)
                    st.success(f"Determinante: {det:.2f}")
                    st.session_state.exibir_matrizes = False
        else:
            st.warning("Nenhuma matriz disponível.")
            st.image("teto2.gif")

    elif opcao == "salvar matrizes em CSV":
        if st.session_state.ms:
            idx = st.selectbox("Escolha a matriz para salvar:", 
                            range(len(st.session_state.ms)), 
                            format_func=lambda i: st.session_state.ts[i])

            with st.form("form_salvar_csv"):
                nome_usuario = st.text_input(
                    "Digite o nome do arquivo (sem .csv):", 
                    value=st.session_state.ts[idx]
                )

                submitted = st.form_submit_button("Clique aqui para gerar um arquivo para Download")
            
            if submitted:
                nome_arquivo_final = f"{nome_usuario.strip()}.csv"
                csv_data = salvar_matriz_especifica_csv(idx)

                st.download_button(
                    label="Clique aqui para baixar",
                    data=csv_data,
                    file_name=nome_arquivo_final,
                    mime='text/csv',
                    key="download_csv_unico"
                )
                st.image("Ralsei.gif", caption=f"'{nome_arquivo_final}' salvo com sucesso!", use_container_width=True)
                st.session_state.exibir_matrizes = False
        else:
            st.warning("Nenhuma matriz disponível para salvar.")

    elif opcao == "carregar matriz de CSV":
        arquivo = st.file_uploader("Escolha o arquivo CSV")
        if arquivo:
            if st.button("Carregar"):
                matriz = carregar_matriz_csv(arquivo)
                if matriz:
                    st.session_state.ms.append(matriz)
                    st.session_state.r += 1
                    st.session_state.ts.append(f"m{st.session_state.r} (CSV)")
                    st.success("Matriz carregada com sucesso!")


    elif opcao == "jogar Doom 🎮":
        st.subheader("Doom no Navegador")
        st.markdown("Clássico jogo de tiro em primeira pessoa dos anos 90. Divirta-se!")

        components.iframe(
            "https://js-dos.com/games/doom.exe.html",  # link da versão jogável online
            height=600,
            scrolling=True
        )

    elif opcao == "lutar contra Sans 💀":
        st.subheader("Luta contra o Sans!")
        st.markdown("Prepare-se para uma batalha difícil...")

        components.iframe(
            src="https://jcw87.github.io/c2-sans-fight/",
            height=640,
            width=960,
            scrolling=False
        )

    elif opcao == "limpar matrizes":
        if st.sidebar.button("Confirmar Limpeza"):
            st.session_state.ms.clear()
            st.session_state.ts.clear()
            st.session_state.r = 0
            st.success("Matrizes apagadas com sucesso!")
            st.image("Ralsei2.gif", caption="Matrizes apagadas com sucesso!", use_container_width=True)

    if st.session_state.exibir_matrizes:
        fig = imprime_lista_matrizes(st.session_state.ms, st.session_state.ts)
        if fig is not None:
            st.pyplot(fig)
    else:
        st.session_state.exibir_matrizes = True  # reseta para exibir na próxima vez        

if __name__ == '__main__':
    menu()
