from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

import sqlite3


def infoAdicional():
	messagebox.showinfo("CRUDApp", "Gestion Base de Datos v2019")


def avisoLicencia():
	messagebox.showwarning("Licencia", "Producto bajo licencia GNU")


def salirAplicacion():
	opcion = messagebox.askquestion(
		"Salir", "Desea salir de la aplicacion????", icon='warning')

	if opcion == "yes":
		raiz.destroy()


def crearDB():
	miConexion = sqlite3.connect("LLAMADAS")
	miCursor = miConexion.cursor()

	try:
		miCursor.execute('''
			CREATE TABLE LLAMADAS(
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			AGENTE VARCHAR(50),
			DURACION INTEGER,
			TELEFONO VARCHAR(50))
		''')

		miConexion.commit()
		messagebox.showinfo("CRUDLlamadas", "BBDD creada con exito!!")
		miConexion.close()
	except:
		messagebox.showinfo("CRUDLlamadas", "BBDD YA EXISTE!!")


def leerInfoInputBox():
	listadata = [datacuadroAgente.get(), datacuadroTelefono.get(),
			 datacuadroDuracion.get()]
	return listadata


def borrarInputBox():
	dataCuadroID.set("")
	datacuadroAgente.set("")
	datacuadroTelefono.set("")
	datacuadroDuracion.set(0)
	
	print("CRUDLlamadas - Se borran todos los campos")

def InsertarData():
	
	try:
		miConexion = sqlite3.connect("LLAMADAS")
		miCursor = miConexion.cursor()
		print("Successfully Connected to SQLite")

		listadata=leerInfoInputBox()
		print (listadata)
		count = miCursor.execute("INSERT INTO LLAMADAS VALUES (NULL,?,?,?)", listadata)

		miConexion.commit()
		print("Record inserted successfully into LLAMADAS table ", miCursor.rowcount)
		messagebox.showinfo("CRUDLlamadas", "BBDD creada con exito!!")
		miConexion.close()
	
	except:
		print("Failed to insert data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")

def ReadData():
	
	try:
		miConexion = sqlite3.connect("LLAMADAS")
		miCursor = miConexion.cursor()
		miCursor.execute("SELECT * FROM LLAMADAS")
		listamiCursor=miCursor.fetchall() #recuperar los datos
		IDleido=dataCuadroID.get()
		for datos in listamiCursor:
			if (datos[0]==int(IDleido)):
				dataCuadroID.set(datos[0])
				datacuadroAgente.set(datos[1])
				datacuadroDuracion.set(datos[2])
				datacuadroTelefono.set(datos[3])
				continue
		miConexion.commit()
		print("Record read successfully")
		miConexion.close()
	except:
		print("Failed to ReadData data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")


def updateData():
	
	try:	
		miConexion = sqlite3.connect("LLAMADAS")
		miCursor = miConexion.cursor()
		miCursor.execute("SELECT * FROM LLAMADAS")
		listamiCursor=miCursor.fetchall() #recuperar los datos
		IDleido=dataCuadroID.get()
		
		for datos in listamiCursor:
			if (datos[0]==int(IDleido)):			
				data= leerInfoInputBox()
				data.append(IDleido)

		sql_update_query = """UPDATE LLAMADAS set AGENTE = ? ,,DURACION = ?,TELEFONO = ? where ID = ?"""
		
		miCursor.execute(sql_update_query, data)

		#print (sql_update_query)
		miConexion.commit()
		print("Record Updated successfully")
		miCursor.close()
	except:
		print("Failed to updateData data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")



def deleteData():

	try:
		miConexion = sqlite3.connect("LLAMADAS")
		miCursor = miConexion.cursor()
		miCursor.execute("SELECT * FROM LLAMADAS")
		listamiCursor=miCursor.fetchall() #recuperar los datos
		IDleido=dataCuadroID.get()
		for datos in listamiCursor:
			if (datos[0]==int(IDleido)):
				miCursor.execute("DELETE FROM LLAMADAS WHERE ID=" + IDleido)
		borrarInputBox()
		miConexion.commit()
		print("Record delete successfully")
		miConexion.close()
	except:
		print("Failed to deleteData data into sqlite table")
	finally:
		if (miConexion):
			miConexion.close()
			print("The SQLite connection is closed")


