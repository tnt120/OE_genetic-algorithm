from population import Population
from config import EPOCHS

if __name__ == "__main__":
    pop = Population()
    print("Start populacji:")
    print(pop)

    for epoch in range(EPOCHS):
        pop.evolve()
        best = pop.best()
        print(f"Epoka {epoch+1}: Najlepszy -> {best}")

    print("\nFinalny wynik:")
    print(pop.best())