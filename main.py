import pickle
import random
import time

# Trabalha com a lógica de leitura dos dados binários.
def carregar_dados(arquivo):
    binario = open(file=arquivo, mode="rb") # Abre o arquivo em modo read binary
    dicionario = pickle.load(binario)
    binario.close()  # Importante fechar o arquivo após uso
    return dicionario

DIC = carregar_dados("entrada100000.bin") # Optei por definir globalmente pois essas coisas vão ser usadas pelo código inteiro.
LISTA = list(DIC) # Forma mais efetiva de transformar o dicionário em uma lista, pelo o que eu testei. Sem precisar iterar.

def nota(dic):
    return dic[1] + dic[2] + dic[3] + dic[4]  # Soma Nota1 + Nota2 + Nota3 + Nota4

def qsort(ptr_esq, ptr_dir): # Foi BEM complicado pois não se pode criar nenhuma lista. Usa o método de dois ponteiros (Two pointer)
    if ptr_esq < ptr_dir:
        ind_pivo = random.randint(ptr_esq, ptr_dir) # De acordo com o livro "Aprendendo algoritmos" essa é a melhor forma de se fazer, com um pivo aleatório.
        esq = ptr_esq + 1 # Começa após o pivô
        dir = ptr_dir
        
        LISTA[ind_pivo], LISTA[ptr_esq] = LISTA[ptr_esq], LISTA[ind_pivo]
        
        while esq <= dir:
            # Encontra elemento maior que o pivô no lado esquerdo
            while esq <= dir and esquerda_menor(LISTA[esq], LISTA[ptr_esq]):
                esq += 1
            
            # Encontra elemento maior que o pivô no lado direito
            while esq <= dir and not esquerda_menor(LISTA[dir], LISTA[ptr_esq]):
                dir -= 1
            
            if esq < dir:
                LISTA[esq], LISTA[dir] = LISTA[dir], LISTA[esq]
        
        # Coloca o pivô na sua posição final
        LISTA[ptr_esq], LISTA[dir] = LISTA[dir], LISTA[ptr_esq]
        
        qsort(ptr_esq, dir - 1)
        qsort(dir + 1, ptr_dir)

def esquerda_menor(esq, dir):
    dic_esq = DIC[esq]
    dic_dir = DIC[dir]

    nota_esq = nota(dic_esq)
    nota_dir = nota(dic_dir)

    if nota_esq != nota_dir: # Compara notas, se não forem iguais retorna se a esquerda é menor
        return nota_esq > nota_dir
    if dic_esq[5] != dic_dir[5]: # Compara execução em segundos
        return dic_esq[5] < dic_dir[5]
    if dic_esq[0] != dic_dir[0]: # Compara nome
        return dic_esq[0] < dic_dir[0]
    return esq < dir # Compara crescentemente por No de matricula

def bonus(): # Acha até onde o indice de bonus vai
    i = 0
    while i < len(LISTA) and nota(DIC[LISTA[i]]) == 40 and (i < 5 or DIC[LISTA[i]][5] == DIC[LISTA[i - 1]][5]):
        i += 1
    return i

def print_aluno(aluno, nota, f):
    f.write(f"{aluno} {nota}\n")

def main():
    start_time = time.time()  # Início da temporização

    qsort(0, len(LISTA) - 1)
    ind_bonus = bonus()

    f = open('saida.txt', 'w')

    for i in range(ind_bonus):
        aluno = LISTA[i]
        total = nota(DIC[aluno])  # Correção 3
        f.write(f"{DIC[aluno][0]} {total + 2}\n")  # Adiciona bônus
    
    for i in range(ind_bonus, len(LISTA)):
        aluno = LISTA[i]
        total = nota(DIC[aluno])  # Correção 3
        f.write(f"{DIC[aluno][0]} {total}\n")  # Sem bônus

    f.close()

    end_time = time.time()  # Fim da temporização
    print(f"Tempo de execução: {end_time - start_time} segundos")

if __name__=="__main__":
    main()