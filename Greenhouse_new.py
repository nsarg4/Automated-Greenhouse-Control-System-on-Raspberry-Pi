'''
Խնդրում ենք ԱՆՊԱՅՄԱՆ դիտել մեր տեսանյութը, որն առկա է կցված .zip արխիվում և հղմամբ

Ծրագիրը ջերմոցի ղեկավարման ավտոմատացված համակարգ է։
Ծրագրի աշխատանքի համար հարկավոր է նախորոք տեղադրել համապատասխան գրադարանները համակարգչում։
Եթե ծրագիրը աշխատելու է ՈՉ Raspberry pi համակարգչի վրա, ապա անհարժեշտ է մեկնաբանություն 
դարձնել բոլոր այն տողերը, որոնցում առկա է Raspberry pi-ի GPIO pin-երի գրադարանի հետ աշխատանք։
Գրաֆիկական ինտերֆեյս ապահովելու համար օգտագործվել է tkinter գրադարանը։
Նշանների ճիշտ աշխատանքի համար պետք է կից ֆայլում եղած նկարներով թղթապանակը տեղադրել 
համապատասխան վայրում և տալ հասցեն, կախված թե ինչ ՕՀ եք օգտագործում։ Դրա մասին մեկնաբանություն
կա նկարների տեղադրման մասում։

'''
#Գրադարանների ներմուծում
#Գրաֆիկական ինտերֆեյսն ապահովող գրադարան
from tkinter import *  
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.ttk import Radiobutton
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter.ttk import Progressbar
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import ttk
import smtplib 
#Ժամանակի և ամսաթվի հետ աշխատելու գրադարան
import datetime
from datetime import datetime
import time
#Առցանց սերվեռին եղանակի մասին հարցում ուղարկելու և պատասխան ստանալու համար գրադարաններ
import requests
import json
#Կայքէջ բացելու համար գրադարան
import webbrowser
#GPIO pin-երի հետ աշխատանքի գրադարան
import RPi.GPIO as GPIO

#GPIO-ի կարգավորում և միացում

GPIO.setmode(GPIO.BOARD)   
GPIO.setwarnings(False)
#Մուտքային և ելքային pin-երի հայտարարում
GPIO.setup(7, GPIO.OUT)   
GPIO.setup(11, GPIO.IN)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
BUZZER = 33
GPIO.setup(BUZZER, GPIO.OUT)

servoPIN = 13
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)
p.start(2.5)

PIN_TRIGGER = 12
PIN_ECHO = 18
 
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

#պատուհանի ստեղծում և կարգավորում
win=tk.Tk()
win.geometry("1024x768+300+100")
#win.resizable(width=False, height=False)
guyn='DarkSeaGreen3'
guyn1='#c4c4c4'
win['bg']=guyn
win.title("Ջերմոցի ղեկավարման ավտոմատացված համակարգ")

#ծրագրի նշանի ներմուծում և տեղադրում
icon = PhotoImage(file="/home/pi/Desktop/logo/greenhouse-1.png")    

win.iconphoto(False, icon)

result=messagebox.askquestion("Լեզու/Язык", "Թողնե՞լ հայերենը (YES), թե՞ անցնել ռուսերենի (NO)։"+"\n"+"\n"+"Остаться на армянском (YES) или переключить язык на русский (NO)?")

if result == 'yes':
    messagebox.showinfo('Զգուշացում', 'Ծրագիրը գործարկելուց առաջ համապատասխան դաշտում մուտքագրե՛ք Ձեր էլ․ հասցեն՝ ջրի քանակի մասին ծանուցումներ ստանալու համար։')
else:
    messagebox.showinfo('Оповещение', 'Перед работой в программе введите Ваш адрес эл. почты, чтобы получать уведомления о количестве воды.')

#Անհրաժեշտ տիպերի փոփոխականների ստեղծում
amsativ = datetime.now()
jur = tk.IntVar()
rejim = tk.IntVar()
sonic = 0
mode = tk.IntVar()
tokos=tk.IntVar()
jertokos = tk.IntVar()
jer = tk.IntVar()
kh = tk.IntVar()
exanak=0
jm = tk.StringVar()
rp = tk.StringVar()
hr=" "
mn=" "
chor=1
m=100
pb=100
hasce=""


