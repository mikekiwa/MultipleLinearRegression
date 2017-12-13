# multiplelinreg.py
#
# Standalone Python/Spark program to perform multiple linear regression.
# Performs multiple linear regression by computing the summation form of the
# closed form expression for the ordinary least squares estimate of beta.
# 
# TODO: Write this.
# 
# Takes the yx file as input, where on each line y is the first element 
# and the remaining elements constitute the x.
#
# Usage: spark-submit multiplelinreg.py <inputdatafile>
# Example usage: spark-submit multiplelinreg.py yxlin.csv
#
# Written by: Ashwin Venkatesh Prabhu
# UNCC ID: 800960400
# Email: avenka11@uncc.edu

import sys
import numpy as np

from pyspark import SparkContext

# Creates X matrix, and returns Transpose(X) * X
def CalculateXTX(value_X):
  # Here, we first form a row matrix from the values of X which are passed
  matX = np.matrix(value_X, dtype='float')
  
  # Here, we insert value 1 at 0th position of row matrix we created in the 
  # previous step to get the X
  X = np.insert(matX, 0, 1, axis = 1)

  # Calculate the transpose of X
  transpose_X = X.T
  
  # Calculate X * transpose(X)
  XTX = np.dot(transpose_X, X)
  
  return XTX

# Creates X and Y matrix, and returns transpose(X) * Y
def CalculateXTY(value_X, value_Y):
  # Here, we first form a row matrix from the values of X which are passed
  matX = np.matrix(value_X, dtype='float')

  # Here, we insert value 1 at 0th position of row matrix we created in the 
  # previous step to get the transpose(X)
  X = np.insert(matX, 0, 1, axis = 1)

  # Calculate the transpose of X
  transpose_X = X.T

  # Here, we first form a row matrix from the values of Y which are passed
  Y = np.matrix(value_Y, dtype='float')

  # Calculate X * Y
  XTY = np.dot(transpose_X, Y)

  return XTY

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print >> sys.stderr, "Usage: multiplelinreg <datafile>"
    exit(-1)

  sc = SparkContext(appName="MultipleLinearRegression")

  # Input yx file has y_i as the first element of each line 
  # and the remaining elements constitute x_i
  yxinputFile = sc.textFile(sys.argv[1])

  yxlines = yxinputFile.map(lambda line: line.split(','))
  yxfirstline = yxlines.first()
  yxlength = len(yxfirstline)
  #print "yxlength: ", yxlength

  # dummy floating point array for beta to illustrate desired output format
  beta = np.zeros(yxlength, dtype=float)

  # Here, we use the map and reduce task to get the sum of transpose(X) * X
  # values of all the data points
  # The map task passes x value in each line to CalculateXTX method, which 
  # creates the X matrix and calculates transponse(X) * X
  # The reduce task will add all the results from the map task
  temp_XTX = yxlines.map(lambda line : CalculateXTX(line[1:]))
  XTX = temp_XTX.reduce(lambda a, b : np.add(a, b))
  print "XTX: ", XTX

  # We use the inbuilt np.linalg.inv method to get the inverse(transpose(X) * X)
  inverseXTX = np.linalg.inv(np.matrix(XTX))
  print "Inverse XTX: ", inverseXTX

  # Here, we use the map and reduce task to get the sum of transpose(X) * Y
  # values of all the data points
  # The map task passes x and y values in each line to CalculateXTY method, which 
  # creates the X and Y matrix, calculates transpose(X) * Y
  # The reduce task will add all the results from the map task
  temp_XTY = yxlines.map(lambda line : CalculateXTY(line[1:], line[0]))
  XTY = temp_XTY.reduce(lambda a, b : np.add(a, b))
  print "XTY: ", XTY

  # We multiply Inverse(transponse(X) * X) and (transpose(X) * Y), which gives use beta
  beta = np.dot(inverseXTX, XTY)

  # print the linear regression coefficients in desired output format
  print "beta: "
  for coeff in beta:
      print coeff

  sc.stop()
