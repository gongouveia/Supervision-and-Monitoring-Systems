

'''
#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOo
#                                                                                          #
#    Trabalho realizado no contexto da Cadeira Sistemas de Monitorização e Supervisão      #    
#                                                                                          #
#    Universidade de Coimbra - FCTUC                                                       #
#    Prof. Jorge Landeck                                                                   #
#                                                                                          #
#    António Caramelo                                                                      #
#    Gonçalo Gouveia                                                                       #
#                                                                                          # 
#                                                                                          # 
#       NOTE: in this code eery 0.5 seconds corresponds to 5 minutes in real life          # 
#       https://demo.thingsboard.io/home                                                   #
#pip install tk                                                                            #
#mqtt library pip install paho-mqtt                                                        #                 
#                                                                                          #
#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOo


#         CREDETIANS
#         USER            smsprojeto2021.22@gmail.com
#         PASS            SMSprojeto2022


'''
#
#
#
import paho.mqtt.client as paho             #mqtt library pip install paho-mqtt
import tkinter as tk                        #pip install tk                 
#
#
import pandas as pd
import time
#
#
#
#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo...
#
def on_publish(client,userdata,result):             #create function for callback
    print("data published to thingsboard \n")
    pass
#
#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo...
#
#
ACCESS_TOKEN='O8KS7o0vnZRqaUJrWtX1'                 #Token of your device
broker="demo.thingsboard.io"                        #host name
port=1883                                           #data listening port
#
client1= paho.Client("control1")                    #create client object
client1.on_publish = on_publish                     #assign function to callback
client1.username_pw_set(ACCESS_TOKEN)               #access token from thingsboard device
client1.connect(broker,port,keepalive=60)           #establish connection
#
#
#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo...
#
#
#
fields = 'Valves Start', 'Valves OFF', 'Controler ON', 'Controler OFF', 'Refresh Time (min)'
aux= []
#
def fetch(entries, aux):
    for entry in entries:
        field = entry[0]
        text  = entry[1].get()
        aux.append(text)
        print('%s: "%s"' % (field, text)) 
    return aux

def makeform(root, fields):
    entries = []

    for field in fields:
        row = tk.Frame(root)
        lab = tk.Label(row, width=25, text=field, anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=6, pady=6)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries.append((field, ent))
    return entries

