import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from pyfirmata import Arduino, util
from tkinter import *
from PIL import Image
from PIL import ImageTk
import time
cont=0
prom1=0
prom2=0
prom3=0

placa = Arduino ('COM6')
it = util.Iterator(placa)
it.start()
a_0 = placa.get_pin('a:0:i')
a_1 = placa.get_pin('a:1:i')
a_2 = placa.get_pin('a:2:i')
led = placa.get_pin('d:3:p')
led1 = placa.get_pin('d:5:p')
led2 = placa.get_pin('d:6:p')
time.sleep(0.5)
ventana = Tk()
ventana.geometry('1090x545')
ventana.title("UI para sistemas de control")

# Fetch the service account key JSON file contents
cred = credentials.Certificate('key/key.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://parcial-8f814.firebaseio.com/'
})


marco1 = Frame(ventana, bg="gray", highlightthickness=1, width=1280, height=800, bd= 5)
marco1.place(x = 0,y = 0)
b=Label(marco1,text="")
valor2= Label(marco1, bg='cadet blue1', font=("Arial Bold", 15), fg="white", width=5)
adc_data=StringVar()
valor3= Label(marco1, bg='cadet blue1', font=("Arial Bold", 15), fg="white", width=5)
adc_data2=StringVar()
valor4= Label(marco1, bg='cadet blue1', font=("Arial Bold", 15), fg="white", width=5)
adc_data3=StringVar()

def adc_read():
    global prom1
    i=0
    while i<15:
        i=i+1
        x=a_0.read()
        print(x)
        adc_data.set(x)
        prom1=x+prom1
        ventana.update()
        time.sleep(0.1)
    ref = db.reference('sensor')
    ref.update({
        'sensor1/adc': x
    })

def adc_read1():
    global prom2
    i=0
    prom=0
    while i<15:
        i=i+1
        y=a_1.read()
        print(y)
        adc_data2.set(y)
        prom2=y+prom2
        ventana.update()
        time.sleep(0.1)
    ref = db.reference('sensor')
    ref.update({
        'sensor2/adc': y
    })

def adc_read2():
    global prom3
    i=0
    while i<15:
        i=i+prom1
        z=a_2.read()
        print(z)
        adc_data3.set(z)
        prom3=z+prom3
        ventana.update()
    ref = db.reference('sensor')
    ref.update({
        'sensor3/adc': z
    })

def update():
    ref1=db.reference("sensor1/adc")
    ref1=db.reference("sensor2/adc")
    ref1=db.reference("sensor3/adc")
    led.write(prom1)
    led1.write(prom2)
    led2.write(prom3)

valor2.configure(textvariable=adc_data)
valor2.place(x=130, y=160)

valor3.configure(textvariable=adc_data2)
valor3.place(x=130, y=200)

valor4.configure(textvariable=adc_data3)
valor4.place(x=130, y=240)

prom_15=Button(marco1,text="adc1_update",command=adc_read)
prom_15.place(x=10, y=160)

prom_15=Button(marco1,text="adc2_update",command=adc_read1)
prom_15.place(x=10, y=200)

prom_15=Button(marco1,text="adc3_update",command=adc_read2)
prom_15.place(x=10, y=240)

prom_15=Button(marco1,text="adc3_update",command=update)
prom_15.place(x=10, y=280)



ventana.mainloop()
