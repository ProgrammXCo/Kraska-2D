import tkinter as tk
from tkinter import colorchooser, ttk, font
from idlelib.tooltip import Hovertip
from PIL import Image, ImageTk
import sys
import datetime
import time
import pickle
import os
from variables import *

class sizeToplevel(tk.Toplevel):
    var = None
    def __init__(self, parent, master):
        self.master = master
        self.parent = parent
        self.name_app = self.parent.name_app

        super().__init__(self.master)
        self.transient(self.master)
        self.focus_set()
        self.grab_set()
        self.master.attributes("-disabled", 1)
        if self.parent.draw_toolbar_toplevel:
            self.parent.draw_toolbar_toplevel.attributes("-disabled", 1)
        if self.parent.colorbar_toplevel:
            self.parent.colorbar_toplevel.attributes("-disabled", 1)
        if self.parent.active_toplevel_text:
            self.parent.active_toplevel_text.attributes("-disabled", 1)
        self.title('{}: изменение размера холста'.format(self.name_app))
        self.x = int(self.master.winfo_x() + (self.master.winfo_width() / 2 - 400 / 2))
        self.y = int(self.master.winfo_y() + (self.master.winfo_height() / 2 - 240 / 2))
        self.geometry('400x240+{}+{}'.format(self.x, self.y + 10))
        self.resizable(0, 0)
        self.color_widget = self.parent.bg_btn
        self['bg'] = self.color_widget

        self.width = 0
        self.height = 0

        self.protocol("WM_DELETE_WINDOW", self.exitWindow)

        self.frame_size = tk.Frame(self, bg=self.color_widget)
        self.frame_size.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.label_frame_old = tk.LabelFrame(self.frame_size, text="Текущий размер", bg=self.color_widget)
        self.label_frame_old.pack(side=tk.TOP, fill='x', padx=10, pady=10)

        self.frame_width_old = tk.Frame(self.label_frame_old)
        self.frame_width_old.pack(side=tk.TOP, pady=5)

        self.label_width_old = tk.Label(self.frame_width_old, text="Ширина: {} пкс".format(self.parent.paper_width),
                                        bg=self.color_widget)
        self.label_width_old.pack(side=tk.LEFT)

        self.frame_height_old = tk.Frame(self.label_frame_old)
        self.frame_height_old.pack(side=tk.TOP, pady=5)

        self.label_height_old = tk.Label(self.frame_height_old, text="Высота: {} пкс".format(self.parent.paper_height),
                                         bg=self.color_widget)
        self.label_height_old.pack(side=tk.LEFT)

        self.label_frame_new = tk.LabelFrame(self.frame_size, text="Новый размер", bg=self.color_widget)
        self.label_frame_new.pack(side=tk.TOP, fill='x', padx=10, pady=(0, 10))

        self.frame_width_new = tk.Frame(self.label_frame_new)
        self.frame_width_new.pack(side=tk.TOP, anchor="e", pady=5, padx=45)

        self.label_width_new = tk.Label(self.frame_width_new, text="Ширина: ", bg=self.color_widget)
        self.label_width_new.pack(side=tk.LEFT)

        self.entry_width = tk.Entry(self.frame_width_new, width=10, validate = "key")
        self.entry_width.insert(0, self.parent.paper_width)
        self.entry_width['validatecommand'] = (self.entry_width.register(self.validateWidth), '%P')
        self.entry_width.pack(side=tk.LEFT)

        self.label_pix_width = tk.Label(self.frame_width_new, text='пкс', bg=self.color_widget)
        self.label_pix_width.pack(side=tk.LEFT)

        self.frame_height_new = tk.Frame(self.label_frame_new)
        self.frame_height_new.pack(side=tk.TOP, anchor="e", pady=5, padx=45)

        self.label_height_new = tk.Label(self.frame_height_new, text="Высота: ", bg=self.color_widget)
        self.label_height_new.pack(side=tk.LEFT)

        self.entry_height = tk.Entry(self.frame_height_new, width=10, validate = "key")
        self.entry_height.insert(0, self.parent.paper_height)
        self.entry_height['validatecommand'] = (self.entry_height.register(self.validateHeight), '%P')
        self.entry_height.pack(side=tk.LEFT)

        self.label_pix_height = tk.Label(self.frame_height_new, text='пкс', bg=self.color_widget)
        self.label_pix_height.pack(side=tk.LEFT)

        if sizeToplevel.var == None:
            sizeToplevel.var = tk.BooleanVar()
            sizeToplevel.var.set(False)

        self.checkbox_fill = tk.Checkbutton(self.frame_size, text="Растянуть/сжать изображение",
                            variable=sizeToplevel.var, onvalue=True, offvalue=False, bg=self.color_widget,
                            activebackground=self.color_widget)
        self.checkbox_fill.pack(side=tk.TOP, anchor='w', padx=10)

        self.button_box=tk.Frame(self, bg=self.color_widget)
        self.button_box.pack(side=tk.RIGHT, fill='y', pady=(7, 0))

        self.button_ok=ttk.Button(self.button_box, default="active", text='OK', width=15,
                                  command=self.changeSize, state="disabled")
        self.button_ok.pack(side=tk.TOP, padx=10, pady=10, fill='x')

        self.button_cancel = ttk.Button(self.button_box, default="active", text='Отмена', width=15,
                                        command=self.exitWindow)
        self.button_cancel.pack(side=tk.TOP, padx=10, fill='x')

    def validateWidth(self, value):
        text_value = str(value)
        if text_value == '':
            self.button_ok.config(state="disabled")
            return True
        elif len(text_value) > 4:
            return False
        elif not text_value.isdigit():
            return False
        elif int(text_value) > 2500:
            return False
        if int(text_value) >= 10 and self.entry_height.get()!='' and int(self.entry_height.get())>=10 and (
            int(text_value) != self.parent.paper_width or int(self.entry_height.get()) != self.parent.paper_height
        ):
            self.button_ok.config(state="normal")
        else:
            self.button_ok.config(state="disabled")
        return True

    def validateHeight(self, value):
        text_value = str(value)
        if text_value == '':
            self.button_ok.config(state="disabled")
            return True
        elif len(text_value) > 4:
            return False
        elif not text_value.isdigit():
            return False
        elif int(text_value) > 2500:
            return False
        if int(text_value) >= 10 and  self.entry_width.get()!='' and int(self.entry_width.get()) >= 10 and (
                int(text_value) != self.parent.paper_height or int(self.entry_width.get()) != self.parent.paper_width
        ):
            self.button_ok.config(state="normal")
        else:
            self.button_ok.config(state="disabled")
        return True

    def changeSize(self):
        width_old = self.parent.paper_width
        height_old = self.parent.paper_height
        self.parent.paper_width = int(self.entry_width.get())
        self.parent.paper_height = int(self.entry_height.get())

        if sizeToplevel.var.get():
            self.parent.canvas.delete("all")
            if self.parent.active_toplevel_text:
                self.parent.active_toplevel_text.exitWindow()
            self.parent.scrollregion = (0, 0, self.parent.paper_width, self.parent.paper_height)
            self.parent.canvas.config(width=self.parent.paper_width, height=self.parent.paper_height,
                               scrollregion=self.parent.scrollregion)
            self.parent.image = self.parent.image.resize((self.parent.paper_width, self.parent.paper_height),
                                                         Image.ANTIALIAS)
            self.parent.canvas.image = ImageTk.PhotoImage(self.parent.image)
            self.parent.canvas.create_image(0, 0, image=self.parent.canvas.image, anchor="nw")
            self.parent.master.title("*{} - {}".format(self.parent.file_name, self.parent.name_app))
            self.parent.changed = True
        else:
            self.parent.canvas.delete("all")
            if self.parent.active_toplevel_text:
                self.parent.active_toplevel_text.exitWindow()
            self.parent.scrollregion = (0, 0, self.parent.paper_width, self.parent.paper_height)
            self.parent.canvas.config(width=self.parent.paper_width, height=self.parent.paper_height,
                                      scrollregion=self.parent.scrollregion)
            self.image1 = Image.new("RGB", (self.parent.paper_width, self.parent.paper_height),
                                    self.parent.bg_color)
            if self.parent.paper_width > width_old:
                crop_width=width_old
            else:
                crop_width = self.parent.paper_width
            if self.parent.paper_height > height_old:
                crop_height=height_old
            else:
                crop_height = self.parent.paper_height
            self.image2 = self.parent.image.crop((0, 0, crop_width, crop_height))
            Image.Image.paste(self.image1, self.image2)
            self.parent.image = self.image1
            self.parent.canvas.image = ImageTk.PhotoImage(self.parent.image)
            self.parent.canvas.create_image(0, 0, image=self.parent.canvas.image, anchor="nw")
            self.parent.master.title("*{} - {}".format(self.parent.file_name, self.parent.name_app))
            self.parent.changed = True
        self.exitWindow()

    def exitWindow(self):
        self.master.attributes("-disabled", 0)
        if self.parent.draw_toolbar_toplevel:
            self.parent.draw_toolbar_toplevel.attributes("-disabled", 0)
        if self.parent.colorbar_toplevel:
            self.parent.colorbar_toplevel.attributes("-disabled", 0)
        if self.parent.active_toplevel_text:
            self.parent.active_toplevel_text.attributes("-disabled", 0)
        self.destroy()

