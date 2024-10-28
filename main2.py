from turtle import color
import pandas as pd
import matplotlib.pyplot as plt

#diavasma tou excel apo to arxeio
df_sheet_name = pd.read_excel('pandas_to_excel.xlsx', sheet_name='sheet1')
print (df_sheet_name)


#upologismos mesou orou twn kenwn keliwn ana stili
percent_missing = df_sheet_name.isnull().sum() * 100 / len(df_sheet_name)
print(percent_missing)

#sumplirwsi keliwn me ton meso oro tis stilis
print (df_sheet_name.fillna(df_sheet_name.mean()))

plot = df_sheet_name.plot.scatter(x = 'rating', y = 'price', color="blue");

plt.savefig('saved_figure.png')