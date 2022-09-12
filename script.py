''' Arquivo: script.py
    Data: 06/06/2022
    
    Descrição: Esse arquivo contém os métodos para realizar as visualizações dados os agrupamentos.
'''

# Importações
import pandas as pd

# Variáveis globais
QTD_AGRUPAMENTO = 3
ANOS = [2008, 2011, 2014, 2017]
IDX = 0

def ordenarDesempenho(dados, labelsClusters, labelsClustersSemEspaco):
    ''' Método ordenarDesempenho:

    Params:
        dados: DataFrame
        labelsClusters: lista de labels dos clusters
        labelsClustersSemEspaco: lista de labels dos clusters sem espaço

    Esse método ordena os dados de acordo com o desempenho de cada cluster.
    '''

    ordDic = {}

    for i in range(3):
        ordDic[dados.loc[dados['cluster'] == i, 'nota_geral'].mean()] = i
        dados.loc[dados['cluster'] == i, 'cluster'] = i+3
    
    indiceMaior = ordDic[max(ordDic)]
    indiceMenor = ordDic[min(ordDic)]

    dados.loc[dados['cluster'] == indiceMaior + 3, 'cluster'] = 0
    dados.loc[dados['cluster'] == indiceMenor + 3, 'cluster'] = 2

    for i in range(3):
        if i != indiceMaior and i != indiceMenor:
            dados.loc[dados['cluster'] == i+3, 'cluster'] = 1

    dados.loc[dados['cluster'] == 0, 'label cluster'] = labelsClusters[0]
    dados.loc[dados['cluster'] == 1, 'label cluster'] = labelsClusters[1]
    dados.loc[dados['cluster'] == 2, 'label cluster'] = labelsClusters[2]
        
    dados.loc[dados['cluster'] == 0, 'label cluster se'] = labelsClustersSemEspaco[0]
    dados.loc[dados['cluster'] == 1, 'label cluster se'] = labelsClustersSemEspaco[1]
    dados.loc[dados['cluster'] == 2, 'label cluster se'] = labelsClustersSemEspaco[2]

    return dados

def mediaNotaGeral(dados):
    ''' Método: mediaNotaGeral

    Params:
        dados: DataFrame

    Esse método calcula a média da nota geral de cada cluster.
    '''

    dataMedia = pd.DataFrame(columns=['nota_geral', 'cluster'])

    for i in range(QTD_AGRUPAMENTO):
        dataMedia.loc[i] = [dados.loc[dados['cluster'] == i, 'nota_geral'].mean()] + [int(i)]

    return dataMedia

def quantidadeAlunos(dados):
    ''' Método: quantidadeAlunos

    Params:
        dados: DataFrame

    Esse método calcula a quantidade de alunos de cada cluster.
    '''

    quantidadeAlunos = pd.DataFrame(columns=['quantidade', 'cluster'])

    for i in range(QTD_AGRUPAMENTO):
        quantidadeAlunos.loc[i] = [dados.loc[dados['cluster'] == i].count()[0]/10000] + [int(i)]

    return quantidadeAlunos

def quantidadeAlunosAno(dados):
    ''' Método: quantidadeAlunosAno

    Params:
        dados: DataFrame

    Esse método calcula a quantidade de alunos de cada cluster por ano.
    '''

    quantidadeAlunosCluster = pd.DataFrame(columns=['cluster', 'ano', 'media'])
    IDX = 0

    for ano in ANOS:

        dataAno = dados[dados['ano'] == ano]
        total = dataAno.count()[0]

        for i in range(QTD_AGRUPAMENTO):
            dataCluster = dataAno.loc[dataAno['cluster'] == i]

            quantidadeAlunosCluster.loc[IDX] = [i] + [ano] + [(dataCluster.count()[0]/total)*100]
            IDX += 1

    return quantidadeAlunosCluster

def categoriaIES(dados):
    ''' Método: categoriaIES

    Params:
        dados: DataFrame

    Esse método calcula a quantidade de aluno pela categoria da IES de cada cluster.
    '''

    categoriaIES = pd.DataFrame(columns=['Cluster', 'IES', 'Valor (em %)'])
    ies = ['IES privada', 'IES publica']
    IDX = 0

    for ie in ies:

        categoriaIESAux = dados.loc[dados[ie] == 1]
        total = categoriaIESAux.count()[0]
        
        for i in range(QTD_AGRUPAMENTO):

            dataCluster = categoriaIESAux.loc[categoriaIESAux['cluster'] == i]

            categoriaIES.loc[IDX] = [i] + [ie[4:]] + [(dataCluster.count()[0]/total)*100]
            IDX += 1

    return categoriaIES   