class infoToplevel(tk.Toplevel):
    def __init__(self, parent, master):
        self.master=master
        self.parent=parent
        self.name_app = self.parent.name_app
        
        super().__init__(self.master)
        self.transient(self.master)
        self.focus_set()
        self.grab_set()
        self.master.attributes("-disabled", 1)
        if self.parent.draw_toolbar_toplevel:
            self.parent.draw_toolbar_toplevel.attributes("-disabled", 1)
        if self.parent.colorbar_toplevel:
            self.parent.colorbar_toplevel.attributes("-disabled", 1)
        if self.parent.active_toplevel_text:
            self.parent.active_toplevel_text.attributes("-disabled", 1)
        self.title('{}: сведения'.format(self.name_app))
        self.x = int(self.master.winfo_x() + (self.master.winfo_width() / 2 - 450 / 2))
        self.y = int(self.master.winfo_y() + (self.master.winfo_height() / 2 - 400 / 2))
        self.geometry('450x400+{}+{}'.format(self.x, self.y+10))
        self.resizable(0, 0)
        self.color_widget = self.parent.bg_btn
        self['bg']=self.color_widget

        self.protocol("WM_DELETE_WINDOW", self.exitWindow)
        
        self.frame_logo=ttk.Frame(self)
        self.frame_logo.pack(side=tk.TOP, pady=10)
        
        self.img_logo=ImageTk.PhotoImage(Image.open('./pic/img_logo.png').resize((60, 60), Image.ANTIALIAS))
        self.label_logo=ttk.Label(self.frame_logo, image=self.img_logo, text='ProgrammX',
                                  font=('Arial', 32, 'bold'), compound='left')
        self.label_logo.pack(side=tk.LEFT)
        
        ttk.Separator(self, orient='horizontal').pack(side=tk.TOP, padx=10, fill='x')
        
        self.frame_text=ttk.Frame(self)
        self.frame_text.pack(side=tk.TOP, anchor='w')

        self.img_icon=ImageTk.PhotoImage(Image.open('./pic/img_icon.png').resize((34, 34), Image.ANTIALIAS))
        self.label_icon=ttk.Label(self.frame_text, image=self.img_icon)
        self.label_icon.pack(side=tk.LEFT, anchor='n', pady=10, padx=10)

        self.label_text = ttk.Label(self.frame_text, text=text_info)
        self.label_text.pack(side=tk.TOP, anchor='w', pady=10)
        
        self.button_close=ttk.Button(self, default="active", text='OK', command=self.exitWindow)
        self.button_close.pack(side=tk.BOTTOM, anchor='e', padx=10, pady=10)

    def exitWindow(self):
        self.master.attributes("-disabled", 0)
        if self.parent.draw_toolbar_toplevel:
            self.parent.draw_toolbar_toplevel.attributes("-disabled", 0)
        if self.parent.colorbar_toplevel:
            self.parent.colorbar_toplevel.attributes("-disabled", 0)
        if self.parent.active_toplevel_text:
            self.parent.active_toplevel_text.attributes("-disabled", 0)
        self.destroy()

