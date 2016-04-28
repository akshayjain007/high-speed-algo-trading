import pyopencl as cl
from pyopencl import array
import numpy
import pandas as pd
import os
from StockData import StockData

if __name__ == "__main__":
    #a array of values we'll pass to the kernel to perform computations to

    os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'
    
    analyst = StockData('goog.csv')
    closing_value = numpy.array(analyst.getClosingValue(),dtype=numpy.float32)
    rsi_14_day = numpy.array(analyst.getRSIArray(),dtype=numpy.float32)
    sam_50_day = numpy.array(analyst.getSMA_50_day(), dtype=numpy.float32)
    sam_25_day = numpy.array(analyst.getSMA_25_day(), dtype=numpy.float32)
    
    a = range(35*36)
    
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
        __kernel void device_function(__global const float *rsi,
        __global const float *sam_25,
        __global const float *sam_50,
        __global const float *closing_value,
        __global const int *size,
         __global float *result)
        {
          float profit = 0;
          int total_bought = 0;
          int total_sold = 0;
          int stocks_left = 0;
          
          int id = get_global_id(0);
          
          int up_rsi = 55 + id/35;
          int lb_rsi = 19 + id%35;
          
          //printf("%d\\n",size[0]);
          int k =0;
          for (k=0;k<size[0];k++){
              //printf(" thread %d - rsi %f sam 25 %f sam 50 %f \\n",id,rsi[k],sam_25[k],sam_50[k]);
              if(rsi[k] > up_rsi && sam_25[k] < sam_50[k]){
                  //printf("buying at thread %d \\n",id);
                  profit = profit - closing_value[k];
                  total_bought = total_bought + 1;
                  stocks_left = stocks_left + 1;
              }else if(rsi[k]< lb_rsi && sam_25[k]>sam_50[k] && stocks_left > 0){
                  //printf("selling at thread %d \\n",id);
                  profit = profit + closing_value[k];
                  total_sold = total_sold + 1;
                  stocks_left = stocks_left - 1;
              }
          }
          
          int diff_num = total_sold - total_bought;
          float settled_profit = profit - diff_num*closing_value[0];
          result[id] = settled_profit;
        }
        """).build()
     
    ## Step #7. Create a command queue for the target device.
    queue = cl.CommandQueue(context)
    no_of_entries = min(len(rsi_14_day), len(sam_50_day), len(sam_25_day))
    
    size = numpy.array([no_of_entries - 50],dtype=numpy.int32)
    ## Step #8. Allocate device memory and move input data from the host to the device memory.
    mem_flags = cl.mem_flags
    rsi_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=rsi_14_day)
    sam_25_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=sam_25_day)
    sam_50_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=sam_50_day)
    values_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=closing_value)
    size_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=size)
    result = numpy.array(a,dtype=numpy.float32)
    destination_buf = cl.Buffer(context, mem_flags.WRITE_ONLY, result.nbytes)
    
    ## Step #9. Associate the arguments to the kernel with kernel object.
    ## Step #10. Deploy the kernel for device execution.
    program.device_function(queue,result.shape, None, rsi_buf,sam_25_buf, sam_50_buf,values_buf,size_buf,destination_buf)
     
    ## Step #11. Move the kernel's output data to host memory.
    cl.enqueue_copy(queue, result, destination_buf)
     
    ## Step #12. Release context, program, kernels and memory.
    ## PyOpenCL performs this step for you, and therefore,
    ## you don't need to worry about cleanup code
    for i in range(35*36):
        print str(19 + i%35)+","+str(55 + i/35) + "->" + str(result[i])
        
    
    
    
    
    
    
    
    
    