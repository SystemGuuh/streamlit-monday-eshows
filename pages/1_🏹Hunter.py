import streamlit as st
from utils.monday import *
from utils.queries import *
import pandas as pd
from datetime import datetime, date

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
                                'Propostas lançadas?', 'Observação Hunting', 'Hunter Responsável']]

def createView(df, hunter):
     return df[df['Hunter Responsável'] == hunter].reset_index(drop=True)

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
    #se datafrma contem mais de uma linha, vamos printar so a primeira demanda de cada casa
    if len(df) > 1:
        for indice, linha in df.iterrows():
            valor_anterior = None
            for coluna in df.columns[11:24]:
                valor = linha[coluna]
                if valor is None or str(valor) == '':
                    nome = linha['Nome']
                    st.markdown(f'- "**{nome}**" está com o campo vazio e precisa ser preenchido.')
                    valor_anterior = None
                    break
                elif str(valor).lower() == 'parado' and valor_anterior != 'não aplica':
                    nome = linha['Nome']
                    st.markdown(f'- "**{nome}**" está com o campo "**{coluna}**" parado.')
                    valor_anterior = valor.lower()
                    break
                else: valor_anterior = valor.lower()
    #senão, mostramos todas as demandar de uma casa
    else:
        for indice, linha in df.iterrows():
            valor_anterior = None
            for coluna in df.columns[11:24]:
                valor = linha[coluna]
                if valor is None or str(valor) == '':
                    nome = linha['Nome']
                    st.markdown(f'- "**{nome}**" está com o campo vazio e precisa ser preenchido.')
                    valor_anterior = None
                    continue
                elif str(valor).lower() == 'parado' and valor_anterior != 'não aplica':
                    nome = linha['Nome']
                    st.markdown(f'- "**{nome}**" está com o campo "**{coluna}**" parado.')
                valor_anterior = valor.lower()
                
def showDataByDayabase(df, dfMonday, id_casa, nome_casa):
    controladoria=None
    day=None; day2=None

    # trata casas desativadas
    if df['CASA_ATIVA'].iloc[0] != 1:
        st.markdown('### Status atuais da casa: <span style="color:red">desativada</span>', unsafe_allow_html=True)
        return -1
    
    st.markdown(f'### Status atuais da casa {nome_casa}')
    id_casa_str = str(id_casa)  # Convertendo id_casa para string
    df = df.query(f'ID_CASA == {id_casa_str}')
    df = df.drop(columns=['ID_CASA', 'CASA', 'STATUS_COMPANY'])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if df.empty or pd.isna(df['CASTING_CADASTRADO'].iloc[0]):
            st.write('Casting: pendente...')
        else:
            st.write('Casting:', str(df['CASTING_CADASTRADO'].iloc[0]))
    with col2:
        if df.empty or pd.isna(df['USUARIOS_ATIVOS'].iloc[0]):
            st.write('Usuários ativos: pendente...')
        else:
            st.write('Usuários ativos:', str(df['USUARIOS_ATIVOS'].iloc[0]))
    with col3:
        if df.empty or pd.isna(df['CONTROLADORIA_ESHOWS'].iloc[0]):
            st.write('Controladoria: pendente...')
            controladoria=0
        else:
            st.write('Controladoria:', str(df['CONTROLADORIA_ESHOWS'].iloc[0]))
            controladoria=int(df['CONTROLADORIA_ESHOWS'].iloc[0])
    
    col4, col5, col6 = st.columns(3)
    with col4:
        if dfMonday['GMV estimado'].empty or pd.isna(dfMonday['GMV estimado'].iloc[0]):
            st.write('GMV: pendente...')
        else:
            st.write('GMV:', dfMonday['GMV estimado'].iloc[0])
    with col5:
        if dfMonday['Login criado?'].empty or pd.isna(dfMonday['Login criado?'].iloc[0]):
            st.write('Login criado precisa ser preenchido')
        else:
            st.write('Login criado?', dfMonday['Login criado?'].iloc[0])
    with col6:
        if dfMonday['Volume (qts dias a eshows terá na casa?)'].empty or pd.isna(dfMonday['Volume (qts dias a eshows terá na casa?)'].iloc[0]):
            st.write('Volume: precisa ser preenchido')
        else:
            st.write('Volume de shows:', dfMonday['Volume (qts dias a eshows terá na casa?)'].iloc[0])

    #formatando data do primeiro show, se tiver
    col7, col8 = st.columns(2)
    if df.empty or pd.isna(df['PRIMEIRO_SHOW'].iloc[0]):
        col7.write('Primeiro Show no BD: pendente...')
    else:
        with col7:
            data_str = df['PRIMEIRO_SHOW'].iloc[0]
            data_obj = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
            day = data_obj.strftime("%d/%m/%Y")
            time = data_obj.strftime("%H:%M:%S")
            st.write('Primeiro Show no BD:', day, ' às ', time)
    
    if dfMonday.empty or pd.isna(dfMonday['Início da parceria'].iloc[0]):
        col8.write('Primeiro Show no Monday: pendente...')
    else:
        with col8:
            data_str = dfMonday['Início da parceria'].iloc[0]
            data_obj = datetime.strptime(data_str, "%Y-%m-%d")
            day2 = data_obj.strftime("%d/%m/%Y")
            st.write('Primeiro Show no Monday:', day2)

    #verificando casting
    if (str(df['CASTING_CADASTRADO'].iloc[0] == '0')):
        st.error("Casting igual a 0 é um problema.")
    #verificar se os dados batem ou se há valores nulos
    if day != day2:
        st.error("Primeiro show e início da parceria apresentam valores diferentes")
    #verificando controladoria em relação a data atual(so da pra fazer se a data tiver cadastrada corretamente)
    else:
        today = date.today().strftime("%d/%m/%Y")
        if today < day and controladoria == 0:
            #calcula quando dias faltam
            today_datetime = datetime.strptime(today, "%d/%m/%Y")
            day_datetime = datetime.strptime(day, "%d/%m/%Y")
            remaining = (day_datetime - today_datetime).days

            st.error(f"Controladoria precisa ser preenchido antes do dia {day}, faltam {remaining} dias.")