class textToplevel(tk.Toplevel):
    def __init__(self, parent, master):
        self.parent=parent
        self.master=master
        super().__init__(self.master)
        self.transient(self.master)
        self.attributes('-toolwindow', True)
        self.focus_set()
        self.title('{}: текст'.format(self.parent.name_app))
        if not self.parent.draw_toolbar_toplevel:
            self.geometry('278x250+{}+{}'.format(self.master.winfo_x()+85, self.master.winfo_y()+60))
        else:
            self.geometry('278x250+{}+{}'.format(self.master.winfo_x()+10, self.master.winfo_y()+60))
        self.minsize(278, 250)
        self.maxsize(400, 350)
        self.protocol("WM_DELETE_WINDOW", self.exitWindow)

        self.color_widget = self.parent.bg_btn
        self.master.style.configure('TCombobox', selectbackground='SystemHighlight')
        self.master.style.configure('TCombobox', selectforeground='white')
        self['bg']=self.color_widget

        self.menubar=tk.Menu(self)
        self.pravka_menu = tk.Menu(self.menubar, tearoff=0)
        self.pravka_menu.add_command(label="Отменить", accelerator='CTRL+Z', command=self.ControlZ)
        self.pravka_menu.add_command(label="Вернуть", accelerator='CTRL+Y', command=self.ControlY)
        self.pravka_menu.add_separator()
        self.pravka_menu.add_command(label="Вырезать", accelerator='CTRL+X', command=self.ControlX)
        self.pravka_menu.add_command(label="Копировать", accelerator='CTRL+C', command=self.ControlC)
        self.pravka_menu.add_command(label="Вставить", accelerator='CTRL+V', command=self.ControlV)
        self.pravka_menu.add_command(label="Удалить", accelerator='Del', command=self.dellSelect)
        self.pravka_menu.add_separator()
        self.pravka_menu.add_command(label="Выделить всё", accelerator='CTRL+A', command=self.selectAll)
        self.pravka_menu.add_command(label="Дата и время", accelerator='F5', command=self.dateTime)
        self.menubar.add_cascade(label="Правка", menu=self.pravka_menu)

        self.wrap_string_var = tk.BooleanVar()
        self.format_menu = tk.Menu(self.menubar, tearoff=0)
        self.format_menu.add_checkbutton(label="Перенос по словам", variable=self.wrap_string_var, onvalue=True,
                                    offvalue=False, command=self.wrapOnWord)
        self.menubar.add_cascade(label="Формат", menu=self.format_menu)

        self.vid_menu = tk.Menu(self.menubar, tearoff=0)
        self.scale_menu = tk.Menu(self.menubar, tearoff=0)
        self.scale_menu.add_command(label="Увеличить", accelerator='CTRL+плюс(+)', command=self.scalePlus)
        self.scale_menu.add_command(label="Уменьшить", accelerator='CTRL+минус(-)', command=self.scaleMin)
        self.scale_menu.add_command(label="Восстановить масштаб по умолчанию", accelerator='CTRL+0', command=self.scale100)
        self.vid_menu.add_cascade(label="Масштаб", menu=self.scale_menu)
        self.status_bar_string_var = tk.BooleanVar()
        self.vid_menu.add_checkbutton(label="Строка состояния", variable=self.status_bar_string_var, onvalue=True,
                                 offvalue=False, command=self.statusBar)
        self.status_bar_string_var.set(True)
        self.menubar.add_cascade(label="Вид", menu=self.vid_menu)

        self.config(menu=self.menubar)
        
        self.frame_font=ttk.Frame(self)
        self.frame_font.pack(side=tk.TOP, padx=8, pady=5, anchor='nw')

        self.list_font=["Arial", "Times New Roman", "Calibri", "Segoe UI", "Comic Sans Ms"]
        self.list_font.sort()
        self.validateComboboxFont=self.register(self.validateComboboxFont)
        self.combobox_font=ttk.Combobox(self.frame_font, values=self.list_font, width=20, validate='key',
                                                    validatecommand=(self.validateComboboxFont, '%P'))
        self.combobox_font.set(self.parent.type_font)
        self.combobox_font.bind("<<ComboboxSelected>>", lambda event: (setattr(self.parent, 'type_font', event.widget.get()), self.configTextWidget()))
        self.combobox_font.bind('<Control-KeyPress>', self.ctrlKeys)
        self.combobox_font.pack(side=tk.LEFT)

        self.list_size=['8', '9', '10', '11', '12', '14', '16', '18', '20', '22', '24', '26', '28', '36', '48', '72']
        self.validateComboboxSize=self.register(self.validateComboboxSize)
        self.combobox_size=ttk.Combobox(self.frame_font, values=self.list_size, width=8, validate='key',
                                        validatecommand=(self.validateComboboxSize, '%P'))
        self.combobox_size.set(str(self.parent.size_font))
        self.combobox_size.bind("<<ComboboxSelected>>", lambda event: (setattr(self.parent, 'size_font', int(event.widget.get())), self.configTextWidget()))
        self.combobox_size.bind('<Control-KeyPress>', self.ctrlKeys)
        self.combobox_size.bind('<Return>', self.chooseComboboxSize)
        self.combobox_size.pack(side=tk.LEFT, padx=8)

        self.btn_bold=ButtonOutline(parent=self, master=self.frame_font, text='B', font=('Times New Roman', 11, 'bold'),
                                    function=self.boldPress)
        self.btn_bold.pack(side=tk.LEFT)

        self.btn_italic = ButtonOutline(parent=self, master=self.frame_font, text='I', font=('Times New Roman', 11, 'italic'),
                                      function=self.italicPress)
        self.btn_italic.pack(side=tk.LEFT)

        self.frame_frame_state = ttk.Frame(self)
        self.frame_frame_state.pack(side=tk.BOTTOM, fill='x')

        self.frame_buttons = ttk.Frame(self.frame_frame_state)
        self.frame_buttons.pack(side=tk.TOP, fill='both')

        self.button_ok = ttk.Button(self.frame_buttons, text='Ok', default="active", command=self.createText)
        self.button_ok.pack(side=tk.RIGHT, anchor='se', pady=(0, 5), padx=8)

        self.button_exit = ttk.Button(self.frame_buttons, text='Отмена', command=self.deleteText)
        self.button_exit.pack(side=tk.RIGHT, anchor='se', pady=(0, 5))

        self.frame_state = ttk.Frame(self.frame_frame_state)
        self.frame_state.pack(side=tk.BOTTOM, fill='x')

        ttk.Separator(self.frame_state, orient='horizontal').pack(side=tk.TOP, fill='x')

        self.label_scale = ttk.Label(self.frame_state, width=10)
        self.label_scale.pack(side=tk.RIGHT, anchor='se', padx=5)

        ttk.Separator(self.frame_state, orient='vertical').pack(side=tk.RIGHT, anchor='se', fill='y')

        self.label_index = ttk.Label(self.frame_state, width=20)
        self.label_index.pack(side=tk.RIGHT, anchor='se', padx=5)

        ttk.Separator(self.frame_state, orient='vertical').pack(side=tk.RIGHT, anchor='se', fill='y')

        self.frame_text=ttk.Frame(self)
        self.frame_text.pack(side=tk.TOP, padx=8, pady=(0, 5), fill='both', expand=True)

        self.font_style=tk.font.Font(family=self.parent.font_style['family'], size=self.parent.font_style['size'],
                                     weight=self.parent.font_style['weight'], slant=self.parent.font_style['slant'],
                                     underline=self.parent.font_style['underline'], overstrike=self.parent.font_style['overstrike'])
        self.text=tk.Text(self.frame_text, relief='sunken', undo=True, wrap='none',
                          font=self.font_style)
        self.text.grid(row=0, column=0, sticky='news')
        self.scaleSet()

        self.scrollbar_x = ttk.Scrollbar(self.frame_text, orient='horizontal', command=self.text.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky="news")
        self.text.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_y = ttk.Scrollbar(self.frame_text, orient='vertical', command=self.text.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="news")
        self.text.configure(yscrollcommand=self.scrollbar_y.set)

        self.frame_text.columnconfigure(0, weight=1)
        self.frame_text.rowconfigure(0, weight=1)

        self.text.bind('<KeyPress>', self.configTextWidget)
        self.text.bind('<KeyRelease>', self.configTextWidget)
        self.text.bind('<Control-c>', self.ControlC)
        self.text.bind('<Control-v>', self.ControlV)
        self.text.bind('<Control-x>', self.ControlX)
        self.text.bind('<Control-z>', self.ControlZ)
        self.text.bind('<Control-y>', self.ControlY)
        self.text.bind('<Control-a>', self.selectAll)
        self.text.bind('<F5>', self.dateTime)
        self.text.bind('<Control-KeyPress>', self.ctrlKeys)
        self.text.bind("<FocusIn>", self.indexCursor)
        self.text.bind('<ButtonRelease-1>', self.indexCursor)
        self.text.bind('<ButtonRelease-2>', self.indexCursor)
        self.text.bind('<ButtonRelease-3>', self.indexCursor)
        self.text.bind('<ButtonPress-1>', self.indexCursor)
        self.text.bind('<ButtonPress-2>', self.indexCursor)
        self.text.bind('<ButtonPress-3>', self.indexCursor)
        self.text.bind('<Motion>', self.indexCursor)
        self.text.bind('<B1-Motion>', self.indexCursor)
        self.text.bind('<B2-Motion>', self.indexCursor)
        self.text.bind('<B3-Motion>', self.indexCursor)
        self.text.bind("<FocusOut>", self.indexCursor)
        self.text.bind('<Control-plus>', self.scalePlus)
        self.text.bind('<Control-minus>', self.scaleMin)
        self.text.bind('<Control-0>', self.scale100)
        self.text.focus_set()

        if 'italic' in self.parent.outline_font:
            self.btn_italic.config(relief='sunken')
            self.btn_italic.pressed=True
        if 'bold' in self.parent.outline_font:
            self.btn_bold.config(relief='sunken')
            self.btn_bold.pressed = True

    def statusBar(self):
        if self.status_bar_string_var.get():
            self.frame_state.pack(side=tk.BOTTOM, fill='x')
        else:
            self.frame_state.pack_forget()

    def scalePlus(self, event=None):
        if self.parent.scale != 250:
            self.parent.scale += 10
            self.scaleSet()

    def scaleMin(self, event=None):
        if self.parent.scale != 50:
            self.parent.scale -= 10
            self.scaleSet()

    def scale100(self, event=None):
        self.parent.scale = 100
        self.scaleSet()

    def scaleSet(self):
        procent = round(self.parent.font_style['size'] / 100 * self.parent.scale)
        self.font_style.configure(size=procent)
        self.text.configure(font=self.font_style)
        self.label_scale.config(text=str(self.parent.scale) + '%')

    def wrapOnWord(self):
        if self.wrap_string_var.get():
            self.text.configure(wrap='word')
        else:
            self.text.configure(wrap='none')

    def indexCursor(self, event=None):
        if self.focus_get()==self.text:
            index_list = self.text.index(tk.INSERT)
            column = index_list.split('.')[0]
            row = int(index_list.split('.')[1]) + 1
            self.label_index.config(text='Стр {}, стлб {}'.format(column, row))
        else:
            self.label_index.config(text='')

    def ControlC(self, event=None):
        if self.focus_get() == self.text:
            self.text.event_generate('<<Copy>>')
        elif event:
            event.widget.event_generate('<<Copy>>')
        return 'break'

    def ControlV(self, event=None):
        if self.focus_get() == self.text:
            self.text.event_generate('<<Paste>>')
            self.configTextWidget()
        elif event:
            event.widget.event_generate('<<Paste>>')
        return 'break'

    def ControlX(self, event=None):
        if self.focus_get() == self.text:
            self.text.event_generate('<<Cut>>')
            self.configTextWidget()
        elif event:
            event.widget.event_generate('<<Cut>>')
        return 'break'

    def ControlZ(self, event=None):
        if self.focus_get() == self.text:
            self.text.event_generate('<<Undo>>')
            self.configTextWidget()
        elif event:
            event.widget.event_generate('<<Undo>>')
        return 'break'

    def ControlY(self, event=None):
        if self.focus_get() == self.text:
            self.text.event_generate('<<Redo>>')
            self.configTextWidget()
        elif event:
            event.widget.event_generate('<<Redo>>')
        return 'break'

    def dateTime(self, event=None):
        if self.text.tag_ranges(tk.SEL):
            content=self.text.selection_get()
            ranges = self.text.tag_ranges(tk.SEL)
        else:
            content=''
        if  self.focus_get() == self.text and not content:
            date = datetime.datetime.now()
            date_time = date.strftime('%H:%M %d.%m.%Y')
            self.text.insert(tk.INSERT, date_time)
            self.configTextWidget()
        elif self.focus_get() == self.text and content:
            date = datetime.datetime.now()
            date_time = date.strftime('%H:%M %d.%m.%Y')
            self.text.delete(*ranges)
            self.text.insert(ranges[0], date_time)
            self.configTextWidget()
        return 'break'

    def dellSelect(self, event=None):
        try:
            if self.focus_get() == self.text:
                self.text.delete('sel.first', 'sel.last')
                self.text.see(tk.INSERT)
                self.configTextWidget()
        except:
            pass

    def selectAll(self, event=None):
        if self.focus_get()==self.text:
            self.text.tag_add(tk.SEL, "1.0", 'end-1c')
            self.text.see(tk.END)
        elif event:
            event.widget.event_generate('<<SelectAll>>')
        return 'break'

    def ctrlKeys(self, event):
        if event.keycode==67:
            self.ControlC(event)
        elif event.keycode==86:
            self.ControlV(event)
        elif event.keycode==88:
            self.ControlX(event)
        elif event.keycode==90:
            self.ControlZ(event)
        elif event.keycode==89:
            self.ControlY(event)
        elif event.keycode==65:
            self.selectAll(event)
        self.configTextWidget()

    def validateComboboxSize(self, value):
        text_value=str(value)
        if text_value=='':
            return True
        elif len(text_value)>7:
            return False
        elif not text_value.isdigit():
            return False
        elif int(text_value)>72:
            return False
        if text_value in  self.list_size:
            self.parent.size_font=int(text_value)
            with open('data/size.dat', 'wb') as file:
                pickle.dump(self.parent.size_font, file)
            self.configTextWidget()
        return True

    def chooseComboboxSize(self, event):
        text_value=self.combobox_size.get()
        if text_value=='':
            self.combobox_size.delete(0, tk.END)
            self.combobox_size.insert(0, self.parent.size_font)
        elif int(text_value)<1:
            self.combobox_size.delete(0, tk.END)
            self.combobox_size.insert(0, self.parent.size_font)
        else:
            self.parent.size_font=int(text_value)
            self.combobox_size.delete(0, tk.END)
            self.combobox_size.insert(0, self.parent.size_font)
        self.configTextWidget()

    def validateComboboxFont(self, value):
        text_value=str(value)
        if len(text_value)>20:
            return False
        if text_value in self.list_font:
            self.parent.type_font=text_value
            with open('data/font.dat', 'wb') as file:
                pickle.dump(self.parent.type_font, file)
            self.configTextWidget()
        return True

    def configTextWidget(self, event=None):
        self.parent.text=self.text.get("1.0", "end-1c")
        if self.parent.text_widget:
            self.parent.canvas.itemconfig(self.parent.text_widget, text=self.parent.text,
                            fill=self.parent.choose_color, font=(self.parent.type_font,
                            self.parent.size_font, self.parent.outline_font))
        with open('data/font.dat', 'wb') as file:
            pickle.dump(self.parent.type_font, file)
        with open('data/size.dat', 'wb') as file:
            pickle.dump(self.parent.size_font, file)
        with open('data/outline.dat', 'wb') as file:
            pickle.dump(self.parent.outline_font, file)
        self.indexCursor()

    def boldPress(self):
        if 'bold' not in self.parent.outline_font:
            list_outline_font=list(self.parent.outline_font)
            list_outline_font.remove('normal')
            list_outline_font.append('bold')
            self.parent.outline_font=tuple(list_outline_font)
        else:
            list_outline_font=list(self.parent.outline_font)
            list_outline_font.remove('bold')
            list_outline_font.append('normal')
            self.parent.outline_font=tuple(list_outline_font)
        self.configTextWidget()

    def italicPress(self):
        if 'italic' not in self.parent.outline_font:
            list_outline_font = list(self.parent.outline_font)
            list_outline_font.remove('roman')
            list_outline_font.append('italic')
            self.parent.outline_font = tuple(list_outline_font)
        else:
            list_outline_font = list(self.parent.outline_font)
            list_outline_font.remove('italic')
            list_outline_font.append('roman')
            self.parent.outline_font = tuple(list_outline_font)
        self.configTextWidget()

    def exitWindow(self):
        if self.parent.text_widget:
            self.parent.canvas.delete(self.parent.text_widget)
            self.parent.text_widget=None
            self.parent.coords=[]
            self.parent.textTool()
        self.parent.active_toplevel_text=None
        self.parent.text=''
        self.destroy()

    def deleteText(self):
        if self.parent.text_widget:
            self.parent.canvas.delete(self.parent.text_widget)
            self.parent.text_widget=None
            self.parent.coords=[]
            self.parent.textTool()

    def createText(self):
        self.parent.drawText()
        self.parent.textTool()

