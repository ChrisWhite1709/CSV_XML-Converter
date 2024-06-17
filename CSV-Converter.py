import csv
import os
import xml.etree.ElementTree as ET
import traceback
from datetime import datetime
import re
from tkinter import Tk     
from tkinter.filedialog import askopenfilename

import sys, os


#lists
csv_list_id =[]
csv_list_name = []
csv_list_name_new = ""
data_csv = []
headers = []
name_logfile = "logfile.txt"
encoding_csv = "utf-8"
file_size = 999999999
name_id = ""



##restart for further file input
def restart():   
    os.execv(sys.executable, ['python'] + sys.argv)

def cleanExport(input_name_csv):
    new_data = []
    with open(input_name_csv, newline='', encoding=encoding_csv) as csvfile:
        
        for line in csvfile:
                new_str = []
                count = 1
                items = line.split('""')               
               
                for x in items:
                
                    new_str.append(cleanString(items[count]))                    
                    count +=2
                    
                    if count >= len(items): 
                        
                        new_data.append(new_str)
                        break
        

        input_name_csv = input_name_csv.split(".csv")
        csv_list_name_new = input_name_csv[0] + "_NEW.csv"

        with open(csv_list_name_new,"w", encoding="utf-8", newline ="") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=",")

            for x in new_data:
                csv_writer.writerow(x)
            
        print("Successful")
        print("Your file is called:" + csv_list_name_new)
            
            
def cleanCSV(input_name_csv):
    start = ""
    end = ""
    new_str = ""
    write_string = ""

    with open(input_name_csv, newline='', encoding=encoding_csv) as csvfile:
        for line in csvfile: 
            
            if len(line)<2:
                print("CSV File is not formated like ID,NAME1,COUNTRY")
                exit()
            else: 
                line = line.split(",")
                start = line.pop(0)
                end = line.pop(-1)              
                

                if(len(line)>1):                
                    for items in line:
                        new_str = new_str + items    
                else:
                    new_str = line.pop(0)             
                
               
                line = start + "," + new_str + "," + end                
                
                write_string = write_string + line

                #reset new
                new_str = ""
               
            
        
        input_name_csv = input_name_csv.split(".csv")
        csv_list_name_new = input_name_csv[0] + "_NEW.csv"

        with open(csv_list_name_new,"w", encoding="utf-8") as csvfile:
            csvfile.write(write_string)
        print("Successful")
        print("Your file is called:" + csv_list_name_new)
                
         
def cleanString(input_text):    
    
    #text = re.sub('[^A-Za-z0-9 ,.-_\']+"',"",str(input_text))
    text = re.sub('\W'," ",str(input_text))
    if "  " in text:
        text = text.replace("  ", " ")
        return text
    else:
        return text

def filepicker():
#windows file pick dialog
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    return filename

def checkNameLenth(name):
        name_set = ""
        new_names = []
        local_count = 0
        if len(name) > 40:
            
            #Teilen bei Delimiter " "
            name = name.split(" ")
                
            #Einzelne Teile durchgehen
            for elements in name:
                name_set = name_set + " " + elements

                if len(name_set) > 40:
                    new_names.append(name_set)
                    name_set = ""
                    local_count = local_count +1
                if local_count == 4:
                    return new_names 
                    

        else:
            new_names = 0  

        return new_names

