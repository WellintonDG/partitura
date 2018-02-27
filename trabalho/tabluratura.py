import cv2
import numpy as np
from matplotlib import pyplot as plt

parte = 0

def valor_nota(x, tt):
    posisao = tt
    for i in range(0, 4):#quantidade de linha
        if (x >= posisao[0+parte] and x <= posisao[1+parte]):
            return ("NOTA (FA)")
        if (x > posisao[1+parte] and x < posisao[2+parte]):
            return ("NOTA (MI)")
        if (x >= posisao[2+parte] and x <= posisao[3+parte]):
            return ("NOTA (RÉ)")
        if (x > posisao[3+parte] and x < posisao[4+parte]):
            return ("NOTA (DÓ)")
        if (x >= posisao[4+parte] and x <= posisao[5+parte]):
            return ("NOTA (SI)")
        if (x > posisao[5+parte] and x < posisao[6+parte]):
            return ("NOTA (LA)")
        if (x >= posisao[6+parte] and x <= posisao[7+parte]):
            return ("NOTA (SOL)")
        if (x > posisao[7+parte] and x < posisao[8+parte]):
            return ("NOTA (FÁ)")
        if (x >= posisao[8+parte] and x <= posisao[9+parte]):
            return ("NOTA (MI)")


def n_rep(notas):#tira valores que não são notas
    tam = len(notas)
    x = []
    i = 0
    while(i < tam-1):
        if (notas[i]+1 == notas[i+1]):
            x.append(notas[i])
            i += 1
        else:
            x.append(notas[i])
        i += 1
    if (x[-1]+1 == notas[-1]):
        return (x)
    else:
        x.append(notas[-1])
        return (x)

def remv_x(t1):
    temp = t1
    tam = len(t1)
    x = []
    for i in range(0, tam, 2):
        x.append(temp[i-1])
    return (x)

def classifica_nota(notas, notas_x_y, l):
    global parte
    tam = len(notas)
    tam1 = len(notas_x_y)

    for i in range(tam):
        nota = notas[i]
        for j in range(0, tam1, 2):
            if (notas_x_y[j] == nota):#verifica em qual posição de y a nota tá
                x = notas_x_y[j+1]
                print (valor_nota(x, l))  # passsa cordenada y da linha, lista das linhas
    parte += 10

def define_nota(img_rgb):#acha as linha e retorna as linhas
    img = img_rgb
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength=50,maxLineGap=20)

    l = []
    final_x = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        l.append(y1)
        final_x.append(x2)
        cv2.line(img, (x1, y1), (x2, y2), (255,255,0), 1)#desenha as linha

    final_x.sort()
    #grava largura das linha
    l = sorted(set(l))
    r = []
    for i in range(0, 10, 2):
        r.append(l[i+1] - l[i])

    # acha largura q mais se repete
    cont = 0
    resultado = r[0]
    repet = 0
    valor = [0]
    print ("largura linha",r[0])

    while(cont <= 4):
        for i in range(4):
            if (r[i] == resultado):
                repet += 1
        valor.append(repet)
        repet = 0
        cont += 1
        resultado = r[cont-1]
    resultado = max(valor)

    cont = valor.index(resultado)#posição a definir como linha
    largura = r[cont]# define como largura da linha

    #exclui linha q nao tem (largura)
    tam = len(l)
    l1 = []
    for i in range(0, tam-1, 2):
        if ((l[i+1] - l[i]) >= largura):
            l1.append(l[i])
            l1.append(l[i+1])
        else:
            l1.append(l[i+1])#grava cordenadas das linhas certas

    print ("espacamento = ", resultado)#espaçamento entre linhas

    return (l1)

def busca(img_rgb, nota, valor):
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    w, h = nota.shape[::-1]
    res = cv2.matchTemplate(img_gray, nota, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    tam = len(loc[1])
    cordenada_x = loc[1]#cordenadas dos objetos achado pela função (matchTemplate)
    cordenada_y = loc[0]
    cordenada_x_y = []

    for i in range(0, tam):
        if (valor == 1):
            cordenada_x_y.append(cordenada_x[i])
            cordenada_x_y.append(cordenada_y[i]+1)
        if (valor == 2):
            cordenada_x_y.append(cordenada_x[i])
            cordenada_x_y.append(cordenada_y[i]+2)
        if (valor == 3):
            cordenada_x_y.append(cordenada_x[i])
            cordenada_x_y.append(cordenada_y[i]+3)

    cordenada_x = []
    x = loc[1]
    tam = len(loc[1])

    for i in range(0, tam-1):
        if (x[i] == x[i+1]):
            continue
        else:
            cordenada_x.append(x[i])
    #cordenada_x.append(x[-1])

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
    return (cordenada_x, cordenada_x_y)

def pega_notas(img_rgb, cordenada_x, cordenada_x_y):
    notas = []
    tt = define_nota(img_rgb)# lista as linha retoranado da função
    qtd_linhas = len(tt)
    l = tt

    tam = len(cordenada_x_y)

    n = 9
    nota_x_y = []
    for i in range(0, qtd_linhas, 10):
        minimo = l[i]
        maximo = l[n]

        for j in range(0, tam-1, 2):
            if (cordenada_x_y[j + 1] >= minimo and cordenada_x_y[j + 1] <= maximo):#if para grava objeto referente a parte verificada
                notas.append(cordenada_x_y[j])  # grava so as cordenada x
                nota_x_y.append(cordenada_x_y[j])
                nota_x_y.append(cordenada_x_y[j+1])

        n += 10
        notas.sort()

        nota = n_rep(notas)

        classifica_nota(nota, nota_x_y, l)
        notas = []
        nota_x_y = []

def load_image():
    img_rgb = cv2.imread('singer.png')

    nota7 = cv2.imread('nota7.png', 0)#passa o objeto (image) como parametro para a função (matchtemplate)
    nota = cv2.imread('nota1.png', 0)
    nota1 = cv2.imread('nota.png', 0)

    image1 = busca(img_rgb, nota7, 1)
    image2 = busca(img_rgb, nota, 2)
    image3 = busca(img_rgb, nota1, 2)

    #busca(img_rgb, nota, 1)
    cordenada_x = image1[0]+image2[0]+image3[0]
    cordenada_x_y = image1[1]+image2[1]+image3[1]

    pega_notas(img_rgb, cordenada_x, cordenada_x_y)

    cv2.imshow('Partitura', img_rgb)

def main():
    load_image()

if __name__ == '__main__':
    main()
    cv2.waitKey(0)