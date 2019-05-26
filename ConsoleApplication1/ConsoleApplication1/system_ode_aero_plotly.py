import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go


# function that returns dz/dt
def model(z,t):
    # входные параметры
    Gi = 9.80665
    ro = 1.185  # плотность, кг/м^3
    V0 = 52  # скорость м/с
    m = 45354 * 2 / Gi  # масса кг
    S = 47.34 * 2  # площадь
    P0 = 2969 * 2  # тяга
    b = 9  # хорда
    xct = 0.2 / 0.9  # центровка по Ox в долях САХ
    yct = 0  # центровка по Oy в долях САХ
    y1p = 0  # ордината приложения тяги, в долях САХ
    fi0 =  0 #3.1415 / 180  # угол тангажа начальный
    InercZ = 2.166e5  # момент инерции вращения по тангажу
    iz = InercZ / (m * b * b)  # безразмерный момент инерции вращения по тангажу
    myu = 2 * m / (ro * S * b)  # безразмерная масса
    mgbezrazm = 2 * m * 9.81 / (ro * V0 * V0 * S)  # безразмерная подъемная сила???
    cpv = 2 * P0 / (ro * S * V0)  # коэффициент тяги
    cx0 = 0.046574  # коэффициент сопротивления
    cy0 = 0.65  # коэффициент подъемной силы
    cp = cx0  # коэффициент тяги
    cx0h = -0.104  # производная коэффициента сопротивления по высоте
    cx0al = 0.777  # производная коэффициента сопротивления по тангажу
    cy0h = -1.65  # производная коэффициента подъемной силы по высоте
    cy0al = 7.65  # производная коэффициента подъемной силы по углу тангажа
    mz0 = 0  # коэффициент момента тангажа
    mz0h = 0.205  # производная коэффициента момента тангажа по высоте
    mz0al = - 1.195  # производная коэффициента момента тангажа по углу
    mzwz = -2.7  # производная коэффициента момента тангажа по безразмерной скорости вращения по тангажу

    V = z[0]
    Theta = z[1]
    H = z[2]
    deltaNu = z[3]
    Omega_z = z[4]

    dVdt = cpv*V*np.cos(np.deg2rad(fi0))-(2*P0*np.sin(np.deg2rad(fi0))/ro*V0**2*S)*(deltaNu-Theta)-2*cx0*V-(cx0al*(deltaNu-Theta)+cx0h*(H-(1-xct)*np.cos(np.deg2rad(fi0))*deltaNu+yct*np.sin(np.deg2rad(fi0))*deltaNu))-(2*m*Gi/ro*V0**2*S)*Theta
    dThetadt = cpv*V*np.sin(np.deg2rad(fi0))+(2*P0*np.cos(np.deg2rad(fi0))/ro*V0**2*S)*(deltaNu-Theta)+2*cy0*V+(cy0al*(deltaNu-Theta)+cy0h*(H-(1-xct)*np.cos(np.deg2rad(fi0))*deltaNu+yct*np.sin(np.deg2rad(fi0))*deltaNu))
    dHdt = Theta*myu
    ddeltaNudt = Omega_z
    dOmega_zdt = (2*mz0*V+mz0al*(deltaNu-Theta)+mz0h*(H-(1-xct)*np.cos(np.deg2rad(fi0))*deltaNu+yct*np.sin(np.deg2rad(fi0))*deltaNu)+mzwz*Omega_z-cpv*y1p*V)*(myu/iz)
    dzdt = [dVdt, dThetadt, dHdt, ddeltaNudt, dOmega_zdt]
    return dzdt

# initial condition
z0 = [0.0, 1.0, 0.0, 0.0, 1.0]

# time points
t = np.linspace(0, 100, 1000)

# solve ODE
z = odeint(model, z0, t)

# plot results
V = z[:,0]
Theta = z[:,1]
H = z[:,2]
deltaNu = z[:,3]
Omega_z = z[:,4]

trace1 = go.Scatter(
    x=t,
    y=V,
    mode='lines+markers',
    name='V'
)

trace2 = go.Scatter(
    x=t,
    y=Theta,
    mode='lines+markers',
    name='Theta'
)

trace3 = go.Scatter(
    x=t,
    y=H,
    mode='lines+markers',
    name='H'
)

trace4 = go.Scatter(
    x=t,
    y=deltaNu,
    mode='lines+markers',
    name='deltaNu'
)

trace5 = go.Scatter(
    x=t,
    y=Omega_z,
    mode='lines+markers',
    name='Omega_z'
)

data = [trace1, trace2, trace3, trace4, trace5]

layout = go.Layout(
        legend=dict(
                orientation="h",
                traceorder='normal',
                bgcolor='white',
                bordercolor='black',
                borderwidth=0.5
        ),
        title='Графики',
        showlegend=True,
        xaxis=dict(
            showgrid=True,
            mirror='ticks',
            title='X',
            ticks='',
            automargin=True,
            gridcolor='grey',
            gridwidth=0.5,
            zerolinecolor='black',
            zerolinewidth=0.25,
            linecolor='black',
            linewidth=0.5),
        yaxis=dict(
            showgrid=True,
            mirror='ticks',
            title='Y',
            ticks='',
            automargin=True,
            gridcolor='grey',
            gridwidth=0.5,
            zerolinecolor='black',
            zerolinewidth=0.25,
            linecolor='black',
            linewidth=0.5),
        width=900,
        height=700,
        margin=dict(
            l=80,
            r=50,
            b=50,
            t=30)
)
config = {
    'linkText': "a&m",
    'scrollZoom': True,
    'displayModeBar': True,
    'editable': True
}

plotly.offline.plot(dict(data=data, layout=layout), config=config, filename='simple-plots.html', auto_open=True)


# plt.plot(t, V, 'b-',label='V')
# plt.plot(t,Theta,'g-',label='Theta')
# plt.plot(t,H,'r-',label='H')
# plt.plot(t,deltaNu,'c-',label='deltaNu')
# plt.plot(t,Omega_z,'m-',label='Omega_z')
# plt.ylabel('Function')
# plt.xlabel('time')
# plt.legend(loc='best')
# plt.show()