raiz = Tk()

raiz.title("CRUDLlamadas - Gestion Base de Datos Llamadas")
raiz.iconbitmap("Iconos/computer_1.ico")
# raiz.geometry("350x500")
# raiz.resizable(False,False)

barraMenu = Menu(raiz)
# raiz.config(menu=barraMenu,width=350,height=400)
raiz.config(menu=barraMenu)

BBDDmenu = Menu(barraMenu, tearoff=0)
BBDDmenu.add_command(label="Conectar", command=crearDB)
BBDDmenu.add_command(label="Salir", command=salirAplicacion)
# BBDDmenu.add_separator()

borrarmenu = Menu(barraMenu, tearoff=0)
borrarmenu.add_command(label="Borrar Campos",command=borrarInputBox)

Crudmenu = Menu(barraMenu, tearoff=0)
Crudmenu.add_command(label="Create",command=lambda:InsertarData())
Crudmenu.add_command(label="Read",command=lambda:ReadData())
Crudmenu.add_command(label="Update",command=lambda:updateData())
Crudmenu.add_command(label="Delete",command=lambda:deleteData())

helpmenu = Menu(barraMenu, tearoff=0)
helpmenu.add_command(label="Licencia", command=avisoLicencia)
helpmenu.add_command(label="Acerca de...", command=infoAdicional)

barraMenu.add_cascade(label="BBDD", menu=BBDDmenu)
barraMenu.add_cascade(label="BORRAR", menu=borrarmenu)
barraMenu.add_cascade(label="CRUD", menu=Crudmenu)
barraMenu.add_cascade(label="AYUDA", menu=helpmenu)

miFrame = Frame(raiz, width=350, height=400)
miFrame.pack()

dataCuadroID = StringVar()
datacuadroAgente = StringVar()
datacuadroTelefono = StringVar()
datacuadroDuracion = IntVar()


cuadroID = Entry(miFrame, textvariable=dataCuadroID)
cuadroID.grid(row=0, column=1, padx=10, pady=10,columnspan=2)
cuadroID.config(fg="red", justify="center")

cuadroAgente = Entry(miFrame, textvariable=datacuadroAgente)
cuadroAgente.grid(row=1, column=1, padx=10, pady=10,columnspan=2)
cuadroAgente.config(justify="center")

cuadroDuracion = Entry(miFrame, textvariable=datacuadroDuracion)
cuadroDuracion.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
cuadroDuracion.config(justify="center")

cuadroTelefono = Entry(miFrame, textvariable=datacuadroTelefono)
cuadroTelefono.grid(row=3, column=1, padx=10, pady=10, columnspan=2)
cuadroTelefono.config(justify="center")

IDLabel = Label(miFrame, text="ID: ")
IDLabel.grid(row=0, column=0, padx=10, pady=10)

AgenteLabel = Label(miFrame, text="Agentee: ")
AgenteLabel.grid(row=1, column=0, padx=10, pady=10)

DuracionLabel = Label(miFrame, text="Duracion (min): ")
DuracionLabel.grid(row=2, column=0, padx=10, pady=10)

TelefonoLabel = Label(miFrame, text="Telefono: ")
TelefonoLabel.grid(row=3, column=0, padx=10, pady=10)

botonCreate = Button(miFrame, text="Create", width=8,command=lambda:InsertarData())
botonCreate.grid(row=4, column=0, padx=10, pady=10)

botonRead = Button(miFrame, text="Read", width=8,command=lambda:ReadData())
botonRead.grid(row=4, column=1, padx=10, pady=10)

botonUpdate = Button(miFrame, text="Update", width=8,command=lambda:updateData())
botonUpdate.grid(row=4, column=2, padx=10, pady=10)

botonDelete = Button(miFrame, text="Delete", width=8,command=lambda:deleteData())
botonDelete.grid(row=4, column=3, padx=10, pady=10)


raiz.mainloop()