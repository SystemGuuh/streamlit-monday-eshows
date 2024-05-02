import streamlit as st
from utils.monday import *
from utils.queries import *
import pandas as pd
from datetime import datetime, date

#retorna um dataframe somente com os dados para hunter
def getHunterData(df):
    return df[['ID EPM', 'Nome', 'Relevância do cliente',
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

#retorna um dataframe somente com os dados para hunter
def getFarmerData(df):
    return df[['ID EPM', 'Nome', 'Relevância do cliente',
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
                                'Propostas lançadas?','Cadastro/Onboarding de artistas', 'Observação Hunting', 'Hunter Responsável', 'Farmer']]

#retorna um dataframe somente com os dados para Implantação
def getImplantacaoData(df):
    return df[['ID EPM', 'Nome', 'Relevância do cliente',
                               'Nome contratante', 'E-mail do contratante',
                               'Cidade do Estabelecimento', 'Cadastro de show padrão',
                               'Recebi programação do Hunter?', 'Criar perfil Espaces', 'Ativou controladoria? (ativar três dias antes)',
                               'Observação Hunting', 'Login criado?', 'Volume (qts gigs a eshows terá na casa?)', 'Início da parceria',
                               'Cadastro/Onboarding de artistas']]

#procura um item parado, para verificação
def checkStopedItens(df):
    try:
        for coluna in df.columns:
            for indice, valor in df[coluna].items():
                if str(valor).lower() == 'parado':
                    return True
        return False
    except Exception as e:
        st.error("Opa, valor inconsistente ou não númerico encontrado, verifique os dados.")
        return False

#printa os itens marcados com parado
def findAndPrintStopedItens(df):
    df = df.reset_index(drop=True)
    pendencies = {}

    #calcula campos parados
    for indice, linha in df.iterrows():
        valor_anterior = None
        count =0
        name = linha['Nome']

        if name not in pendencies:
            pendencies[name] = {
                "stopedItensCount": 0,
                "stopedItensValues": []
            }

        for coluna in df.columns:
            valor = str(linha[coluna])
            if valor is None or str(valor) == '' and valor_anterior != 'não aplica':
                pendencies[name]["stopedItensValues"].append(f'"{name}" está com o campo "{coluna}" vazio e precisa ser preenchido.\n')
                count += 1
            elif str(valor).lower() == 'parado' and valor_anterior != 'não aplica':
                name = linha['Nome']
                pendencies[name]["stopedItensValues"].append(f'"{name}" está com o campo "{coluna}" parado.\n')
                count += 1
            valor_anterior = valor.lower()
        pendencies[name]["stopedItensCount"] = count

    #printa campos parados
    for name, pendencie in pendencies.items():
        if pendencie["stopedItensCount"] > 0:
            with st.expander(f"⚠️ **{name}**: {pendencies[name]['stopedItensCount']} itens pendentes"):
                st.write('\n'.join(pendencies[name]["stopedItensValues"]))

#mostra dados de acordo com o bando de dados e monday
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

    col1, col2, col3, col4 = st.columns(4)
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
    with col4:
            statusCompny = getStatusCompany(id_casa_str)
            st.write('Status:', str(statusCompny['status'].iloc[0]))


    col4, col5, col6 = st.columns(3)
    with col4: # mostra completo caso nao tenha nada faltando no cadastro
        tempdf = pd.DataFrame(getMissingRegisterValue(id_casa))
        if tempdf['ERRO_CADASTRO'].isna().any() or tempdf['ERRO_CADASTRO'].astype(str).iloc[0] == '':
            st.markdown('Cadastro <span style="color:green">COMPLETO</span>', unsafe_allow_html=True)
        else:
            st.markdown('Cadastro <span style="color:red">INCOMPLETO</span>', unsafe_allow_html=True)
    with col5: # verifica se a casas exige nota fiscal
        if df['NOTA_FISCAL'].empty or df['NOTA_FISCAL'].iloc[0] == 0:
            st.write('Casa não exige nota fiscal')
        else:
            st.write('Casa exige nota fiscal')
    with col6:
        if dfMonday['Volume'].empty or pd.isna(dfMonday['Volume'].iloc[0]) or str(dfMonday['Volume'].iloc[0])=="":
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

    #adicionando data da próxima oportunidade em andamento
    if df.empty or pd.isna(df['PROXIMA_OPORTUNIDADE_EM_ANDAMENTO'].iloc[0]):
        st.markdown('Próxima oportunidade em andamento: <span style="color:red">Não encontrado</span>', unsafe_allow_html=True)
    else:
        data_str = df['PROXIMA_OPORTUNIDADE_EM_ANDAMENTO'].iloc[0]
        data_obj = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
        day3 = data_obj.strftime("%d/%m/%Y")
        time3 = data_obj.strftime("%H:%M:%S")
        st.write(f'Próxima oportunidade em andamento: {day3} às {time3}')

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

#mostra os campos que devem ser preechidos no banco de dados
def showMissingRegisterValuesFromDatabase(id):
    df = getMissingRegisterValue(id)
    missingValues = df['ERRO_CADASTRO'].astype(str).iloc[0]
    missingValues = missingValues.split('-')
    with st.expander("Ver dados incompletos"):
        for value in missingValues:
            st.error(value)
