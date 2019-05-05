import pandas as pd
import matplotlib.pyplot as plt

dn = pd.Series(["время","скорость","угол_траектории","высота","угол_тангажа","угловая_скорость_тангажа"])
df = pd.read_csv('rezultatiP1_10s_pikir.csv', names=dn)
df = df.convert_objects(convert_numeric=True)

def inOneFrame():
    ax = plt.gca()
    df.plot(x='время', y='скорость',ax=ax)
    df.plot(x='время', y='угол_траектории',ax=ax)
    df.plot(x='время', y='высота',ax=ax)
    df.plot(x='время', y='угол_тангажа',ax=ax)
    df.plot(x='время', y='угловая_скорость_тангажа',ax=ax)
    plt.grid(True)
    plt.show()

def allSeparatedFrames():
    df.plot(x='время', y='скорость')
    plt.grid(True)
    df.plot(x='время', y='угол_траектории')
    plt.grid(True)
    df.plot(x='время', y='высота')
    plt.grid(True)
    df.plot(x='время', y='угол_тангажа')
    plt.grid(True)
    df.plot(x='время', y='угловая_скорость_тангажа')
    plt.grid(True)
    plt.show()

# inOneFrame()

allSeparatedFrames()
