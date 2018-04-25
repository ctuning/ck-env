import os
import string
default_value = 'Not defined'
mpi = os.getenv('CK_ENV_LIB_MPI_CC', default_value)
version = mpi.split(".")[1]
print version