def showMissingRegisterValuesFromDatabase(id):
    df = getMissingRegisterValue(id)
    st.markdown("#### Dados incompletos da casa:")
    missingValues = df['ERRO_CADASTRO'].astype(str).iloc[0]
    missingValues = missingValues.split('-')
    for value in missingValues:
        st.markdown(f'{value}')

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
            st.markdown(f"### Próximos passos de cada casa")
            printStopedItens(radarMondaydf ,filterHunter)


        if filterHause:
            tab1, tab2= st.tabs(["Pendências", "Situação Cadastral"])
            with tab1:
                showDataByDayabase(cleanBdDataUsingMonday(radarMondaydf, getRadarDataFromLocal()), radarMondaydf[radarMondaydf['Nome'] == filterHause],df.loc[df['Nome'] == filterHause, 'ID EPM'].iloc[0], filterHause)

                if(checkStopedItens(radarMondaydf[radarMondaydf['Nome']  == filterHause],filterHunter)):
                    with st.expander("⚠️ Lista de pendências para resolver"):
                        printStopedItens(radarMondaydf[radarMondaydf['Nome'] == filterHause] ,filterHunter)
                else:
                    st.success("Essa casa não tem pendências no Monday para resolver!!")
            with tab2:
                stringObs = radarMondaydf.loc[radarMondaydf['Nome'] == filterHause, 'Observação Hunting'].astype(str).iloc[0]
                st.markdown("#### Observação do hunter:")
                st.write(stringObs)
                showMissingRegisterValuesFromDatabase(radarMondaydf.loc[radarMondaydf['Nome'] == filterHause, 'ID EPM'].astype(int).iloc[0])
        
        else:
            st.warning('Selecione dados de uma casa para ver mais campos e próximos passos.')
    
    

    else:
        st.divider()
        st.markdown("### Radar do Monday")
        st.dataframe(radarMondaydf, hide_index=True)
else: 
    st.error("Erro de requisição, não foi possível coletar os dados do Monday.")   