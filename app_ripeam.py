import streamlit as st
import random

# ==========================================
# 1. BASE DE DADOS (CONTEÚDO)
# ==========================================

questoes_taticas = [
    {
        "cenario": "O seu navio de propulsão mecânica (Navio Alfa) navega no rumo 000° à noite. Avista aos 315° Relativos (amura de bombordo) as seguintes luzes: duas luzes de mastro brancas, uma luz verde e três luzes encarnadas na vertical. A marcação é constante. Qual a atitude correta?",
        "opcoes": [
            "(a) O Navio Alfa tem preferência (avistou por bombordo). Deve manter rumo e velocidade.",
            "(b) Trata-se de uma embarcação a pescar por arrasto. O Navio Alfa guina para bombordo.",
            "(c) O Navio Alfa deve manobrar para se manter fora do caminho, pois a outra embarcação está restrita devido ao seu calado.",
            "(d) Trata-se de um rebocador. O Navio Alfa deve guinar para boreste e cruzar a popa."
        ],
        "resposta_correta": 2, # Índice da opção (c)
        "explicacao": "**Regra 28 e 18:** Três luzes encarnadas na vertical indicam uma embarcação restrita devido ao seu calado. Pela Regra 18(d), o seu navio (propulsão mecânica) deve evitar cruzar a proa desta embarcação, perdendo a preferência que teria numa situação normal de rumos cruzados (Regra 15)."
    },
    {
        "cenario": "Um Navio Petroleiro navega num canal estreito e aproxima-se de uma curva onde a visibilidade é obscurecida. Qual o sinal sonoro correto a emitir segundo a Regra 34(e)?",
        "opcoes": [
            "(a) Dois apitos curtos.",
            "(b) Um apito longo.",
            "(c) Três apitos curtos.",
            "(d) Um apito longo seguido de dois curtos."
        ],
        "resposta_correta": 1, # Índice da opção (b)
        "explicacao": "**Regra 9(f) e 34(e):** Embarcações a aproximar-se de uma curva num canal estreito devem fazer soar um apito longo. Qualquer embarcação a aproximar-se no outro sentido, do outro lado da curva, deverá responder com um apito longo."
    }
]

flashcards = [
    {
        "frente": "Qual a distância vertical mínima exigida entre a luz de mastro de vante e a de ré para navios com 50 metros ou mais? (Anexo I)",
        "verso": "Mínimo de **4,5 metros** de diferença na vertical. A luz de ré deve estar obrigatoriamente mais alta."
    },
    {
        "frente": "Sinais Sonoros (Regra 35) - Qual o intervalo para um navio de propulsão mecânica em movimento, MAS parado e sem seguimento, em visibilidade restrita?",
        "verso": "Intervalos não superiores a **2 minutos**, emitindo **DOIS apitos longos** (separados por cerca de 2 segundos entre si)."
    },
    {
        "frente": "Marcas Diurnas - O que significa a exibição de três esferas pretas numa linha vertical?",
        "verso": "**Embarcação encalhada** (Regra 30). *Dica: Duas esferas é sem governo, três esferas é encalhada.*"
    }
]

# ==========================================
# 2. CONFIGURAÇÃO DO ESTADO DA APLICAÇÃO (MEMÓRIA)
# ==========================================

if 'q_atual' not in st.session_state:
    st.session_state.q_atual = 0
if 'mostrar_explicacao' not in st.session_state:
    st.session_state.mostrar_explicacao = False
if 'fc_atual' not in st.session_state:
    st.session_state.fc_atual = 0
if 'fc_virado' not in st.session_state:
    st.session_state.fc_virado = False

# ==========================================
# 3. INTERFACE DA APLICAÇÃO (UI)
# ==========================================

st.set_page_config(page_title="App RIPEAM Tático", page_icon="⚓", layout="centered")

st.sidebar.title("⚓ Navegação RIPEAM")
st.sidebar.write("Escolha o módulo de estudo:")
modulo = st.sidebar.radio("", ["Quiz Tático", "Flashcards (Decoreba)"])

if modulo == "Quiz Tático":
    st.title("🎯 Simulador de Cenários Táticos")
    st.write("Analise a situação cinemática e escolha a atitude correta segundo o COLREG/RIPEAM.")
    
    questao = questoes_taticas[st.session_state.q_atual]
    
    st.markdown(f"### Cenário {st.session_state.q_atual + 1}")
    st.info(questao["cenario"])
    
    # Formulário de resposta
    escolha = st.radio("Selecione a sua manobra:", questao["opcoes"], index=None)
    
    if st.button("Submeter Manobra"):
        if escolha:
            idx_escolha = questao["opcoes"].index(escolha)
            if idx_escolha == questao["resposta_correta"]:
                st.success("✅ Excelente! Manobra correta e segura.")
            else:
                st.error("❌ Risco de Abalroamento! Manobra incorreta.")
            st.session_state.mostrar_explicacao = True
        else:
            st.warning("Selecione uma opção antes de submeter.")
            
    if st.session_state.mostrar_explicacao:
        st.markdown("---")
        st.markdown("### 📚 Análise da Regra")
        st.write(questao["explicacao"])
        
        if st.button("Próximo Cenário ➡️"):
            st.session_state.q_atual = (st.session_state.q_atual + 1) % len(questoes_taticas)
            st.session_state.mostrar_explicacao = False
            st.rerun()

elif modulo == "Flashcards (Decoreba)":
    st.title("📇 Flashcards de Memorização")
    st.write("Treine a sua memória fotográfica para os Anexos e sinais sonoros.")
    
    cartao = flashcards[st.session_state.fc_atual]
    
    st.markdown(f"**Cartão {st.session_state.fc_atual + 1} de {len(flashcards)}**")
    
    # Desenhar o cartão
    st.markdown("### ❓ Pergunta:")
    st.info(cartao["frente"])
    
    if not st.session_state.fc_virado:
        if st.button("🔄 Virar Cartão"):
            st.session_state.fc_virado = True
            st.rerun()
    else:
        st.markdown("### 💡 Resposta:")
        st.success(cartao["verso"])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Ocultar Resposta"):
                st.session_state.fc_virado = False
                st.rerun()
        with col2:
            if st.button("Próximo Cartão ➡️"):
                st.session_state.fc_atual = (st.session_state.fc_atual + 1) % len(flashcards)
                st.session_state.fc_virado = False
                st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido para treino intensivo de Oficiais e Práticos.")
