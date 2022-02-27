import tkinter as tk


window = tk.Tk()                         # vytvorme okno
window.title("Calculator")               # jmeno aplikace nahore
window.configure(bg='black')             # barva okoli
window.geometry("230x380")               # rozmery okna
window.resizable(0, 0)                   # jsou vzdy stejne

e = ""                                   # promenne pro kontrolu
start = True                             #stavu vypoctu
operator = False
first_eq = True
ever_op = False
ever_num = False
z_error = False
is_calc = False
plmi = False
is_AC = True
is_Cl = False
eq_add = 0
inputText = tk.StringVar()

#vytvorme frame pro radek vstupu/vystupu a pouzijeme .pack
inputFrame = tk.Frame(window, bd=0, highlightbackground="black", highlightcolor="gray", highlightthickness=2)
inputFrame.pack(side=tk.TOP, pady=(40,0), padx = 23)

#vytvorme radek vstupu/vystupu, pouzijeme .grid pro polohu, .pack
inputField = tk.Entry(inputFrame, font=('Georgia', 20), textvariable=inputText, fg="white", bg="black", bd=0, justify=tk.RIGHT, highlightthickness=0)
inputField.grid(row=0, column=0)
inputField.pack(ipady=5)

# vytvorme frame pto tlacitka, .pack
mainFrame = tk.Frame(window, bg="black", bd=0)
mainFrame.pack()

#zacatecni stav kalkulacky
inputText.set("0")

#FUNKCE PRO TLACITKA:

#funkce pro rychlou zmenu pozitini vs negativni cslo
def P_M():
    global plmi  #bool jestli mame negativni cislo
    if (ever_num is False) and (start is False):  # pr: 56 (+) (+/-) ($) 5 
      inputText.set("0")                          # na ($) v enter musi byt -0
    input = inputText.get()
    if input[0]== "-":
      inputText.set(input[1:])                    #vezmeme radek a pridame nebo                                                           odebereme -, neg vs pos
      plmi = False
    else:
      inputText.set((str("-"))+input)
      plmi = True

def Cl_All():               #vracime kalkulacku v zacatecni stav
    global start
    global e
    global operator
    global first_eq
    global eq_add
    global ever_op
    global ever_num
    global z_error
    global is_calc
    global plmi
    global is_AC
     

    inputText.set("0")
    e = ""
    start = True
    operator = False
    first_eq = True
    eq_add = 0
    ever_op = False
    ever_num = False
    z_error = False
    is_calc = False
    plmi = False
    is_AC = True
    swich_op(0)               
    
    
# funkce delici na 100 (%)
def Per():                          
  global start
  if start is False:                 #v IOS kalkulacce nelze pouzit pro zacatecni stav
    input = inputText.get()
    input = float(input) / 100
    inputText.set(str(input))

def Op(oper):                       # funkce pro /, +, -, *
  global operator                   # bool vyraz koci operatorem vs ne
  global first_eq                   # bool jestli ted prave vyuzivame, ze pokud 
                                    # nekolikrat po rade pouzijeme =, bude se 
                                    # opakovat  posledni operace
  global e                          # vyraz
  global ever_op                    # bool v aktualnim vyrazu byl vs nebyl operator
  global ever_num                   # bool bylo vs nebylo cislo
  global z_error                    # bool jestli vznikalo deleni 0
  global plmi                       # bool jetli mame negat. vyraz pouzitim (+/-)
  first_eq = True
  if z_error is False:               
    if (ever_op is True) and (is_calc is False):
      Equ()                                        # po operaci pocitame mezivysledek.
      first_eq = True                              # aby se nekazili vyrazy typu 2+2+2
    if (operator is False) and (start is False):
      input = inputText.get()
      e += input+(str(oper))                         
    elif operator is True:
        e = e[:-1]
        e += str(oper)                             
        swich_op(oper)                            # muzeme zmenit plan, a zmenit 
                                                  # opeator pr: 3++-/3 = 1
    operator = True                               # meli jsme operator, cislo, menime operator
    swich_op(oper)                                
    ever_op = True
    ever_num = False
  else:
    inputText.set("Error")                        # deleni 0
  plmi = False                                    # do zac. stavu
    
def Cl():                                         # funkce C
    global is_AC                                  # bool je v zac. stavu nebo neni
    global is_Cl                                  # bool pro 0 v mezistavu
    global is_calc                                # bool pro nekolik = a vlastnost
    is_Cl = True
    if is_AC is False:
      is_AC = True                                # promena AC a C v zavislosti na etapu vypoctu
      swich()
    if is_calc:
      Cl_All()
    inputText.set("0")                            # 0 v mezistavu