def tipoEM(dados):
    ''' Método: tipoEM
    
    Params:
        dados: DataFrame
    
    Esse método calcula a quantidade de aluno pelo tipo do EM de cada cluster.
    '''

    dataEM = pd.DataFrame(columns=['Cluster', 'Ensino', 'Valor (em %)'])
    escolaridade = ['EM particular', 'EM publico']
    IDX = 0

    for escol in escolaridade:

        dataEMAux = dados.loc[dados[escol] == 1]
        total = dataEMAux.count()[0]

        for i in range(QTD_AGRUPAMENTO):

            dataCluster = dataEMAux.loc[dataEMAux['cluster'] == i]

            dataEM.loc[IDX] = [i] + [escol[3:]] + [(dataCluster.count()[0]/total)*100]
            IDX += 1

    return dataEM

def tipoEMPais(dados, juntos = False, dataEMPai = None, dataEMMae = None):
    ''' Método: tipoEMPais

    Params:
        dados: DataFrame
        juntos: boolean
        dataEMPai: DataFrame
        dataEMMae: DataFrame
    
    Esse método calcula a quantidade de alunos pelo tipo do EM de seus pais, para cada cluster.
    
    '''
    
    if not juntos:
        dataEMPai = pd.DataFrame(columns=['Cluster', 'Ensino', 'Valor (em %)'])
        dataEMMae = pd.DataFrame(columns=['Cluster', 'Ensino', 'Valor (em %)'])

        escolaridade = ['Pai EF', 'Pai EM', 'Pai ES']
        labels = ['fundamental', 'medio', 'superior']
        IDX = 0

        for y, escol in enumerate(escolaridade):
            
            dataEMPaiAux = dados.loc[dados[escol] == 1]
            total = dataEMPaiAux.count()[0]

            for i in range(QTD_AGRUPAMENTO):
                
                dataCluster = dataEMPaiAux.loc[dataEMPaiAux['cluster'] == i]

                dataEMPai.loc[IDX] = [i] + [labels[y]] + [(dataCluster.count()[0]/total)*100]
                IDX += 1

        escolaridade = ['Mae EF', 'Mae EM', 'Mae ES']
        IDX = 0

        for y, escol in enumerate(escolaridade):

            dataEMMaeAux = dados.loc[dados[escol] == 1]
            total = dataEMMaeAux.count()[0]

            for i in range(QTD_AGRUPAMENTO):

                dataCluster = dataEMMaeAux.loc[dataEMMaeAux['cluster'] == i]

                dataEMMae.loc[IDX] = [i] + [labels[y]] + [(dataCluster.count()[0]/total)*100]
                IDX += 1

        return dataEMPai, dataEMMae

    else:
        
        dataEMPais = pd.DataFrame(columns=['cluster', 'Ensino', 'Valor (em %)'])
        labelEM = ['fundamental', 'medio', 'superior']
        IDX = 0

        for cluster in range(3):
            for ensino in labelEM:
                VP = dataEMPai.loc[(dataEMPai['Cluster'] == cluster) & (dataEMPai['Ensino'] == ensino), 'Valor (em %)'].values[0]
                VM = dataEMMae.loc[(dataEMMae['Cluster'] == cluster) & (dataEMMae['Ensino'] == ensino), 'Valor (em %)'].values[0]

                dataEMPais.loc[IDX] = [cluster] + [ensino] + [(VP + VM) / 2]
                IDX += 1

        return dataEMPais

def cotas(dados):
    ''' Método: cotas

    Params:
        dados: DataFrame

    Esse método calcula a quantidade de alunos por cota de cada cluster.
    '''

    dataCotas = pd.DataFrame(columns=['cluster', 'ano', 'media', 'ies'])
    dataSemCotas = pd.DataFrame(columns=['cluster', 'ano', 'media', 'ies'])
    iesLabel = ['IES privada', 'IES publica']
    IDX = 0

    for ano in ANOS:

        dataAno = dados.loc[dados['ano'] == ano]
        total = dataAno.count()[0]

        for i in range(QTD_AGRUPAMENTO):

                dataCluster = dataAno.loc[dataAno['cluster'] == i]

                for iesCluster in iesLabel:
                    dataIes = dataCluster.loc[dataCluster[iesCluster] == 1]

                    mediaCotas = (dataIes.loc[dataIes['recebeu_cota'] == 1].count()[0]/total)
                    mediaSemCostas = (dataIes.loc[dataIes['recebeu_cota'] == 0].count()[0]/total) 

                    dataCotas.loc[IDX] = [i] + [ano] + [mediaCotas] + [iesCluster[4:]]
                    dataSemCotas.loc[IDX] = [i] + [ano] + [mediaSemCostas] + [iesCluster[4:]]

                    IDX += 1

    return dataCotas, dataSemCotas

