from tkinter import*
import forecast_back_end


list_areas = ["ΑΓ.ΚΩΝ/ΝΟΣ - ΣΚΙΑΘΟΣ","ΑΡΓΟΛΙΚΟΣ ΚΟΛΠΟΣ","ΒΟΡ.ΑΝΑΤΟΛΙΚΟ ΑΙΓΑΙΟ","ΒΟΡΕΙΟ ΙΟΝΙΟ","ΗΓΟΥΜΕΝΙΤΣΑ - ΚΕΡΚΥΡΑ","ΘΑΛΑΣΣΑ ΚΥΘΗΡΩΝ"
,"ΘΑΛΑΣΣΑ ΡΟΔΟΥ","ΘΡΑΚΙΚΟ ΠΕΛΑΓΟΣ","ΚΑΡΠΑΘΙΟ","ΚΕΡΑΜΩΤΗ - ΘΑΣΟΣ","Ν. ΕΥΒΟΪΚΟΣ","ΝΟΤΙΟ ΙΟΝΙΟ","ΡΙΟ - ΑΝΤΙΡΡΙΟ","ΑΝΑΤΟΛΙΚΟ ΚΡΗΤΙΚΟ"
,"Β. ΕΥΒΟΪΚΟΣ","ΒΟΡΕΙΟ ΑΙΓΑΙΟ","ΔΥΤΙΚΟ ΚΡΗΤΙΚΟ","ΘΑΛΑΣΣΑ ΚΑΣΤΕΛΟΡΙΖΟΥ","ΘΑΛΑΣΣΑ ΚΩ","ΘΕΡΜΑΪΚΟΣ ΚΟΛΠΟΣ","ΚΑΒΟ ΝΤΟΡΟ"
,"ΚΕΝΤΡΙΚΟ ΑΙΓΑΙΟ","ΚΟΡΙΝΘΙΑΚΟΣ ΚΟΛΠΟΣ","ΝΟΤ.ΑΝΑΤΟΛΙΚΟ ΑΙΓΑΙΟ","ΝΟΤΙΟΔΥΤΙΚΟ ΑΙΓΑΙΟ","ΣΑΡΩΝΙΚΟΣ ΚΟΛΠΟΣ"]


window = Tk()


def export_file():
    forecast_back_end.export()


def select_row1(event):
    global select
    index = list1.curselection()
    select = list1.get(index)
    forecast_back_end.select_area(select)
    list.delete(0,END)
    for item in forecast_back_end.view():
        list.insert(END,item)
    return select


#forecast_back_end.select_area(select)

def select_row(event):
    index = list.curselection()
    select = list.get(index)

    t1.delete(1.0,END)
    t1.insert(END,select[1])
    t2.delete(1.0,END)
    t2.insert(END,select[2])
    t3.delete(1.0,END)
    t3.insert(END,select[3])
    t4.delete(1.0,END)
    t4.insert(END,select[4])



l1 = Label(window,text = "date",)
l1.grid(row = 0,column = 0)
l2 = Label(window,text = "time")
l2.grid(row = 0,column = 2)
l3 = Label(window,text = "wave height")
l3.grid(row = 0,column = 4)
l4 = Label(window,text = "wave degrees")
l4.grid(row = 0,column = 6)

t1 = Text(window,width = 10,height = 1)
t1.grid(row = 0,column = 1)
t2 = Text(window,width = 10,height = 1)
t2.grid(row = 0,column = 3)
t3 = Text(window,width = 10,height = 1)
t3.grid(row = 0,column = 5)
t4 = Text(window,width = 10,height = 1)
t4.grid(row = 0,column = 7)


list = Listbox(window,width = 23,height = 10)
list.grid(row = 1,column = 0,rowspan = 6,columnspan = 2)
list.bind('<<ListboxSelect>>',select_row)



list1 = Listbox(window,width =23,height = 10)
list1.grid(row = 1,column = 6,rowspan = 6,columnspan = 2)
list1.bind('<<ListboxSelect>>',select_row1)

for i in range(0,26):
    items = list_areas[i]
    list1.insert(END,items)

b1 = Button(window,text = "export file",command = export_file,width = 8)
b1.grid(row = 8,column = 6)
b2 = Button(window,text = "close",command = window.destroy,width = 8)
b2.grid(row = 8,column = 7)



window.mainloop()
