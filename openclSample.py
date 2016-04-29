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
    min_rsi = analyst.getMinRSI()
    max_rsi = analyst.getMaxRSI()
    mid_rsi = analyst.getAverageRSI()    
    ''''
    a = range((mid_rsi - min_rsi - 1) * (max_rsi - mid_rsi))
    n = mid_rsi - min_rsi - 1
    m = max_rsi - mid_rsi
    matrix = numpy.zeros( (n,m),numpy.float32 )
    
    platform = cl.get_platforms()[0]
    device = platform.get_devices()[0]
    context = cl.Context([device])
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
          int id2 = get_global_id(1);

          int up_rsi = size[2]+ id;
          int lb_rsi = size[1]+ id2;
          
          int n = size[2] - size[1] - 1;
          
          int k =0;
        for (k=0;k<size[0];k++){
            //printf(" thread %d - rsi %f sam 25 %f sam 50 %f \\n",id,rsi[k],sam_25[k],sam_50[k]);
            if(rsi[k] > up_rsi && sam_25[k] < sam_50[k]){
                //printf("day %d - buying at thread %d %d \\n",k,lb_rsi,up_rsi);
                profit = profit - closing_value[k];
                total_bought = total_bought + 1;
                stocks_left = stocks_left + 1;
            }else if(rsi[k]< lb_rsi && sam_25[k]>sam_50[k] && stocks_left > 0){
                //printf("day %d - selling at thread %d %d \\n",k,lb_rsi,up_rsi);
                profit = profit + closing_value[k];
                total_sold = total_sold + 1;
                stocks_left = stocks_left - 1;
            }
        }

        int diff_num = total_sold - total_bought;
        float settled_profit = profit - diff_num*closing_value[0];
        result[id + n*id2 ] = settled_profit;
        
        //printf("%d %d -> %f\\n",lb_rsi,up_rsi,settled_profit);
        }
        """).build()
     
    queue = cl.CommandQueue(context)
    no_of_entries = analyst.getNumberOfEntries()
    
    size = numpy.array([no_of_entries,min_rsi,mid_rsi,max_rsi],dtype=numpy.int32)

    mem_flags = cl.mem_flags
    rsi_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=rsi_14_day)
    sam_25_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=sam_25_day)
    sam_50_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=sam_50_day)
    values_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=closing_value)
    size_buf = cl.Buffer(context, mem_flags.READ_ONLY | mem_flags.COPY_HOST_PTR, hostbuf=size)
    
    destination_buf = cl.Buffer(context, mem_flags.WRITE_ONLY, matrix.nbytes)
    
    
    program.device_function(queue,matrix.shape, None, rsi_buf,sam_25_buf, sam_50_buf,values_buf,size_buf,destination_buf)
     
    cl.enqueue_copy(queue, matrix, destination_buf)
    
    colmax = 0
    rowmax = 0
    max_profit = 0
    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            profit = row[j]
            if profit > max_profit:
                colmax = j
                rowmax = i
                max_profit = profit
            
    
    print "max profit obtained is ",max_profit,"at bounds",rowmax+min_rsi,colmax+mid_rsi-1
            

    # for i in range(35*36):
 #        print str(19 + i%35)+","+str(55 + i/35) + "->" + str(result[i])
 #     
    
    
    
    
    '''
    
    
    
    