class ButtonOutline(tk.Button):
    def __init__(self, parent, master, text, font, function):
        self.parent=parent
        self.function=function
        self.img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        self.img = ImageTk.PhotoImage(self.img)
        self.color_widget=self.parent.color_widget
        self.pressed=False
        super().__init__(master, bg=self.color_widget, activebackground=self.color_widget,
                         text=text, font=font, image=self.img, width=14, height=14, compound="c", bd=2,
                         command=self.press, relief='raised')

    def press(self):
        if not self.pressed:
            self.config(relief='sunken')
            self.pressed=True
        else:
            self.config(relief='raised')
            self.pressed=False
        self.function()
        
class ToolButton(tk.Button):
    def __init__(self, parent, master, name, path_image, function):
        self.parent=parent
        self.function=function
        self.name=name
        self.image=createIconImage(path_image, (20, 20))
        self.color_widget=self.parent.bg_btn
        super().__init__(master, height=25, width=25, image=self.image, relief='raised',
            command=self.press, bg=self.color_widget, activebackground=self.color_widget, bd=2)
        Hovertip(self, button_description[self.name][0])

    def press(self):
        self.parent.active_button.config(relief='raised')
        self.parent.active_button=self
        self.config(relief='sunken')
        self.parent.label_description.configure(text=button_description[self.name][1])
        self.function()

