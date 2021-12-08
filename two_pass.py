import matplotlib.pyplot as plt
import numpy as np

def negate(B):
    array = B.copy()
    array[np.where(array == 1)] = -1
    return array

def check(B, y, x): #передаем изображ и координаты
    if not 0 <= x < B.shape[0]: #если коррд столбца выходят за пределы изобр
        return False
    if not 0 <= y < B.shape[1]: #аналогичн строка
        return False
    if B[y, x] != 0: #и если они не равны 0
        return True
    return False

def neighbors2(B, y, x): #изображб,текущ строка и столбец
    left = y, x-1 #координ клетки слева
    top = y - 1, x #координ клетки сверху
    if not check(B, *left):  #смотрим на наличие соседа слева
        left = None
    if not check(B, *top): #аналогичн сверху
        top = None
    return left, top #возвращ наличие соседей слева и сверху (координ если true)

def exists(neighbors): #получает координ\None
    return not all([n is None for n in neighbors]) #если все None то вернет False

def find(label, linked): #метка
   # print('linked ',linked)
    j = label #изначательно = метке
    while linked[j] != 0:# до первого нуля в массиве
        j = linked[j] #заменяем значения
    return j #возвращаем крайнее значение в массиве до 0

def union(label1, label2, linked): #тек метка, метка соседн клетки
    j = find(label1, linked) 
    k = find(label2, linked)
    #print("j k ",j," ",k)
    if j != k: #если не равны
        linked[k] = j #заменяем в массиве индекс метки соседней клетки значением метки
        #текущей


def two_pass_labeling(B):
    linked = np.zeros(len(B), dtype="uint") #cтрока из 20 элем
    #print(linked)
    labels = np.zeros_like(B) #массив из 0 аналогич передан изображ
    #print("2 ",labels)
    label = 1
    for row in range(B.shape[0]): #по кол-ву строк
        for col in range(B.shape[1]): #по кол-ву столбцов
            if B[row, col] != 0: #если в изо клетка не пуста
                n = neighbors2(B, row, col) # n = наличие соседей слева и сверху(координ\None)
                if not exists(n): #если все None(соседей нет, начало фигуры?)
                    m = label #тек метка присвается m
                    label += 1 #счетчик метки увелич на 1
                else: #не все None
                    lbs = [labels[i] for i in n if i is not None] #заносим значения марок соседей
                    #они уже прошли алгоритм и с марками
                    m = min(lbs) #тек метка будет миним из меток соседей
                    
                labels[row, col] = m #на 0 поле заполняем эту клетку численным маркером
                for i in n: #обращаемся к координ соседей слева-верх
                    if i is not None: #если не нулевые
                        lb = labels[i] #метка тек соседней клетки
                        if lb != m: #если метка клетки не сопадает с тек меткой
                            union(m, lb, linked) #заменяем метку соседней клетки текущей
     
                            

    used_labels = []
    for row in range(B.shape[0]): #для всей текущей строки изобр
        for col in range(B.shape[1]): #
            if B[row, col] != 0:
                new_label = find(labels[row, col], linked)
                if new_label not in used_labels:
                    used_labels.append(new_label)
                new_label = used_labels.index(new_label) + 1
                if new_label != labels[row, col]:
                    labels[row, col] = new_label
    
    print(labels)
    return labels


if __name__ == "__main__":
    B = np.zeros((20, 20), dtype='int32') #массив 20 на 20 из 0
    
    
    B[1:-1, -2] = 1 #делаем фигурки
    
    B[1, 1:5] = 1
    B[1, 7:12] = 1
    B[2, 1:3] = 1
    B[2, 6:8] = 1
    B[3:4, 1:7] = 1
    
    B[7:11, 11] = 1
    B[7:11, 14] = 1
    B[10:15, 10:15] = 1
    
    B[5:10, 5] = 1
    B[5:10, 6] = 1
   # print(B)
    LB = two_pass_labeling(B) #ручная маркировка, передаем изобр
    
    print("Labels - ", list(set(LB.ravel()))[1:])
    
    \
    plt.figure(figsize=(12, 5))
    plt.subplot(121)
    plt.imshow(B, cmap="hot")
    plt.colorbar(ticks=range(int(2)))
    plt.axis("off")
    plt.subplot(122)
    plt.imshow(LB.astype("uint8"), cmap="hot")
    plt.colorbar()
    plt.axis("off")
    plt.tight_layout()
    plt.show()