#Ֆունկցիաների հայտարարում/ֆունկցիաների մի մասը կանչվում են ծրագրի կոճակներով, մյուս մասը անընդհատ են աշխատում/
#Կայքէջը բացելու կոճակի ֆունկցիան
def fmd():
    webbrowser.open_new("http://physmath.am/")
#Մենյուի տողի ենթամենյուի ցուցանակի ֆունկցիան    
def about():
    if result == 'yes':
        messagebox.showinfo('Ծրագրի մասին', 'Ծրագիրը ջերմոցի ղեկավարման ավտոմատացված համակարգ է, որը գրված է Python ծրագրավորման լեզվով և աշխատում է Raspberry Pi համակարգչի հետ։ Ծրագրի հեղինակներն են Ֆիզմաթ հատուկ դպրոցի աշակերտներ Նարեկ Սարգսյանը և Գևորգ Սարգսյանը։ Ծրագրում օգտագործված նկարները, գրադարանները վերցված են համացանցի ազատ աղբյուրներից և պատկանում են իրենց ստեղծողներին։ Ծրագիրը ստեղծված է 2021-2022թթ․')
    else:
        messagebox.showinfo('О программе', 'Программа является системой автоматического управления теплицей, которая написана на языке программирования Python и работает с микрокомпьютером Raspberry Pi. Авторы программы ученики школы ФИЗМАТ Нарек Саргсян и Геворг Саргсян. Картинки, библиотеки, использованные в программе, были взяты из открытых источников интернета и принадлежат их создателям. Программа была создана в 2021-2022 годах.')
    
#Խոնավության տվիչի արժեքի հիման վրա խոնավության աստիճանը էկրանին տպելու ֆունկցիա
def yl():
    #GPIO.input(11):
    if GPIO.input(11):
        moisture = tk.Label(win, text="", font=('Arial', 17), compound = tk.LEFT, image=drsoil)
        moisture.grid(column=3, row=0, padx=5, pady=5)
        #print("CHOR")

    else:
        moisture = tk.Label(win, text="", font=('Arial', 17), compound = tk.LEFT, image=soil)
        moisture.grid(column=3, row=0, padx=5, pady=5)
        #print("TAC")        
    clock.after(200, yl)

#Հեռաչափ տվիչի արժեքից կախված աշխատողներկ վիճակագրական տվյալներ ստեղծող ֆունկցիա

def son ():
    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO)==0:
          pulse_start_time = time.time()
    while GPIO.input(PIN_ECHO)==1:
          pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)
    #print (distance,"cm")
    if distance <= 20:
        GPIO.output(37, 1)
        
        def buzz(noteFreq, duration):
            halveWaveTime = 1 / (noteFreq * 2 )
            waves = int(duration * noteFreq)
            for i in range(waves):
               GPIO.output(BUZZER, True)
               time.sleep(halveWaveTime)
               GPIO.output(BUZZER, False)
               time.sleep(halveWaveTime)

        def play():
            t=0
            notes=[262,294,330,262]
            duration=[0.5,0.5,0.5,0.5]
            for n in notes:
                buzz(n, duration[t])
                time.sleep(duration[t] *0.1)
                t+=1

        play()

        time.sleep(1)
        GPIO.output(37, 0)               
        f = open("/home/pi/Desktop/logo/emp.txt", "a")
        f.write("\n"+"Today, employees have been entered at"+"\n"+time.strftime('%H:%M:%S')+"\n"+amsativ.strftime("%a, %d %B %Y")+"\n")
        f.close()
        
    clock.after(500, son)


#def jmak ():
#    bar.configure(value=m)
#    bar.update()
#    jqan=100
    
#def jurminus():
#    global jqan
#    jqan -= 5
#    bar.configure(value=jqan)
#    bar.update()
        
 #Կենդանի ժամացույցի ֆունկցիա   
def tick():
    global time1
    time2 = time.strftime('%H:%M')    
    if time2 != time1:
        time1 = time2
        date = tk.Label(win,  text=time2, bg=guyn1, font=('Arial', 17), )
        date.place(x=60, y=155)
      
    clock.after(200, tick)

