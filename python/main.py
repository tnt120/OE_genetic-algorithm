from population import Population
from config import EPOCHS
import time

if __name__ == "__main__":
    pop = Population()
    print("Start populacji:")
    print(pop)

    start_time = time.time()
    for epoch in range(EPOCHS):
        pop.evolve()
        best = pop.best()
        print(f"Epoka {epoch+1}: Najlepszy -> {best}")
        if round(best.fitness, 4) == 0.0000:
            print("Znaleziono optymalne rozwiazanie")
            break
    
    end_time = time.time()
    ellapsed_time = round(end_time - start_time, 2)
    print("\nFinalny wynik:")
    print(pop.best())
    print(f"Czas wykonania: {ellapsed_time}s")