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
                                'Cadastro de show padrão',
                                'Coletar contatos de artista', 'Coletar programação',
                                'Recebi programação do Hunter?',
                                'Estrutura da programação (dias da semana)',
                                'Volume (qts gigs a eshows terá na casa?)',
                                'Cliente irá atuar de forma independente?',
                                'Propostas lançadas?','Cadastro/Onboarding de artistas', 'Observação Hunting', 'Hunter Responsável']]

def renameColumns(df):
    df = df.rename(columns={'Volume (qts gigs a eshows terá na casa?)': 'Volume'})
    return df

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

def printStopedItens(df):
    df = df.reset_index(drop=True)
    stopedItensCount = []
    stopedItensValues = []

    #calcula campos parados
    for indice, linha in df.iterrows():
        valor_anterior = None
        count =0
        for coluna in df.columns[11:24]:
            valor = linha[coluna]
            if valor is None or str(valor) == '':
                nome = linha['Nome']
                stopedItensValues.append(f'"**{nome}**" está com o campo vazio e precisa ser preenchido.\n')
                count += 1
                valor_anterior = None
                continue
            elif str(valor).lower() == 'parado' and valor_anterior != 'não aplica':
                nome = linha['Nome']
                stopedItensValues.append(f'"**{nome}**" está com o campo "**{coluna}**" parado.\n')
                count += 1
            valor_anterior = valor.lower()
        stopedItensCount.append(count)

    #printa campos parados
    aux = 0
    for indice, linha in df.iterrows():
        if stopedItensCount[indice] > 0:
            with st.expander(f"⚠️ **{linha['Nome']}**: {stopedItensCount[indice]} itens pendentes"):
                st.write('\n'.join(map(str, stopedItensValues[aux:stopedItensCount[indice]])))
            aux = stopedItensCount[indice]


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
    with col1: # se tiver casting cadastrado printa
        if df.empty or pd.isna(df['CASTING_CADASTRADO'].iloc[0]):
            st.write('Casting: pendente...')
        else:
            st.write('Casting:', str(df['CASTING_CADASTRADO'].iloc[0]))
    with col2: # se tiver usuarios ativos printa
        if df.empty or pd.isna(df['USUARIOS_ATIVOS'].iloc[0]):
            st.write('Usuários ativos: pendente...')
        else:
            st.write('Usuários ativos:', str(df['USUARIOS_ATIVOS'].iloc[0]))
    with col3: # se tiver estatus da controladoria printa
        if df.empty or pd.isna(df['CONTROLADORIA_ESHOWS'].iloc[0]):
            st.write('Controladoria: pendente...')
            controladoria=0
        else:
            st.write('Controladoria:', str(df['CONTROLADORIA_ESHOWS'].iloc[0]))
            controladoria=int(df['CONTROLADORIA_ESHOWS'].iloc[0])

    col4, col5, col6 = st.columns(3)
    with col4: # mostra completo caso nao tenha nada faltando no cadastro
        tempdf = pd.DataFrame(getMissingRegisterValue(id_casa))
        if tempdf['ERRO_CADASTRO'].isna().any() or tempdf['ERRO_CADASTRO'].astype(str).iloc[0] == '':
            st.markdown('Cadastro <span style="color:green">COMPLETO</span>', unsafe_allow_html=True)
        else:
            st.markdown('Cadastro <span style="color:red">INCOMPLETO</span>', unsafe_allow_html=True)
    with col5: # verifica status do login peelo banco de dados
        if dfMonday['Login criado?'].empty or pd.isna(dfMonday['Login criado?'].iloc[0]):
            st.write('Login criado precisa ser preenchido')
        else:
            st.write('Login criado?', dfMonday['Login criado?'].iloc[0])
    with col6:
        if dfMonday['Volume'].empty or pd.isna(dfMonday['Volume'].iloc[0]):
            st.write('Volume: precisa ser preenchido')
        else:
            st.write('Volume de shows:', dfMonday['Volume'].iloc[0])

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

    #formatando data do primeiro show, e verifa se está no banco de dados
    if dfMonday.empty or pd.isna(dfMonday['Início da parceria'].iloc[0]):
        col8.write('Primeiro Show no Monday: pendente...')
    else:
        with col8:
            data_str = dfMonday['Início da parceria'].iloc[0]
            data_obj = datetime.strptime(data_str, "%Y-%m-%d")
            day2 = data_obj.strftime("%d/%m/%Y")
            st.write('Primeiro Show no Monday:', day2)
        if(df.empty or pd.isna(df['PRIMEIRO_SHOW'].iloc[0])) and not (dfMonday.empty or pd.isna(dfMonday['Início da parceria'].iloc[0])):
            remainingDays = (datetime.strptime(day2, "%d/%m/%Y") - datetime.strptime(date.today().strftime("%d/%m/%Y"), "%d/%m/%Y")).days
            if (remainingDays < 0):
                st.error(f"Estamos atrasados para lançar o show, foi há {-1 * remainingDays} dias.")
            elif (remainingDays == 0):
                st.error(f"O show vai ocorrer hoje, precisamos lanaçar no bando de dados.")
            else:
                st.error(f"Opa, parece que o primeiro show não foi lançado ainda! Faltam {remainingDays} dias.")

    #verificando casting
    if str(dfMonday['Cadastro/Onboarding de artistas'].iloc[0]) != "Não aplica" and (df['CASTING_CADASTRADO'].empty or str(df['CASTING_CADASTRADO'].iloc[0]) == '0'):
        st.error("Casting igual a 0 é um problema, precisamos ver!")

    #verifica os dados das datasVolume (qts dias a eshows terá na casa?)
    if  day != day2:
        st.error("Primeiro show e início da parceria apresentam valores diferentes")
    else:
        today = date.today().strftime("%d/%m/%Y")
        if today <= day and controladoria == 0:
            #calcula quando dias faltam
            today_datetime = datetime.strptime(today, "%d/%m/%Y")
            day_datetime = datetime.strptime(day, "%d/%m/%Y")
            remaining = (day_datetime - today_datetime).days

            st.error(f"Controladoria precisa ser preenchido antes do dia {day}, faltam {remaining} dias.")
        elif today > day and controladoria == 0:
            today_datetime = datetime.strptime(today, "%d/%m/%Y")
            day_datetime = datetime.strptime(day, "%d/%m/%Y")
            remaining = (today_datetime - day_datetime).days
            st.error(f"Controladoria precisa ser preenchido, está atrasada há {remaining} dias!")
        #verificar o sim do login criado com o BD: 'USUARIOS_ATIVOS'