#Գրաֆիկով ջրելու կոճակների աշխատանքային ֆունկցիաներ
def graphwater ():
    submit.place_forget()
    jam1.place_forget()
    rope1.place_forget()
    jam.place_forget()
    rope.place_forget()
    hr = jm.get()
    mn = rp.get()

def alarm ():
    hr = jm.get()
    mn = rp.get()
    #print(hr)
    #print(mn)
    hr1=time.strftime('%H')
    mn1=time.strftime('%M')
    mode=rejim.get()
    print(mode)
    if mode == 2 and hr == hr1 and mn == mn1:
        
        print("YES")
        jurr()
        vichak()
        
        GPIO.output(7, 1)      

        time.sleep(7)          

        GPIO.output(7, 0)      

        time.sleep(54)
        

    elif mode == 1:
        print("auto")
        if GPIO.input(11):
            GPIO.output(7, 1)      

            time.sleep(3)          

            vichak()

            GPIO.output(7, 0)
            jurr()
            print("AUTO-CHOR")

        else:
            
            print("AUTO-chjrel")    
        
        
    else:
        
        print("No")

    clock.after(1000, alarm)    
  
#Կենդանի ամսաթվի արտատպման ֆունկցիա
def amsat ():
    amsativ = datetime.now()
    date = tk.Label(win, font=('Arial', 17), compound = tk.LEFT, image=cal)
    date.grid(column=1, row=0)
    date = tk.Label(win,  text=amsativ.strftime("%a, %d %B %Y"), bg=guyn1, font=('Arial', 10) )
    date.place(x=200, y=147)
    clock.after(1000, amsat)
#Գրաֆիկով ջրելու ընտրանքների արտատպման ֆունկցիա
def graphwater1 ():
    submit.place(x=210, y=395)
    jam1.place(x=195, y=360)
    rope1.place(x=268, y=360)
    jam.place(x=238, y=365)
    rope.place(x=318, y=365)

#Աշխատողների վիճակագրական տվյալների արտատպման ֆունկցիա
def employee():
    OK.place(x=940, y=520)
    txt.delete(1.0,tk.END)
    f = open("/home/pi/Desktop/logo/emp.txt", "r")
    txt.insert('1.0', f.read())

#Վիճակագրական տվյալների արտատպման ֆունկցիա
def stat():
    OK.place(x=940, y=520)
    txt.delete(1.0,tk.END)
    f = open("/home/pi/Desktop/logo/st.txt", "r")
    txt.insert('1.0', f.read())

#Տեքստային տիրույթի մաքրման կոճակի ֆունկցիա
def tx():
    OK.place_forget()
    txt.delete(1.0,tk.END)

#Օդափոխման կոճակների և ընդհանուր աշխատանքի ֆունկցիա        
def khonavutyun ():
    
    khon.place(x=570, y=400)
    khon1.place(x=560, y=360)
    khon2.place(x=600, y=395)
    khsubmit.place(x=630, y=390)

def khonavutyun1 ():
    
    khon.place_forget()
    khon1.place_forget()
    khon2.place_forget()
    khsubmit.place_forget()
    
def khonavutyun3 ():

    tokos=khon.get()	

    api_key = "2b54f03171c9e9260ef99b9cb5a4dca2"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name = town.get()

    complete_url = base_url + "appid=" + "2b54f03171c9e9260ef99b9cb5a4dca2" + "&q=" + city_name + "&units=metric"

    response = requests.get(complete_url)

    x = response.json()

    if x["cod"] != "404":

            y = x["main"]

            current_temperature = y["temp"]
            exanak = y["temp"]

            current_pressure = y["pressure"]

            current_humidiy = y["humidity"]

            z = x["weather"]

            weather_description = z[0]["description"]

            #celsius['text']=str(current_temperature) +'°C'+ "\n" +str(weather_description)

	

    else:
            print(" City Not Found ")
    tok=int(tokos)
    #print(type(tok))
    #print(type(current_temperature))

    if tok <= current_temperature:
        
        p.ChangeDutyCycle(5)              
        #print("Odapoxel")
        
        
    else:
        p.ChangeDutyCycle(12.5)
        
        
        #print("chodapoxel")
        

        
   
    clock.after(1000, khonavutyun3)


