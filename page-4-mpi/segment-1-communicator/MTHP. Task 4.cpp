#include "mpi.h"
#include <stdio.h>


int main(int argc, char* argv[])
{
    int size, rank, i;

    // ініціалізаія MPI-середовища
    MPI_Init(&argc, &argv);

    // отримати кількість процесів
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // отримати ранг (process ID)
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // процес з рангом 0 друкуватиме загальну кількість процесів
    if (rank == 0)
        printf("Amount of tasks = %d\n", size);

    // синхронізувати всі процеси перед друком
    MPI_Barrier(MPI_COMM_WORLD);
    
    // кожен процес друкує свій ранг та парне (even) / непарне (odd)
    printf("My number in MPI_COMM_WORLD = %d, and it is %s\n", rank, (rank % 2 == 0) ? "even" : "odd");
        
    // синхронізувати всі процеси перед друком
    MPI_Barrier(MPI_COMM_WORLD);

    // процес з рангом 0 друкує аргументи командної стрічки
    if (rank == 0) {
        printf("CommandLine for task 0:\n");
        for (i = 0; i < argc; i++)
            printf("%d: \"%s\"\n", i, argv[i]);
    }

    // завершення MPI-середовища
    MPI_Finalize();

    return 0;
}
