import cv2
import numpy as np
from matplotlib import pyplot as plt

notas = []
#minimo = 0
#maximo = 0

def valor_nota(x, tt, notas):
    posisao = tt[2]
    for i in range(0, 4):#quantidade de linha
        if (x >= posisao[0] and x <= posisao[1]):
            return ("NOTA (FA)")
        if (x >= posisao[2] and x <= posisao[3]):
            return ("NOTA (RÉ)")
        if (x >= posisao[4] and x <= posisao[5]):
            return ("NOTA (SI)")
        if (x >= posisao[6] and x <= posisao[7]):
            return ("NOTA (SOL)")
        if (x >= posisao[8] and x <= posisao[9]):
            return ("NOTA (MI)")

def classifica_nota(notas, cordenada_x_y, tt): # tt tupla com valor minimo e maximo das linha e todos os elementos de valor y da linha
    tam = len(notas)
    tam1 = len(cordenada_x_y)
    x = 0
    for i in range(tam):
        nota = notas[i]
        for j in range(0, tam1, 2):
            if (cordenada_x_y[j] == nota):
                x = cordenada_x_y[j+1]
                print (valor_nota(x, tt, notas))  # passsa cordenada y da linha, tupla e notas ordenadas

def define_nota(img_rgb):#acha as linha e retorna as linhas
    img = img_rgb
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength=50,maxLineGap=20)

    #print (lines[0])
    l = []
    final_x = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        l.append(y1)
        final_x.append(x2)
        cv2.line(img, (x1, y1), (x2, y2), (255,255,0), 1)#desenha as linha

    final_x.sort()
    #print (final_x[0])
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

    minimo = l1[0]
    maximo = l1[9]
    return (maximo, minimo, l1)

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
        cordenada_x_y.append(cordenada_x[i])
        cordenada_x_y.append(cordenada_y[i]+1)

    cordenada_x = []
    x = loc[1]
    tam = len(loc[1])
    for i in range(0, tam-1):
        if (x[i] == x[i+1]):
            continue
        else:
            cordenada_x.append(x[i])
    #notas = []

    tt = define_nota(img_rgb)# tupla contendo 3 lista retoranado da função
    maximo = tt[0] #linha bot
    minimo = tt[1] #linha top

    for i in range(0, tam-1, 2):
        if (cordenada_x_y[i + 1] >= minimo and cordenada_x_y[i + 1] <= maximo):
            notas.append(cordenada_x_y[i])#grava so as cordenada x das nota

    notas.sort()
    classifica_nota(notas, cordenada_x_y, tt)#envia lista nota, cordenada delas (x,y) e tupla retornado da função (define_nota)

    notas.sort()

    cordenada_x.sort()

    for pt in zip(*loc[::-1]):
        if valor == 1:
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)


def load_image():
    img_rgb = cv2.imread('partitura1.png')

    nota7 = cv2.imread('nota7.png', 0)#passa o objeto (image) como parametro para a função (matchtemplate)

    busca(img_rgb, nota7, 1)
    #define_nota(img_rgb)

    cv2.imshow('Partitura', img_rgb)

def main():
    load_image()

if __name__ == '__main__':
    main()
    cv2.waitKey(0)