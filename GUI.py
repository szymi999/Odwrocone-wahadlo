import tkinter as tk
import DoMath as Dm
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Gui(tk.Tk):
	
	def __init__(self, width, height, title):
		super().__init__()
		self.dm = Dm.DoingMath(h=0.01, g=10)
		self.animationFlag = False
		
		self.title(title)
		self.windowWidth = width
		self.windowHeight = height
		self.windowPositionX = self.winfo_screenwidth() / 2 - self.windowWidth / 2
		self.windowPositionY = self.winfo_screenheight() / 2 - self.windowHeight / 2
		self.geometry("{}x{}+{}+{}".format(self.windowWidth, self.windowHeight, int(self.windowPositionX),
										   int(self.windowPositionY)))
		
		self.simulationName = tk.Frame(self, width=self.windowWidth * 0.4, height=self.windowHeight * 0.05)
		self.simulationName.place(relx=0.55, rely=0, relwidth=0.4, relheight=0.05)
		self.simulation = tk.Canvas(self, relief="solid", bd="1", bg="white")
		self.simulation.place(relx=0.55, rely=0.05, relwidth=0.4, relheight=0.50)
		
		self.signalName = tk.Frame(self, width=self.windowWidth * 0.4, height=self.windowHeight * 0.05)
		self.signalName.place(relx=0.05, rely=0.55)
		self.signalGraph = tk.Canvas(self, width=self.windowWidth * 0.4, height=self.windowHeight * 0.35,
									 relief="solid", bd="1", bg="white")
		self.signalGraph.place(relx=0.05, rely=0.6, relwidth=0.4, relheight=0.35)
		
		self.outputName = tk.Frame(self)
		self.outputName.place(relx=0.55, rely=0.55, relwidth=0.4, relheight=0.05)
		self.outputGraph = tk.Canvas(self, relief="solid", bd="1", bg="white")
		self.outputGraph.place(relx=0.55, rely=0.6, relwidth=0.4, relheight=0.35)
		
		self.frame = tk.Frame(self, width=self.windowWidth * 0.5, height=self.windowHeight * 0.55)
		self.frame.place(relx=0, rely=0)
		
		self.create_widgets()
	
	def create_widgets(self):
		self.signalXAxis = tk.Label(self, text="Czas")
		self.signalXAxis.place(relx=0.15, rely=0.95, relwidth=0.2, relheight=0.05)
		self.signalYAxis = tk.Label(self, text="Ampl")
		self.signalYAxis.place(relx=0.01, rely=0.75, relwidth=0.04, relheight=0.05)
		
		self.outputXAxis = tk.Label(self, text="Czas")
		self.outputXAxis.place(relx=0.65, rely=0.95, relwidth=0.2, relheight=0.05)
		self.outputYAxis = tk.Label(self, text="Kąt")
		self.outputYAxis.place(relx=0.51, rely=0.75, relwidth=0.04, relheight=0.05)
		
		self.simulationNameLabel = tk.Label(self.simulationName, text="Symulacja:")
		self.simulationNameLabel.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.6)
		
		self.signalNameLabel = tk.Label(self.signalName, text="Sygnał wejściowy:")
		self.signalNameLabel.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.6)
		
		self.outputNameLabel = tk.Label(self.outputName, text="Sygnał wyjściowy:")
		self.outputNameLabel.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.6)
		
		self.signalLabel = tk.Label(self.frame, text="Sygnał:")
		self.signalLabel.place(relx=0.3, rely=0.03, relwidth=0.2, relheight=0.06)
		
		self.v = tk.IntVar()
		self.square = tk.Radiobutton(self.frame, text="Prostokątny", variable=self.v, value=0,
									 command=self.radio_clicked)
		self.square.place(relx=0.05, rely=0.10, relwidth=0.21, relheight=0.06)
		
		self.triangle = tk.Radiobutton(self.frame, text="Trójkątny", variable=self.v, value=1,
									   command=self.radio_clicked1)
		self.triangle.place(relx=0.27, rely=0.10, relwidth=0.20, relheight=0.06)
		
		self.sinusoid = tk.Radiobutton(self.frame, text="Sinusoidalny", variable=self.v, value=2,
									   command=self.radio_clicked1)
		self.sinusoid.place(relx=0.48, rely=0.10, relwidth=0.22, relheight=0.06)
		
		self.periodLabel = tk.Label(self.frame, text="Okres sygnału(sek):")
		self.periodLabel.place(relx=0.02, rely=0.20, relwidth=0.45, relheight=0.05)
		self.periodEntry = tk.Entry(self.frame)
		self.periodEntry.place(relx=0.5, rely=0.20, relwidth=0.2, relheight=0.05)
		self.periodError = tk.Label(self.frame, text="", fg="red")
		self.periodError.place(relx=0.1, rely=0.25, relwidth=0.4, relheight=0.05)
		
		self.pulseWidthLabel = tk.Label(self.frame, text="Wypełninie sygnału(%):")
		self.pulseWidthLabel.place(relx=0.02, rely=0.30, relwidth=0.45, relheight=0.05)
		self.pulseWidthEntry = tk.Entry(self.frame)
		self.pulseWidthEntry.place(relx=0.5, rely=0.30, relwidth=0.2, relheight=0.05)
		self.pulseWidthError = tk.Label(self.frame, text="", fg="red")
		self.pulseWidthError.place(relx=0.1, rely=0.35, relwidth=0.4, relheight=0.05)
		
		self.amplitudeLabel = tk.Label(self.frame, text="Amplituda/moment silnika(N*m):")
		self.amplitudeLabel.place(relx=0.02, rely=0.40, relwidth=0.45, relheight=0.05)
		self.amplitudeEntry = tk.Entry(self.frame)
		self.amplitudeEntry.place(relx=0.5, rely=0.40, relwidth=0.2, relheight=0.05)
		self.amplitudeError = tk.Label(self.frame, text="", fg="red")
		self.amplitudeError.place(relx=0.1, rely=0.45, relwidth=0.4, relheight=0.05)
		
		self.frictionLabel = tk.Label(self.frame, text="Współczynnik tarcia:")
		self.frictionLabel.place(relx=0.02, rely=0.50, relwidth=0.45, relheight=0.05)
		self.frictionEntry = tk.Entry(self.frame)
		self.frictionEntry.place(relx=0.5, rely=0.50, relwidth=0.2, relheight=0.05)
		self.frictionError = tk.Label(self.frame, text="", fg="red")
		self.frictionError.place(relx=0.1, rely=0.55, relwidth=0.4, relheight=0.05)
		
		self.lengthLabel = tk.Label(self.frame, text="Dlugość wahadła(m):")
		self.lengthLabel.place(relx=0.02, rely=0.60, relwidth=0.45, relheight=0.05)
		self.lengthEntry = tk.Entry(self.frame)
		self.lengthEntry.place(relx=0.5, rely=0.60, relwidth=0.2, relheight=0.05)
		self.lengthError = tk.Label(self.frame, text="", fg="red")
		self.lengthError.place(relx=0.1, rely=0.65, relwidth=0.4, relheight=0.05)
		
		self.massLabel = tk.Label(self.frame, text="Masa wahadła(kg):")
		self.massLabel.place(relx=0.02, rely=0.70, relwidth=0.45, relheight=0.05)
		self.massEntry = tk.Entry(self.frame)
		self.massEntry.place(relx=0.5, rely=0.70, relwidth=0.2, relheight=0.05)
		self.massError = tk.Label(self.frame, text="", fg="red")
		self.massError.place(relx=0.1, rely=0.75, relwidth=0.4, relheight=0.05)
		
		self.startAngleLabel = tk.Label(self.frame, text="Kąt początkowy(°):")
		self.startAngleLabel.place(relx=0.02, rely=0.80, relwidth=0.45, relheight=0.05)
		self.startAngleEntry = tk.Entry(self.frame)
		self.startAngleEntry.place(relx=0.5, rely=0.80, relwidth=0.2, relheight=0.05)
		self.startAngleError = tk.Label(self.frame, text="", fg="red")
		self.startAngleError.place(relx=0.1, rely=0.85, relwidth=0.4, relheight=0.05)
		
		self.simulationTimeLabel = tk.Label(self.frame, text="Czas trwania symulacji(s):")
		self.simulationTimeLabel.place(relx=0.02, rely=0.90, relwidth=0.45, relheight=0.05)
		self.simulationTimeEntry = tk.Entry(self.frame)
		self.simulationTimeEntry.place(relx=0.5, rely=0.90, relwidth=0.2, relheight=0.05)
		self.simulationTimeError = tk.Label(self.frame, text="", fg="red")
		self.simulationTimeError.place(relx=0.1, rely=0.95, relwidth=0.4, relheight=0.05)
		
		self.values = tk.Button(self.frame,
								text="Wczytaj\ndane",
								command=lambda: self.get_values(self.periodEntry.get(),
																self.pulseWidthEntry.get(),
																self.amplitudeEntry.get(),
																self.frictionEntry.get(),
																self.lengthEntry.get(),
																self.massEntry.get(),
																self.startAngleEntry.get(),
																self.simulationTimeEntry.get()))
		self.values.place(relx=0.75, rely=0.03, relwidth=0.2, relheight=0.1)
		
		self.instruction1 = tk.Label(self.frame, text="1. Wprowadż dane\npo czym je wczytaj")
		self.instruction1.place(relx=0.7, rely=0.13, relwidth=0.3, relheight=0.1)
		
		self.drawSignalGraph = tk.Button(self.frame,
										 text="Rysuj sygnał\nwejściowy",
										 command=lambda: self.plot_signal(),
										 state="disabled")
		self.drawSignalGraph.place(relx=0.75, rely=0.23, relwidth=0.2, relheight=0.1)
		
		self.instruction2 = tk.Label(self.frame, text="2. Narysuj wykres\nsygnału i wyjścia")
		self.instruction2.place(relx=0.7, rely=0.33, relwidth=0.3, relheight=0.1)
		
		self.drawOutputGraph = tk.Button(self.frame,
										 text="Rysuj sygnał\nwyjściowy",
										 command=lambda: self.plot_output(),
										 state="disabled")
		self.drawOutputGraph.place(relx=0.75, rely=0.43, relwidth=0.2, relheight=0.1)
		
		self.instruction3 = tk.Label(self.frame, text="3. Po narysowaniu wyjścia\nmożna rozpocząć symulację")
		self.instruction3.place(relx=0.7, rely=0.53, relwidth=0.3, relheight=0.1)
		
		self.drawSimulation = tk.Button(self.frame,
										text="Rozpocznij\nsymulację",
										command=lambda: self.start_simulation(),
										state="disabled")
		self.drawSimulation.place(relx=0.75, rely=0.63, relwidth=0.2, relheight=0.1)
		
		self.instruction4 = tk.Label(self.frame, text="4. Aby konynuować\nzatrzymaj symulację")
		self.instruction4.place(relx=0.7, rely=0.73, relwidth=0.3, relheight=0.1)
		
		self.stopSimulation = tk.Button(self.frame,
										text="Zatrzymaj\nsymulację",
										command=lambda: self.stop_simulation(),
										state="disabled")
		self.stopSimulation.place(relx=0.75, rely=0.83, relwidth=0.2, relheight=0.1)
	
	def get_values(self, periodentry, pulsewidthentry, amplitudeentry, frictionentry, lengthentry, massentry,
				   startangleentry, simulationtimeentry):
		everything_right = True
		checkboxes = self.check_checkboxes(self.v.get())
		
		if self.check_if_empty(periodentry, self.periodError):
			self.check_if_float(periodentry, self.periodError, (0, 100))
			if self.periodError["text"] == "":
				self.dm.p = float(periodentry)
			else:
				everything_right = False
		else:
			everything_right = False
		
		if checkboxes == 0:
			if self.check_if_empty(pulsewidthentry, self.pulseWidthError):
				self.check_if_float(pulsewidthentry, self.pulseWidthError, (0, 100))
				if self.pulseWidthError["text"] == "":
					self.dm.w = float(pulsewidthentry) / 100
				else:
					everything_right = False
			else:
				everything_right = False
		else:
			self.pulseWidthError["text"] = ""
		
		if self.check_if_empty(amplitudeentry, self.amplitudeError):
			self.check_if_float(amplitudeentry, self.amplitudeError)
			if self.amplitudeError["text"] == "":
				self.dm.ampl = float(amplitudeentry)
			else:
				everything_right = False
		else:
			everything_right = False
		
		if self.check_if_empty(frictionentry, self.frictionError):
			self.check_if_float(frictionentry, self.frictionError)
			if self.frictionError["text"] == "":
				self.dm.b = float(frictionentry)
			else:
				everything_right = False
		else:
			everything_right = False
		
		if self.check_if_empty(lengthentry, self.lengthError):
			self.check_if_float(lengthentry, self.lengthError)
			if self.lengthError["text"] == "":
				self.dm.l = round(float(lengthentry), 1)
			else:
				everything_right = False
		else:
			everything_right = False
		
		if self.check_if_empty(massentry, self.massError):
			self.check_if_float(massentry, self.massError)
			if self.massError["text"] == "":
				self.dm.m = float(massentry)
			else:
				everything_right = False
		else:
			everything_right = False
		
		if self.check_if_empty(startangleentry, self.startAngleError):
			self.check_if_float(startangleentry, self.startAngleError)
			if self.startAngleError["text"] == "":
				self.dm.fi0 = float(startangleentry)
			else:
				everything_right = False
		else:
			everything_right = False
		
		if self.check_if_empty(simulationtimeentry, self.simulationTimeError):
			self.check_if_float(simulationtimeentry, self.simulationTimeError)
			if self.simulationTimeError["text"] == "":
				self.dm.t = np.arange(0, float(simulationtimeentry), self.dm.h)
			else:
				everything_right = False
		else:
			everything_right = False
		
		if everything_right:
			if checkboxes == 0:  # sygnal prostokatny
				self.dm.sigM = self.dm.square_signal()
			elif checkboxes == 1:  # sygnal trojkatny
				self.dm.sigM = self.dm.triangle_signal()
			elif checkboxes == 2:  # sygnal sinusoidalny
				self.dm.sigM = self.dm.sinusoid_signal()
			self.drawSignalGraph.config(state="normal")
			self.drawOutputGraph.config(state="normal")
			self.drawSimulation.config(state="disabled")
			self.stopSimulation.config(state="disabled")
		else:
			self.drawSignalGraph.config(state="disabled")
			self.drawOutputGraph.config(state="disabled")
			self.drawSimulation.config(state="disabled")
			self.stopSimulation.config(state="disabled")
	
	def check_if_empty(self, ob1, ob2):
		if ob1 is "":
			ob2["text"] = "Puste pole!"
			return False
		else:
			ob2["text"] = ""
			return True
	
	def check_if_float(self, ob1, ob2, additionalcondition=None):
		try:
			float(ob1)
			if additionalcondition is not None:
				if float(ob1) < additionalcondition[0] or float(ob1) > additionalcondition[1]:
					raise Exception
			ob2["text"] = ""
		except Exception as e:
			ob2["text"] = "To nie jest poprawna liczba!"
	
	def check_checkboxes(self, v):
		return v
	
	def radio_clicked(self):
		self.pulseWidthEntry.config(state="normal")
	
	def radio_clicked1(self):
		self.pulseWidthEntry.delete(0, 'end')
		self.pulseWidthEntry.config(state="disabled")
	
	def plot_signal(self):
		fig = Figure(figsize=(5, 4))
		fig.add_subplot(111).plot(self.dm.t, self.dm.sigM)
		
		canvas = FigureCanvasTkAgg(fig, master=self.signalGraph)
		canvas.draw()
		canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
	
	def plot_output(self):
		self.drawSimulation.config(state="normal")
		self.dm.calculate()
		
		fig = Figure(figsize=(5, 4), dpi=100)
		fig.add_subplot(111).plot(self.dm.t, self.dm.fi)
		
		canvas = FigureCanvasTkAgg(fig, master=self.outputGraph)
		canvas.draw()
		canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=1)
	
	def start_simulation(self):
		self.values.config(state="disabled")
		self.drawSignalGraph.config(state="disabled")
		self.drawOutputGraph.config(state="disabled")
		self.drawSimulation.config(state="disabled")
		self.stopSimulation.config(state="normal")
		
		self.animationFlag = True
		self.simulation.delete('all')
		
		anglestr = str(round(self.dm.fi[0], 2))
		angle = tk.Label(self.simulation, text="Kąt: {}".format(anglestr), bg="white")
		angle.place(relx=0.8, rely=0.01, relwidth=0.15, relheight=0.05)
		
		timestr = str(round(self.dm.t[0], 2))
		timet = tk.Label(self.simulation, text="Czas: {}".format(timestr), bg="white")
		timet.place(relx=0.01, rely=0.01, relwidth=0.15, relheight=0.05)
		
		xx = 200 + 75 * np.cos((self.dm.fi[0] - 90) * np.pi / 180)
		yy = 150 + 75 * np.sin((self.dm.fi[0] - 90) * np.pi / 180)
		pendulum = self.simulation.create_line(200, 150, xx, yy, width=10)
		self.simulation.create_oval(180, 130, 220, 170, fill="black")
		points = [200, 150, 220, 180, 180, 180]
		self.simulation.create_polygon(points, fill="black")
		
		for i in range(0, self.dm.t.shape[0], 10):
			if not self.animationFlag:
				break
			
			self.simulation.delete(pendulum)
			xx = int(200 + 75 * np.cos((self.dm.fi[i] - 90) * np.pi / 180))
			yy = int(150 + 75 * np.sin((self.dm.fi[i] - 90) * np.pi / 180))
			pendulum = self.simulation.create_line(200, 150, xx, yy, width=10)
			
			anglestr = str(round(self.dm.fi[i], 2))
			angle = tk.Label(self.simulation, text="Kąt: {}".format(anglestr), bg="white")
			angle.place(relx=0.8, rely=0.01, relwidth=0.15, relheight=0.05)
			
			timestr = str(round(self.dm.t[i], 2))
			timet = tk.Label(self.simulation, text="Czas: {}".format(timestr), bg="white")
			timet.place(relx=0.01, rely=0.01, relwidth=0.15, relheight=0.05)
			
			self.simulation.update()
			# time.sleep(0.1)
	
	def stop_simulation(self):
		self.values.config(state="normal")
		self.drawSignalGraph.config(state="normal")
		self.drawOutputGraph.config(state="normal")
		self.drawSimulation.config(state="normal")
		self.stopSimulation.config(state="disabled")
		
		self.animationFlag = False


gui = Gui(1000, 600, "Symulacja odwrotnego wahadła")
gui.mainloop()