#Ջեռուցման կոճակների և ընդհանուր աշխատանքի ֆունկցիա    
def jerucum ():
    
    jer.place(x=15, y=620)
    jer1.place(x=15, y=585)
    jer2.place(x=45, y=615)
    jersubmit.place(x=80, y=615)

def jerucum1 ():
    
    jer.place_forget()
    jer1.place_forget()
    jer2.place_forget()
    jersubmit.place_forget()
    
def jerucum3 ():
    jertokos=jer.get()

    api_key = "2b54f03171c9e9260ef99b9cb5a4dca2"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name = town.get()

    complete_url = base_url + "appid=" + "2b54f03171c9e9260ef99b9cb5a4dca2" + "&q=" + city_name + "&units=metric"

    response = requests.get(complete_url)

    x = response.json()

    if x["cod"] != "404":

            y = x["main"]

            current_temperature = y["temp"]
            exanak = y["temp"]

            current_pressure = y["pressure"]

            current_humidiy = y["humidity"]

            z = x["weather"]

            weather_description = z[0]["description"]

            #celsius['text']=str(current_temperature) +'°C'+ "\n" +str(weather_description)

	

    else:
            print(" City Not Found ")

    jr = int(jertokos)
    #print(type(jr))
    #print(type(current_temperature))

    if jr >= current_temperature:
        
        #miacnel luysy              
        #print("Jerucel")
        GPIO.output(38, 1)
        
        
    else:
        #anjatel luysy
        
        GPIO.output(38, 0)
       # print("chjerucel")
        
    # Полученные данные добавляем в текстовую надпись для отображения пользователю
    clock.after(1000, jerucum3)

#Ջրելու ռեժիմի կարգավորումների արտատպման և թաքցնելու ֆունկցիաներ
def watmode():  
    avtomat.place(x=15, y=370)
    graph.place(x=15, y=400)
    submit1.place(x=103, y=400)

def watmode1():  
    avtomat.place_forget()
    graph.place_forget()
    submit1.place_forget()
    mode=rejim.get()
    #print(mode)

#Վիճակագրական տվյալները կից ֆայլում գրանցելու ֆունկցիա
def vichak():
    mode=rejim.get()
    global md
    if mode == 1:
        
        md="Automatic mode"
        
    else:
        
        md="Scheduled mode"
        
    f = open("/home/pi/Desktop/logo/st.txt", "a")
    f.write("\n"+"Planted have been watered at"+"\n"+time.strftime('%H:%M:%S')+"\n"+amsativ.strftime("%a, %d %B %Y")+"\n"+md+"\n")
    f.close()

#Աշխատողների վիճակագրական տվյալների կից ֆայլում գրանցման ֆունկցիա
def ash():
    f = open("/home/pi/Desktop/logo/emp.txt", "a")
    f.write("\n"+"Today, employees have been entered at"+"\n"+time.strftime('%H:%M:%S')+"\n"+amsativ.strftime("%a, %d %B %Y")+"\n")
    f.close()

#Ջրել հիմա կոճակի աշխատանքային ֆունկցիա
def watern():
    GPIO.output(7, 1)      #включение светодиода

    time.sleep(5)          #ожидание 1 секунды

    GPIO.output(7, 0)      #выключение светодиода
    jurr()
   # jurminus()
    if result == 'yes':
        messagebox.showinfo('Ջրել հիմա', 'Բույսերը ջրվեցին')
    else:
        messagebox.showinfo('Полить сейчас', 'Растения были политы!')
    md="Forced watering"
        
    f = open("/home/pi/Desktop/logo/st.txt", "a")
    f.write("\n"+"Planted have been watered at"+"\n"+time.strftime('%H:%M:%S')+"\n"+amsativ.strftime("%a, %d %B %Y")+"\n"+md+"\n")
    f.close()
    #pompi ashtxatanq
    
#Ներկա պահին նշված քաղաքում եղանակային տվյալների սերվերից ստացման ֆունկցիա    
def weathernow():

    api_key = "2b54f03171c9e9260ef99b9cb5a4dca2"

    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    city_name = town.get()

    complete_url = base_url + "appid=" + "2b54f03171c9e9260ef99b9cb5a4dca2" + "&q=" + city_name + "&units=metric"

    response = requests.get(complete_url)

    x = response.json()

    if x["cod"] != "404":

            y = x["main"]

            current_temperature = y["temp"]
            exanak = y["temp"]

            current_pressure = y["pressure"]

            current_humidiy = y["humidity"]

            z = x["weather"]

            weather_description = z[0]["description"]

            celsius['text']=str(current_temperature) +'°C'+ "\n" +str(weather_description)

	

    else:
            print(" City Not Found ")
