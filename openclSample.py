import pyopencl as cl
from pyopencl import array
import numpy


 
if __name__ == "__main__":
    vector = numpy.zeros((1, 1), cl.array.vec.float4)
    matrix = numpy.zeros((1, 4), cl.array.vec.float4)
    matrix2 = numpy.zeros((1,4), cl.array.vec.float4)
    
    matrix[0, 0] = (1, 2, 4, 8)
    matrix[0, 1] = (16, 32, 64, 128)
    matrix[0, 2] = (3, 6, 9, 12)
    matrix[0, 3] = (5, 10, 15, 25)
    
    matrix2[0, 0] = (1, 2, 4, 8)
    matrix2[0, 1] = (16, 32, 64, 128)
    matrix2[0, 2] = (3, 6, 9, 12)
    matrix2[0, 3] = (5, 10, 15, 25)
    
    vector[0, 0] = (1, 2, 4, 8)
     
    ## Step #1. Obtain an OpenCL platform.
    platform = cl.get_platforms()[0]
     
    ## It would be necessary to add some code to check the check the support for
    ## the necessary platform extensions with platform.extensions
     
    ## Step #2. Obtain a device id for at least one device (accelerator).
    device = platform.get_devices()[0]
     
    ## It would be necessary to add some code to check the check the support for
    ## the necessary device extensions with device.extensions
     
    ## Step #3. Create a context for the selected device.
    context = cl.Context([device])
     
    ## Step #4. Create the accelerator program from source code.
    ## Step #5. Build the program.
    ## Step #6. Create one or more kernels from the program functions.
    program = cl.Program(context, """
        #pragma OPENCL EXTENSION cl_amd_printf: enable
        __kernel void matrix_dot_vector(__global const float4 *matrix,
        __global const float4 *matrix2, __global float4 *result)
        {
          int i = get_global_id(0);
          int j = get_global_id(1);
          
          int k = 0;
          result[i][j] = 0;
          for(k=0;k<4;k++){
              result[i][j] += matrix[i][k] * matrix2[k][j];
              printf("for (%d,%d) multiplying %f and %f got %f\\n ",i,j,matrix[i][k],matrix2[k][j],result[i][j]);
          }
          
        }
        """).build()
     
    ## Step #7. Create a command queue for the target device.
    queue = cl.CommandQueue(context)
     
    ## Step #8. Allocate device memory and move input data from the host to the device memory.
    mem_flags = cl.mem_flags
    matrix_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=matrix)
    matrix2_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=matrix2)
    matrix_result = numpy.zeros((4,4), numpy.float32)
    destination_buf = cl.Buffer(context, mem_flags.WRITE_ONLY, matrix_result.nbytes)
     
    ## Step #9. Associate the arguments to the kernel with kernel object.
    ## Step #10. Deploy the kernel for device execution.
    program.matrix_dot_vector(queue, matrix_result.shape, None, matrix_buf, matrix2_buf, destination_buf)
     
    ## Step #11. Move the kernel's output data to host memory.
    cl.enqueue_copy(queue, matrix_result, destination_buf)
     
    ## Step #12. Release context, program, kernels and memory.
    ## PyOpenCL performs this step for you, and therefore,
    ## you don't need to worry about cleanup code
     
    print(matrix_result)