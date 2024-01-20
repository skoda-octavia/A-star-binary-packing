import matplotlib.pyplot as plt
import numpy as np

plt.ion()  # Włącz interaktywny tryb rysowania

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

for i in range(50):
    y = np.random.random([10, 1])

    # Rysuj aktualizację wykresu
    axs[0].plot(y, color='blue', alpha=0.1)  # Użyj alpha, aby utworzyć efekt nakładania się
    axs[1].plot(y, color='blue', alpha=0.1)  # Użyj alpha, aby utworzyć efekt nakładania się
    plt.draw()
    plt.pause(0.0001)

plt.ioff()  # Wyłącz interaktywny tryb rysowania po zakończeniu pętli
plt.show()  # Wyświetl ostateczny wykres
