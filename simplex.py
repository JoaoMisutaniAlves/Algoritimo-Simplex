import os
import numpy as np


def leitura_arquivo():
    linhas = []
    arquivos = os.listdir(".")
    for f in arquivos:
        if f.endswith(".txt"):
            f = open(f)
            for linha in f:
                linhas.append(linha.replace("\n", "").split(" "))
    variaveis = len(linhas[0])
    restricoes = len(linhas) - 1
    return linhas, variaveis, restricoes


def geracao_tabela(variaveis, restricoes):
    tabela = np.zeros((restricoes + 1, variaveis + restricoes + 2))
    return tabela


def obtem_objetivo_restricoes(linhas):
    objetive = []
    restricoes = []
    for linha in linhas:
        if linhas.index(linha) == 0:
            objetive = linha
        else:
            restricoes.append(linha)
    return objetive, restricoes


def converter(equacao):
    equacao = [float(valor) for valor in equacao]
    return equacao


def preencher_restricoes(tabela, restricoes):
    for restricao in restricoes:
        quant_colunas = len(tabela[0, :])
        quant_linhas = len(tabela[:, 0])
        valores_tabela = quant_colunas - quant_linhas - 1
        j = 0
        while j < quant_linhas:
            verifica = tabela[j, :]
            total = 0
            for i in verifica:
                total += float(i ** 2)
            if total == 0:
                linha = verifica
                break
            j += 1
        restricao = converter(restricao)
        i = 0
        while i < len(restricao) - 1:
            linha[i] = restricao[i]
            i += 1
        linha[-1] = restricao[-1]
        linha[valores_tabela + j] = 1


def preencher_objetivo(tabela, equacao):
    equacao = converter(equacao)
    quant_linhas = len(tabela[:, 0])
    linha = tabela[quant_linhas - 1, :]
    for i in range(len(equacao)):
        linha[i] = equacao[i] * -1
    linha[-2] = 1


def valida_func_linha_objetivo(tabela):
    quant_linhas = len(tabela[:, 0])
    m = min(tabela[quant_linhas - 1, :-1])
    if m >= 0:
        return False
    else:
        return True


def valida_func_coluna_objetivo(tabela):
    m = min(tabela[:-1, -1])
    if m >= 0:
        return False
    else:
        return True


def elemento_negativo_func_coluna_objetivo(tabela):
    quant_linhas = len(tabela[:, 0])
    m = min(tabela[quant_linhas - 1, :-1])
    if m <= 0:
        n = np.where(tabela[quant_linhas - 1, :-1] == m)[0][0]
    else:
        n = None
    return n


def localizar_pivo(tabela):
    if valida_func_linha_objetivo(tabela):
        total = []
        n = elemento_negativo_func_coluna_objetivo(tabela)
        for i, b in zip(tabela[:-1, n], tabela[:-1, -1]):
            if ( b / i ) > 0 and i ** 2 > 0:
                total.append(b / i)
            else:
                total.append(None)
        m = min(filter(lambda x: x is not None, total))
        index = total.index(m)
        return [index, n]


def pivo(linha, coluna, tabela):
    quant_linhas = len(tabela[:, 0])
    quant_colunas = len(tabela[0, :])
    tabela_imagem = np.zeros((quant_linhas, quant_colunas))
    linha_transformacao = tabela[linha, :]
    if tabela[linha, coluna] ** 2 > 0:
        valor = 1 / tabela[linha, coluna]
        linha_transformada = linha_transformacao * valor
        for i in range(len(tabela[:, coluna])):
            k = tabela[i, :]
            c = tabela[i, coluna]
            if list(k) == list(linha_transformacao):
                continue
            else:
                tabela_imagem[i, :] = list(k - linha_transformada * c)
        tabela_imagem[linha, :] = list(linha_transformada)
    return tabela_imagem


def gerar_variaveis(tabela):
    quant_colunas = len(tabela[0, :])
    quant_linhas = len(tabela[:, 0])
    variaveis = quant_colunas - quant_linhas - 1
    lista_variaveis = []
    for i in range(variaveis):
        lista_variaveis.append("x" + str(i + 1))
    return lista_variaveis


def maximizacao(linhas, variaveis, restricoes):
    tabela = geracao_tabela(variaveis, restricoes)
    objetive, restricoes = obtem_objetivo_restricoes(linhas)
    preencher_restricoes(tabela, restricoes)
    preencher_objetivo(tabela, objetive)
    print(tabela)
    while valida_func_linha_objetivo(tabela) == True:
        tabela = pivo(localizar_pivo(tabela)[0], localizar_pivo(tabela)[1], tabela)
    quant_colunas = len(tabela[0, :])
    quant_linhas = len(tabela[:, 0])
    quant_var = quant_colunas - quant_linhas - 1
    i = 0
    valores = {}
    for i in range(quant_var):
        coluna = tabela[:, i]
        soma = sum(coluna)
        maximo = max(coluna)
        if float(soma) == float(maximo):
            valor_localizado = np.where(coluna == maximo)[0][0]
            valores[gerar_variaveis(tabela)[i]] = tabela[valor_localizado, -1]
        else:
            valores[gerar_variaveis(tabela)[i]] = 0
    valores["maximo"] = tabela[-1, -1]
    return valores


def maximizacao(linhas, variaveis, restricoes):
    tabela = geracao_tabela(variaveis, restricoes)
    objetive, restricoes = obtem_objetivo_restricoes(linhas)
    preencher_restricoes(tabela, restricoes)
    preencher_objetivo(tabela, objetive)
    while valida_func_linha_objetivo(tabela) == True:
        tabela = pivo(localizar_pivo(tabela)[0], localizar_pivo(tabela)[1], tabela)
    quant_colunas = len(tabela[0, :])
    quant_linhas = len(tabela[:, 0])
    quant_var = quant_colunas - quant_linhas - 1
    i = 0
    valores = {}
    for i in range(quant_var):
        coluna = tabela[:, i]
        soma = sum(coluna)
        maximo = max(coluna)
        if float(soma) == float(maximo):
            valor_localizado = np.where(coluna == maximo)[0][0]
            valores[gerar_variaveis(tabela)[i]] = tabela[valor_localizado, -1]
        else:
            valores[gerar_variaveis(tabela)[i]] = 0
    valores["maximo"] = tabela[-1, -1]
    return valores

def escrita_arquivo(resultado):
    linhas = []
    arquivos = os.listdir(".")
    for f in arquivos:
        if f.endswith(".txt"):
            f = open(f, "a+")
            f.write("\n")
            f.write(str(resultado))
            f.close()

if __name__ == "__main__":
    linhas, variaveis, restricoes = leitura_arquivo()
    valores = maximizacao(linhas, variaveis, restricoes)
    escrita_arquivo(valores)