def Number(n):                                 #funkce pro cisla
  global e
  global operator
  global start
  global ever_num
  global z_error
  global is_calc
  global plmi
  global is_AC
  global is_Cl
  if is_AC:                                            #zmena AC/C
    is_AC = False
    swich()
  if is_Cl:
    inputText.set("")                                    # aby 0 v mezistavu nevadila ostatnim funkcim
    is_Cl = False
  if (ever_num is False) and (start is False) and (plmi is False):
    inputText.set("")
  if start is True:                                #jsme v zacatecnim stavu, je prvni cislice vyrazu
    input = inputText.get()                                 
    if (plmi is True) and (n!=0):                  
      inputText.set(input[:-1:]+(str(n)))              
      operator = False
      swich_op(0)
      start = False
      ever_num = True                                          # muze byt -
      is_calc = False
    if (plmi is False) and (n!=0):
      inputText.set(str(n))
      operator = False
      swich_op(0)
      start = False
      ever_num = True
      is_calc = False
  else:                                                #cislice neni prvni
    if z_error is True:
      inputText.set((str(n)))
    elif n == "0" and e[len(e)-1] == "/":               # deleni 0
        z_error = True
    elif (plmi is True) and (n!=0):
      input = inputText.get()
      if input[1] == "0":                      #pr: 56 (+) (+/-) 52 ($)
        inputText.set(input[:-1:]+(str(n)))    # ($) neni -052; neni -5 -> -2
      else:
        inputText.set(input+(str(n)))
      operator = False
      swich_op(0)
      start = False
      ever_num = True
      is_calc = False
    else:
      input = inputText.get()                          # IOS kalkulacka prijima max 9 cislic za jeden input
      if len(input)<=8:
          inputText.set(input+(str(n)))
          operator = False
          swich_op(0)
          start = False
          ever_num = True
          is_calc = False

def Point():                                       # funkce pro , 
  global start
  global is_AC
  if is_AC:
    is_AC = False                                     # v IOS se meni AC/C
    swich()
  start = False
  input = inputText.get()
  if input[len(input)-1] != ".":               
    inputText.set(input+".")

def Equ():                                                            # funkce pro =
  if z_error is False:
    if (operator is False) and (start is False) and (ever_op is True):
      global e
      global eq_add
      global first_eq
      global is_calc 
      
      if first_eq is False:                                            # nekolik = ve rade
        temp = eq_add
        r = inputText.get()                             
        r += temp
      else:
        first_eq = False
        
        input = inputText.get()
        e += input
        r = e
        
        temp = e[::-1]
        k = 0                                                       # najdeme operaci kterou budeme opakovat
        i = temp[k]
        cislo = i
        while i!="*" and i!="-" and i!="+" and i!="/":
          k += 1
          i = temp[k]
          cislo += i
        temp = cislo[::-1]
        eq_add = temp
      result = str(eval(r))                                        #spocitame vysledek
      if len(result) > 2:
        if result[-1] == "0" and result[-2] == ".":                   # misto 3.0 vypise 3
          result = result[0:-2]
      inputText.set(result)
      e = ""
      is_calc = True
  else:                                                               #deleni 0
    Op("=")
    
#TLACITKA:
                                             # ti, ktere menime rozmistujejeme pomoci grid na soukromrm radku
AC = tk.PhotoImage(file = r"buttons/AC.png")
ac = AC.subsample(4,4)
ac = tk.Button(mainFrame, fg="black", image=AC, bd=0, highlightthickness=0, bg="black", command=lambda: Cl_All())
ac.grid(row=0, column=0)


PM = tk.PhotoImage(file = r"buttons/pm.png")
pm = PM.subsample(4,4)
pm = tk.Button(mainFrame, fg="black", image=PM, bd=0, highlightthickness=0, bg="black", command=lambda: P_M()).grid(row=0, column=1)

PE = tk.PhotoImage(file = r"buttons/%.png")
pe = PE.subsample(4,4)
pe = tk.Button(mainFrame, image=PE, bd=0, highlightthickness=0, bg="black", command=lambda: Per()).grid(row=0, column=2)

DI = tk.PhotoImage(file = r"buttons/div.png")
di = DI.subsample(4,4)
di = tk.Button(mainFrame, fg="black", image=DI, bd=0, highlightthickness=0, bg="black", command=lambda: Op("/"))
di.grid(row=0, column=3)

SE = tk.PhotoImage(file = r"buttons/7.png")
se = SE.subsample(4,4)
se = tk.Button(mainFrame, fg="black", image=SE, bd=0, highlightthickness=0, bg="black", command=lambda: Number("7")).grid(row=1, column=0)

EI = tk.PhotoImage(file = r"buttons/8.png")
ei = EI.subsample(4,4)
ei = tk.Button(mainFrame, fg="black", image=EI, bd=0, highlightthickness=0, bg="black", command=lambda: Number("8")).grid(row=1, column=1)

NI = tk.PhotoImage(file = r"buttons/9.png")
ni = NI.subsample(4,4)
ni = tk.Button(mainFrame, fg="black", image=NI, bd=0, highlightthickness=0, bg="black", command=lambda: Number("9")).grid(row=1, column=2)