def fixTurno(dados):
    ''' Método: fixTurno

    Params:
        dados: DataFrame

    Esse método cria uma coluna 'Turno', baseado nos valores das outras colunas.
    '''

    dados['Turno'] = 'Não informado'
    dados.loc[dados['Turno integral'] == 1, 'Turno'] = 'Integral'
    dados.loc[dados['Turno diurno'] == 1, 'Turno'] = 'Diurno'
    dados.loc[dados['Turno noturno'] == 1, 'Turno'] = 'Noturno'

    dados.drop(['Turno integral', 'Turno diurno', 'Turno noturno'], axis=1, inplace=True)

    return dados

def turnos(dados):
    ''' Método: turnos

    Params:
        dados: DataFrame

    Esse método calcula a quantidade de alunos por turno de cada cluster.
    '''

    if 'Turno' not in dados.columns:
        dados = fixTurno(dados)

    dataTurnoIntegral = pd.DataFrame(columns=['cluster', 'ano', 'media'])
    dataTurnoDiurno = pd.DataFrame(columns=['cluster', 'ano', 'media'])
    dataTurnoNoturno = pd.DataFrame(columns=['cluster', 'ano', 'media'])
    IDX = 0

    for ano in ANOS:

        dataAnoQtd = dados.loc[(dados['ano'] == ano)]
        total = dataAnoQtd.count()[0]

        dataAnoIntegral = dados.loc[(dados['ano'] == ano) & (dados['Turno'] == 'Integral')]
        dataAnoDiurno = dados.loc[(dados['ano'] == ano) & (dados['Turno'] == 'Diurno')]
        dataAnoNoturno = dados.loc[(dados['ano'] == ano) & (dados['Turno'] == 'Noturno')]

        for i in range(QTD_AGRUPAMENTO):
            dataIntegralCluster = dataAnoIntegral.loc[dataAnoIntegral['cluster'] == i]
            dataDiurnoCluster = dataAnoDiurno.loc[dataAnoDiurno['cluster'] == i]
            dataNoturnoCluster = dataAnoNoturno.loc[dataAnoNoturno['cluster'] == i]

            dataTurnoIntegral.loc[IDX] = [i] + [ano] + [(dataIntegralCluster.loc[dataIntegralCluster['Turno'] == 'Integral'].count()[0]/total)*100]
            dataTurnoDiurno.loc[IDX] = [i] + [ano] + [(dataDiurnoCluster.loc[dataDiurnoCluster['Turno'] == 'Diurno'].count()[0]/total)*100]
            dataTurnoNoturno.loc[IDX] = [i] + [ano] + [(dataNoturnoCluster.loc[dataNoturnoCluster['Turno'] == 'Noturno'].count()[0]/total)*100]
            
            IDX += 1

    return dataTurnoNoturno, dataTurnoDiurno, dataTurnoIntegral

def mudarCurso(dados):
    ''' Método: mudarCurso

    Params:
        dados: DataFrame

    Esse método altera o dataframe.
    '''

    dados['Curso'] = 'Não informado'
    dados.loc[dados['ADS'] == 1, 'Curso'] = 'ADS'
    dados.loc[dados['BCC'] == 1, 'Curso'] = 'BCC'
    dados.loc[dados['EC'] == 1, 'Curso'] = 'EC'
    dados.loc[dados['RC'] == 1, 'Curso'] = 'RC'
    dados.loc[dados['SI'] == 1, 'Curso'] = 'SI'
    dados.loc[dados['LCC'] == 1, 'Curso'] = 'LCC'
    dados.loc[dados['GTI'] == 1, 'Curso'] = 'GTI'

    dados.drop(['ADS','BCC', 'EC', 'RC', 'SI', 'LCC', 'GTI'], axis=1, inplace=True)
    
    return dados

def cursos(dados):
    ''' Método: cursos

    Params:
        dados: DataFrame

    Esse método calcula a quantidade de alunos pelos cursos de cada cluster.
    '''

    if 'Curso' not in dados.columns:
        dados = mudarCurso(dados)

    notaCursoAno = pd.DataFrame(columns=['cluster', 'ano', 'curso', 'media'])
    cursos = ['ADS', 'BCC', 'EC', 'RC', 'SI', 'LCC', 'GTI']
    IDX = 0

    for curso in cursos:

        dataCurso = dados[dados['Curso'] == curso]

        for ano in ANOS:

            dataAno = dataCurso[dataCurso['ano'] == ano]
            total = dataAno.count()[0]

            for i in range(QTD_AGRUPAMENTO):

                datacluster = dataAno.loc[dataAno['cluster'] == i]
                
                notaCursoAno.loc[IDX] = [i] + [ano] + [curso] + [datacluster.count()[0]/total]
                IDX += 1

    notaCursoAno.loc[notaCursoAno['media'].isnull(), 'media'] = 0
    return notaCursoAno