class ToolColorButton(tk.Button):
    def __init__(self, parent, master, color):
        self.parent=parent
        self.color=color
        self.image=createColorImage(self.color, (20, 20))
        self.color_widget=self.parent.bg_btn
        super().__init__(master, height=16, width=16, image=self.image, bg=self.color_widget,
                activebackground=self.color_widget, relief='sunken', bd=2, command=self.press)
        
    def press(self):
        self.parent.choose_color=self.color
        self.parent.image_custom_color=createColorImage(self.color, (20, 20))
        if not self.parent.colorbar_toplevel:
            self.parent.colorbar.btn_custom_color.config(image=self.parent.image_custom_color)
        else:
            self.parent.colorbar_toplevel.colorbar.btn_custom_color.config(image=self.parent.image_custom_color)
        if self.parent.text_widget:
            self.parent.canvas.itemconfig(self.parent.text_widget, fill=self.color)

class ButtonOption(tk.Button):
    button_choose_tk = dict()
    button_choose_toplevel = dict()
    btn_dict_tk = dict()
    btn_dict_toplevel = dict()
    def __init__(self, parent, master, var, value, image_notchoose, image_choose, text=''):
        self.var=var
        self.value=value
        self.parent=parent
        self.image_notchoose=image_notchoose
        self.image_choose=image_choose
        self.color_widget=self.parent.bg_btn
        super().__init__(master, image=self.image_notchoose,
            relief="flat", bd=0, command=self.press, bg=self.color_widget,
            activebackground=self.color_widget, text=text, fg="black", compound="right",
            activeforeground="black")
        if not self.parent.draw_toolbar_toplevel:
            ButtonOption.btn_dict_tk[value]=self
        else:
            ButtonOption.btn_dict_toplevel[value] = self

    def press(self):
        if not self.parent.draw_toolbar_toplevel:
            if ButtonOption.button_choose_tk.get(self.var):
                ButtonOption.button_choose_tk[self.var].config(image=ButtonOption.button_choose_tk[self.var].image_notchoose,
                                              bg=self.color_widget, activebackground=self.color_widget,
                                            fg='black', activeforeground='black')
            ButtonOption.button_choose_tk[self.var]=self
            setattr(self.parent, self.var, self.value)
            self.config(image=self.image_choose, bg='#01017c', activebackground='#01017c', fg='white',
                     activeforeground='white')
        else:
            if ButtonOption.button_choose_toplevel.get(self.var):
                ButtonOption.button_choose_toplevel[self.var].config(image=ButtonOption.button_choose_toplevel[self.var].image_notchoose,
                                              bg=self.color_widget, activebackground=self.color_widget,
                                            fg='black', activeforeground='black')
            ButtonOption.button_choose_toplevel[self.var]=self
            setattr(self.parent, self.var, self.value)
            self.config(image=self.image_choose, bg='#01017c', activebackground='#01017c', fg='white',
                     activeforeground='white')

class ButtonCuctomColor(tk.Button):
    def __init__(self, parent, master, color, function):
        self.color = color
        self.image = createColorImage(self.color, (20, 20))
        self.color_widget = parent.bg_btn
        super().__init__(master, height=14, width=14, image=self.image, bg=self.color_widget,
                         activebackground=self.color_widget, relief='raised', bd=2, command=function)

class AutoScrollbar(ttk.Scrollbar):
    def set(self, lo, hi):
        ttk.Scrollbar.set(self, lo, hi)
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()

class DrawToolbar(ttk.Frame):
    def __init__(self,  parent, master):
        super().__init__(master)

        self.intvar = tk.IntVar()
        self.intvar.set(1)

        self.frame_tool = ttk.Frame(self)
        self.frame_tool.pack(padx=(8, 4), side=tk.TOP)

        buttons_dict = {"btn_pencil": parent.pencilTool,
                        "btn_eraser": parent.eraserTool,
                        "btn_brush": parent.brushTool,
                        "btn_floodfill": parent.floodfillTool,
                        "btn_pipette": parent.pipetteTool,
                        "btn_text": parent.textTool,
                        "btn_line": parent.lineTool,
                        "btn_oval": parent.ovalTool,
                        "btn_rectangle": parent.rectangleTool,
                        "btn_triangle": parent.triangleTool}

        row, column = 0, 0
        for i in range(len(buttons_dict)):
            key = list(buttons_dict.keys())[i]
            if not parent.draw_toolbar_toplevel:
                parent.dict_btn_tk[key]=ToolButton(parent, self.frame_tool, key, list_btns[i], buttons_dict[key])
                parent.dict_btn_tk[key].grid(row=row, column=column)
            else:
                parent.dict_btn_toplevel[key] = ToolButton(parent, self.frame_tool, key, list_btns[i], buttons_dict[key])
                parent.dict_btn_toplevel[key].grid(row=row, column=column)
            column += 1
            if column == 2:
                row, column = row + 1, 0

        self.frame_option = ttk.Frame(self, relief="sunken", borderwidth=2, height=81)
        self.frame_option.pack(side=tk.TOP, pady=4, padx=(12, 10), fill="x")
        self.frame_option.pack_propagate(0)

        self.frame_option_filling = ttk.Frame(self.frame_option)
        ButtonOption(parent, self.frame_option_filling, 'option_fill', 'outline',
                     createIconImage(outline_notchoose_icon_pic, (33, 18)),
                     createIconImage(outline_choose_icon_pic, (33, 18))).pack(side=tk.TOP,
                                                                              fill='both', expand=True)

        btn = ButtonOption(parent, self.frame_option_filling, 'option_fill',
                           'fill_and_outline', createIconImage(fill_and_outline_notchoose_icon_pic, (33, 18)),
                           createIconImage(fill_and_outline_choose_icon_pic, (33, 18)))
        btn.press()
        btn.pack(side=tk.TOP, fill='both', expand=True)

        ButtonOption(parent, self.frame_option_filling, 'option_fill', 'fill',
                     createIconImage(fill_notchoose_icon_pic, (33, 18)),
                     createIconImage(fill_choose_icon_pic, (33, 18))).pack(side=tk.TOP, fill='both',
                                                                           expand=True)

        self.frame_option_size = ttk.Frame(self.frame_option)
        ButtonOption(parent, self.frame_option_size, 'width_brush', 2,
                     createIconImage(size_notchoose_icon_pic, (2, 2)),
                     createIconImage(size_choose_icon_pic, (2, 2)), text='2x   ').pack(side=tk.TOP,
                                                                                    fill='both', expand=True)

        btn = ButtonOption(parent, self.frame_option_size, 'width_brush', 4,
                           createIconImage(size_notchoose_icon_pic, (4, 4)),
                           createIconImage(size_choose_icon_pic, (4, 4)), text='4x  ')
        btn.press()
        btn.pack(side=tk.TOP, fill='both', expand=True)

        self.btn_size_8 = ButtonOption(parent, self.frame_option_size, 'width_brush', 8,
                                        createIconImage(size_notchoose_icon_pic, (8, 8)),
                                        createIconImage(size_choose_icon_pic, (8, 8)), text='8x ').pack(side=tk.TOP,
                                                                                            fill='both', expand=True)

        self.update_idletasks()

