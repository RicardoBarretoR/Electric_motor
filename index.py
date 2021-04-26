from tkinter import ttk
from tkinter import *

import sqlite3

class Motor:

    db_name = "database.db"

    def __init__(self, window):
        self.wind = window
        self.wind.title("Motores Electricos")

        #creating a Frame Container
        frame = LabelFrame(self.wind, text = "Registro de Motores")
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 10)

        #  Customer Input
        Label(frame, text = "Cliente: ").grid(row = 1, column = 0)
        self.cliente = Entry(frame)
        self.cliente.focus()
        self.cliente.grid(row = 1, column = 1)

        # Name Input
        Label(frame, text = "Marca: ").grid(row = 2, column = 0)
        self.marca = Entry(frame)
        self.marca.grid(row = 2, column = 1)

        # Pass Input
        Label(frame, text = "Paso: ").grid(row = 3, column = 0)
        self.paso = Entry(frame)
        self.paso.grid(row = 3, column = 1)

        # Turns Input
        Label(frame, text = "Espiras: ").grid(row = 4, column = 0)
        self.espiras = Entry(frame)
        self.espiras.grid(row = 4, column = 1)

        # Gauge Input
        Label(frame, text = "Calibre: ").grid(row = 5, column = 0)
        self.calibre = Entry(frame)
        self.calibre.grid(row = 5, column = 1)

        # Conection Input
        Label(frame, text = "Conexión: ").grid(row = 6, column = 0)
        self.conexion = Entry(frame)
        self.conexion.grid(row = 6, column = 1)

        #  Weight Input
        Label(frame, text = "Peso: ").grid(row = 7, column = 0)
        self.peso = Entry(frame)
        self.peso.grid(row = 7, column = 1)


        # Button Add Motor
        ttk.Button(frame, text = "Guardar", command = self.add_product).grid(row = 8, columnspan = 2, sticky = W + E)

        #Output Messages
        self.message = Label(text = '', fg ='red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Table
        columns = ("#0","#1", "#2", "#3", "#4", "#5")
        
        self.tree = ttk.Treeview(height = 20, columns = columns)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.column("#0", width=250, minwidth=270, stretch=NO)
        self.tree.column("#1", width=250, minwidth=270, stretch=NO)
        self.tree.heading("#0", text = "Cliente", anchor = CENTER)
        self.tree.heading("#1", text = "Marca", anchor = CENTER)
        self.tree.heading("#2", text = "Paso", anchor = CENTER)
        self.tree.heading("#3", text = "Espiras", anchor = CENTER)
        self.tree.heading("#4", text = "Calibre", anchor = CENTER)
        self.tree.heading("#5", text = "Conexion", anchor = CENTER)
        self.tree.heading("#6", text = "Peso", anchor = CENTER)

         #creating a Frame2 Container
        frame2 = LabelFrame(self.wind, text = "Selecciona un registro en caso de:")
        frame2.grid(row = 5, column = 0, columnspan = 3, pady = 10)

        # Buttons
        ttk.Button(frame2, text = 'Eliminar', command = self.delete_motors).grid(padx = 13, 
                    pady = 5, row = 5, column = 0, sticky = E)
        ttk.Button(frame2, text = 'Editar', command = self.edit_motors).grid(row = 5, column = 1, sticky = E)

        #Filling the row
        self.get_motors()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_motors(self):
        #Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #Quering data
        query = 'SELECT * FROM product'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text = row[1],  values = (row[2], row[3], 
                            row[4], row[5], row[6], row[7]))
    def validation(self):
        return len(self.cliente.get()) != 0 and len(self.marca.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)'
            parameters = (self.cliente.get(), self.marca.get(), self.paso.get(),
                        self.espiras.get(), self.calibre.get(), self.conexion.get(),
                        self.peso.get())
            self.run_query(query, parameters)
            self.message['text'] = '{} a sido agregado satisfactoriamente'.format(self.marca.get())
            self.cliente.delete(0, END)
            self.marca.delete(0, END)
            self.paso.delete(0, END)
            self.espiras.delete(0, END)
            self.calibre.delete(0, END)
            self.conexion.delete(0, END)
            self.peso.delete(0, END)
        else:
           self.message['text'] = 'Cliente y marca son requeridos'
        self.get_motors()

    def delete_motors(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona un registro'
            return
        self.message['text'] = ''
        cliente = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE cliente = ?'
        self.run_query(query, (cliente,))
        self.message['text'] = 'Registro {} fue eliminado satisfactoriamente'.format(cliente)
        self.get_motors()

    def edit_motors(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor selecciona un registro'
            return
        cliente = self.tree.item(self.tree.selection())['text']
        marca = self.tree.item(self.tree.selection())['values'][0]
        paso = self.tree.item(self.tree.selection())['values'][1]
        espiras = self.tree.item(self.tree.selection())['values'][2]
        calibre = self.tree.item(self.tree.selection())['values'][3]
        conexion = self.tree.item(self.tree.selection())['values'][4]
        peso = self.tree.item(self.tree.selection())['values'][5]

        #old_data = self.tree.item(self.tree.selection())['values'] = (1, 2, 3, 4, 5, 6)
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Motors'

        # Current Customer
        Label(self.edit_wind, text = 'Cliente: ').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, 
        value = cliente), state = 'readonly').grid(row = 0, column = 2)

        # Edit customer
        Label(self.edit_wind, text = 'Editar Cliente: ').grid(row = 0, column = 3)
        customer = Entry(self.edit_wind)
        customer.grid(row = 0, column = 4)

        # Current Brand
        Label(self.edit_wind, text = 'Marca: ').grid(row = 1, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, 
        value = marca), state = 'readonly').grid(row = 1, column = 2)

        # Edit Brand
        Label(self.edit_wind, text = 'Editar Marca: ').grid(row = 1, column = 3)
        brand = Entry(self.edit_wind)
        brand.grid(row = 1, column = 4)

        # Current Passage
        Label(self.edit_wind, text = 'Paso: ').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, 
        value = paso), state = 'readonly').grid(row = 2, column = 2)

        # Edit passage
        Label(self.edit_wind, text = 'Editar Paso: ').grid(row = 2, column = 3)
        passage = Entry(self.edit_wind)
        passage.grid(row = 2, column = 4)

        # Current Loops
        Label(self.edit_wind, text = 'Espiras: ').grid(row = 3, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, 
        value = espiras), state = 'readonly').grid(row = 3, column = 2)

        # Edit loops
        Label(self.edit_wind, text = 'Editar Espiras: ').grid(row = 3, column = 3)
        loops = Entry(self.edit_wind)
        loops.grid(row = 3, column = 4)

        # Current Caliber
        Label(self.edit_wind, text = 'Calibre: ').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, 
        value = calibre), state = 'readonly').grid(row = 4, column = 2)

        # Edit Caliber
        Label(self.edit_wind, text = 'Editar Calibre: ').grid(row = 4, column = 3)
        caliber = Entry(self.edit_wind)
        caliber.grid(row = 4, column = 4)

        # Current conexion
        Label(self.edit_wind, text = 'Conexion: ').grid(row = 5, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, 
        value = conexion), state = 'readonly').grid(row = 5, column = 2)

        # Edit Conexion
        Label(self.edit_wind, text = 'Editar Conexion: ').grid(row = 5, column = 3)
        conection = Entry(self.edit_wind)
        conection.grid(row = 5, column = 4)

        # Current Weight
        Label(self.edit_wind, text = 'Peso: ').grid(row = 6, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, 
        value = peso), state = 'readonly').grid(row = 6, column = 2)

        # Edit Weight
        Label(self.edit_wind, text = 'Editar Peso: ').grid(row = 6, column = 3)
        weight = Entry(self.edit_wind)
        weight.grid(row = 6, column = 4)

        ttk.Button(self.edit_wind, text = 'Actualizar', command = lambda: self.edit_records).grid(row = 8, column = 3, sticky = W)
    
    def edit_records(self,  cliente, marca, paso, espiras, calibre, conexion, peso, customer, brand, passage, loops, caliber, conection, weight):
        query = 'UPDATE product SET cliente = ?, marca = ?, paso = ?, espiras = ?, calibre = ?, conexion = ?, peso = ?, WHERE customer = ? AND brand = ? AND passage =? AND loops = ? AND caliber = ? AND conection = ? AND weight = ?)'
        

        parameters = (customer, brand, passage, loops, caliber, conection, weight)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = '{} a sido actualizado satisfactoriamente'.format(brand)
        # New data


         

if __name__ == "__main__":
    window = Tk()
    aplication = Motor(window)
    window.mainloop()