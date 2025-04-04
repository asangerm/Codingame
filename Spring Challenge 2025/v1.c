#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define MODULO (1 << 30)  // 2^30

// Fonction pour convertir la matrice en un entier modulo 2^30
long long encode_matrix(int *matrix[9])
{
    long long encoded = 0;
    for (int i = 0; i < 9; i++)
        encoded = (encoded * 10 + (*matrix[i])) % MODULO;  // Appliquer modulo 2^30
    return encoded;
}

void explore(int depth, int board[9]) {
    if (depth == 0) {
        sum = (sum + encode_matrix(board)) % MODULO;
        return;
    }

    for (int i = 0; i < 9; i++) {
        if (board[i] != 0) continue; // Case non vide

        int values[4], indices[4], count = 0;
        for (int j = 0; neighbors[i][j] != -1; j++) {
            int n = neighbors[i][j];
            if (board[n] > 0) {
                values[count] = board[n];
                indices[count] = n;
                count++;
            }
        }

        bool capture_done = false;

        // Générer toutes les combinaisons possibles de 2 à count voisins
        int total = 1 << count;
        for (int mask = 1; mask < total; mask++) {
            int bits = __builtin_popcount(mask);
            if (bits < 2) continue;

            int sum_vals = 0;
            for (int b = 0; b < count; b++) {
                if (mask & (1 << b)) sum_vals += values[b];
            }

            if (sum_vals <= 6) {
                // Appliquer la capture
                int new_board[9];
                memcpy(new_board, board, sizeof(int) * 9);
                for (int b = 0; b < count; b++) {
                    if (mask & (1 << b)) {
                        new_board[indices[b]] = 0;
                    }
                }
                new_board[i] = sum_vals;

                capture_done = true;
                explore(depth - 1, new_board);
            }
        }

        // Si pas de capture possible
        if (!capture_done) {
            int new_board[9];
            memcpy(new_board, board, sizeof(int) * 9);
            new_board[i] = 1;
            explore(depth - 1, new_board);
        }
    }
}

int main()
{
    int depth;      // profondeur du nombre de coups
    int *tab[9];    // Tableau de 9 pointeurs sur int
    int neighbors_count[9] = {2, 3, 2, 3, 4, 3, 2, 3, 2}; // Nombre de voisins par case

    scanf("%d", &depth); // Lecture de depth

    // Lecture et stockage des valeurs
    for (int i = 0; i < 9; i++)
    {
        int value;
        scanf("%d", &value); // Lire une valeur

        tab[i] = malloc(sizeof(int)); // Allouer de la mémoire
        if (tab[i] == NULL)
        {
            fprintf(stderr, "Erreur d'allocation mémoire\n");
            return 1; // Arrêter le programme en cas d'échec
        }

        *tab[i] = value; // Stocker la valeur lue dans la mémoire allouée
    }

    // Tableau d'adjacence stockant des pointeurs vers les voisins
    int **adjacency[9];

    // Allocation mémoire pour stocker les pointeurs de voisins
    for (int i = 0; i <9; i++)
    {
        adjacency[i] = malloc(neighbors_count[i] * sizeof(int *));
        if (adjacency[i] == NULL)
        {
            fprintf(stderr, "Erreur d'allocation mémoire\n");
            return 1;
        }
    }

    // Définition des voisins (stocke les pointeurs vers les cases detab)
    adjacency[0][0] =tab[1]; adjacency[0][1] =tab[3];               // a -> b, d
    adjacency[1][0] =tab[0]; adjacency[1][1] =tab[2]; adjacency[1][2] =tab[4]; // b -> a, c, e
    adjacency[2][0] =tab[1]; adjacency[2][1] =tab[5];               // c -> b, f
    adjacency[3][0] =tab[0]; adjacency[3][1] =tab[4]; adjacency[3][2] =tab[6]; // d -> a, e, g
    adjacency[4][0] =tab[1]; adjacency[4][1] =tab[3]; adjacency[4][2] =tab[5]; adjacency[4][3] =tab[7]; // e -> b, d, f, h
    adjacency[5][0] =tab[2]; adjacency[5][1] =tab[4]; adjacency[5][2] =tab[8]; // f -> c, e, i
    adjacency[6][0] =tab[3]; adjacency[6][1] =tab[7];               // g -> d, h
    adjacency[7][0] =tab[4]; adjacency[7][1] =tab[6]; adjacency[7][2] =tab[8]; // h -> e, g, i
    adjacency[8][0] =tab[5]; adjacency[8][1] =tab[7];               // i -> f, h

    // Affichage des valeurs des voisins
    for (int i = 0; i < 9; i++)
    {
        fprintf(stderr ,"Case %c (%d) -> ", 'a' + i, *tab[i]);
        for (int j = 0; j < neighbors_count[i]; j++)
            fprintf(stderr ,"%d ", *adjacency[i][j]); // Affichage des valeurs des voisins
        fprintf(stderr ,"\n");
    }

    // Modification d'une case et impact sur ses voisins
    fprintf(stderr ,"\nModification de la case 'e' (milieu) : +10\n");
    *tab[4] += 10;  // Modification directe de la case 'e'

    // Vérification de l'impact sur les voisins
    for (int i = 0; i < 9; i++)
    {
        fprintf(stderr ,"Case %c (%d) -> ", 'a' + i, *tab[i]);
        for (int j = 0; j < neighbors_count[i]; j++)
            fprintf(stderr ,"%d ", *adjacency[i][j]);
        fprintf(stderr ,"\n");
    }

    // Libération mémoire
    for (int i = 0; i <9; i++)
    {
        free(tab[i]);
        free(adjacency[i]);
    }

    return 0;
}