### FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead. df = df.append(df2)
  
**Don't do**

df = df.append(df2)

**Do**

df = pd.concat([df, df2], ignore_index=True)