class Colorbar(ttk.Frame):
    def __init__(self, parent, master):
        self.master=master
        self.parent=parent

        super().__init__(self.master)

        ttk.Frame(self).pack()

        self.colorbar = ttk.Frame(self)
        self.colorbar.pack(fill="x", pady=9)

        self.intvar=tk.IntVar()
        self.intvar.set(1)

        color_widget = self.parent.bg_btn

        self.frame_custom_color = ttk.Frame(self.colorbar, relief="sunken", borderwidth=2, width=42,
                                             height=42)
        self.frame_custom_color.pack(side=tk.LEFT, padx=(4, 0))

        self.btn_invert_color = ButtonCuctomColor(parent, self.frame_custom_color, self.parent.service_color,
                                                   lambda: invertColor(self.parent))
        self.btn_invert_color.place(x=14, y=14)
        Hovertip(self.btn_invert_color, invert_color_description)

        self.btn_custom_color = ButtonCuctomColor(parent, self.frame_custom_color, self.parent.choose_color,
                                                   lambda: customColor(self.parent))
        self.btn_custom_color.place(x=4, y=4)
        Hovertip(self.btn_custom_color, custom_color_description)

        self.frame_color = ttk.Frame(self.colorbar)
        self.frame_color.pack(side=tk.LEFT)

        row, column = 0, 0
        for i in range(len(list_colors)):
            ToolColorButton(self.parent, self.frame_color, list_colors[i]).grid(row=row, column=column)
            row += 1
            if row == 2:
                column, row = column + 1, 0

        self.update_idletasks()

class DrawToolbarToplevel(tk.Toplevel):
    def __init__(self, parent, master):
        self.parent=parent
        self.master=master
        super().__init__(self.master)
        self.transient(self.master)
        self.attributes('-toolwindow', True)
        self.focus_set()
        self.title("Панель инструментов")
        self.geometry("+{}+{}".format(self.master.winfo_x()+10, self.master.winfo_y()+60))
        self.resizable(0, 0)
        self['bg'] = self.parent.bg_btn

        self.protocol("WM_DELETE_WINDOW", self.exitWindow)

        self.parent.draw_toolbar_toplevel=self

        self.draw_toolbar = DrawToolbar(self.parent, self)
        self.draw_toolbar.pack()

        invert_dict = {value: key for key, value in self.parent.dict_btn_tk.items()}
        key = invert_dict[self.parent.active_button]

        self.parent.dict_btn_toplevel[key].press()
        self.parent.active_button = self.parent.dict_btn_toplevel[key]

        value=ButtonOption.button_choose_tk["option_fill"].value
        ButtonOption.btn_dict_toplevel[value].press()

        value = ButtonOption.button_choose_tk["width_brush"].value
        ButtonOption.btn_dict_toplevel[value].press()

    def exitWindow(self):
        self.parent.draw_toolbar_toplevel = None
        self.parent.state_closed=True

        invert_dict = {value: key for key, value in self.parent.dict_btn_toplevel.items()}
        key=invert_dict[self.parent.active_button]

        self.parent.dict_btn_tk[key].press()
        self.parent.active_button=self.parent.dict_btn_tk[key]

        value = ButtonOption.button_choose_toplevel["option_fill"].value
        ButtonOption.btn_dict_tk[value].press()

        value = ButtonOption.button_choose_toplevel["width_brush"].value
        ButtonOption.btn_dict_tk[value].press()

        if self.parent.draw_toolbar.intvar.get():
            self.parent.frame_draw.pack(side=tk.TOP, fill="both", expand=True)

        self.destroy()

        ButtonOption.button_choose_toplevel = dict()
        ButtonOption.btn_dict_toplevel = dict()

        self.parent.state_closed = None

class ColorbarToplevel(tk.Toplevel):
    def __init__(self, parent, master):
        self.parent=parent
        self.master=master
        super().__init__(self.master)
        self.transient(self.master)
        self.attributes('-toolwindow', True)
        self.focus_set()
        self.title("Палитра")
        self.geometry("+{}+{}".format(self.master.winfo_x()+self.parent.frame_draw_toolbar.winfo_width()+10, self.master.winfo_y()+self.master.winfo_height()-88))
        self.resizable(0, 0)
        self['bg'] = self.parent.bg_btn

        self.protocol("WM_DELETE_WINDOW", self.exitWindow)

        self.colorbar = Colorbar(self.parent, self)
        self.colorbar.pack()

    def exitWindow(self):
        self.parent.colorbar_toplevel = None

        self.parent.colorbar.btn_custom_color.config(image=self.parent.image_custom_color)
        self.parent.colorbar.btn_invert_color.config(image=self.parent.image_invert_color)

        if self.parent.colorbar.intvar.get():
            self.parent.frame_color.pack(side=tk.LEFT, fill="both", expand=True)

        self.destroy()

def openDrawToolbarToplevel(self_):
    if not self_.draw_toolbar_toplevel and self_.draw_toolbar.intvar.get():
        self_.state_closed = True
        self_.frame_draw.pack_forget()
        self_.draw_toolbar_toplevel=DrawToolbarToplevel(self_, self_.master)
        self_.state_closed = None

def openColorbarToplevel(self_):
    if not self_.colorbar_toplevel and self_.colorbar.intvar.get():
        self_.frame_color.pack_forget()
        self_.colorbar_toplevel=ColorbarToplevel(self_, self_.master)

def controlKey(self_, event):
    char=chr(event.keycode)
    if char=='N':
        self_.newFile()
    elif char=='O':
        self_.openFile()
    elif char=='S':
        self_.saveFile()
    elif char=='L':
        self_.invertImageColors()

def controlShiftKey(self_, event):
    char = chr(event.keycode)
    if char=='S':
        self_.saveFileAs()

def getPaperWidth(self_):
    self_.master.update()
    width = round((self_.master.winfo_screenwidth() - self_.frame_draw_toolbar.winfo_width() - 8) * 0.945)
    return width

def getPaperHeight(self_):
    self_.master.update()
    height = round((self_.master.winfo_screenheight() - self_.frame_colorbar.winfo_height() -
                    self_.frame_state_main.winfo_height() - 100 - 8) * 0.9)
    return height