MU = tk.PhotoImage(file = r"buttons/mult.png")
mu = MU.subsample(4,4)
mu = tk.Button(mainFrame, fg="black", image=MU, bd=0, highlightthickness=0, bg="black", command=lambda: Op
("*"))
mu.grid(row=1, column=3)

FO = tk.PhotoImage(file = r"buttons/4.png")
fo = FO.subsample(4,4)
fo = tk.Button(mainFrame, fg="black", image=FO, bd=0, highlightthickness=0, bg="black", command=lambda: Number("4")).grid(row=2, column=0)

FI = tk.PhotoImage(file = r"buttons/5.png")
fi = FI.subsample(4,4)
fi = tk.Button(mainFrame, fg="black", image=FI, bd=0, highlightthickness=0, bg="black", command=lambda: Number("5")).grid(row=2, column=1)

SI = tk.PhotoImage(file = r"buttons/6.png")
si = SI.subsample(4,4)
si = tk.Button(mainFrame, fg="black", image=SI, bd=0, highlightthickness=0, bg="black", command=lambda: Number("6")).grid(row=2, column=2)

MI = tk.PhotoImage(file = r"buttons/-.png")
mi = MI.subsample(4,4)
mi = tk.Button(mainFrame, fg="black", image=MI, bd=0, highlightthickness=0, bg="black", command=lambda: Op("-"))
mi.grid(row=2, column=3)

ON = tk.PhotoImage(file = r"buttons/1.png")
on = ON.subsample(4,4)
on = tk.Button(mainFrame, fg="black", image=ON, bd=0, highlightthickness=0, bg="black", command=lambda: Number("1")).grid(row=3, column=0)

TW = tk.PhotoImage(file = r"buttons/2.png")
tw = FI.subsample(4,4)
tw = tk.Button(mainFrame, fg="black", image=TW, bd=0, highlightthickness=0, bg="black", command=lambda: Number("2")).grid(row=3, column=1)

TH = tk.PhotoImage(file = r"buttons/3.png")
th = TH.subsample(4,4)
th = tk.Button(mainFrame, fg="black", image=TH, bd=0, highlightthickness=0, bg="black", command=lambda: Number("3")).grid(row=3, column=2)

PL = tk.PhotoImage(file = r"buttons/+.png")
pl = PL.subsample(4,4)
pl = tk.Button(mainFrame, fg="black", image=PL, bd=0, highlightthickness=0, bg="black", command=lambda: Op("+"))
pl.grid(row=3, column=3)

ZE = tk.PhotoImage(file = r"buttons/0.png")
ze = ZE.subsample(4,4)
ze = tk.Button(mainFrame, fg="black", image=ZE, bd=0, highlightthickness=0, bg="black", command=lambda: Number("0")).grid(row=4, column=0, columnspan=2)

PO = tk.PhotoImage(file = r"buttons/carka.png")
po = PO.subsample(4,4)
po = tk.Button(mainFrame, fg="black", image=PO, bd=0, highlightthickness=0, bg="black", command=lambda: Point()).grid(row=4, column=2)

EQ = tk.PhotoImage(file = r"buttons/=.png")
eq = EQ.subsample(4,4)
eq = tk.Button(mainFrame, fg="black", image=EQ, bd=0, highlightthickness=0, bg="black", command=lambda: Equ()).grid(row=4, column=3)


#Foto na ktere menime
C = tk.PhotoImage(file = r"buttons/C.png")
Tr_p = tk.PhotoImage(file = r"buttons/tr_+.png")
Tr_m = tk.PhotoImage(file = r"buttons/tr_-.png")
Tr_mu = tk.PhotoImage(file = r"buttons/tr_mult.png")
Tr_d = tk.PhotoImage(file = r"buttons/tr_div.png")




def swich():                                  # menime AC/C
  if is_AC is False:
    ac.config(image=C, command=lambda: Cl())
  else:
    ac.config(image=AC, command=lambda: Cl_All())


def swich_op(oper):                            # menime operace 
  if oper == "+":
    pl.config(image=Tr_p)
    mi.config(image=MI)
    mu.config(image=MU)
    di.config(image=DI)
  elif oper == "-":
    pl.config(image=PL)
    mi.config(image=Tr_m)
    mu.config(image=MU)
    di.config(image=DI)
  elif oper == "*":
    pl.config(image=PL)
    mi.config(image=MI)
    mu.config(image=Tr_mu)
    di.config(image=DI)
  elif oper == "/":
    pl.config(image=PL)
    mi.config(image=MI)
    mu.config(image=MU)
    di.config(image=Tr_d)
  else:
    pl.config(image=PL)
    mi.config(image=MI)
    mu.config(image=MU)
    di.config(image=DI)
    
    
    


window.mainloop()