def main_gui(error = False):
    root = tk.Tk()
    
    
    
    tk.Label(root, text="Trabalho realizado por:\n\n").pack()
    tk.Label(root, text="António Caramelo MEF").pack()
    tk.Label(root, text="Gonçalo Gouveia MEF\n").pack()
    
    if error == True:
        tk.Label(root, text="\n\n ERROR INVALID FORMATS:\n\n").pack()

        tk.Label(root, text="Insert valid  Formats:\n").pack()

    tk.Label(root, text="Time Format >>> hour:minutes:seconds").pack()
    tk.Label(root, text="Refresh time Format >>> 5min-60min").pack()
    tk.Label(root, text="multiples of 5").pack()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e,aux)))   
    b1 = tk.Button(root, text='SEND',command=(lambda e=ents: fetch(e,aux)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    tk.Label(root, text="Press X to send Data to Thingsboard").pack()
    root.mainloop()

main_gui()
#
#if (int(aux[4])/5)%1 != 0:
#    main_gui(True)
#  
#   
#
#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo...
# values threshold 
#
#Retrieve values from the GUI
#
refresh_time = int(aux[4])                 #min      #only values allowed between 5-60minutes, multiples of 5 minutes                 
time_start_running_valves = aux[0]
time_close_running_valves = aux[1]
time_start_running_controler = aux[2]
time_close_running_controler =aux[3]
#
#
################# Constants
#
water_running_per_5minute = 15    # about 4 liter per minute for when all valves are running
#
#                                           Descomentar para o caso em que se queira tirar o gui
#
#
#refresh_time = int(aux[4])                 #min      #only values allowed between 5-60minutes, multiples of 5 minutes                 
#
#time_start_running_valves = '06:00:00'
#time_close_running_valves = '06:15:00'
#
#time_start_running_controler ='08:00:00'
#time_close_running_controler ='23:00:00'
#
#
#    
#                                    #valves open then this conditions values are activated
Temperature_threshold      = 40          #ºC
Water_Consuption_threshold = 25          #l
#
#
solar_pannel_area = 0.65                 #m^2
solar_pannel_efficiency  =  0.22
#
#
power_router = 10                        #W
power_valves = 5.52                      #W
power_plc = 40.40                        #W
power_controler = 33                     #W
power_meteo_station = 1.2                #W
power_power_counter = 0.40               #W
inverter_eff = 0.8                       #W
#
#
############### Initialize Parameters
#
daily_water_consumed = 0    #l
daily_power_consumed = 0    #W
power_consumed_total = 0    #kW/h
total_precepitation = 0     #mm
#
#
#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo...


def on_publish(client,userdata,result):             #create function for callback
    print("data published to thingsboard \n")
    pass


def read_data(csv_file):
    A = pd.read_csv(csv_file)  # read csv file with raw data

    dataTime =           A['dataTime'].values.tolist()  
    Temperature =        A['Temperature (ºC)'].values.tolist() 
    Relative_Humidity =  A['Relative_Humidity (prc)'].values.tolist() 
    Precipitation =      A['Precipitation (mm)'].values.tolist() 
    Solar_Radiation =    A['Solar_Radiation (W/m2)'].values.tolist()
    Wind_direction =     A['Wind_direction (º)'].values.tolist() 
    Wind_Speed =         A['Wind_Speed (Km/h)'].values.tolist()

    
    #Programmer

    return  dataTime,Temperature, Relative_Humidity, Precipitation, Solar_Radiation,Wind_direction,Wind_Speed


def run_valves_time(time_start_running_valves,time_close_running_valves,daily_power_consumed,power_consumed, time):
    
    var_1 = time >= time_start_running_valves 
    var_2 = time < time_close_running_valves
    
    if var_1&var_2 :
        power_consumed = power_consumed +3
        return ['RUNNING','RUNNNG','RUNNING','RUNNING',power_consumed]
        
    else:
        return ['OFF','OFF','OFF','OFF',power_consumed]


def controler(time, time_open, time_close,power_consumed):
    var_1 = time >= time_open 
    var_2 = time < time_close
    if (var_1 & var_2) :
        power_consumed = power_consumed + power_controler
        return 'RUNNING',power_consumed
    else:
        return 'OFF',power_consumed

#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo...



dataTime,Temperature, Relative_Humidity, Precipitation, Solar_Radiation,Wind_direction,Wind_Speed = read_data('SMS_data_final.csv')

did_it_rain_day_before = False
i = 0


while True: 

    if dataTime[i] == '00:00:00':        #reset values every day 
        print('NEW_DAY')
        if total_precepitation>10:          #evaluate at the end of the day if it has rainned
            did_it_rain_day_before = True   #if yes it water the garden
        else:
            did_it_rain_day_before = False
        total_precepitation = 0            
        daily_water_consumed = 0
        power_consumed_total = 0



    power_consumed = daily_power_consumed + power_plc + power_power_counter + power_meteo_station    #static consume
    water_consumed = 0                                                                               #auxiliary step

        
    valve1,valve2,valve3,valve4,power_consumed = run_valves_time(time_start_running_valves,time_close_running_valves,daily_power_consumed,power_consumed, dataTime[i])
    
    if did_it_rain_day_before == True:
        valve1,valve2,valve3,valve4 = ['OFF','OFF','OFF','OFF']
        

    controls,power_consumed = controler(dataTime[i], time_start_running_controler, time_close_running_controler,power_consumed)
    solar_converted = Solar_Radiation[i]*solar_pannel_area*solar_pannel_efficiency * inverter_eff
    ratio = 100*solar_converted/power_consumed
    
    power_consumed_total = power_consumed_total + (power_consumed*refresh_time*60)/3600000
    if  valve1 == 'RUNNING':
        water_consumed = water_running_per_5minute
        daily_water_consumed = daily_water_consumed + water_consumed
    
    total_precepitation = total_precepitation + Precipitation[i]      #mm
            
        
    payload="{"
    payload+="\"Temperature (ºC)\":"+str(Temperature[i])+",";
    payload+="\"Relative_Humidity (%)\":"+str(Relative_Humidity[i])+",";
    payload+="\"Precipitation (mm)\":"+str(Precipitation[i])+","; 
    payload+="\"Solar_Radiation (W/m2)\":"+str(Solar_Radiation[i])+","; 
    payload+="\"Wind direction (º)\":"+str(Wind_direction[i])+","; 
    payload+="\"Valve1\":"+str(valve1)+",";
    payload+="\"Valve2\":"+str(valve2)+",";
    payload+="\"Valve3\":"+str(valve3)+",";
    payload+="\"Valve4\":"+str(valve4)+","; 
    payload+="\"Controler\":"+str(controls)+",";   
    payload+="\"Power Consuption (day)\":"+str(round(power_consumed_total, 2))+","; 
    payload+="\"Power Consuption\":"+str(round(power_consumed, 2))+","; 
    payload+="\"Water Consuption\":"+str(round(water_consumed, 2))+","; 
    payload+="\"Power Sun Converted (W)\":"+str(solar_converted)+","; 
    payload+="\"Water Consuption (day)\":"+str(daily_water_consumed)+","; 
    payload+="\"power prod/cons\":"+str(ratio)+","; 
    payload+="\"Wind_Speed (Km/h)\":"+str(Wind_Speed[i]);
    payload+="}"
    
    print(dataTime[i])
    print("Telemetry sent with exit")
    
                                                                       #send data to thingsboard 
    ret = client1.publish("v1/devices/me/telemetry",payload)           #topic- v1/devices/me/telemetry
    print(payload)

    #if i%refresh_time == 0:            #send only with teh aquisition time that we desire
        #ret= client1.publish("v1/devices/me/telemetry",payload) #topic- v1/devices/me/telemetry


    i = i+int(refresh_time/5)
    time.sleep(0.5) #alterar timer para 15 min em 15 




#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo...
#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo...
#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo...
#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo...
#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo...
#...oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo......oooOOOOooo...