def initVars(self_):
    self_.name_app='Краска 2D'
    
    self_.file_name='Безымянный'
    self_.changed=False
    self_.path=None

    self_.bg_color="white"
    self_.choose_color="black"
    self_.service_color="white"
    self_.eraser_width=10
    self_.width=4
    self_.width_brush=4
    
    self_.coords=[]
    self_.previous_point=None
    self_.drawn_shape=None
    
    self_.onMotion=onMotion
    self_.onMotionButton=onMotionButton
    self_.onRelease=onRelease

    self_.flag_l=False
    self_.flag_r=False
    self_.active_frame_option=None

    if not os.path.exists ("data/font.dat"):
        with open('data/font.dat', 'wb') as file:
            self_.type_font = 'Times New Roman'
            pickle.dump(self_.type_font, file)
    else:
        with open('data/font.dat', 'rb') as file:
            self_.type_font = pickle.load(file)
    if not os.path.exists("data/size.dat"):
        with open('data/size.dat', 'wb') as file:
            self_.size_font = 12
            pickle.dump(self_.size_font, file)
    else:
        with open('data/size.dat', 'rb') as file:
            self_.size_font = pickle.load(file)
    if not os.path.exists("data/outline.dat"):
        with open('data/outline.dat', 'wb') as file:
            self_.outline_font=('normal', 'roman')
            pickle.dump(self_.outline_font, file)
    else:
        with open('data/outline.dat', 'rb') as file:
            self_.outline_font = pickle.load(file)
    if not os.path.exists("data/size.dat"):
        with open('data/size.dat', 'wb') as file:
            self_.size_font = 12
            pickle.dump(self_.size_font, file)
    else:
        with open('data/size.dat', 'rb') as file:
            self_.size_font = pickle.load(file)
    if not os.path.exists("data/language.dat"):
        with open('data/language.dat', 'wb') as file:
            self_.language = "Русский"
            pickle.dump(self_.language, file)
    else:
        with open('data/language.dat', 'rb') as file:
            self_.language = pickle.load(file)
    if not os.path.exists("data/language.dat"):
        with open('data/language.dat', 'wb') as file:
            self_.language = "Русский"
            pickle.dump(self_.language, file)
    else:
        with open('data/language.dat', 'rb') as file:
            self_.language = pickle.load(file)

    self_.active_toplevel_text=None
    self_.text_widget=None
    self_.text=''
    self_.font_style = font.Font(family="Arial", size=12, weight="normal", slant="roman",
                                underline=False, overstrike=False)
    self_.scale=100

    self_.draw_toolbar_toplevel=None
    self_.colorbar_toplevel=None
    self_.state_closed = None
    self_.dict_btn_tk = dict()
    self_.dict_btn_toplevel = dict()
    
    self_.bg_btn=self_.master.style.lookup("TButton", "background")
    self_.fg_btn=self_.master.style.lookup("TButton", "foreground")

def onMotion(self_, event):
    x = int(event.x + self_.scrollbar_x.get()[0] * self_.scrollregion[2])
    y = int(event.y + self_.scrollbar_y.get()[0] * self_.scrollregion[3])
    self_.label_coords.config(text='{}, {}'.format(x, y))

def onLeave(self_):
    self_.label_coords.config(text='')

def onMotionButton(self_, event):
    x_event=event.x+self_.scrollbar_x.get()[0]*self_.scrollregion[2]
    y_event=event.y+self_.scrollbar_y.get()[0]*self_.scrollregion[3]
    x=int(abs(x_event-self_.previous_point[0]))
    y=int(abs(y_event-self_.previous_point[1]))
    self_.label_size.config(text='{} x {}'.format(x, y))

def onRelease(self_):
    self_.label_size.config(text='')

def customColor(self_):
    color=colorchooser.askcolor(self_.choose_color)[1]
    if color:
        self_.choose_color=color
        self_.image_custom_color=createColorImage(self_.choose_color, (20, 20))
        if not self_.colorbar_toplevel:
            self_.colorbar.btn_custom_color.config(image=self_.image_custom_color)
        else:
            self_.colorbar_toplevel.colorbar.btn_custom_color.config(image=self_.image_custom_color)
        if self_.text_widget:
            self_.canvas.itemconfig(self_.text_widget, fill=self_.choose_color)

def invertColor(self_):
    self_.service_color, self_.choose_color=self_.choose_color, self_.service_color

    self_.image_custom_color=createColorImage(self_.choose_color, (20, 20))
    self_.image_invert_color=createColorImage(self_.service_color, (20, 20))

    if not self_.colorbar_toplevel:
        self_.colorbar.btn_custom_color.config(image=self_.image_custom_color)
        self_.colorbar.btn_invert_color.config(image=self_.image_invert_color)
    else:
        self_.colorbar_toplevel.colorbar.btn_custom_color.config(image=self_.image_custom_color)
        self_.colorbar_toplevel.colorbar.btn_invert_color.config(image=self_.image_invert_color)
    if self_.text_widget:
            self_.canvas.itemconfig(self_.text_widget, fill=self_.choose_color)

def createColorImage(color, size):
    image = ImageTk.PhotoImage(Image.new("RGB", size, color))
    return(image)

def createIconImage(iconPath, size):
  image=ImageTk.PhotoImage(Image.open(iconPath).resize(size, Image.ANTIALIAS))
  return(image)

def initCanvas(self_):
    self_.master.iconphoto(True, tk.PhotoImage(file=".\pic\img_icon.png"))
    self_.master.title("{} - {}".format(self_.file_name, self_.name_app))
    self_.master.protocol("WM_DELETE_WINDOW", self_.exitWindow)

    self_.default_paper_width=self_.paper_width=getPaperWidth(self_)
    self_.default_paper_height=self_.paper_height=getPaperHeight(self_)
    
    self_.canvas_frame=tk.Frame(self_.master, bg="#808080", relief="flat", bd=0)
    
    self_.scrollregion=(0, 0, self_.paper_width, self_.paper_height)
    self_.canvas=tk.Canvas(self_.canvas_frame, width=self_.paper_width, height=self_.paper_height,
                          highlightthickness=0, cursor="tcross", scrollregion=self_.scrollregion)
    self_.canvas.grid(row=0, column=0, sticky="nw", padx=(4, 0), pady=(4, 0))

    self_.image=Image.new("RGB", (self_.paper_width, self_.paper_height), self_.bg_color)
    self_.canvas.image=ImageTk.PhotoImage(self_.image)
    self_.canvas.create_image(0, 0, image=self_.canvas.image, anchor="nw")

    self_.scrollbar_x=AutoScrollbar(self_.canvas_frame, orient="horizontal",
                                    command=self_.canvas.xview)
    self_.scrollbar_x.grid(row=1, column=0, sticky="news")
    self_.canvas.configure(xscrollcommand=self_.scrollbar_x.set)

    self_.scrollbar_y=AutoScrollbar(self_.canvas_frame, orient="vertical",
                                    command=self_.canvas.yview)
    self_.scrollbar_y.grid(row=0, column=1, sticky="news")
    self_.canvas.configure(yscrollcommand=self_.scrollbar_y.set)

    ttk.Frame(self_.canvas_frame).grid(row=1, column=1, sticky="news")

    self_.canvas_frame.columnconfigure(0, weight=1)
    self_.canvas_frame.rowconfigure(0, weight=1)

    self_.canvas.bind("<Motion>", lambda event: onMotion(self_, event))
    self_.canvas.bind("<Leave>", lambda event: onLeave(self_))
    
    self_.canvas_frame.pack(side=tk.LEFT, fill="both", expand=True)
    self_.canvas_frame.propagate(0)

    self_.active_button=self_.dict_btn_tk["btn_pencil"]
    self_.active_button.press()
    
