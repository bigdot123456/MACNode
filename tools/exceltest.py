import pandas as pd
import os
import numpy as np

path = os.path.dirname(os.path.abspath(__file__))
source_file = os.path.join(path, 'source.xlsx')
output_file = os.path.join(path, 'output.xlsx')
df = pd.read_excel(source_file, sheet_name=0)
df.to_excel(output_file)

A = np.array([[1,2,3],[4,5,6]])
df = pd.DataFrame(A)
df.to_excel('test_excel.xlsx',sheet_name='A')

writer = pd.ExcelWriter('test_excel.xlsx')
A = np.array([[1,2,3],[4,5,6]])
B = np.array([[10, 20, 30], [40, 50, 60]])

df1 = pd.DataFrame(A)
df2 = pd.DataFrame(B)
df1.to_excel(writer,sheet_name='AAA')
df2.to_excel(writer,sheet_name='BBB')
writer.close()
