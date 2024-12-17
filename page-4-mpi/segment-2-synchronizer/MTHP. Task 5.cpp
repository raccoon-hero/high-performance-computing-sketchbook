#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    int size, rank, count;
    long* longData;  // динамічний масив
    MPI_Status status; // інформація про отримане повідомлення (джерело, тег, кількість отриманих елементів)

    int rank = 3;  // довільний номер

    // ініціалізація MPI-середовища
    MPI_Init(&argc, &argv);

    // отримати кількість процесів
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // отримати ранг (process ID)
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // запевнитись, що саме 2 процеси запущені
    if (size != 2)
    {
        if (rank == 0)
            printf("Only 2 tasks required instead of %d, abort\n", size);

        MPI_Barrier(MPI_COMM_WORLD);
        MPI_Abort(MPI_COMM_WORLD, MPI_ERR_OTHER);
        return -1;
    }

    // обчислити розмір буферу та кількість елементів для відправлення
    int buffer_size = rank * 10;  // розмір буферу (rank * 10)
    int num_elements = rank + 1;  // кількість елементів для відправлення (rank + 1)

    // виділення динамічної пам'яті для буфера
    longData = (long*)malloc(buffer_size * sizeof(long));

    if (rank == 1) // ПРОЦЕС #1 надсилає дані
    {
        // заповнити динамічний масив індексами
        for (int i = 0; i < num_elements; i++) {
            longData[i] = i + 1;
        }

        // відправити динамічний масив
        MPI_Send(longData, num_elements, MPI_LONG, 0, 100, MPI_COMM_WORLD);
    }
    else if (rank == 0) // ПРОЦЕС #0 отримує дані
    {
        // отримати дані у динамічний буфер
        MPI_Recv(longData, buffer_size, MPI_LONG, 1, 100, MPI_COMM_WORLD, &status);

        // визначити точне число отриманих елементів
        MPI_Get_count(&status, MPI_LONG, &count);

        // друк кількості отриманих елементів
        printf("Process 0: Received %d elements\n", count);

        // друк отриманих даних
        for (int i = 0; i < count; i++) {
            printf("Received data[%d] = %ld\n", i, longData[i]);
        }
    }

    // вивільнити динамічно розміщену пам'ять
    free(longData);

    // завершення MPI-середовища
    MPI_Finalize();

    return 0;
}