def showMissingRegisterValuesFromDatabase(id):
    df = getMissingRegisterValue(id)
    missingValues = df['ERRO_CADASTRO'].astype(str).iloc[0]
    missingValues = missingValues.split('-')
    with st.expander("Ver dados incompletos"):
        for value in missingValues:
            st.error(value)

st.set_page_config(page_title="Monday Hunter Data", page_icon="🏹")
col1, col2 = st.columns([4,1])
col1.markdown(f"# Radar de implantação")
col2.image("./assets/imgs/eshows-logo.png", width=100)
if st.button("Atualizar dados BD", type="secondary"): getRadarDataFromDatabse()
st.divider()


radarMondaydf = getHunterData(getMondayDataframe())
radarMondaydf = renameColumns(radarMondaydf)

if  not radarMondaydf.empty:
    with st.sidebar:
            if (filterHunter := st.selectbox("Selecione um Hunter", radarMondaydf['Hunter Responsável'].unique().tolist(), index=None,placeholder="Hunter")):
                filterHause = st.selectbox("Dados de uma casa", radarMondaydf[radarMondaydf['Hunter Responsável'] == filterHunter]['Nome'].unique().tolist(), index=None, placeholder="Selecione a casa")

    if filterHunter:
        st.markdown(f"### Radar do {filterHunter}")
        df = radarMondaydf[radarMondaydf['Hunter Responsável'] == filterHunter].reset_index(drop=True)
        st.dataframe(df, hide_index=True)

        st.divider()
        if(checkStopedItens(radarMondaydf ,filterHunter)):
            st.markdown(f"### Próximos passos de cada casa")
            printStopedItens(radarMondaydf[radarMondaydf['Hunter Responsável'] == filterHunter])
        else:
            st.success("Parece que tudo está completo no radar das suas casas!")

        #rodar query para pegar dados do BD com o ID da casa
        if filterHause:
            tab1, tab2= st.tabs(["Pendências", "Situação Cadastral"])
            with tab1:
                showDataByDayabase(cleanBdDataUsingMonday(radarMondaydf, getRadarDataFromLocal()), radarMondaydf[radarMondaydf['Nome'] == filterHause],df.loc[df['Nome'] == filterHause, 'ID EPM'].iloc[0], filterHause)
            with tab2:
                stringObs = radarMondaydf.loc[radarMondaydf['Nome'] == filterHause, 'Observação Hunting'].astype(str).iloc[0]
                st.markdown("#### Observação do hunter:")
                st.info(stringObs)
                showMissingRegisterValuesFromDatabase(radarMondaydf.loc[radarMondaydf['Nome'] == filterHause, 'ID EPM'].astype(int).iloc[0])

        else:
            st.warning('Selecione dados de uma casa para ver mais campos e próximos passos.')



    else:
        st.markdown("### Radar do Monday")
        st.dataframe(radarMondaydf, hide_index=True)
else:
    st.error("Erro de requisição, não foi possível coletar os dados do Monday.")