def progresjur():
    jurr()
    
def jurr():
    global pb
    global hasce
    hasce = entmail.get()
    pb=pb-7
    bar['value'] = pb
    if pb <= 30:
        lbl.place_forget()
        lbl1.place(x=750, y=540)
        sender = "physmath.greenhouse@gmail.com"
        reciever = hasce
        password = "jerm2222"
        SUBJECT = "Զգուշացում ջերմոցում ջրի քանակի մասին։ Оповещение о количестве воды в теплице."
        TEXT = "Բույսերն արդեն ջրվել են 10 (կամ ավելի) անգամ։ Հետևե՛ք ջրի քանակին։ \n \nРастения уже были политы 10 (или более) раз. Следите за количеством воды!"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        server=smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, reciever, message.encode('utf-8'))
    else:
        lbl1.place_forget()
        lbl.place(x=750, y=540)
        
def zro():
    global pb
    pb=100
    bar['value'] = pb
    lbl1.place_forget()
    lbl.place(x=750, y=540)

    
#Անհրաժեշտ նկարների ներմուծում
#wins-ում ծրագիրն աշխատացնելու դեպում ծրագրի ԲՈԼՈՐ ֆայլերը/նկարներ, տեքստային ֆայլեր/ իրենց logo թղթապանակում տեղադրել .py ֆայլի նույն թղթապանակում և հասցեն դարձնել file="/home/pi/Desktop/logo/ֆայլի—անուն․ընդլայնում"
# Raspberry PI-ի Linux Debian ՕՀ-ում ծրագիրն աշխատացնելու դեպում ծրագրի ԲՈԼՈՐ ֆայլերը/նկարներ, տեքստային ֆայլեր/ իրենց logo թղթապանակում տեղադրել աշխ․ սեղանում /Desktop/ և հասցեն դարձնել file="/home/pi/Desktop/logo/ֆայլի—անուն․ընդլայնում"
if result == 'yes':
    graphic = PhotoImage(file="/home/pi/Desktop/logo/graph.png")
    weather = PhotoImage(file="/home/pi/Desktop/logo/weather.png")
    air = PhotoImage(file="/home/pi/Desktop/logo/air.png")
    mode = PhotoImage(file="/home/pi/Desktop/logo/mode.png")
    emp = PhotoImage(file="/home/pi/Desktop/logo/emp.png")
    water = PhotoImage(file="/home/pi/Desktop/logo/wtrnow.png")
    cal = PhotoImage(file="/home/pi/Desktop/logo/calendar1.png")
    cl = PhotoImage(file="/home/pi/Desktop/logo/time.png")
    soil = PhotoImage(file="/home/pi/Desktop/logo/soil.png")
    drsoil = PhotoImage(file="/home/pi/Desktop/logo/drsoil.png")
    wtr = PhotoImage(file="/home/pi/Desktop/logo/physmath.png")
    firing = PhotoImage(file="/home/pi/Desktop/logo/firing.png")
    statistic = PhotoImage(file="/home/pi/Desktop/logo/statistics.png")
else:
    graphic = PhotoImage(file="/home/pi/Desktop/logo/graph_r.png")
    weather = PhotoImage(file="/home/pi/Desktop/logo/weather_r.png")
    air = PhotoImage(file="/home/pi/Desktop/logo/air_r.png")
    mode = PhotoImage(file="/home/pi/Desktop/logo/mode_r.png")
    emp = PhotoImage(file="/home/pi/Desktop/logo/emp_r.png")
    water = PhotoImage(file="/home/pi/Desktop/logo/wtrnow_r.png")
    cal = PhotoImage(file="/home/pi/Desktop/logo/calendar1_r.png")
    cl = PhotoImage(file="/home/pi/Desktop/logo/time_r.png")
    soil = PhotoImage(file="/home/pi/Desktop/logo/soil_r.png")
    drsoil = PhotoImage(file="/home/pi/Desktop/logo/drsoil_r.png")
    wtr = PhotoImage(file="/home/pi/Desktop/logo/physmath_r.png")
    firing = PhotoImage(file="/home/pi/Desktop/logo/firing_r.png")
    statistic = PhotoImage(file="/home/pi/Desktop/logo/statistics_r.png")
    
