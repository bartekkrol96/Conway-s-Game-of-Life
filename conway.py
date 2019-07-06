"""
Prosta implementacja Gry w życie Conwaya z wykorzystaniem pythona i biblioteki matplotlib.

Autora: Mahesh Venkitachalam
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]


def randomGrid(N):
    """zwraca planszę N x N losowych wartości"""
    return np.random.choice(vals, N * N, p=[0.2, 0.8]).reshape(N, N)


def addGlider(i, j, grid):
    """dodaje szybowiec z lewą górną komórką w (i, j)"""
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i + 3, j:j + 3] = glider


def addGosperGliderGun(i, j, grid):
    """dodaje Gosper Glider Gun z lewą górną komórką w (i, j)"""
    gun = np.zeros(11 * 38).reshape(11, 38)

    gun[5][1] = gun[5][2] = 255
    gun[6][1] = gun[6][2] = 255

    gun[3][13] = gun[3][14] = 255
    gun[4][12] = gun[4][16] = 255
    gun[5][11] = gun[5][17] = 255
    gun[6][11] = gun[6][15] = gun[6][17] = gun[6][18] = 255
    gun[7][11] = gun[7][17] = 255
    gun[8][12] = gun[8][16] = 255
    gun[9][13] = gun[9][14] = 255

    gun[1][25] = 255
    gun[2][23] = gun[2][25] = 255
    gun[3][21] = gun[3][22] = 255
    gun[4][21] = gun[4][22] = 255
    gun[5][21] = gun[5][22] = 255
    gun[6][23] = gun[6][25] = 255
    gun[7][25] = 255

    gun[3][35] = gun[3][36] = 255
    gun[4][35] = gun[4][36] = 255

    grid[i:i + 11, j:j + 38] = gun


def update(frameNum, img, grid, N):
    # kopiowanie planszy, ponieważ potrzebujemy 8 sąsiadów do obliczeń
    # i idziemy linia po linii
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # obliczanie sumy dla 8 sąsiadów przy użyciu
            # toroidalnych warunków brzegowych - x i y są zawijane,
            # aby symulacja odbywała się na powierzchni toroidalnej.
            total = int((grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                         grid[(i - 1) % N, j] + grid[(i + 1) % N, j] +
                         grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N] +
                         grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / 255)
            # zastosowanie reguł Conwaya
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
    # aktualizacja danych
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,


# funkcja main()
def main():
    # Argumenty wiersza poleceń są w sys.argv[1], sys.argv[2], ...
    # sys.argv[0] jest nazwą samego skryptu i może być zignorowane
    # parsowanie argumentów
    parser = argparse.ArgumentParser(description="Uruchamianie symulacji Gry w życie Conwaya.")
    # dodawanie argumentów
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()

    # ustawianie rozmiaru planszy
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # ustawianie interwału aktualizacji animacji
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # deklarowanie planszy
    grid = np.array([])
    # sprawdzenie, czy została określona flaga demo "glider"
    if args.glider:
        grid = np.zeros(N * N).reshape(N, N)
        addGlider(1, 1, grid)
    elif args.gosper:
        grid = np.zeros(N * N).reshape(N, N)
        addGosperGliderGun(10, 10, grid)
    else:
        # zapełnianie planszy losowymi włączonymi i wyłączonymi komórkami - więcej wyłączonych niż włączonych
        grid = randomGrid(N)

    # konfigurowanie animacji
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)

    # liczba ramek?
    # konfigurowanie pliku wyjściowego
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


# wywołanie main
if __name__ == '__main__':
    main()
