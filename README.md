ITCS 6190 - Cloud Computing for Data Analysis - Assignment 4
-----------------------------------------------------------------------------------------

This is a read me document for the assignment 4 and explains all the files involved.

The input files used for this program are yxlin.csv and yxlin2.csv. These files contain y and x values.

The program works in the following way.
1) multiplelinreg.py contains the source code. This program will access the file passed in at command line and take in all the y and x values as input.

2) This program runs on two MapReduce jobs. The first map reduce job does the following task. The mapper will take in the x values from each line and pass it to CalculateXTX method, which will generate the x matrix and find the transpose of that matrix. Then multiply transpose(x) and x. The reducer will combine all the results from the mapper.

3) The result from the first map reduce job gives us, transpose(X) * X. Now we calculate Inverse(transpose(X) * X) needed for the final calculation. 

4) The second map reduce job does the following. The mapper will take in the x and y values from each line and pass it to CalculateXTY method, which will generate the x matrix and y matrix. It will also find the transpose of x matrix. Then multiply transpose(x) and y. The reducer will combine all the results from the mapper. Now we have value of transpose(X) * Y

5) Finally, we multiply Inverse(transpose(X) * X) and transpose(X) * Y to get the beta coefficients.

REFERENCES USED:
-----------------------------------------------------------------------------------------

1) NumPy - https://docs.scipy.org/doc/numpy-dev/reference/index.html

-----------------------------------------------------------------------------------------
NOTE: I HAVE RAN THIS PROGRAM ON A CLUSTER

- Copy all the source code files and input files onto the cluster
- Copy the input files into an input location on hdfs, say INPUT_DIR
- Run the source code using the following command - spark-submit multiplelinreg.py <inputdatafile>
-----------------------------------------------------------------------------------------
