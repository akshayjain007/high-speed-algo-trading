import pyopencl as cl
from pyopencl import array
import numpy


 
if __name__ == "__main__":
    #a array of values we'll pass to the kernel to perform computations to
    a = range(10)
    values = numpy.array(a,dtype=numpy.float32)
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
        __kernel void device_function(__global const float *values, __global float *result)
        {
          int id = get_global_id(0);
          result[id] = 2 * values[id];
        }
        """).build()
     
    ## Step #7. Create a command queue for the target device.
    queue = cl.CommandQueue(context)
     
    ## Step #8. Allocate device memory and move input data from the host to the device memory.
    mem_flags = cl.mem_flags
    values_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=values)
    result = numpy.array(a,dtype=numpy.float32)
    destination_buf = cl.Buffer(context, mem_flags.WRITE_ONLY, result.nbytes)
     
    ## Step #9. Associate the arguments to the kernel with kernel object.
    ## Step #10. Deploy the kernel for device execution.
    program.device_function(queue,result.shape, None, values_buf, destination_buf)
     
    ## Step #11. Move the kernel's output data to host memory.
    cl.enqueue_copy(queue, result, destination_buf)
     
    ## Step #12. Release context, program, kernels and memory.
    ## PyOpenCL performs this step for you, and therefore,
    ## you don't need to worry about cleanup code
     
    print(result)