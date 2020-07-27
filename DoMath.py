import numpy as np


class DoingMath:
	
	def __init__(self, h=None, g=None, m=None, b=None, l=None, ampl=None, p=None, w=None, fi0=None):
		self.h = h
		self.t = np.arange(0, 5, self.h)
		self.fi = np.zeros(1)
		self.u = np.zeros(1)  # u = fi'
		self.sigM = np.zeros(self.t.shape)  # moment napedowy silnika
		
		self.fi0 = fi0
		self.w = w
		self.ampl = ampl
		self.p = p
		self.m = m
		self.g = g
		self.b = b
		self.l = l
		self.I = None
	
	def square_signal(self):
		x = []
		
		size = int(self.t.shape[0])
		samples = int(self.p / self.h)
		flag = True
		count = 0
		while True:
			if size <= 0:
				break
			if (count == int(self.t.shape[0])):
				break
			if self.w == 1:
				x.append(self.ampl)
				count += 1
				size -= 1
			elif self.w == 0:
				x.append(0)
				count += 1
				size -= 1
			elif flag:
				for i in range(int(self.w * samples)):
					if (count == int(self.t.shape[0])):
						break
					x.append(self.ampl)
					count += 1
				flag = False
				size -= int(self.w * samples)
			else:
				for i in range(int((1 - self.w) * samples)):
					if (count == int(self.t.shape[0])):
						break
					x.append(0)
					count += 1
				flag = True
				size -= int((1 - self.w) * samples)
		
		return x
	
	def triangle_signal(self):
		x = np.zeros(self.t.shape)
		for i in range(1, 99, 2):
			for a, b in enumerate(self.t):
				x[a] += self.ampl * (8 / pow(np.pi, 2)) * (pow(-1, (i - 1) / 2) / pow(i, 2)) * np.sin(
					2 * np.pi * i * b / self.p)
		
		return x
	
	def sinusoid_signal(self):
		x = np.zeros(self.t.shape)
		for i, j in enumerate(self.t):
			x[i] = self.ampl * np.sin(2 * np.pi * j / self.p)
		
		return x
	
	def calculate(self):
		self.I = 1 / 3 * self.m * pow(self.l, 2)
		self.fi = np.zeros(self.t.shape)
		self.u = np.zeros(self.t.shape)
		self.fi[0] = self.fi0
		for i, j in enumerate(self.t):  # i - indeksy, j - czasy
			k1 = self.h * self.u[i]
			q1 = self.h * self.func(self.I, self.b, self.m, self.g, self.l, self.sigM[i], 0, 0, self.fi[i], self.u[i])
			
			k2 = self.h * (self.u[i] + q1 / 2)
			q2 = self.h * self.func(self.I, self.b, self.m, self.g, self.l, self.sigM[i], k1 / 2, q1 / 2, self.fi[i],
									self.u[i])
			
			k3 = self.h * (self.u[i] + q2 / 2)
			q3 = self.h * self.func(self.I, self.b, self.m, self.g, self.l, self.sigM[i], k2 / 2, q2 / 2, self.fi[i],
									self.u[i])
			
			k4 = self.h * (self.u[i] + q3)
			q4 = self.h * self.func(self.I, self.b, self.m, self.g, self.l, self.sigM[i], k3, q3, self.fi[i], self.u[i])
			
			if i < len(self.t) - 1:
				self.fi[i + 1] = self.fi[i] + 1 / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
				# if self.fi[i + 1] > 360:
				# 	self.fi[i + 1] -= 360
				# elif self.fi[i + 1] < 0:
				# 	self.fi[i + 1] += 360
				self.u[i + 1] = self.u[i] + 1 / 6 * (q1 + 2 * q2 + 2 * q3 + q4)
	
	def func(self, I, b, m, g, l, sigM, k, q, fi, u):
		return (-sigM - b * (u + q) + m * g * (l / 2) * np.sin((fi + k) * np.pi / 180)) / I
	
	def prepare_output(self):
		if self.fi[0] > 124:
			self.fi[0] = 124
		elif self.fi[0] < -124:
			self.fi[0] = -124
		else:
			self.fi[0] = self.fi[0]
	
	def get_output(self):
		return self.fi