def initMenubar(self_):
    self_.menubar=tk.Menu(self_.master)

    self_.file_menu=tk.Menu(self_.menubar, tearoff=0)
    self_.file_menu.add_command(label="Создать", command=self_.newFile, accelerator='CTRL+N')
    self_.file_menu.add_command(label="Открыть...", command=self_.openFile, accelerator='CTRL+O')
    self_.file_menu.add_command(label="Сохранить", command=self_.saveFile, accelerator='CTRL+S')
    self_.file_menu.add_command(label="Сохранить как...", command=self_.saveFileAs, accelerator='CTRL+SHIFT+S')
    self_.file_menu.add_separator()
    self_.file_menu.add_command(label="Выход", command=self_.exitWindow)
    self_.menubar.add_cascade(label="Файл", menu=self_.file_menu)

    self_.vid_menu=tk.Menu(self_.menubar, tearoff=0)
    self_.vid_menu.add_checkbutton(label="Набор инструментов", variable=self_.draw_toolbar.intvar, onvalue=1, offvalue=0,
                                   command=lambda : packDrawToolbar(self_))
    self_.vid_menu.add_checkbutton(label="Палитра", variable=self_.colorbar.intvar, onvalue=1, offvalue=0,
                                   command=lambda: packColorbar(self_))
    self_.vid_menu.add_checkbutton(label="Строка состояния", variable=self_.intvar_frame_state, onvalue=1, offvalue=0,
                                   command=lambda: packFrameState(self_))
    self_.menubar.add_cascade(label="Вид", menu=self_.vid_menu)

    self_.radio_outline_size=tk.IntVar()
    self_.radio_outline_size.set(self_.width)
    self_.radio_outline_size.trace('w', lambda *args: setattr(self_, "width", self_.radio_outline_size.get()))

    self_.outline_size_menu=tk.Menu(self_.menubar, tearoff=0)
    self_.outline_size_menu.add_radiobutton(label="1 пкс", value=1, variable=self_.radio_outline_size)
    self_.outline_size_menu.add_radiobutton(label="2 пкс", value=2, variable=self_.radio_outline_size)
    self_.outline_size_menu.add_radiobutton(label="3 пкс", value=3, variable=self_.radio_outline_size)
    self_.outline_size_menu.add_radiobutton(label="4 пкс", value=4, variable=self_.radio_outline_size)
    self_.outline_size_menu.add_radiobutton(label="5 пкс", value=5, variable=self_.radio_outline_size)
    self_.menubar.add_cascade(label="Толщина", menu=self_.outline_size_menu)

    self_.image_menu=tk.Menu(self_.menubar, tearoff=0)
    self_.image_menu.add_command(label="Повернуть на 90° вправо", command=self_.rotateImage)
    self_.image_menu.add_command(label="Отразить по вертикали", command=self_.flipImageTopBottom)
    self_.image_menu.add_command(label="Отразить по горизонтали", command=self_.flipImageLeftRight)
    self_.image_menu.add_command(label="Инвертировать цвета", command=self_.invertImageColors)
    self_.image_menu.add_command(label="Изменить размер холста", command=lambda: sizeToplevel(self_, self_.master))
    self_.menubar.add_cascade(label="Рисунок", menu=self_.image_menu)

    self_.menubar.add_command(label='О программе',
                              command=lambda: infoToplevel(self_, self_.master))

    self_.master.config(menu=self_.menubar)

    self_.master.bind('<Control-KeyPress>', lambda event: controlKey(self_, event))
    self_.master.bind('<Control-Shift-KeyPress>', lambda event: controlShiftKey(self_, event))

def packDrawToolbar(self_):
    if self_.draw_toolbar.intvar.get():
        if not self_.draw_toolbar_toplevel:
            self_.frame_draw.pack(side=tk.TOP, fill="both", expand=True)
        else:
            self_.draw_toolbar_toplevel.deiconify()
    else:
        if not self_.draw_toolbar_toplevel:
            self_.frame_draw.pack_forget()
        else:
            self_.draw_toolbar_toplevel.withdraw()

def packColorbar(self_):
    if self_.colorbar.intvar.get():
        if not self_.colorbar_toplevel:
            self_.frame_color.pack(side=tk.LEFT, fill="both", expand=True)
        else:
            self_.colorbar_toplevel.deiconify()
    else:
        if not self_.colorbar_toplevel:
            self_.frame_color.pack_forget()
        else:
            self_.colorbar_toplevel.withdraw()

def packFrameState(self_):
    if self_.intvar_frame_state.get():
        self_.frame_state.pack(fill="x")
    else:
        self_.frame_state.pack_forget()

def initFrameState(self_):
    self_.frame_state_main = ttk.Frame(self_.master)
    self_.frame_state_main.pack(side=tk.BOTTOM, fill="x")

    ttk.Frame(self_.frame_state_main).pack()

    self_.frame_state = ttk.Frame(self_.frame_state_main)
    self_.frame_state.pack(fill='x')

    self_.intvar_frame_state = tk.IntVar()
    self_.intvar_frame_state.set(1)

    self_.label_size = ttk.Label(self_.frame_state, width=12, relief="sunken")
    self_.label_size.pack(side=tk.RIGHT, padx=(2, 2), pady=2)

    self_.label_coords = ttk.Label(self_.frame_state, width=12, relief="sunken")
    self_.label_coords.pack(side=tk.RIGHT, padx=(2, 0), pady=2)

    self_.label_description = ttk.Label(self_.frame_state, relief="sunken")
    self_.label_description.pack(side=tk.LEFT, padx=(8, 0), pady=2, fill="x", expand=True)

def initDrawToolbar(self_):
    self_.frame_draw_toolbar=ttk.Frame(self_.master)
    self_.frame_draw_toolbar.pack(side=tk.LEFT, fill='y')

    ttk.Frame(self_.frame_draw_toolbar).pack(side=tk.BOTTOM)

    self_.frame_draw=ttk.Frame(self_.frame_draw_toolbar)
    self_.frame_draw.pack(side=tk.TOP, fill="both", expand=True)

    ttk.Separator(self_.frame_draw, orient='horizontal').pack(side=tk.BOTTOM, fill='x', padx=(4, 2))

    self_.frame_draw_toolbar_btn=tk.Frame(self_.frame_draw, highlightbackground=self_.bg_btn,
                                           highlightthickness=1)
    self_.frame_draw_toolbar_btn.pack(side=tk.TOP)

    self_.draw_toolbar = DrawToolbar(self_, self_.frame_draw_toolbar_btn)
    self_.draw_toolbar.pack()

    self_.draw_toolbar.bind("<ButtonPress-1>", lambda event: self_.frame_draw_toolbar_btn.config(highlightbackground='black'))
    self_.draw_toolbar.bind("<ButtonRelease-1>", lambda event: self_.frame_draw_toolbar_btn.config(highlightbackground=self_.bg_btn))
    self_.draw_toolbar.bind("<Double-ButtonPress-1>", lambda event: openDrawToolbarToplevel(self_))

def initColorToolbar(self_):
    self_.frame_colorbar = ttk.Frame(self_.master)
    self_.frame_colorbar.pack(side=tk.BOTTOM, fill="x")

    ttk.Frame(self_.frame_colorbar).pack(side=tk.RIGHT)

    self_.frame_color = ttk.Frame(self_.frame_colorbar)
    self_.frame_color.pack(side=tk.LEFT, fill="both", expand=True)

    ttk.Separator(self_.frame_color, orient="horizontal").pack(side=tk.BOTTOM, fill="x")

    self_.frame_color_btn = tk.Frame(self_.frame_color, highlightbackground=self_.bg_btn,
                                            highlightthickness=1)
    self_.frame_color_btn.pack(side=tk.LEFT)

    self_.colorbar = Colorbar(self_, self_.frame_color_btn)
    self_.colorbar.pack()

    self_.colorbar.bind("<ButtonPress-1>",
                            lambda event: self_.frame_color_btn.config(highlightbackground="black"))
    self_.colorbar.bind("<ButtonRelease-1>",
                            lambda event: self_.frame_color_btn.config(highlightbackground=self_.bg_btn))
    self_.colorbar.bind("<Double-ButtonPress-1>", lambda event: openColorbarToplevel(self_))