#Պատուհանում տեքստային դաշտերի ստեղծում
time1 = ''
clock = tk.Label(win, font=('times', 20, 'bold'), image=cl, compound = tk.LEFT)
clock.grid(column=0, row=0)
#Դաշտերի վերնագրեր
if result == 'yes':
    tk.Label(text='Տեղեկատվություն', bd=5, bg=guyn, font=('Arial', 11, 'bold')).place(x=300, y=-7)
else:
    tk.Label(text='Информация', bd=5, bg=guyn, font=('Arial', 11, 'bold')).place(x=300, y=-7)
if result == 'yes':    
    tk.Label(text='Տեքստային տիրույթ', bd=5, bg=guyn, font=('Arial', 12, 'bold')).place(x=800, y=1)
else:
    tk.Label(text='Текстовая область', bd=5, bg=guyn, font=('Arial', 12, 'bold')).place(x=800, y=1)
if result == 'yes':
    tk.Label(text='Կարգավորումներ', bd=5, bg=guyn, font=('Arial', 11, 'bold')).place(x=300, y=222)
else:
    tk.Label(text='Настройки', bd=5, bg=guyn, font=('Arial', 11, 'bold')).place(x=300, y=222)
#Պատուհանում կոճակների ստեղծում
#գրաֆիկով ջրելու ժամ
gr=tk.Button(text='',image=graphic, compound = tk.LEFT, bd=5, font=('Arial', 16), command=graphwater1)
gr.grid(row=(1), column=(1), stick='wens', padx=10, pady=5)

#Եղանակ
tk.Button(text='', image=weather, compound = tk.LEFT, bd=5, font=('Arial', 16), command=weathernow).grid(row=(0), column=(2), stick='wens', padx=10, pady=15)
#Եղանակն իմանալու համար քաղաքի ընտրության ցուցակ
town = Combobox(win, font=('Arial', 9))
town['values'] = ("Yerevan, AM", "Gyumri, AM", "Vanadzor, AM", "Ijevan, AM", "Ashtarak, AM", "Hrazdan, AM", "Gavar, AM", "Armavir, AM", "Artashat, AM", "Kapan, AM", "Yeghegnadzor, AM") 
town.current(0)
town.place(x=380, y=167)
#Եղանակի արտատպման դաշտ
celsius = tk.Label(win, text="  Weather  ", bg=guyn1, font=('Arial', 13))
celsius.grid(row=0, column=2)
#Օդափոխում
tk.Button(text='',image=air, compound = tk.LEFT, bd=5, font=('Arial', 16), command=khonavutyun).grid(row=(1), column=(3), stick='wens', padx=5, pady=5)
#Ջեռուցում
tk.Button(text='',image=firing, compound = tk.LEFT, bd=5, font=('Arial', 16), command=jerucum).grid(row=(2), column=(0), stick='wens', padx=5, pady=5)
#Ջրելու ռեժիմ
tk.Button(text='', image=mode, compound = tk.LEFT, bd=5, font=('Arial', 16), command=watmode).grid(row=(1), column=(0), stick='wens', padx=5, pady=5)
#Աշխատողներ
tk.Button(text='', image=emp, compound = tk.LEFT, bd=5, font=('Arial', 16), command=employee).grid(row=(2), column=(1), stick='wens', padx=10, pady=5)
#Վիճակագրույուն
tk.Button(text='', image=statistic, compound = tk.LEFT, bd=5, font=('Arial', 16), command=stat).grid(row=(2), column=(2), stick='wens', padx=10, pady=5)
#Ջրել հիմա
tk.Button(text='', image=water, compound = tk.LEFT, bd=5, font=('Arial', 16), command=watern).grid(row=(1), column=(2), stick='wens', padx=10, pady=5)
tk.Label(text=' ', font=('Arial', 17), bd=0, bg=guyn).grid(row=(3), column=(1), stick='w', pady=20)
#Գրաֆիկով ջրելու կարգավորման հաստատում
if result == 'yes':
    submit = tk.Button(text='Հաստատել ժամը', bd=5, font=('Arial', 9), command=graphwater)
