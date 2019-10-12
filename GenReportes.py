from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import csv
import sqlite3


def infoAdicional():
	
	messagebox.showinfo("GenReportesApp", "GenReportesApp v2019")


def avisoLicencia():
	
	messagebox.showwarning("Licencia", "Producto bajo licencia GNU")

def avisoFileCsvGenerado():
	
	messagebox.showinfo("GenReportesApp", "Archivo CSV Generado OK")


def avisoCompletarInput():
	
	messagebox.showwarning("GenReportesApp", "Completar InputBox")

def avisoFallaConectarDB():
	
	messagebox.showwarning("GenReportesApp", "avisoFallaConectarDB")

def salirAplicacion():
	
	opcion = messagebox.askquestion(
		"Salir", "Desea salir de la aplicacion????", icon='warning')

	if opcion == "yes":
		raiz.destroy()

def leerInfoInputBox():
	
	listadata = [datacuadroReporte.get(), datacuadrodb.get(),
			 datacuadroguardar.get()]
	return listadata

def borrarInputBox():
	
	datacuadroReporte.set("")
	datacuadrodb.set("")
	datacuadroguardar.set("")

	print("GenReportesApp - Se borran todos los campos")

def abreFichero(data):
		
	fichero=filedialog.askopenfilename(title="Abrir",initialdir="C:/Users/srcoco/Dropbox/02_Workana/00_Propuestas/02_GenReportes",filetypes=(("CSV files","*.csv"),("Todos los ficheros","*.*")))
	data.set(fichero)

def saveFichero(data):
		
	fichero=filedialog.asksaveasfilename(title="Abrir",initialdir="C:/Users/srcoco/ropbox/02_Workana/00_Propuestas/02_GenReportes",filetypes=(("CSV files","*.csv"),("Todos los ficheros","*.*")))
	data.set(fichero)


def ReadData(numeroTelefono,fecha,opcion,namadb):
	
	try:
		paquete=[]
		miConexion = sqlite3.connect(namadb)
		miCursor = miConexion.cursor()
		miCursor.execute("SELECT * FROM " + namadb + " WHERE TELEFONO = " + numeroTelefono)
		listamiCursor=miCursor.fetchall() #recuperar los datos
		print("Para el telefono: " + str(numeroTelefono) + " se encontraron coincidencias =  ",len(listamiCursor))
		for data in listamiCursor:
			paquete.append((opcion,fecha) + data)
		print (paquete)
		miConexion.commit()
		print("Record read successfully")
		miConexion.close()
		return paquete
		#writeCSV_new(paquete)
	except:
		#print("Failed to ReadData data into sqlite table")
		avisoFallaConectarDB()
	finally:
		if (miConexion):
			miConexion.close()
			#print("The SQLite connection is closed")



def writeCSV_new(myData,filename):
	
	myFile = open(filename,'a',newline='')
	with myFile:
		writer = csv.writer(myFile)
		writer.writerows(myData)

def validadInfoInputBox(listdata):
	if(listdata[0]== "" or listdata[1]== "" or listdata[2]== ""):
		return False
	else:
		return True
		
def genReporte(filename):

	try:	
		listdata=leerInfoInputBox()

		if(validadInfoInputBox(listdata)):
			borrarInputBox()

			with open(listdata[0]) as File:
				reader = csv.reader(File, delimiter=',', quotechar=',',quoting=csv.QUOTE_MINIMAL)
				for row in reader:
					data=ReadData(row[0],row[1],row[2],listdata[1])
					writeCSV_new(data,filename)
				#print ("Se leyeron del csv " + str(reader.line_num) + " registros")
			avisoFileCsvGenerado()
		else:
			avisoCompletarInput()
	except:
		print("Failed to genReporte TO csv")


raiz = Tk()

raiz.title("GenReportesApp")
raiz.iconbitmap("Iconos/Reportes.ico")
# raiz.geometry("350x500")
# raiz.resizable(False,False)

barraMenu = Menu(raiz)
# raiz.config(menu=barraMenu,width=350,height=400)
raiz.config(menu=barraMenu)

Infomenu = Menu(barraMenu, tearoff=0)
Infomenu.add_command(label="Salir", command=salirAplicacion)

borrarmenu = Menu(barraMenu, tearoff=0)
borrarmenu.add_command(label="Borrar Campos",command=borrarInputBox)

helpmenu = Menu(barraMenu, tearoff=0)
helpmenu.add_command(label="Licencia", command=avisoLicencia)
helpmenu.add_command(label="Acerca de...", command=infoAdicional)

barraMenu.add_cascade(label="MENU", menu=Infomenu)
barraMenu.add_cascade(label="BORRAR", menu=borrarmenu)
barraMenu.add_cascade(label="AYUDA", menu=helpmenu)

miFrame = Frame(raiz, width=350, height=400)
miFrame.pack()

datacuadroReporte = StringVar()
datacuadrodb = StringVar()
datacuadroguardar = StringVar()

cuadroReporte = Entry(miFrame, textvariable=datacuadroReporte)
cuadroReporte.grid(row=0, column=1, padx=10, pady=10,columnspan=1)
cuadroReporte.config(justify="center")

botonOpenCsv=Button(miFrame,text="...",command=lambda:abreFichero(datacuadroReporte))
botonOpenCsv.grid(row=0, column=2, padx=10, pady=10,columnspan=1)

cuadrodb = Entry(miFrame, textvariable=datacuadrodb)
cuadrodb.grid(row=1, column=1, padx=10, pady=10,columnspan=1)
cuadrodb.config(justify="center")

#botonDB=Button(miFrame,text="...",command=lambda:abreFichero(datacuadrodb))
#botonDB.grid(row=1, column=2, padx=10, pady=10,columnspan=1)

cuadroguardar = Entry(miFrame, textvariable=datacuadroguardar)
cuadroguardar.grid(row=2, column=1, padx=10, pady=10, columnspan=1)
cuadroguardar.config(justify="center")

botonSave=Button(miFrame,text="...",command=lambda:saveFichero(datacuadroguardar))
botonSave.grid(row=2, column=2, padx=10, pady=10,columnspan=1)

ReporteLabel = Label(miFrame, text="Reporte: ")
ReporteLabel.grid(row=0, column=0, padx=10, pady=10,sticky="e")

NombreDBLabel = Label(miFrame, text="Nombre DB: ")
NombreDBLabel.grid(row=1, column=0, padx=10, pady=10,sticky="e")

guardarLabel = Label(miFrame, text="Guardar: ")
guardarLabel.grid(row=2, column=0, padx=10, pady=10,sticky="e")

botonSet = Button(miFrame, text="Generar Reporte", width=15,command=lambda:genReporte(datacuadroguardar.get()))
botonSet.grid(row=3, column=1, padx=10, pady=10)


raiz.mainloop()