#this function will look for all values in csv & convert them to xml
#function to convert xml -> input is path to csv & xml
def convertcsv_multiple(input_name_csv, input_name_xml,filesize):
    count = 0    
    data = ET.Element('dataroot')
    
   
    #get headers from csv
    with open(input_name_csv, newline='', encoding=encoding_csv) as csvfile:
        r = csv.reader(csvfile, delimiter=',')
        headers = next(r)  


   #get data from csv
    with open(input_name_csv, newline='', encoding=encoding_csv) as csvfile:    
       
        reader = csv.DictReader(csvfile) 
        for row in reader:    
           data_csv.append(row)
               
      
    try:
        #count is used for automatic ADDRNUMBER assignment
        count = 1
        count_size = 0
        file_count = 1
        

        #use data & write to xml format
        for row in data_csv:              
            element1 = ET.SubElement(data, 'Address')
            
            #automatic ADDRNUMBER assignment
            s_elem2 = ET.SubElement(element1,"ADDRNUMBER")
            s_elem2.text = str(count)

            for header in headers:
                #used to seperate long names (over 40 characters), they will be split up to NAME1 to NAME4

                if "NAME" in header:
                    count_name = 1
                    names= checkNameLenth(row[header])
                    if names != 0:
                        for name in names:
                            s_elem1 = ET.SubElement(element1,'NAME'+str(count_name))
                            s_elem1.text = name 
                            count_name = count_name +1
                    else:
                        s_elem1 = ET.SubElement(element1,header)
                        s_elem1.text = row[header]

                elif name_id in header: 
                    s_elem1 = ET.SubElement(element1,"BPVSY") 
                    s_elem1.text = row[header]

                    s_elem1 = ET.SubElement(element1,"BPTYP") 
                    s_elem1.text = "2"




                else:
                    s_elem1 = ET.SubElement(element1,header) 
                    s_elem1.text = row[header]

            count = count + 1
            count_size = count_size + 1            
            
            #if entered file size is reached -> write to xml file
            if(count_size == int(filesize)):
                b_xml = ET.tostring(data, encoding_csv) 
               
                #input_name_xml = input_name_xml.split(".xml")                
                new_xml_name = input_name_xml
                new_xml_name = new_xml_name + str(file_count) + ".xml"                
                
                with open(new_xml_name, "wb") as f:          
                    f.write(b_xml)
                
                print("Successful - File created. File name is: " + new_xml_name)    

                #reset counter
                count_size = 0
                #increase filecount
                file_count = int(file_count) + 1
                #reset list
                data.clear()

    
        new_xml_name = input_name_xml
        new_xml_name = new_xml_name + str(file_count) + ".xml"

        b_xml = ET.tostring(data, encoding_csv)     

        with open(new_xml_name, "wb") as f:          
            f.write(b_xml)

        print("Successful - File created. File name is: " + new_xml_name)  
        

    except Exception:
        with open (name_logfile, "w") as g:
            g.write(traceback.format_exc())
            print (traceback.format_exc())
            restart()  




## THIS IS THE START OF THE PROGRAM!
try:    
    #start_dialog
    print("Hello! This tool is to convert CSV files to XML files!")
    

    #ask for function
    print("")
    print("Press Press [1] for CleanUp [OLD] (remove false characters from NAME1)")
    print('Press Press [2] for CleanUp (SalesForce Export, Seperated with "" ')
    print("Press Press [3] for CSV-XML Conversion")
    print("")
    response =  input("")

    match response:

        case "1":  
            cleanCSV(filepicker())
        case "2":        
            cleanExport(filepicker())
        case "3":
            print("Make sure that the HEADERS are correct -> They will be transfered to e.g. <HEADER1>")
            print("Please provide path to csv. XML will automatically updated or created with the CSVNAME.xml")

            print("Do you want to split the XML files? Press Y or N")
            
            resp_splitfiles = input("")
            if resp_splitfiles == "Y":
                print("How many addresses should one file contain?")            
                file_size = input("")

            print("Please state the CSV header containing the ID")        
            name_id = input("")

            #remove csv from input path & add xml to the end
            input_name_csv = filepicker()   
            input_name_xml = input_name_csv.split(".csv")
            input_name_xml = input_name_xml[0]

            #start reading function 
            convertcsv_multiple(input_name_csv, input_name_xml,file_size)
   
    
    #ask for further input
    print("")
    print("Do you want to take another action? Press Y")
    print("")
    response =  input()
    if response == "y" or "yes":
        restart()    
    
# raise exepction if error occurs
except Exception:
        print (traceback.format_exc())
        with open (name_logfile, "w") as g:
            g.write(traceback.format_exc())
            print (traceback.format_exc())
            restart()  
        