else:
    submit = tk.Button(text='Подтвердить', bd=5, font=('Arial', 9), command=graphwater)

#Գրաֆիկով ջրելու ժամի և րոպեի ընտրման սողնակների ստեղծում
jam = tk.Spinbox(win, values=('00', '01', '02', '03', '04', '05', '06', '07',
         '08', '09', '10', '11', '12', '13', '14', '15',
         '16', '17', '18', '19', '20', '21', '22', '23', '24'), width=2, state='readonly', textvariable=jm)
rope = tk.Spinbox(win, values=('00', '01', '02', '03', '04', '05', '06', '07',
           '08', '09', '10', '11', '12', '13', '14', '15',
           '16', '17', '18', '19', '20', '21', '22', '23',
           '24', '25', '26', '27', '28', '29', '30', '31',
           '32', '33', '34', '35', '36', '37', '38', '39',
           '40', '41', '42', '43', '44', '45', '46', '47',
           '48', '49', '50', '51', '52', '53', '54', '55',
           '56', '57', '58', '59', '60'), width=2, state='readonly', textvariable=rp)
#Տեքստային դաշտերի ստեղծում գրաֆիկով ջրելու համար
if result == 'yes':
    jam1 = tk.Label(text='ժամ:', bd=5, font=('Arial', 10))
else:
    jam1 = tk.Label(text='Час:', bd=5, font=('Arial', 10))
if result == 'yes':
    rope1 = tk.Label(text='Րոպե:', bd=5, font=('Arial', 10))
else:
    rope1 = tk.Label(text='Мин.:', bd=5, font=('Arial', 10))
#Ընտրման, հաստատման կոճակների, թվային սողնակի ստեղծում
#Ջրելու ռեժիմի ընտրման կոճակներ
if result == 'yes':
    avtomat = Radiobutton(win, text='Ավտոմատ', value=1, variable=rejim)
else:
    avtomat = Radiobutton(win, text='Автомат.', value=1, variable=rejim)
if result == 'yes':
    graph = Radiobutton(win, text='Գրաֆիկով', value=2, variable=rejim)
else:
    graph = Radiobutton(win, text='По графику', value=2, variable=rejim)
if result == 'yes':
    submit1 = tk.Button(text='Հաստատել', bd=5, font=('Arial', 7), command=watmode1)
else:
    submit1 = tk.Button(text='Подтвердить', bd=5, font=('Arial', 7), command=watmode1)
#Այն ջերմաստիճանի ընտրման կոճակները և  սողնակը, որից բարձրի դեպքում միանում է օդափոխումը
if result == 'yes':
    khon1 = tk.Label(text='Օդափոխման ջերմաստիճան', bd=5, font=('Arial', 8))
else:
    khon1 = tk.Label(text='Темп. проветривания', bd=5, font=('Arial', 8))
khon2 = tk.Label(text='°C', bd=5, bg=guyn1, font=('Arial', 10))
khon = tk.Spinbox(win, from_=0, to=50, width=2, state='readonly', textvariable=kh)
if result == 'yes':
    khsubmit = tk.Button(text='Հաստատել', bd=5, font=('Arial', 10), command=khonavutyun1)
else:
    khsubmit = tk.Button(text='Подтвердить', bd=5, font=('Arial', 10), command=khonavutyun1)
bar1 = tk.Button(text='', bd=5, font=('Arial', 10), compound = tk.LEFT, image=wtr, command=fmd).grid(row=(2), column=(3), stick='w', padx=5, pady=5)

#Այն ջերմաստիճանի ընտրման կոճակները և սողնակը, որից ցածրի դեպքում միանում է ջեռուցումը
if result == 'yes':
    jer1 = tk.Label(text='Ջեռուցման ջերմաստիճան', bd=5, font=('Arial', 8))
else:
    jer1 = tk.Label(text='Темп. отопления', bd=5, font=('Arial', 8))
jer2 = tk.Label(text='°C', bd=5, bg=guyn1, font=('Arial', 10))
jer = tk.Spinbox(win, from_=0, to=50, width=2, state='readonly', textvariable=jer)
if result == 'yes':
    jersubmit = tk.Button(text='Հաստատել', bd=5, font=('Arial', 10), command=jerucum1)
