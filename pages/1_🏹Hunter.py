import streamlit as st
from utils.monday import *
from utils.queries import *
import pandas as pd

def getHunterData(radarMondaydf):
    return radarMondaydf[['ID EPM', 'Nome', 'Relevância do cliente', 
                               'Nome contratante', 'E-mail do contratante', 
                               'Cidade do Estabelecimento', 'GMV estimado', 
                               'Início da parceria', 'Tipo de negociação', 'Carência?', 
                               'Carência até (data)', 'Formulário Hub', 'Grupo no Whatsapp',
                                'Companie criado?', 'Criação da marca', 'Login criado?', 
                                'Cadastro de show padrão (QUEM VAI FAZER?)', 
                                'Coletar contatos de artista', 'Coletar programação', 
                                'Recebi programação do Hunter?', 
                                'Estrutura da programação (dias da semana)', 
                                'Volume (qts dias a eshows terá na casa?)',
                                'Cliente irá atuar de forma independente?',
                                'Propostas lançadas?', 'Hunter Responsável']]

def createView(df, hunter):
     return df[df['Hunter Responsável'] == hunter].reset_index(drop=True)

def checkNextSteps(df):
     searchMissingValues(df)

def checkStopedItens(df, hunter):
    try:
        df = df[df['Hunter Responsável'] == hunter]
        for coluna in df.columns[11:24]:
            for indice, valor in df[coluna].items():
                if str(valor).lower() == 'parado':
                    return True
        return False
    except Exception as e:
        st.error("Opa, valor inconsistente ou não númerico encontrado no entre colunas 11 e 24 do dataframe")
        return False

def printStopedItens(df, hunter):
    df = df[df['Hunter Responsável'] == hunter]
    for indice, linha in df.iterrows():
        valor_anterior = None
        for coluna in df.columns[11:24]:
            valor = linha[coluna]
            if str(valor).lower() == 'parado' and valor_anterior != 'não aplica':
                nome = linha['Nome']
                st.markdown(f'- "**{nome}**" está com o campo "**{coluna}**" parado.')
            valor_anterior = valor.lower()

def showDataByDayabase(df, id_casa, nome_casa):
    st.divider()

    # trata casas desativadas
    if df['CASA_ATIVA'].iloc[0] != 1:
        st.markdown('### Status atuais da casa: <span style="color:red">desativada</span>', unsafe_allow_html=True)
        return -1
    
    st.markdown(f'### Status atuais da casa {nome_casa}')
    id_casa_str = str(id_casa)  # Convertendo id_casa para string
    df = df.query(f'ID_CASA == {id_casa_str}')
    df = df.drop(columns=['ID_CASA', 'CASA', 'STATUS_COMPANY'])
    
    #condição para mostrar os dados
    #tem que ter primeiro show batendo com o monday
    #casting ter que ver se tá ok, sinal vermelho se tiver 0
    #show lançado do banco tem que estar igual ao início da parceria
    #controladoria tem que ser diferente de 0 antes da parceria
    #situação cadastral - incompleto adicionar campo para dados faltando
    #adcionar campo para comentário do hunter
    col1, col2, col3 = st.columns(3)
    with col1:
        if df.empty or pd.isna(df['CASTING_CADASTRADO'].iloc[0]):
            st.write('Casting: pendente...')
        else:
            st.write('Casting:', df['CASTING_CADASTRADO'].iloc[0])
    with col2:
        if df.empty or pd.isna(df['USUARIOS_ATIVOS'].iloc[0]):
            st.write('Usuários ativos: pendente...')
        else:
            st.write('Usuários ativos:', df['USUARIOS_ATIVOS'].iloc[0])
    with col3:
        if df.empty or pd.isna(df['CONTROLADORIA_ESHOWS'].iloc[0]):
            st.write('Controladoria: pendente...')
        else:
            st.write('Controladoria:', df['CONTROLADORIA_ESHOWS'].iloc[0])

    #formatando data se tiver
    if df.empty or pd.isna(df['PRIMEIRO_SHOW'].iloc[0]):
        st.write('Primeiro Show: pendente...')
    else:
        data_str = df['PRIMEIRO_SHOW'].iloc[0]
        data_obj = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
        day = data_obj.strftime("%d/%m/%Y")
        time = data_obj.strftime("%H:%M:%S")
        st.write('Primeiro Show:', day, ' às ', time)

st.set_page_config(page_title="Monday Hunter Data", page_icon="🏹")
col1, col2 = st.columns([4,1])
col1.markdown(f"# Radar de implantação")
col2.image("./assets/imgs/eshows-logo.png", width=100)


radarMondaydf = getHunterData(getMondayDataframe())

if  not radarMondaydf.empty:
    with st.sidebar:
            if (filterHunter := st.selectbox("Selecione Hunter", radarMondaydf['Hunter Responsável'].unique().tolist(), index=None,placeholder="Hunter")):
                filterHause = st.selectbox("Dados de uma casa", radarMondaydf[radarMondaydf['Hunter Responsável'] == filterHunter]['Nome'].unique().tolist(), index=None, placeholder="Selecione a casa")

    if filterHunter:
        st.divider()
        st.markdown(f"### Radar do {filterHunter}")
        df = createView(radarMondaydf ,filterHunter)
        st.dataframe(df, hide_index=True)

        if(checkStopedItens(radarMondaydf ,filterHunter)):
            st.divider()
            st.markdown(f"### ⚠️ Itens para resolver")
            printStopedItens(radarMondaydf ,filterHunter)


        if filterHause:
            checkNextSteps(df[df['Nome']==filterHause])
            showDataByDayabase(cleanBdDataUsingMonday(radarMondaydf, getRadarDataFromLocal()), df.loc[df['Nome'] == filterHause, 'ID EPM'].iloc[0], filterHause)
    else:
        st.divider()
        st.markdown("### Radar do Monday")
        st.dataframe(radarMondaydf, hide_index=True)
else: 
    st.error("Erro de requisição, não foi possível coletar os dados do Monday.")   