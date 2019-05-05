// ConsoleApplication1.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

//#include "pch.h"
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <vector>
#include "math.h"

using namespace std;

//входные параметры
float Pi = 3.1415926535;
float Gi = 9.80665;

float ro = 1.185; //плотность, кг/м^3
float V0 = 52; //скорость м/с
float m = 45354 * 2 / Gi; //масса кг
float S = 47.34 * 2; //площадь
float P0 = 2969 * 2; //тяга
float b = 9; //хорда
float xct = 0.2 / 0.9; //центровка по Ox в долях САХ
float yct = 0; //центровка по Oy в долях САХ
float y1p = 0; //ордината приложения тяги, в долях САХ
float fi0 = 3.1415 / 180; //угол тангажа начальный
float InercZ = 2.166 * pow(10, 5); //момент инерции вращения по тангажу
float iz = InercZ / (m * b * b); //безразмерный момент инерции вращения по тангажу
float myu = 2 * m / (ro * S * b); //безразмерная масса
float mgbezrazm = 2 * m * 9.81 / (ro * V0 * V0 * S); //безразмерная подъемная сила???
float cpv = 2 * P0 / (ro * S * V0); //коэффициент тяги
float cx0 = 0.046574; //коэффициент сопротивления
float cy0 = 0.65; //коэффициент подъемной силы
float cp = cx0; //коэффициент тяги
float cx0h = -0.104; //производная коэффициента сопротивления по высоте
float cx0al = 0.777; //производная коэффициента сопротивления по тангажу
float cy0h = -1.65; //производная коэффициента подъемной силы по высоте
float cy0al = 7.65; //производная коэффициента подъемной силы по углу тангажа
float mz0 = 0; //коэффициент момента тангажа
float mz0h = 0.205; //производная коэффициента момента тангажа по высоте
float mz0al = -1.195; //производная коэффициента момента тангажа по углу
float mzwz = -2.7; //производная коэффициента момента тангажа по безразмерной скорости вращения по тангажу 
float tau = 2 * m / (ro * S * V0);
float fulltime = 0;

float dimdeltaV = 1; //начальное приближение изменения скорости

float deltaV = 0;
float deltateta = 0;
float deltaphi = 0;
float deltaclearence = 0;
float deltaomegazet = 0;

vector<float> V; //скорость;
vector<float> teta; //угол траектории;
vector<float> clearence; //высота;
vector<float> phi; //угол тангажа;
vector<float> omegazet; //угловая скорость тангажа;

int main()
{
	ofstream fout("rezultatiP1_10s_pikir.csv"); // создаём объект класса ofstream для записи и связываем его с файлом cppstudio.txt
	//fout << "время" << "," << "скорость" << "," << "угол_траектории" << "," << "высота" << "," << "угол_тангажа" << "," << "угловая_скорость_тангажа" << "\n"; // запись строки в файл
	int length = 1000;
	float dt = 0.01 / tau;
	int eto;

	/*размеры массивов*/
	V.resize(length + 1);
	teta.resize(length + 1);
	clearence.resize(length + 1);
	phi.resize(length + 1);
	omegazet.resize(length + 1);

	/*исходные значения*/
	V[0] = dimdeltaV / V0;
	teta[0] = Pi / 180 * 0;
	clearence[0] = 0.1;
	phi[0] = Pi / 180 * 1;
	omegazet[0] = -0.1;

	/*запись исходных значений*/
	fout << fulltime << "," << V[0] * V0 + V0 << "," << teta[0] << " " << clearence[0] << "," << phi[0] << "," << omegazet[0] << "\n";

	for (int i = 0; i < length; i++)
	{
		/*все величины в безразмерной форме*/
		deltaV = cpv * V[i] * cos(phi[i]) - 2 * P0 * sin(phi[i]) * (phi[i] - teta[i]) / (ro * V0 * V0 * S) - 2 * cx0 * V[i] - (cx0al * ((phi[i] - teta[i]) + cx0h * (clearence[i] - (1 - xct) * cos(phi[i]) * phi[i]) + yct * sin(phi[i]) * phi[i])) - 2 * m * Gi * teta[i] / (ro * V0 * V0 * S);
		deltateta = cpv * V[i] * sin(phi[i]) + 2 * P0 * cos(phi[i]) * (phi[i] - teta[i]) / (ro * V0 * V0 * S) + 2 * cy0 * V[i] + (cy0al * ((phi[i] - teta[i]) + cy0h * (clearence[i] - (1 - xct) * cos(phi[i]) * phi[i]) + yct * sin(phi[i]) * phi[i]));
		deltaomegazet = 2 * mz0 * V[i] + mz0al * (phi[i] - teta[i]) + mz0h * (clearence[i] - (1 - xct) * cos(phi[i]) * phi[i] + yct * sin(phi[i]) * phi[i]) + mzwz * omegazet[i] - cpv * y1p * V[i];

		V[i + 1] = V[i] + dt * deltaV;
		clearence[i + 1] = clearence[i] + teta[i] * dt * myu;
		phi[i + 1] = phi[i] + omegazet[i] * dt;
		teta[i + 1] = teta[i] + deltateta * dt;
		omegazet[i + 1] = omegazet[i] + dt * myu / iz * deltaomegazet;

		fulltime = fulltime + dt;

		if (i % 5 == 0)
		{
			fout << fulltime * tau << "," << V0 + V[i + 1] * V0 << "," << teta[i + 1] / 0.0174 << "," << clearence[i + 1] << "," << phi[i + 1] / 0.0174 << "," << omegazet[i + 1] / b * V[i + 1] << "\n";
		}

	}



	fout.close(); // закрываем файл
	system("pause");
	return 0;
}

// Запуск программы: CTRL+F5 или меню "Отладка" > "Запуск без отладки"
// Отладка программы: F5 или меню "Отладка" > "Запустить отладку"

// Советы по началу работы 
//   1. В окне обозревателя решений можно добавлять файлы и управлять ими.
//   2. В окне Team Explorer можно подключиться к системе управления версиями.
//   3. В окне "Выходные данные" можно просматривать выходные данные сборки и другие сообщения.
//   4. В окне "Список ошибок" можно просматривать ошибки.
//   5. Последовательно выберите пункты меню "Проект" > "Добавить новый элемент", чтобы создать файлы кода, или "Проект" > "Добавить существующий элемент", чтобы добавить в проект существующие файлы кода.
//   6. Чтобы снова открыть этот проект позже, выберите пункты меню "Файл" > "Открыть" > "Проект" и выберите SLN-файл.