else:
    jersubmit = tk.Button(text='Подтвердить', bd=5, font=('Arial', 10), command=jerucum1)
#bar1 = tk.Button(text='', bd=5, font=('Arial', 10), compound = tk.LEFT, image=wtr, command=fmd).grid(row=(2), column=(3), stick='w', padx=5, pady=5)
#tk.Button(text='Զրոյացնել', bd=5, font=('Arial', 10), command=jmak).place(x=605, y=635)
 
#bar = Progressbar(win, length=150, style='black.Horizontal.TProgressbar')  
#bar.configure(value=100)
#bar.place(x=565, y=610)  

#Տեքստային դաշտի ստեղծում
txt = scrolledtext.ScrolledText(win, width=30, height=40)  
txt.place(x=750, y=30)

OK = tk.Button(text='OK', bd=5, font=('Arial',13), command=tx)

if result == 'yes':    
    lbl = Label(win, text="Ջրի քանակ", fg="black", bd=5, bg=guyn, font=('Arial', 11, 'bold'))
else:    
    lbl = Label(win, text="Количество воды", fg="black", bd=5, bg=guyn, font=('Arial', 11, 'bold'))  
lbl.place(x=750, y=540)
if result == 'yes':
    lbl1 = Label(win, text="Հետևե՛ք ջրի քանակին։", fg="red", bd=5, bg=guyn, font=('Arial', 11, 'bold'))  
else:
    lbl1 = Label(win, text="Следите за колиюеством воды!", fg="red", bd=5, bg=guyn, font=('Arial', 11, 'bold'))  

#btn = Button(win, text="Ջրել", command=progresjur)
#btn.place(x=750, y=300)
if result == 'yes':
    btn1 = Button(win, text="Զրոյացնել", command=zro)
else:
    btn1 = Button(win, text="Обнулить", command=zro)

btn1.place(x=750, y=600)

bar = Progressbar(win, length=200)
bar.place(x=750, y=570)
bar['value'] = pb

if result == 'yes':
    mail = Label(win, text="Մուտքագրե՛ք Ձեր էլ․ հասցեն։", bd=5, bg=guyn, font=('Arial', 11, 'bold'))
else:
    mail = Label(win, text="Введите адрес Вашей эл. почты!", bd=5, bg=guyn, font=('Arial', 11, 'bold'))
mail.place(x=750, y=670)  
entmail = Entry(win,width=30)  
entmail.place(x=750, y=700)

if result == 'yes':
    #Մենյուի տողի ստեղծում և կոճակների ավելացում
    menu = Menu(win)  
    new_item = Menu(menu, tearoff=0) 
    #Ենթամենյուի ավելացում 
    new_item.add_command(label='Ծրագրի մասին', command=about)
    #Բաժանիչ գծի ստեղծում
    new_item.add_separator()
    #Ենթամենյուի ավելացում
    new_item.add_command(label='Դուրս գալ', command=win.destroy)
    #Մենյուի անվանում
    menu.add_cascade(label='Ֆայլ', menu=new_item)

    win.config(menu=menu)  

else:
    #Մենյուի տողի ստեղծում և կոճակների ավելացում
    menu = Menu(win)  
    new_item = Menu(menu, tearoff=0) 
    #Ենթամենյուի ավելացում 
    new_item.add_command(label='О программе', command=about)
    #Բաժանիչ գծի ստեղծում
    new_item.add_separator()
    #Ենթամենյուի ավելացում
    new_item.add_command(label='Выйти', command=win.destroy)
    #Մենյուի անվանում
    menu.add_cascade(label='Файл', menu=new_item)

    win.config(menu=menu)  
    
#Grid տիպի դասավորման կարգավորումներ
win.grid_columnconfigure(0, minsize=100)
win.grid_columnconfigure(1, minsize=100)
win.grid_columnconfigure(2, minsize=100)

win.grid_rowconfigure(0, minsize=100)
win.grid_rowconfigure(1, minsize=100)

#Անդադար աշխատող ֆունկցիաների կանչ
yl()
tick()
alarm()
son()
amsat()
khonavutyun3()
jerucum3()
weathernow()
win.mainloop()
