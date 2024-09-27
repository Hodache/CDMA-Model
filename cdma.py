import numpy as np
import textwrap

def codeWord(word):
    return ''.join(f'{ord(c):08b}' for c in word)

def decodeWord(binaryWord):
    return ''.join([chr(int(byte, 2)) for byte in textwrap.wrap(binaryWord, 8)])

## Функция для генерации матрицы Адамара
def hadamard_matrix(n):
    if n == 1:
        return np.array([[1]])
    else:
        H_n_minus_1 = hadamard_matrix(n // 2)
        top = np.hstack((H_n_minus_1, H_n_minus_1))
        bottom = np.hstack((H_n_minus_1, -H_n_minus_1))
        return np.vstack((top, bottom))

## Функция для генерации кодов Уолша размером 8 символов
def walsh_codes(n=8):
    H = hadamard_matrix(n)
    return H.astype(int)

stationsWords = {
    "A": "GOD",
    "B": "CAT",
    "C": "HAM",
    "D": "SUNset",
    "E": "1234567",
    "F": "A",
    "G": "",
    "H": "+-?*(')!",
}

## Генерация и присваивание случайных кодов станциям
walshCount = 32 # длина и число кодов Уолша
walshCodes = walsh_codes(walshCount)
chosenCodes = walshCodes[np.random.choice(len(walshCodes), len(stationsWords), replace=False)]

stationsCodes = {s:c for s, c in zip(stationsWords, np.array(chosenCodes))}

print(f'Случайные коды Уолша станций (из общего числа {walshCount})')
for station, code in stationsCodes.items():
    print(station, ''.join(str(char) + " " for char in code))

## Перевод слов в двоичный вид по ASCII
binaryWords = {}
print("\nСлова в двоичном виде до вещания")
for station, word in stationsWords.items():
    binaryWords[station] = codeWord(word)
    print(station, binaryWords[station], stationsWords[station])

## Максимальная длина сигнала в битах
longestWord = max(binaryWords.values(), key = len)
bitsCount = len(longestWord)

## Одновременное вещание
totalSignal = np.zeros((bitsCount, walshCount), int)

# По станциям и словам
for station, bword in binaryWords.items():
    # По битам слов
    for wordBit, i in zip(bword, range(len(bword))):
        # Выбор между прямым и обратным кодом в зависимости от бита
        toAdd = stationsCodes[station] if int(wordBit) == 1 else (stationsCodes[station] * -1)
        totalSignal[i] += toAdd
        # print(station, bword, wordBit, i, toAdd)

print(f"\nСуммарное вещание станций ({len(totalSignal)} бита)\n", totalSignal)

## Расшифровка сообщений из суммарного сигнала для каждой станции
print("\nРезультаты расшифровки вещания")
for station, code in stationsCodes.items():
    binResult = ""
    for bit in totalSignal:
        wordBit = (np.sum(bit * code) // walshCount + 1) // 2
        binResult += str(wordBit)
    word = decodeWord(binResult)
    print(station, binResult, word)





        

    

