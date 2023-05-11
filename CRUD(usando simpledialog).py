from tkinter import ttk
from tkinter import *
from tkinter import messagebox, simpledialog 
import pymysql 
import re

class Registro:
    def __init__(self, root):
        self.wind = root
        self.wind.title("REGISTRO DE ALUMNOS")
        self.wind.geometry("850x600")
        self.wind.config(bg="aqua")

        self.credenciales_permitidas = {"Usu1": "Cont1", "Usu2": "Cont2"}

        usuario = simpledialog.askstring("Inicio de sesión", "Ingrese su nombre de usuario")
        contrasena = simpledialog.askstring("Inicio de sesión", "Ingrese su contraseña", show="*")

        if usuario not in self.credenciales_permitidas or self.credenciales_permitidas[usuario] != contrasena:
            messagebox.showerror("Error", "Credenciales incorrectas. El programa se cerrará.")
            self.wind.destroy() 
            return

        frame1 = LabelFrame(self.wind, text="REGISTRO", font=("calibri", 14))
        frame2 = LabelFrame(self.wind, text="BASE DE DATOS", font=("calibri", 14))

        frame1.pack(fill="both", expand="yes", padx=20, pady=15)  
        frame2.pack(fill="both", expand="yes", padx=20, pady=15)

        ID = StringVar()
        Nombre = StringVar()
        Edad = StringVar()
        Email = StringVar()
        
        def Agregar():
            if not validar_email(Email.get()):
              messagebox.showerror("Por favor", "Ingrese una dirección de correo electrónico válida")
            elif ID.get() == "" or Nombre.get() == "" or Edad.get() == "":
              messagebox.showerror("Por favor", "Ingrese la información correcta")
            elif not validar_edad(Edad.get()):
              messagebox.showerror("Por favor", "Ingrese una edad válida") 
            elif not validar_nombre(Nombre.get()):
              messagebox.showerror("Por favor", "Ingrese un nombre válido") 
            else:
                alumnos = pymysql.connect(host="localhost", user="root", password="", database="alumnos")
                cursor = alumnos.cursor()
                cursor.execute("insert into registro values(%s,%s,%s,%s)", (

                ID.get(),
                Nombre.get(),
                Edad.get(),
                Email.get(),
                ))
                alumnos.commit() 
                alumnos.close() 
                messagebox.showinfo("Datos Completado", "Se agregaron correctamente")  
        
        def Limpiar():
            self.entID.delete(0, END) 
            self.entNombre.delete(0, END) 
            self.entEdad.delete(0, END) 
            self.entEmail.delete(0, END)  

        def Mostrar():
            alumnos = pymysql.connect(host="localhost", user="root", password="", database="alumnos")
            cursor = alumnos.cursor()
            cursor.execute("select * from registro")
            result = cursor.fetchall()
            alumnos = pymysql.connect(host="localhost", user="root", password="", database="alumnos")
            cursor = alumnos.cursor()
            cursor.execute("select * from registro")
            result = cursor.fetchall()
            if len(result) != 0:
                self.trv.delete(*self.trv.get_children())
                for row in result:
                    self.trv.insert('',END,values =row) 
            alumnos.commit()
            alumnos.close()  
        
        def validar_email(email):
            pattern = r"[^@]+@[^@]+\.[^@]+"
            return re.match(pattern, email)
        
        def validar_edad(edad):
            try:
                edad_int = int(edad)
                return 1 <= edad_int <= 150
            except ValueError:
                return False
        def validar_nombre(nombre):
            return bool(re.match(r"^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$", nombre))

        def traineeInfo(ev):
            viewInfo =   self.trv.focus()
            learnerData =  self.trv.item(viewInfo) 
            row = learnerData['values'] 
            ID.set(row[0])
            Nombre.set(row[1])
            Edad.set(row[2])
            Email.set(row[3]) 


        def Actualizar():
            alumnos = pymysql.connect(host="localhost", user="root", password="", database="alumnos")
            cursor = alumnos.cursor()
            cursor.execute("update registro set nombre=%s,edad=%s,email=%s where idalumno=%s", (
            Nombre.get(), 
            Edad.get(),
            Email.get(),
            ID.get()
            ))   
            alumnos.commit()
            Mostrar()
            alumnos.close()  

        def Buscar():
            try: 
                alumnos = pymysql.connect(host="localhost", user="root", password="", database="alumnos")
                cursor = alumnos.cursor()
                cursor.execute("select * from registro where nombre='%s'"%Nombre.get())

                row = cursor.fetchone()

                ID.set(row[0])
                Nombre.set(row[1])
                Edad.set(row[2])
                Email.set(row[3]) 

                alumnos.commit()  
            except:
                Limpiar()
            alumnos.close() 

        def Eliminar(): 
            alumnos = pymysql.connect(host="localhost", user="root", password="", database="alumnos")
            cursor = alumnos.cursor()
            cursor.execute("delete from registro where idalumno=%s",ID.get())
            alumnos.commit()
            Mostrar()
            alumnos.close()
            Limpiar()                 


        lbl1 = Label(frame1, text="ID Alumno", width=20)
        lbl1.grid(row=0, column=0, padx=5, pady=3)
        self.entID = Entry(frame1, textvariable=ID)   
        self.entID.grid(row=0, column=1, padx=5, pady=3) 

        lbl2 = Label(frame1, text="Nombre Del Alumno", width=20)
        lbl2.grid(row=1, column=0, padx=5, pady=3)
        self.entNombre = Entry(frame1, textvariable=Nombre)   
        self.entNombre.grid(row=1, column=1, padx=5, pady=3) 

        lbl3 = Label(frame1, text="Edad", width=20)
        lbl3.grid(row=2, column=0, padx=5, pady=3)
        self.entEdad = Entry(frame1, textvariable=Edad)   
        self.entEdad.grid(row=2, column=1, padx=5, pady=3) 

        lbl4 = Label(frame1, text="Email", width=20)
        lbl4.grid(row=3, column=0, padx=5, pady=3)
        self.entEmail = Entry(frame1, textvariable=Email)   
        self.entEmail.grid(row=3, column=1, padx=5, pady=3)

        btn1 = Button(frame1, text="Agregar", width=12, height=2, command=Agregar)
        btn1.grid(row=6, column=0, padx=10, pady=10)

        btn2 = Button(frame1, text="Eliminar", width=12, height=2, command=Eliminar)
        btn2.grid(row=6, column=1, padx=10, pady=10)

        btn3 = Button(frame1, text="Actualizar", width=12, height=2, command=Actualizar)
        btn3.grid(row=6, column=2, padx=10, pady=10)

        btn4 = Button(frame1, text="Mostrar", width=12, height=2, command=Mostrar)
        btn4.grid(row=6, column=3, padx=10, pady=10)

        btn5 = Button(frame1, text="Limpiar", width=12, height=2, command=Limpiar)
        btn5.grid(row=6, column=4, padx=10, pady=10)

        btn6 = Button(frame1, text="Buscar", width=12, height=2, command=Buscar) 
        btn6.grid(row=6, column=5, padx=10, pady=10)

        self.trv = ttk.Treeview(frame2, columns=(1,2,3,4), show="headings", height="15")
        self.trv.pack()

        self.trv.heading(1, text="ID Alumno")
        self.trv.heading(2, text="Nombre Del Alumno")
        self.trv.heading(3, text="Edad")
        self.trv.heading(4, text="Email")
        self.trv.bind("<ButtonRelease-1>",traineeInfo)

if __name__ == '__main__':
    root = Tk()
    Registro = Registro(root)
    root.mainloop()