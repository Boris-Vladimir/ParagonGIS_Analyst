from tkinter import HORIZONTAL, BOTTOM, CENTER, FALSE, ALL, E, W, EW, NS, \
    SEPARATOR, Tk, Frame, Label, Button, Message, Menu, Canvas, Toplevel, \
    StringVar, BooleanVar, filedialog, ttk, SUNKEN, TOP, TRUE, BOTH, LEFT, \
    Text, NORMAL, DISABLED, Entry, simpledialog, DoubleVar, IntVar, \
    Checkbutton, VERTICAL, RIGHT, Radiobutton, messagebox, font as fontTK
import os
from time import sleep
from datetime import datetime

class window(object):

    def __init__(self):
        global icon_color
        global icon_scale
        global cgi_time
        self.master = Tk()  # Tk() object
        self.master.title('Paragon GIS Analyst - ver. 1.5')  # window name
        icons = os.getcwd() + os.sep + "icons" + os.sep  # path to icons
        icon = icons + "maps.ico"
        self.master.iconbitmap(icon)  # window icon
        self.master.resizable(width=FALSE, height=FALSE)
        self.master.geometry("520x120")
        self.file_name = ""  # the name of the EXEL file
        self.last_dir = "C:/"

        # user theme
        self.style = ttk.Style()
        self.style.theme_create( "vladimir", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0] , 
                                        "background": "#404040"}},
            "TNotebook.Tab": {
                "configure": {"padding": [1, 1], "background": "#404040" ,
                              "foreground": '#ff8c00'},
                "map": {"background": [("selected", '#ff8c00')],
                        "foreground": [("selected", '#404040')],}}})

        # to use in frame, message, labels and buttons ------------------------
        self.message = StringVar()
        self.message.set("\nSelecciona um ficheiro EXCEL")
        bg = "gray25"
        bg1 = "dark orange"
        fc = "white smoke"
        font = ("Helvetica", "8", "bold")
        text0 = " ----- "
        text1 = " Boris & Vladimir Software "
        text = text0 + text1 + text0
        self.cor_icon = StringVar()
        self.scale_icon = DoubleVar()
        self.cgi_time = IntVar()

        # Menu ----------------------------------------------------------------
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        filemenu = Menu(self.menu)
        self.menu.add_cascade(label="Ficheiro", menu=filemenu)
        filemenu.add_command(label="Abrir...", command=self.__callback)
        filemenu.add_command(label="Gravar", command=self.__callback_2)
        filemenu.add_command(label="Sair", command=self.__callback_3)
        
        bdmenu = Menu(self.menu)
        self.menu.add_cascade(label="BD Operadoras Móveis", menu=bdmenu)
        bdmenu.add_command(label="Actualizar", command=None)  # FALTA COMANDO ###############################################################################
        #bdmenu.add_command(label="Consultar", command=lambda: (DbGui(self.master)))  # FALTA COMANDO ###############################################################################
        bdmenu.add_command(label="Consultar", command=lambda:(self.__queryDB()))
        exportmenu = Menu(bdmenu)
        bdmenu.add_cascade(label="Exportar", menu=exportmenu)
        exportmenu.add_command(label="MEO", command=None)  # FALTA COMANDO ###############################################################################
        exportmenu.add_command(label="NOS", command=None)  # FALTA COMANDO ###############################################################################
        exportmenu.add_command(label="Vodafone", command=None)  # FALTA COMANDO ###############################################################################
        exportmenu.add_command(label="Todos", command=None)  # FALTA COMANDO ###############################################################################

        docsmenu = Menu(self.menu)
        docs = ["docs\manual.pdf", "docs\icons.pdf", "docs\colors.pdf"]
        self.menu.add_cascade(label="Documentação", menu=docsmenu)
        docsmenu.add_command(label="Manual",
                             command=lambda: (self.__open_file(docs[0])))
        docsmenu.add_command(label="Ícones",
                             command=lambda: (self.__open_file(docs[1])))
        docsmenu.add_command(label="Cores",
                             command=lambda: (self.__open_file(docs[2])))

        helpmenu = Menu(self.menu)
        self.menu.add_cascade(label='Ajuda', menu=helpmenu)
        helpmenu.add_command(label="Sobre", command=self.__about)
        helpmenu.add_command(label="Ver erros",
                             command=lambda: (self.__open_file("erros.log")))

        # Frame to suport butons, labels and separators -----------------------
        self.f = Frame(self.master, bg=bg)
        self.f.pack_propagate(0)  # don't shrink
        self.f.pack(side=BOTTOM, padx=0, pady=0)

        # Message, Labels and Entries -----------------------------------------
        self.l1 = Message(
            self.f, bg=bg1, bd=5, fg=bg, textvariable=self.message,
            font=("Helvetica", "13", "bold italic"), width=500).grid(
            row=0, columnspan=6, sticky=EW, padx=5, pady=5)

        self.l6 = Label(
            self.f, text=text, font=("Helvetica", "11", "bold"), bg=bg, fg=bg1
            ).grid(row=3, column=2, columnspan=3, sticky=EW, pady=5)

        # Buttons -------------------------------------------------------------
        self.b0 = Button(
            self.f, text="Abrir EXCEL...", command=self.__callback, width=10,
            bg="forest green", fg=fc, font=font
            ).grid(row=3, column=0, padx=5, sticky=W)
        self.b1 = Button(
            self.f, text="Gravar KMZ", command=self.__callback_2, width=10,
            bg="DodgerBlue4", fg=fc, font=font
            ).grid(row=3, column=1, sticky=W)
        self.b2 = Button(
            self.f, text="Sair", command=self.__callback_3, width=10,
            bg="orange red", fg=fc, font=font
            ).grid(row=3, column=5, sticky=E, padx=5)

        # Mainloop ------------------------------------------------------------
        self.master.mainloop()

    def __callback(self):  # "Abrir ECXEL..." button handler ------------------
        '''
        None -> None

        Opens a new window (filedialog.askopenfilename) to choose the
        EXCEL file that is necessary to make the KMZ file.
        '''
        title = 'Selecciona um ficheiro Excel'
        message = 'Ficheiro EXCEL carregado em memória.\nTransforma-o em KMZ!'
        self.file_name = filedialog.askopenfilename(title=title,
                                                    initialdir=self.last_dir)
        self.last_dir = self.file_name[:self.file_name.rfind('/')]

        if self.file_name[self.file_name.rfind('.') + 1:] != 'xls' and \
                self.file_name[self.file_name.rfind('.') + 1:] != 'xlsx':
            message = self.file_name + ' não é um ficheiro Excel válido!'
        else:
            sleep(1)
            message = 'Ficheiro EXCEL carregado em memória.\n\
            Defina as propriedades do Icon'
            self.message.set(message)
            MyDialog(self.master)
            self.cor_icon.set(icon_color)
            self.scale_icon.set(icon_scale)
            self.cgi_time.set(cgi_time)
            sleep(1)
            message = 'Propriedades do Icon definidas.\nClique em Gravar'
            self.message.set(message)

        self.message.set(message)

    def __callback_2(self):  # "Gravar KMZ" button handler --------------------
        '''
        None -> None

        Calls the function self.__threat()
        '''
        sleep(1)
        message = 'Propriedades do Icon definidas.\nClique em Gravar'
        if self.message.get() != message:
            self.message.set("\nEscolhe um ficheiro EXCEL primeiro")
            self.master.update_idletasks()
        else:
            '''
            self.message.set("\nA processar...")
            '''
            ui = UiControler()  # start interface
            ui.input_file_name = self.file_name
            filter_list = [self.cgi_time.get(), 'mvn', '234', 'n', None]
            ui.filter_list = filter_list
            # choose build an icon or polygon file ----------------------------
            color = self.cor_icon.get()
            scale = self.scale_icon.get()
            kmz = ui.icon_or_polygon(color, scale)
            kmz.file_name = ui.input_file_name
            # make the new Excel file -----------------------------------------
            kmz_file = Conversor()
            if isinstance(kmz, Icon):
                kmz_file.build_icon_file(kmz, filter_list)
            else:
                kmz_file.build_polygon_file(kmz, filter_list)

            self.message.set('\n Ficheiro criado com sucesso')

            self.master.update_idletasks()
            sleep(1)

    def __callback_3(self):  # "Sair" button handler --------------------------
        '''
        None -> None

        Kills the window
        '''
        self.master.destroy()

    def __about(self):
        '''
        None -> None

        Associated with the Help Menu.
        Creates a new window with the "About" information
        '''
        appversion = "1.5"
        appname = "Paragon GIS Analyst"
        copyright = 14 * ' ' + '(c) 2014' + 12 * ' ' + \
            'SDATO - DP - UAF - GNR\n' + 34 * ' '\
            + "No Rights Reserved... ask the code ;)"
        licence = 18 * ' ' + 'http://opensource.org/licenses/GPL-3.0\n'
        contactname = "Nuno Venâncio"
        contactphone = "(00351) 969 564 906"
        contactemail = "venancio.gnr@gmail.com"

        message = "Version: " + appversion + 5 * "\n"
        message0 = "Copyleft: " + copyright + "\n" + "Licença: " + licence
        message1 = contactname + '\n' + contactphone + '\n' + contactemail

        icons = os.getcwd() + os.sep + "icons" + os.sep  # path to icons
        icon = icons + "maps.ico"

        tl = Toplevel(self.master)
        tl.configure(borderwidth=5)
        tl.title("Sobre...")
        tl.iconbitmap(icon)
        tl.resizable(width=FALSE, height=FALSE)
        f1 = Frame(tl, borderwidth=2, relief=SUNKEN, bg="gray25")
        f1.pack(side=TOP, expand=TRUE, fill=BOTH)

        l0 = Label(f1, text=appname, fg="white", bg="gray25",
                   font=('courier', 16, 'bold'))
        l0.grid(row=0, column=0, sticky=W, padx=10, pady=5)
        l1 = Label(f1, text=message, justify=CENTER,
                   fg="white", bg="gray25")
        l1.grid(row=2, column=0, sticky=E, columnspan=3, padx=10, pady=0)
        l2 = Label(f1, text=message0,
                   justify=LEFT, fg="white", bg="gray25")
        l2.grid(row=6, column=0, columnspan=2, sticky=W, padx=10, pady=0)
        l3 = Label(f1, text=message1,
                   justify=CENTER, fg="white", bg="gray25")
        l3.grid(row=7, column=0, columnspan=2, padx=10, pady=0)

        button = Button(tl, text="Ok", command=tl.destroy, width=10)
        button.pack(pady=5)

    def __queryDB(self):
        y = datetime.now().year
        m = datetime.now().month
        d = datetime.now().day
        today = "{:0>2d}".format(d) + '/' + "{:0>2d}".format(m) + '/' + str(y)
        self.query_dict = {'cgi': None,
                           'tec': '234',
                           'date': {'first': '01/01/2013', 'last': today, 
                                    'd_all': False},
                           'pol': {'cp': None, 'loc': None, 'con': None, 
                                   'dis': None},
                           'fis': {'form': None, 'lat': None, 'lon': None, 
                                   'lat2': None, 'lon2': None, 'radius': None},
                           'kmz': {'ico_or_pol': None, 'n': 338, 'scale': 1,
                                   'color': "orange", 'radius': None,
                                   'alt': 35, 'amp': 110}}
        # MAIN WINDOW #########################################################
        # --- Theme configuration ---------------------------------------------
        bg = "gray25"
        fg = "dark orange"
        font = ("Helvetica", "10", "bold")
        self.style.theme_use("vladimir")
        tfs = ttk.Style()
        tfs.configure("TFrame", background="#404040")
        # --- Toplevel --------------------------------------------------------
        tl = Toplevel(self.master)
        #tl.geometry("410x420")
        tl.geometry("530x420")
        tl.configure(borderwidth=5, bg=bg)
        tl.title("Pesquisar Base de Dados")
        icons = os.getcwd() + os.sep + "icons" + os.sep  # path to icons
        icon = icons + "maps.ico"
        tl.iconbitmap(icon)
        tl.resizable(width=FALSE, height=FALSE)
        # --- Base Frame ------------------------------------------------------
        f1 = Frame(tl, bg=bg)
        f1.pack_propagate(0)  # don't shrink
        f1.pack(side=BOTTOM, padx=0, pady=0, expand=TRUE, fill=BOTH)
        # --- Notebook --------------------------------------------------------
        nf = fontTK.Font(root=tl, family='helvetica', size='12', weight='bold')
        s = ttk.Style()
        s.configure('.', font=nf)
        n = ttk.Notebook(f1)
        n.pack(side=TOP)        
        # --- Messages / Log Frame --------------------------------------------
        self.msg = StringVar()
        self.msg.set("Log...\nMensagens do programa...")
        l1 = Message(f1, bg=fg, bd=5, fg=bg, textvariable=self.msg,
            font=("Helvetica", "10", "bold italic"), width=500)
        l1.pack_propagate(0)
        l1.pack(expand=TRUE, fill=BOTH, pady=5)
        # --- Pesquisar Button ------------------------------------------------
        b = Button(f1, text="Pesquisar", command=self.__queryDB_button,
                   width=10, bg="forest green", fg="white smoke", 
                   font=("Helvetica", "8", "bold"))
        b.pack(side=BOTTOM, anchor=E)

        # CGI TAB #############################################################
        # --- Main Frame ------------------------------------------------------
        tab_cgi = ttk.Frame(n)
        n.add(tab_cgi, text='CGI')
        # --- inside Frame ----------------------------------------------------
        f_cgi = ttk.Frame(tab_cgi)
        f_cgi.pack_propagate(0)
        f_cgi.pack(padx=16, pady=33)
        # --- Labels ----------------------------------------------------------
        cgi_l1 = Label(f_cgi, text=None, bg=bg)        
        cgi_l2 = Label(f_cgi, text="Operadora", bg=bg, fg=fg, width=7,
                       justify=RIGHT)        
        cgi_l3 = Label(f_cgi, text="LAC", bg=bg, fg=fg, width=7, justify=RIGHT)        
        cgi_l4 = Label(f_cgi, text="CID", bg=bg, fg=fg, width=7, justify=RIGHT)        
        cgi_l5 = Label(f_cgi, text="CGI", bg=bg, fg=fg)
        cgi_l1.grid(row=0, pady=0)
        cgi_l2.grid(row=1, column=0, padx=5, pady=5)
        cgi_l3.grid(row=1, column=2, pady=5)
        cgi_l4.grid(row=1, column=4, pady=5)
        cgi_l5.grid(row=4, pady=5, padx=5)
        # --- Entries ---------------------------------------------------------
        self.cgi_e1 = Entry(f_cgi, width=2)
        self.cgi_e2 = Entry(f_cgi, width=4)
        self.cgi_e3 = Entry(f_cgi, width=6)
        self.cgi_e4 = Entry(f_cgi, width=25)
        self.cgi_e1.grid(row=1, column=1, pady=5)
        self.cgi_e2.grid(row=1, column=3, pady=5)
        self.cgi_e3.grid(row=1, column=5, pady=5)
        self.cgi_e4.grid(row=4, column=1, columnspan=4, pady=5)
        # --- Separator -------------------------------------------------------
        cgi_s = ttk.Separator(f_cgi, orient=HORIZONTAL)
        cgi_s.grid(row=3, column=0, columnspan=6, sticky=EW, padx=5, pady=5)        

        # TECNOLOGIA TAB ######################################################
        # --- Main Frame ------------------------------------------------------
        tab_tec = ttk.Frame(n)
        n.add(tab_tec, text='Tecnologia')
        # --- inside Frame ----------------------------------------------------
        f_tec = ttk.Frame(tab_tec)
        f_tec.pack_propagate(0)
        f_tec.pack(padx=40, pady=45)
        # --- variables -------------------------------------------------------
        self.tec_2g = IntVar()
        self.tec_3g = IntVar()
        self.tec_4g = IntVar()
        # --- Checkbuttons ----------------------------------------------------
        tec_cb1 = Checkbutton(f_tec, text="2G", onvalue=2,
                              variable=self.tec_2g, bg=bg, fg=fg)
        tec_cb2 = Checkbutton(f_tec, text="3G", onvalue=3,
                              variable=self.tec_3g, bg=bg, fg=fg)
        tec_cb3 = Checkbutton(f_tec, text="4G", onvalue=4,
                              variable=self.tec_4g, bg=bg, fg=fg)  
        tec_cb1.grid(row=1, pady=5, padx=5)
        tec_cb2.grid(row=2, pady=5, padx=5)
        tec_cb3.grid(row=3, pady=5, padx=5)
        # --- Labels ----------------------------------------------------------
        tec_l1 = Label(f_tec, text="(GSM)", bg=bg, fg=fg)        
        tec_l2 = Label(f_tec, text="(WCDMA, HSPA, UMTS)", bg=bg, fg=fg)        
        tec_l3 = Label(f_tec, text="(WIMAX, LTE)", bg=bg, fg=fg)
        tec_l1.grid(row=1, column=1, pady=5, sticky=W)
        tec_l2.grid(row=2, column=1, pady=5)
        tec_l3.grid(row=3, column=1, pady=5, sticky=W)

        # DATA TAB ############################################################
        # --- Main Frame ------------------------------------------------------
        tab_dat = ttk.Frame(n)
        n.add(tab_dat, text='Data')
        # --- inside Frame ----------------------------------------------------
        f_dat = ttk.Frame(tab_dat)
        f_dat.pack_propagate(0)
        f_dat.pack(padx=0, pady=55)
        # --- variables -------------------------------------------------------
        days = ["{:0>2d}".format(n + 1) for n in range(31)]
        months = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET',
                'OUT', 'NOV', 'DEC']
        years = [n + 1 for n in range(2012, datetime.now().year)]
        self.date_all = IntVar()
        # --- Labels ----------------------------------------------------------
        dat_l1 = Label(f_dat, text="De", bg=bg, fg=fg)        
        dat_l2 = Label(f_dat, text="/", bg=bg, fg=fg)        
        dat_l3 = Label(f_dat, text="/", bg=bg, fg=fg)        
        dat_l4 = Label(f_dat, text="a", bg=bg, fg=fg)        
        dat_l5 = Label(f_dat, text="/", bg=bg, fg=fg)        
        dat_l6 = Label(f_dat, text="/", bg=bg, fg=fg)        
        dat_l7 = Label(f_dat, text=" ", bg=bg, fg=fg)
        dat_l1.grid(row=1, column=0, pady=5, padx=5)
        dat_l2.grid(row=1, column=2, pady=5, padx=0)
        dat_l3.grid(row=1, column=4, pady=5, padx=0)
        dat_l4.grid(row=1, column=6, pady=5, padx=2)
        dat_l5.grid(row=1, column=8, pady=5, padx=0)
        dat_l6.grid(row=1, column=10, pady=5, padx=0)
        dat_l7.grid(row=1, column=12, pady=5, padx=0)
        # --- Comboboxes ------------------------------------------------------
        self.dat_cb1 = ttk.Combobox(f_dat, width=3, textvariable=None,
                                    values=days)        
        self.dat_cb2 = ttk.Combobox(f_dat, width=5, textvariable=None,
                                    values=months)        
        self.dat_cb3 = ttk.Combobox(f_dat, width=4, textvariable=None,
                                    values=years)                
        self.dat_cb4 = ttk.Combobox(f_dat, width=3, textvariable=None,
                                    values=days)               
        self.dat_cb5 = ttk.Combobox(f_dat, width=5, textvariable=None,
                                    values=months)                
        self.dat_cb6 = ttk.Combobox(f_dat, width=4, textvariable=None,
                                    values=years)
        self.dat_cb1.grid(row=1, column=1, padx=0)
        self.dat_cb2.grid(row=1, column=3, padx=0)
        self.dat_cb3.grid(row=1, column=5, padx=0)
        self.dat_cb4.grid(row=1, column=7, padx=0)
        self.dat_cb5.grid(row=1, column=9, padx=0)
        self.dat_cb6.grid(row=1, column=11, padx=0)
        # --- Separator -------------------------------------------------------
        dat_s = ttk.Separator(f_dat, orient=HORIZONTAL)
        dat_s.grid(row=2, columnspan=13, sticky=EW, pady=5, padx=5)
        # --- Radiobuttons ----------------------------------------------------
        dat_rb1 = Radiobutton(f_dat, text='Todas', variable=self.date_all, 
                              value=1, bg=bg, fg=fg)
        dat_rb1.grid(row=3, column=0, columnspan=6, pady=5, padx=5)
        dat_rb2 = Radiobutton(f_dat, text='Mais Recentes', 
                              variable=self.date_all, value=0, bg=bg, fg=fg)        
        dat_rb2.grid(row=3, column=6, columnspan=5, pady=5, padx=5)
        dat_rb1.deselect()
        dat_rb2.select()

        # LOCALIZAÇÃO ADMINISTRATIVA TAB ######################################
        # --- Main Frame ------------------------------------------------------
        tab_pol = ttk.Frame(n)
        n.add(tab_pol, text='Localização Administrativa')
        # --- inside Frame ----------------------------------------------------
        f_pol = ttk.Frame(tab_pol)
        f_pol.pack_propagate(0)
        f_pol.pack(padx=0, pady=40)
        # --- Labels ----------------------------------------------------------
        pol_l1 = Label(f_pol, text="Cod Postal", bg=bg, fg=fg)        
        pol_l2 = Label(f_pol, text="Localidade", bg=bg, fg=fg)        
        pol_l3 = Label(f_pol, text="Concelho", bg=bg, fg=fg)        
        pol_l4 = Label(f_pol, text="Distrito", bg=bg, fg=fg)
        pol_l1.grid(row=2, column=0, padx=5, pady=5)
        pol_l2.grid(row=3, column=0, padx=5, pady=5)
        pol_l3.grid(row=4, column=0, padx=5, pady=5)
        pol_l4.grid(row=5, column=0, padx=5, pady=5)
        # --- Entries ---------------------------------------------------------
        self.pol_e1 = Entry(f_pol)        
        self.pol_e2 = Entry(f_pol)        
        self.pol_e3 = Entry(f_pol)        
        self.pol_e4 = Entry(f_pol)
        self.pol_e1.grid(row=2, column=1)
        self.pol_e2.grid(row=3, column=1)
        self.pol_e3.grid(row=4, column=1)
        self.pol_e4.grid(row=5, column=1)

        # LOCALIZAÃÇÃO FÍSICA TAB #############################################
        # --- Main Frame ------------------------------------------------------
        tab_fis = ttk.Frame(n)
        n.add(tab_fis, text='Localização Fí­sica')
        # --- inside Frame ----------------------------------------------------
        f_fis = ttk.Frame(tab_fis)
        f_fis.pack_propagate(0)
        f_fis.pack(padx=5, pady=10)
        # --- Labels ----------------------------------------------------------
        fis_l1 = Label(f_fis, text="Cí­rculo", bg=bg, fg=fg, font=font)        
        fis_l2 = Label(f_fis, text="Latitude", bg=bg, fg=fg)        
        fis_l3 = Label(f_fis, text="Longitude", bg=bg, fg=fg)        
        fis_l4 = Label(f_fis, text="Raio (Kms)", bg=bg, fg=fg)        
        fis_l5 = Label(f_fis, text="Quadrado", bg=bg, fg=fg, font=font)        
        fis_l6 = Label(f_fis, text="Latitude 1", bg=bg, fg=fg)        
        fis_l7 = Label(f_fis, text="Longitude 1", bg=bg, fg=fg)        
        fis_l8 = Label(f_fis, text="Latitude 2", bg=bg, fg=fg)        
        fis_l9 = Label(f_fis, text="Longitude 2", bg=bg, fg=fg)
        fis_l1.grid(row=1, column=0, columnspan=4, padx=5, pady=0)
        fis_l2.grid(row=2, column=0, padx=5, pady=5)
        fis_l3.grid(row=2, column=2, padx=5, pady=5)
        fis_l4.grid(row=3, column=0, padx=5, pady=5)
        fis_l5.grid(row=5, column=0, columnspan=4, padx=5, pady=0)
        fis_l6.grid(row=6, column=0, padx=5, pady=5)
        fis_l7.grid(row=6, column=2, padx=5, pady=5)
        fis_l8.grid(row=7, column=0, padx=5, pady=5)
        fis_l9.grid(row=7, column=2, padx=5, pady=5)
        # --- Entries ---------------------------------------------------------
        self.fis_e1 = Entry(f_fis, width=18)        
        self.fis_e2 = Entry(f_fis, width=18)        
        self.fis_e3 = Entry(f_fis, width=18)        
        self.fis_e4 = Entry(f_fis, width=18)        
        self.fis_e5 = Entry(f_fis, width=18)        
        self.fis_e6 = Entry(f_fis, width=18)        
        self.fis_e7 = Entry(f_fis, width=18)
        self.fis_e1.grid(row=2, column=1)
        self.fis_e2.grid(row=2, column=3)
        self.fis_e3.grid(row=3, column=1)
        self.fis_e4.grid(row=6, column=1)
        self.fis_e5.grid(row=6, column=3)
        self.fis_e6.grid(row=7, column=1)
        self.fis_e7.grid(row=7, column=3)
        # --- Separator -------------------------------------------------------
        fis_s = ttk.Separator(f_fis, orient=HORIZONTAL)
        fis_s.grid(row=4, columnspan=4, sticky=EW, pady=5, padx=5)

        # EXCEL KMZ READY TAB #################################################
        # --- Main Frame ------------------------------------------------------
        tab_kmz = ttk.Frame(n)
        n.add(tab_kmz, text='Excel KMZ')
        # --- inside Frame ----------------------------------------------------
        f_kmz = ttk.Frame(tab_kmz)
        f_kmz.pack_propagate(0)
        f_kmz.pack(padx=25, pady=25)
        # --- Labels ----------------------------------------------------------
        kmz_l1 = Label(f_kmz, text="Icons", bg=bg, fg=fg, font=font)
        kmz_l2 = Label(f_kmz, text="Nº Icon", bg=bg, fg=fg)
        kmz_l3 = Label(f_kmz, text="Escala", bg=bg, fg=fg)
        kmz_l4 = Label(f_kmz, text="Cor", bg=bg, fg=fg)
        kmz_l5 = Label(f_kmz, text=" ", bg=bg, fg=fg)
        kmz_l6 = Label(f_kmz, text="Polígonos", bg=bg, fg=fg, font=font)
        kmz_l7 = Label(f_kmz, text="Raio", bg=bg, fg=fg)
        kmz_l8 = Label(f_kmz, text="Altitude", bg=bg, fg=fg)
        kmz_l9 = Label(f_kmz, text="Cor", bg=bg, fg=fg)
        kmz_l1.grid(row=1, column=0, columnspan=6, padx=5, pady=5)        
        kmz_l2.grid(row=2, column=0, padx=5, pady=5)        
        kmz_l3.grid(row=2, column=2, padx=5, pady=5)        
        kmz_l4.grid(row=2, column=4, padx=5, pady=5)        
        kmz_l5.grid(row=2, column=6, padx=5, pady=5)        
        kmz_l6.grid(row=5, column=0, columnspan=6, padx=5, pady=5)        
        kmz_l7.grid(row=6, column=0, padx=5, pady=5)        
        kmz_l8.grid(row=6, column=2, padx=5, pady=5)        
        kmz_l9.grid(row=6, column=4, padx=5, pady=5)
        # --- Entries ---------------------------------------------------------
        self.kmz_e1 = Entry(f_kmz, width=3)
        self.kmz_e2 = Entry(f_kmz, width=3)
        self.kmz_e3 = Entry(f_kmz)
        self.kmz_e4 = Entry(f_kmz, width=3)
        self.kmz_e5 = Entry(f_kmz, width=3)
        self.kmz_e6 = Entry(f_kmz)
        self.kmz_e1.grid(row=2, column=1)        
        self.kmz_e2.grid(row=2, column=3)        
        self.kmz_e3.grid(row=2, column=5)        
        self.kmz_e4.grid(row=6, column=1)        
        self.kmz_e5.grid(row=6, column=3)        
        self.kmz_e6.grid(row=6, column=5)
        # --- Separator -------------------------------------------------------
        kmz_s = ttk.Separator(f_kmz, orient=HORIZONTAL)
        kmz_s.grid(row=4, columnspan=7, sticky=EW, pady=5, padx=5)

    def __queryDB_button(self):
        all_querys = ''  ######################################################
        msg = 'Pesquisas selecionadas:\n'
        # CGI TAB QUERY -------------------------------------------------------
        cgi_op = self.cgi_e1.get()
        cgi_lac = self.cgi_e2.get()
        cgi_cid = self.cgi_e3.get()
        cgi_cgi = self.cgi_e4.get()
        if cgi_cgi and (cgi_op or cgi_lac or cgi_cid):
            message = "Não é possí­vel pesquisar por CGI em partes e CGI completo ao mesmo tempo."
            messagebox.showerror(title="Erro CGI", message=message)  # falta parent="" e activar a tab CGI
            return          
        else:
            if cgi_op and not cgi_lac and not cgi_cid:
                self.query_dict['cgi'] = "268-" + cgi_op + "%"
                msg += "  - CGI por Operadora\n"
            elif cgi_op and cgi_lac and not cgi_cid:
                self.query_dict['cgi'] = "268-" + cgi_op + "-" + cgi_lac + "%"
                msg += "  - CGI por Operadora e LAC\n"
            elif cgi_op and cgi_cid and not cgi_lac:
                self.query_dict['cgi'] = "268-" + cgi_op + "-" + "%" + "-" + cgi_cid
                msg += "  - CGI por Operadora e CID\n"
            elif cgi_op and cgi_cid and cgi_lac:
                self.query_dict['cgi'] = "268-" + cgi_op + "-" + cgi_lac + "-" + cgi_cid
                msg += "  - CGI por Operadora, LAC e CID\n"
            elif cgi_cid and not cgi_lac and not cgi_op:
                self.query_dict['cgi'] = "%" + "-" + cgi_cid
                msg += "  - CGI por CID\n"
            elif cgi_cid and cgi_lac and not cgi_op:
                self.query_dict['cgi'] = "%" + "-" + cgi_lac + "-" + cgi_cid
                msg += "  - CGI por LAC e CID\n"
            elif cgi_lac and not cgi_op and not cgi_cid:
                self.query_dict['cgi'] = "268-" + "%" + "-" + cgi_lac + "-" + "%"
                msg += "  - CGI por LAC\n"
            elif cgi_cgi:
                self.query_dict['cgi'] = cgi_cgi
                msg += "  - CGI por CGI completo\n"
        # TECNOLOGIA TAB QUERY ------------------------------------------------
        tecs = ''
        tec_lst = [self.tec_2g.get(), self.tec_3g.get(), self.tec_4g.get()]
        for i in tec_lst:
            if i > 0:
                tecs += str(i)
        if tecs:
            self.query_dict['tec'] = tecs
            msg += "  - Por Geração Tecnológica\n"
        # DATA TAB QUERY ------------------------------------------------------
        month_dict = {'JAN': '01', 'FEV': '02', 'MAR': '03', 'ABR': '04',
                      'MAI': '05', 'JUN': '06', 'JUL': '07', 'AGO': '08',
                      'SET': '09', 'OUT': '10', 'NOV': '11', 'DEC': '12'}
        day_1 = self.dat_cb1.get()
        try:
            month_1 = month_dict[self.dat_cb2.get()]
        except:
            month_1 = None
        year_1 = self.dat_cb3.get()
        day_2 = self.dat_cb4.get()
        try:
            month_2 = month_dict[self.dat_cb5.get()]
        except:
            month_2 = None
        year_2 = self.dat_cb6.get()
        try:
            from_date = day_1 + "/" + month_1 + "/" + year_1
        except:
            from_date = "None"
        try:
            to_date = day_2 + "/" + month_2 + "/" + year_2
        except:
            to_date = "None"
        if (not day_1 and not month_1 and not year_1) and \
           (not day_2 and not month_2 and not year_2):
            pass # Assim está tudo bem, não faz pesquisa por data
        elif (day_1 and month_1 and year_1) and \
             (not day_2 and not month_2 and not year_2):
            pass # Preenche são a data de início
        elif (not day_1 and not month_1 and not year_1) and \
             (day_2 and month_2 and year_2):
            pass # Preenche só a data de fim
        elif (not day_1 or not month_1 or not year_1) and \
            ((not day_2 and not month_2 and not year_2) or \
            (day_2 and month_2 and year_2)):
            message = "A primeira data está incompleta"
            messagebox.showerror(title="Erro Pesquisa por Data", message=message)  # falta parent="" e activar a tab Data
            return
        elif (not day_2 or not month_2 or not year_2):
            message = "A segunda data está incompleta"
            messagebox.showerror(title="Erro Pesquisa por Data", message=message)  # falta parent="" e activar a tab Data
            return
        else:
            if from_date:
                self.query_dict['date']['first'] = from_date
            if to_date:
                self.query_dict['date']['last'] = to_date            
            msg += "  - Por Espaço Temporal\n"
        if self.date_all.get():
                self.query_dict['date']['d_all'] = True
                msg += "  - Incluir todas as actualizações\n"

        # LOCALIZAÇÃO ADMINISTRATIVA TAB QUERY --------------------------------
        pol_cp = self.pol_e1.get()
        pol_loc = self.pol_e2.get()
        pol_con = self.pol_e3.get()
        pol_dis = self.pol_e4.get()
        if pol_cp and not pol_loc and not pol_con and not pol_dis:
            self.query_dict['pol']['cp'] = pol_cp
            msg += "  - Loc. Administrativa por Cód Postal\n"
        elif pol_cp and pol_loc and not pol_con and not pol_dis:
            self.query_dict['pol']['cp'] = pol_cp
            self.query_dict['pol']['loc'] = pol_loc
            msg += "  - Loc. Administrativa por Cód Postal e Localidade\n"
        elif pol_cp and not pol_loc and pol_con and not pol_dis:
            self.query_dict['pol']['cp'] = pol_cp
            self.query_dict['pol']['con'] = pol_con
            msg += "  - Loc. Administrativa por Cód Postal e Concelho\n"
        elif pol_cp and not pol_loc and not pol_con and pol_dis:
            self.query_dict['pol']['cp'] = pol_cp
            self.query_dict['pol']['dis'] = pol_dis
            msg += "  - Loc. Administrativa por Cód Postal e Distrito\n"
        elif pol_cp and pol_loc and pol_con and not pol_dis:
            self.query_dict['pol']['cp'] = pol_cp
            self.query_dict['pol']['loc'] = pol_loc
            self.query_dict['pol']['con'] = pol_con
            msg += "  - Loc. Administrativa por Cód Postal, Localidade e Concelho\n"
        elif pol_cp and pol_loc and not pol_con and pol_dis:
            self.query_dict['pol']['cp'] = pol_cp
            self.query_dict['pol']['loc'] = pol_loc
            self.query_dict['pol']['dis'] = pol_dis
            msg += "  - Loc. Administrativa por Cód Postal, Localidade e Distrito\n"
        elif pol_cp and not pol_loc and pol_con and pol_dis:
            self.query_dict['pol']['cp'] = pol_cp
            self.query_dict['pol']['con'] = pol_con
            self.query_dict['pol']['dis'] = pol_dis
            msg += "  - Loc. Administrativa por Cód. Postal, Concelho e Distrito\n"
        elif pol_cp and pol_loc and pol_con and pol_dis:
            self.query_dict['pol']['cp'] = pol_cp
            self.query_dict['pol']['loc'] = pol_loc
            self.query_dict['pol']['con'] = pol_con
            self.query_dict['pol']['dis'] = pol_dis
            msg += "  - Loc. Administrativa por Cód. Postal, Localidade, Concelho e Distrito\n"
        elif pol_loc and not pol_cp and not pol_con and not pol_dis:
            self.query_dict['pol']['loc'] = pol_loc
            msg += "  - Loc. Administrativa por Localidade\n"
        elif pol_loc and pol_con and not pol_dis and not pol_cp:
            self.query_dict['pol']['loc'] = pol_loc
            self.query_dict['pol']['con'] = pol_con
            msg += "  - Loc. Administrativa por Localidade e Concelho\n"
        elif pol_loc and pol_dis and not pol_cp and not pol_con:
            self.query_dict['pol']['loc'] = pol_loc
            self.query_dict['pol']['dis'] = pol_dis
            msg += "  - Loc. Administrativa por Localidade e Distrito\n"
        elif pol_loc and pol_con and pol_dis and not pol_cp:
            self.query_dict['pol']['loc'] = pol_loc
            self.query_dict['pol']['con'] = pol_con
            self.query_dict['pol']['dis'] = pol_dis
            msg += "  - Loc. Administrativa por Localidade, Concelho e Distrito\n"
        elif pol_con and not pol_cp and not pol_loc and not pol_dis:
            self.query_dict['pol']['con'] = pol_con
            msg += "  - Loc. Administrativa por Concelho\n"
        elif pol_con and pol_dis and not pol_cp and not pol_loc:
            self.query_dict['pol']['con'] = pol_con
            self.query_dict['pol']['dis'] = pol_dis
            msg += "  - Loc. Administrativa por Concelho e Distrito\n"
        if pol_dis and not pol_cp and not pol_loc and not pol_con:
            self.query_dict['pol']['dis'] = pol_dis
            msg += "  - Loc. Administrativa por Distrito\n"

        # LOCALIZAÇÃO FÍSICA TAB QUERY ----------------------------------------
        fis_lat = self.fis_e1.get()
        fis_lon = self.fis_e2.get()
        fis_rad = self.fis_e3.get()
        fis_lat1 = self.fis_e4.get()
        fis_lon1 = self.fis_e5.get()
        fis_lat2 = self.fis_e6.get()
        fis_lon2 = self.fis_e7.get()
        if (fis_lat or fis_lon or fis_rad) and \
           (fis_lat1 or fis_lon1 or fis_lat2 or fis_lon2):
            message = "Não é possí­vel desenhar círculo e quadrado ao mesmo tempo."
            messagebox.showerror(title="Erro Pesquisa por Localização Física", message=message)  # falta parent="" e activar a tab Loc FÃ­sica
            return
        else:
            if fis_lat and fis_lon and fis_rad:
                self.query_dict['fis']['form'] = 'circle'
                self.query_dict['fis']['lat'] = fis_lat
                self.query_dict['fis']['lon'] = fis_lon
                self.query_dict['fis']['radius'] = fis_rad
                msg += "  - Loc. Física por cí­rculo\n"
            elif fis_lat1 and fis_lon1 and fis_lat2 and fis_lon2:
                self.query_dict['fis']['form'] = 'square'
                self.query_dict['fis']['lat'] = fis_lat1
                self.query_dict['fis']['lon'] = fis_lon1
                self.query_dict['fis']['lat2'] = fis_lat2
                self.query_dict['fis']['lon2'] = fis_lon2
                msg += "  - Loc. Fí­sica por quadrado\n"
        # EXCEL KMZ READY TAB -------------------------------------------------
        kmz_i_n = self.kmz_e1.get()
        kmz_i_sca = self.kmz_e2.get()
        kmz_i_col = self.kmz_e3.get()
        kmz_p_rad = self.kmz_e4.get()
        kmz_p_alt = self.kmz_e5.get()
        kmz_p_col = self.kmz_e6.get()
        if (kmz_i_n or kmz_i_sca or kmz_i_col) and \
           (kmz_p_rad or kmz_p_alt or kmz_p_col):
            message = "Só é possí­vel criar Excel ou de Icones ou de Polí­gonos."
            messagebox.showerror(title="Erro no Excel KMZ", message=message)  # falta parent="" e activar a tab KMZ
            return
        else:
            if kmz_i_n or kmz_i_sca or kmz_i_col:
                self.query_dict['kmz']['ico_or_pol'] = 'icon'
                if kmz_i_n:
                    self.query_dict['kmz']['n'] = kmz_i_n
                if kmz_i_sca:
                    self.query_dict['kmz']['scale'] = kmz_i_sca
                if kmz_i_col:
                    self.query_dict['kmz']['color'] = kmz_i_col
                msg += "  - Excel para KMZ de Icones\n"
            elif kmz_p_rad:
                self.query_dict['kmz']['ico_or_pol'] = 'polygon'
                if kmz_p_alt:
                    self.query_dict['kmz']['alt'] = kmz_p_alt
                if kmz_p_col:
                    self.query_dict['kmz']['color'] = kmz_p_col
                msg += "  - Excel para KMZ de Polígonos\n"


        print(msg)
        self.msg.set(msg)
        print()
        print(self.query_dict)


class MyDialog(simpledialog.Dialog):

    def body(self, master):
        # --- Labels ----------------------------------------------------------
        l1 = Label(master, text='ICON')        
        l2 = Label(master, text="Cor:")        
        l3 = Label(master, text="Escala:")        
        l4 = Label(master, text='Retirar CGIs repetidas')        
        l5 = Label(master, text='Tempo (min)')
        l1.grid(row=0, columnspan=2)
        l2.grid(row=1)
        l3.grid(row=2)
        l4.grid(row=3, columnspan=2)
        l5.grid(row=4)
        # --- Entries ---------------------------------------------------------
        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=4, column=1)
        #return self.e1 # initial focus

    def apply(self):
        global icon_color, icon_scale, cgi_time
        icon_color = self.e1.get()
        icon_scale = float(self.e2.get())
        cgi_time = int(self.e3.get())

if __name__ == '__main__':
    go = window()