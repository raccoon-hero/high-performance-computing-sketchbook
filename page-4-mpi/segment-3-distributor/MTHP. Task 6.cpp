#include <mpi.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

#define MAX_STRING_SIZE 100

#ifndef M_PI
    #define M_PI 3.14159265358979323846
#endif

int main(int argc, char* argv[])
{
    int rank, size;
    MPI_Status status;

    // ініціалізація MPI-середовища
    MPI_Init(&argc, &argv);

    // отримати кількість процесів
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // отримати ранг (process ID)
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // упевнитись, що саме 4 процеси запущено
    if (size != 4) {
        if (rank == 0)
            printf("This program requires 4 processes. Terminating...\n");
        MPI_Abort(MPI_COMM_WORLD, MPI_ERR_OTHER);
        MPI_Finalize();
        return -1;
    }

    // визначення змінних
    char surname[MAX_STRING_SIZE] = "Petrachyk";  // прізвище для відправлення
    char fullname[MAX_STRING_SIZE]; // повне ім'я [від ПРОЦЕС 1]
    int num_chars; // кількість символів прізвища [від ПРОЦЕС 2]
    double sum_ascii_pi; // сума ASCII-значень * π [від ПРОЦЕС 3]

    if (rank == 0) { 
        // ПРОЦЕС 0: надсилає прізвище до ПРОЦЕС 1, ПРОЦЕС 2, ПРОЦЕС 3
        
        for (int i = 1; i < 4; i++) {
            MPI_Send(surname, strlen(surname) + 1, MPI_CHAR, i, 0, MPI_COMM_WORLD);
        }

        // отримати конкатиноване ім'я від ПРОЦЕС 1
        MPI_Recv(fullname, MAX_STRING_SIZE, MPI_CHAR, 1, 1, MPI_COMM_WORLD, &status);
        printf("Process 0 received full name: %s\n", fullname);

        // отримати кількість символів від ПРОЦЕС 2
        MPI_Recv(&num_chars, 1, MPI_INT, 2, 2, MPI_COMM_WORLD, &status);
        printf("Process 0 received number of characters: %d\n", num_chars);

        // отримати суму ASCII-кодів * π від ПРОЦЕС 3
        MPI_Recv(&sum_ascii_pi, 1, MPI_DOUBLE, 3, 3, MPI_COMM_WORLD, &status);
        printf("Process 0 received sum of ASCII codes * pi: %.2f\n", sum_ascii_pi);
    }
    else if (rank == 1) {
        // ПРОЦЕС 1: конкатинує прізвище з іменем та надсилає назад до ПРОЦЕС 0
        
        char first_name[] = "Kyryl";  // ім'я для конкатинації з прізвищем
        char received_surname[MAX_STRING_SIZE];

        // отримати прізвище від ПРОЦЕС 0
        MPI_Recv(received_surname, MAX_STRING_SIZE, MPI_CHAR, 0, 0, MPI_COMM_WORLD, &status);

        int chars_received;
        MPI_Get_count(&status, MPI_CHAR, &chars_received);
        received_surname[chars_received] = '\0';  // нуль-термінований рядок

        // конкатинувати ім'я та прізвище
        snprintf(fullname, MAX_STRING_SIZE, "%s %s", first_name, received_surname);

        // відправити конкатиноване ім'я назад до ПРОЦЕС 0
        MPI_Send(fullname, strlen(fullname) + 1, MPI_CHAR, 0, 1, MPI_COMM_WORLD);
    }
    else if (rank == 2) {
        // ПРОЦЕС 2: обчислює кількість символів у прізвищі та надсилає наза до ПРОЦЕС 0
        
        char received_surname[MAX_STRING_SIZE];

        // отримати прізвище від ПРОЦЕС 0
        MPI_Recv(received_surname, MAX_STRING_SIZE, MPI_CHAR, 0, 0, MPI_COMM_WORLD, &status);

        int chars_received;
        MPI_Get_count(&status, MPI_CHAR, &chars_received);
        received_surname[chars_received] = '\0';  // нуль-термінований рядок

        // злічити кілкьість символів
        num_chars = strlen(received_surname);

        // відправити кількість символів назад до ПРОЦЕС 0
        MPI_Send(&num_chars, 1, MPI_INT, 0, 2, MPI_COMM_WORLD);
    }
    else if (rank == 3) {
        // ПРОЦЕС 3: розраховує суму ASCII-кодів символів прізвища * π, відправляє назад до ПРОЦЕС 0
        
        char received_surname[MAX_STRING_SIZE];
        double sum_ascii = 0.0;

        // отримати прізвище від ПРОЦЕС 0
        MPI_Recv(received_surname, MAX_STRING_SIZE, MPI_CHAR, 0, 0, MPI_COMM_WORLD, &status);

        int chars_received;
        MPI_Get_count(&status, MPI_CHAR, &chars_received);
        received_surname[chars_received] = '\0';  // нуль-термінований рядок

        // сумування ASCII-значень кожного символу
        for (int i = 0; i < strlen(received_surname); i++) {
            sum_ascii += (double)received_surname[i];
        }

        // * π
        sum_ascii_pi = sum_ascii * M_PI;

        // відправити результат назад до ПРОЦЕС 0
        MPI_Send(&sum_ascii_pi, 1, MPI_DOUBLE, 0, 3, MPI_COMM_WORLD);
    }

    // завершення MPI-середовища
    MPI_Finalize();

    return 0;
}
