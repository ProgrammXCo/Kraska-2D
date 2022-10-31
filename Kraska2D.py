import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk, ThemedStyle
from PIL import Image, ImageTk
from os import path
import sys
import init_gui as init
import drawing as draw

class App(dict):
    def __getattr__(self, attr):
        return self.get(attr)

    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

    def __init__(self, master):
        self.master = master
        init.initVars(self)
        init.initFrameState(self)
        init.initColorToolbar(self)
        init.initDrawToolbar(self)
        init.initCanvas(self)
        init.initMenubar(self)

    def exitWindow(self):
        if not self.changed:
            sys.exit()
        elif self.path and path.exists(self.path):
            message='Хотите сохранить изменения в '+str(self.path)+'.'
            answer=messagebox.askquestion(self.name_app, message, type='yesnocancel')
            if path.exists(self.path):
                if answer=='yes':
                    self.saveFile()
                    sys.exit()
                elif answer=='no':
                    sys.exit()
        else:
            message='Хотите сохранить изменения в '+str(self.file_name)+'.'
            answer=messagebox.askquestion(self.name_app, message, type='yesnocancel')
            if answer=='yes':
                self.saveFile()
                sys.exit()
            elif answer=='no':
                sys.exit()

    def newFile(self):
        if not self.changed:
            self.canvas.delete("all")
            if self.active_toplevel_text:
                self.active_toplevel_text.exitWindow()
            self.paper_width=self.default_paper_width
            self.paper_height=self.default_paper_height
            self.scrollregion=(0, 0, self.paper_width, self.paper_height)
            self.canvas.config(width=self.paper_width, height=self.paper_height,
                               scrollregion=self.scrollregion)
            self.image=Image.new("RGB", (self.paper_width, self.paper_height), self.bg_color)
            self.canvas.image=ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")
            self.file_name="Безымянный"
            self.master.title("{} - {}".format(self.file_name, self.name_app))
            self.changed=False
            self.path=None
        else:
            if self.path and path.exists(self.path):
                message="Хотите сохранить изменения в "+str(self.path)+"."
                ansver=messagebox.askquestion(self.name_app, message, type="yesnocancel")
                if path.exists(self.path):
                    if ansver=="yes":
                        self.saveFile()
                        self.canvas.delete("all")
                        if self.active_toplevel_text:
                            self.active_toplevel_text.exitWindow()
                        self.paper_width=self.default_paper_width
                        self.paper_height=self.default_paper_height
                        self.scrollregion=(0, 0, self.paper_width, self.paper_height)
                        self.canvas.config(width=self.paper_width, height=self.paper_height,
                               scrollregion=self.scrollregion)
                        self.image=Image.new("RGB", (self.paper_width, self.paper_height), self.bg_color)
                        self.canvas.image=ImageTk.PhotoImage(self.image)
                        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
                        self.file_name='Безымянный'
                        self.master.title('{} - {}'.format(self.file_name, self.name_app))
                        self.changed=False
                        self.path=None
                    elif ansver=='no':
                        self.canvas.delete("all")
                        if self.active_toplevel_text:
                            self.active_toplevel_text.exitWindow()
                        self.paper_width=self.default_paper_width
                        self.paper_height=self.default_paper_height
                        self.scrollregion=(0, 0, self.paper_width, self.paper_height)
                        self.canvas.config(width=self.paper_width, height=self.paper_height,
                               scrollregion=self.scrollregion)
                        self.image=Image.new("RGB", (self.paper_width, self.paper_height), self.bg_color)
                        self.canvas.image=ImageTk.PhotoImage(self.image)
                        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
                        self.file_name='Безымянный'
                        self.master.title('{} - {}'.format(self.file_name, self.name_app))
                        self.changed=False
                        self.path=None
            else:
                message='Хотите сохранить изменения в '+str(self.file_name)+'.'
                ansver=messagebox.askquestion(self.name_app, message, type='yesnocancel')
                if ansver=='yes':
                    self.saveFile()
                    self.canvas.delete("all")
                    if self.active_toplevel_text:
                        self.active_toplevel_text.exitWindow()
                    self.paper_width=self.default_paper_width
                    self.paper_height=self.default_paper_height
                    self.scrollregion=(0, 0, self.paper_width, self.paper_height)
                    self.canvas.config(width=self.paper_width, height=self.paper_height,
                               scrollregion=self.scrollregion)
                    self.image=Image.new("RGB", (self.paper_width, self.paper_height), self.bg_color)
                    self.canvas.image=ImageTk.PhotoImage(self.image)
                    self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
                    self.file_name='Безымянный'
                    self.master.title('{} - {}'.format(self.file_name, self.name_app))
                    self.changed=False
                    self.path=None
                elif ansver=='no':
                    self.canvas.delete("all")
                    if self.active_toplevel_text:
                        self.active_toplevel_text.exitWindow()
                    self.paper_width=self.default_paper_width
                    self.paper_height=self.default_paper_height
                    self.scrollregion=(0, 0, self.paper_width, self.paper_height)
                    self.canvas.config(width=self.paper_width, height=self.paper_height,
                               scrollregion=self.scrollregion)
                    self.image=Image.new("RGB", (self.paper_width, self.paper_height), self.bg_color)
                    self.canvas.image=ImageTk.PhotoImage(self.image)
                    self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
                    self.file_name='Безымянный'
                    self.master.title('{} - {}'.format(self.file_name, self.name_app))
                    self.changed=False
                    self.path=None

    def saveFileAs(self):
        if self.active_toplevel_text:
            self.active_toplevel_text.exitWindow()
        path_new=filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG", "*.png"),
                ("GIF", "*.gif"), ("JPEG", ("*.jpg", "*.jpeg", "*.jpe", "*.jfif"))),
                initialfile=self.file_name)
        if path_new:
            self.file_name=path.basename(path_new)
            self.master.title('{} - {}'.format(self.file_name, self.name_app))
            self.image.save(path_new)
            self.changed = False
            self.path=path_new

    def saveFile(self):
        if self.path and path.exists(self.path):
            if self.active_toplevel_text:
                self.active_toplevel_text.exitWindow()
            self.master.title('{} - {}'.format(self.file_name, self.name_app))
            self.image.save(self.path)
            self.changed = False
        else:
            self.saveFileAs()

    def openFile(self):
        path_new=filedialog.askopenfilename(filetypes=(("PNG", "*.png"), ("GIF", "*.gif"),
                                        ("JPEG", ("*.jpg", "*.jpeg", "*.jpe", "*.jfif"))))
        if path_new:
            if self.changed:
                if self.path and path.exists(self.path):
                    message='Хотите сохранить изменения в '+str(self.path)+'.'
                    ansver=messagebox.askquestion(self.name_app, message, type='yesnocancel')
                    if ansver=='yes':
                        self.saveFile()
                        self.file_name=path.basename(path_new)
                        self.master.title('{} - {}'.format(self.file_name, self.name_app))
                        self.image=Image.open(path_new)
                        self.image=self.image.convert('RGB')
                        self.paper_width = self.image.size[0]
                        self.paper_height = self.image.size[1]
                        self.scrollregion=(0, 0, self.image.size[0], self.image.size[1])
                        self.canvas.config(width=self.image.size[0], height=self.image.size[1],
                               scrollregion=self.scrollregion)
                        self.canvas.delete('all')
                        if self.active_toplevel_text:
                            self.active_toplevel_text.exitWindow()
                        self.canvas.image=ImageTk.PhotoImage(self.image)
                        self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")
                        self.changed=False
                        self.path=path_new
                    elif ansver=='no':
                        self.file_name=path.basename(path_new)
                        self.master.title('{} - {}'.format(self.file_name, self.name_app))
                        self.image=Image.open(path_new)
                        self.image=self.image.convert('RGB')
                        self.paper_width = self.image.size[0]
                        self.paper_height = self.image.size[1]
                        self.scrollregion=(0, 0, self.image.size[0], self.image.size[1])
                        self.canvas.config(width=self.image.size[0], height=self.image.size[1],
                               scrollregion=self.scrollregion)
                        self.canvas.delete('all')
                        if self.active_toplevel_text:
                            self.active_toplevel_text.exitWindow()
                        self.canvas.image=ImageTk.PhotoImage(self.image)
                        self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")
                        self.changed=False
                        self.path = path_new
                else:
                    message='Хотите сохранить изменения в '+str(self.file_name)+'.'
                    ansver=messagebox.askquestion(self.name_app, message, type='yesnocancel')
                    if ansver=='yes':
                        self.saveFile()
                        self.file_name=path.basename(path_new)
                        self.master.title('{} - {}'.format(self.file_name, self.name_app))
                        self.image=Image.open(path_new)
                        self.image=self.image.convert('RGB')
                        self.paper_width = self.image.size[0]
                        self.paper_height = self.image.size[1]
                        self.scrollregion=(0, 0, self.image.size[0], self.image.size[1])
                        self.canvas.config(width=self.image.size[0], height=self.image.size[1],
                               scrollregion=self.scrollregion)
                        self.canvas.delete('all')
                        if self.active_toplevel_text:
                            self.active_toplevel_text.exitWindow()
                        self.canvas.image=ImageTk.PhotoImage(self.image)
                        self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")
                        self.changed=False
                        self.path = path_new
                    elif ansver=='no':
                        self.file_name=path.basename(path_new)
                        self.master.title('{} - {}'.format(self.file_name, self.name_app))
                        self.image=Image.open(path_new)
                        self.image=self.image.convert('RGB')
                        self.paper_width = self.image.size[0]
                        self.paper_height = self.image.size[1]
                        self.scrollregion=(0, 0, self.image.size[0], self.image.size[1])
                        self.canvas.config(width=self.image.size[0], height=self.image.size[1],
                               scrollregion=self.scrollregion)
                        self.canvas.delete('all')
                        if self.active_toplevel_text:
                            self.active_toplevel_text.exitWindow()
                        self.canvas.image=ImageTk.PhotoImage(self.image)
                        self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")
                        self.changed=False
                        self.path = path_new
            else:
                self.file_name=path.basename(path_new)
                self.master.title('{} - {}'.format(self.file_name, self.name_app))
                self.image=Image.open(path_new)
                self.image=self.image.convert('RGB')
                self.paper_width = self.image.size[0]
                self.paper_height = self.image.size[1]
                self.scrollregion=(0, 0, self.image.size[0], self.image.size[1])
                self.canvas.config(width=self.image.size[0], height=self.image.size[1],
                               scrollregion=self.scrollregion)
                self.canvas.delete('all')
                if self.active_toplevel_text:
                    self.active_toplevel_text.exitWindow()
                self.canvas.image=ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")
                self.changed=False
                self.path = path_new

    def pencilTool(self):
        if self.active_frame_option:
            self.active_frame_option.pack_forget()
        if self.active_toplevel_text:
            self.active_toplevel_text.exitWindow()
        self.flag_l=False
        self.flag_r=False
        self.canvas.bind('<ButtonPress-1>', lambda event: (self.pencilPress(event, 1),
                            setattr(self, 'flag_l', True),
                            (self.canvas.delete('all'), self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw'), setattr(self, 'previous_point', None), setattr(self, 'coords', []), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.unbind('<B1-Motion>'), self.canvas.unbind('<B3-Motion>'), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.pencilTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.pencilTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.bind('<B1-Motion>', lambda event: (self.pencilMotion(event, 1),
                                                       self.onMotion(self, event)))
        self.canvas.bind('<ButtonRelease-1>', lambda event: (self.drawPencil(event, 1),
                                                    setattr(self, 'changed', True),
                                                    self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                                                    setattr(self, 'flag_l', False)))

        self.canvas.bind('<ButtonPress-3>', lambda event: (self.pencilPress(event, 3),
                            setattr(self, 'flag_r', True),
                            (self.canvas.delete('all'), self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw'), setattr(self, 'previous_point', None), setattr(self, 'coords', []), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.unbind('<B1-Motion>'), self.canvas.unbind('<B3-Motion>'), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.pencilTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.pencilTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.bind('<B3-Motion>', lambda event: (self.pencilMotion(event, 3),
                                                       self.onMotion(self, event)))
        self.canvas.bind('<ButtonRelease-3>', lambda event: (self.drawPencil(event, 3),
                                                    setattr(self, 'changed', True),
                                                    self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                                                    setattr(self, 'flag_r', False)))

    def eraserTool(self):
        if self.active_frame_option:
            self.active_frame_option.pack_forget()
        if self.active_toplevel_text:
            self.active_toplevel_text.exitWindow()
        self.canvas.bind('<ButtonPress-1>', lambda event: (self.eraserPress(event),
                            setattr(self, 'changed', True),
                            self.master.title('*{} - {}'.format(self.file_name, self.name_app))))
        self.canvas.bind('<B1-Motion>', lambda event: (self.eraserMotion(event),
                                                       self.onMotion(self, event)))
        self.canvas.bind('<ButtonRelease-1>', self.drawEraser)

        self.canvas.unbind('<ButtonPress-3>')
        self.canvas.unbind('<B3-Motion>')
        self.canvas.unbind('<ButtonRelease-3>')

    def brushTool(self):
        if self.active_frame_option:
            self.active_frame_option.pack_forget()
        if self.active_toplevel_text:
            self.active_toplevel_text.exitWindow()
        if not self.draw_toolbar_toplevel:
            self.active_frame_option=self.draw_toolbar.frame_option_size
            self.active_frame_option.pack(fill='both', expand=True)
        else:
            self.active_frame_option = self.draw_toolbar_toplevel.draw_toolbar.frame_option_size
            self.active_frame_option.pack(fill='both', expand=True)
        self.flag_l=False
        self.flag_r=False
        self.canvas.bind('<ButtonPress-1>', lambda event: (self.brushPress(event, 1),
                            setattr(self, 'flag_l', True),
                            (self.canvas.delete('all'), self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw'), setattr(self, 'previous_point', None), setattr(self, 'coords', []), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.unbind('<B1-Motion>'), self.canvas.unbind('<B3-Motion>'), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.brushTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.brushTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.bind('<B1-Motion>', lambda event: (self.brushMotion(event, 1),
                                                       self.onMotion(self, event)))
        self.canvas.bind('<ButtonRelease-1>', lambda event: (self.drawBrush(event, 1),
                                                    setattr(self, 'changed', True),
                                                    self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                                                    setattr(self, 'flag_l', False)))

        self.canvas.bind('<ButtonPress-3>', lambda event: (self.brushPress(event, 3),
                            setattr(self, 'flag_r', True),
                            (self.canvas.delete('all'), self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw'), setattr(self, 'previous_point', None), setattr(self, 'coords', []), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.unbind('<B1-Motion>'), self.canvas.unbind('<B3-Motion>'), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.brushTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.brushTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.bind('<B3-Motion>', lambda event: (self.brushMotion(event, 3),
                                                       self.onMotion(self, event)))
        self.canvas.bind('<ButtonRelease-3>', lambda event: (self.drawBrush(event, 3),
                                                    setattr(self, 'changed', True),
                                                    self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                                                    setattr(self, 'flag_r', False)))

    def floodfillTool(self):
        if self.active_frame_option:
            self.active_frame_option.pack_forget()
        if self.active_toplevel_text:
            self.active_toplevel_text.exitWindow()
        self.flag_l=False
        self.flag_r=False
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<ButtonRelease-1>", lambda event: setattr(self, 'flag_l', False))
        self.canvas.bind('<ButtonPress-1>', lambda event: (self.drawFloodfill(event, 1),
                            setattr(self, 'changed', True),
                            self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                            setattr(self, 'flag_l', True),
                            (self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.floodfillTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.floodfillTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))

        self.canvas.unbind("<B3-Motion>")
        self.canvas.bind("<ButtonRelease-3>", lambda event: setattr(self, 'flag_r', False))
        self.canvas.bind('<ButtonPress-3>', lambda event: (self.drawFloodfill(event, 3),
                            setattr(self, 'changed', True),
                            self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                            setattr(self, 'flag_r', True),
                            (self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.floodfillTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.floodfillTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))

    def pipetteTool(self):
        if self.active_frame_option:
            self.active_frame_option.pack_forget()
        if self.active_toplevel_text:
            self.active_toplevel_text.exitWindow()
        self.flag_l=False
        self.flag_r=False
        self.canvas.bind('<ButtonPress-1>', lambda event: (setattr(self, 'flag_l', True),
                            (self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.pipetteTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.pipetteTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.unbind('<B1-Motion>')
        self.canvas.bind('<ButtonRelease-1>', lambda event: (self.pipetteGet(event, 1),
                                                            setattr(self, 'flag_l', False)))

        self.canvas.bind('<ButtonPress-3>', lambda event: (setattr(self, 'flag_r', True),
                            (self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.pipetteTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.pipetteTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.unbind('<B3-Motion>')
        self.canvas.bind('<ButtonRelease-3>', lambda event: (self.pipetteGet(event, 3),
                                                             setattr(self, 'flag_r', False)))

    def textTool(self):
        if self.active_frame_option:
            self.active_frame_option.pack_forget()
        if not self.active_toplevel_text:
            if not self.state_closed:
                self.active_toplevel_text=init.textToplevel(self, self.master)
        self.coords=[]
        self.canvas.bind('<ButtonPress-1>', lambda event: (self.createTextWidget(event),
                            setattr(self, 'active_toplevel_text', init.textToplevel(self, self.master)) if not self.active_toplevel_text else False,
                            self.canvas.bind('<ButtonPress-1>', lambda event: (self.drawText(), self.textTool())), self.canvas.bind('<ButtonPress-3>', lambda event: (self.canvas.delete(self.text_widget) if self.text_widget else False, self.textTool()))))
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.canvas.unbind('<ButtonPress-3>')
        self.canvas.unbind('<B3-Motion>')
        self.canvas.unbind('<ButtonRelease-3>')

    def lineTool(self):
        if self.active_frame_option:
            self.active_frame_option.pack_forget()
        if self.active_toplevel_text:
            self.active_toplevel_text.exitWindow()
        self.flag_l=False
        self.flag_r=False
        self.drawn_shape=None
        self.canvas.bind('<ButtonPress-1>', lambda event: (self.buttonPress(event),
                            setattr(self, 'flag_l', True),
                            (self.onRelease(self), self.canvas.delete('all'), self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw'), setattr(self, 'drawn_shape', None), setattr(self, 'previous_point', None), setattr(self, 'coords', []), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.unbind('<B1-Motion>'), self.canvas.unbind('<B3-Motion>'), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.lineTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.lineTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.bind('<B1-Motion>', lambda event: (self.lineMotion(event, 1),
                                                       self.onMotion(self, event),
                                                       self.onMotionButton(self, event)))
        self.canvas.bind('<ButtonRelease-1>', lambda event: (self.drawLine(event, 1),
                            setattr(self, 'changed', True),
                            self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                            self.onRelease(self),
                            setattr(self, 'flag_l', False)))

        self.canvas.bind('<ButtonPress-3>', lambda event: (self.buttonPress(event),
                            setattr(self, 'flag_r', True),
                            (self.onRelease(self), self.canvas.delete('all'), self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw'), setattr(self, 'drawn_shape', None), setattr(self, 'previous_point', None), setattr(self, 'coords', []), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.unbind('<B1-Motion>'), self.canvas.unbind('<B3-Motion>'), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.lineTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.lineTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.bind('<B3-Motion>', lambda event: (self.lineMotion(event, 3),
                                                       self.onMotion(self, event),
                                                       self.onMotionButton(self, event)))
        self.canvas.bind('<ButtonRelease-3>', lambda event: (self.drawLine(event, 3),
                            setattr(self, 'changed', True),
                            self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                            self.onRelease(self),
                            setattr(self, 'flag_r', False)))

    def ovalTool(self):
        if self.active_frame_option:
            self.active_frame_option.pack_forget()
        if self.active_toplevel_text:
            self.active_toplevel_text.exitWindow()
        if not self.draw_toolbar_toplevel:
            self.active_frame_option=self.draw_toolbar.frame_option_filling
            self.active_frame_option.pack(fill='both', expand=True)
        else:
            self.active_frame_option = self.draw_toolbar_toplevel.draw_toolbar.frame_option_filling
            self.active_frame_option.pack(fill='both', expand=True)
        self.flag_l=False
        self.flag_r=False
        self.drawn_shape=None
        self.canvas.bind('<ButtonPress-1>', lambda event: (self.buttonPress(event),
                            setattr(self, 'flag_l', True),
                            (self.onRelease(self), self.canvas.delete('all'), self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw'), setattr(self, 'drawn_shape', None), setattr(self, 'previous_point', None), setattr(self, 'coords', []), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.unbind('<B1-Motion>'), self.canvas.unbind('<B3-Motion>'), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.ovalTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.ovalTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.bind('<B1-Motion>', lambda event: (self.ovalMotion(event, 1),
                                                       self.onMotion(self, event),
                                                       self.onMotionButton(self, event)))
        self.canvas.bind('<ButtonRelease-1>', lambda event: (self.drawOval(event, 1),
                            setattr(self, 'changed', True),
                            self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                            self.onRelease(self),
                            setattr(self, 'flag_l', False)))

        self.canvas.bind('<ButtonPress-3>', lambda event: (self.buttonPress(event),
                            setattr(self, 'flag_r', True),
                            (self.onRelease(self), self.canvas.delete('all'), self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw'), setattr(self, 'drawn_shape', None), setattr(self, 'previous_point', None), setattr(self, 'coords', []), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.unbind('<B1-Motion>'), self.canvas.unbind('<B3-Motion>'), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.ovalTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.ovalTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.bind('<B3-Motion>', lambda event: (self.ovalMotion(event, 3),
                                                       self.onMotion(self, event),
                                                       self.onMotionButton(self, event)))
        self.canvas.bind('<ButtonRelease-3>', lambda event: (self.drawOval(event, 3),
                            setattr(self, 'changed', True),
                            self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                            self.onRelease(self),
                            setattr(self, 'flag_r', False)))

    def rectangleTool(self):
        if self.active_frame_option:
            self.active_frame_option.pack_forget()
        if self.active_toplevel_text:
            self.active_toplevel_text.exitWindow()
        if not self.draw_toolbar_toplevel:
            self.active_frame_option = self.draw_toolbar.frame_option_filling
            self.active_frame_option.pack(fill='both', expand=True)
        else:
            self.active_frame_option = self.draw_toolbar_toplevel.draw_toolbar.frame_option_filling
            self.active_frame_option.pack(fill='both', expand=True)
        self.flag_l=False
        self.flag_r=False
        self.drawn_shape=None
        self.canvas.bind('<ButtonPress-1>', lambda event: (self.buttonPress(event),
                            setattr(self, 'flag_l', True),
                            (self.onRelease(self), self.canvas.delete('all'), self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw'), setattr(self, 'drawn_shape', None), setattr(self, 'previous_point', None), setattr(self, 'coords', []), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.unbind('<B1-Motion>'), self.canvas.unbind('<B3-Motion>'), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.rectangleTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.rectangleTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.bind('<B1-Motion>', lambda event: (self.rectangleMotion(event, 1),
                                                       self.onMotion(self, event),
                                                       self.onMotionButton(self, event)))
        self.canvas.bind('<ButtonRelease-1>', lambda event: (self.drawRectangle(event, 1),
                            setattr(self, 'changed', True),
                            self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                            self.onRelease(self),
                            setattr(self, 'flag_l', False)))

        self.canvas.bind('<ButtonPress-3>', lambda event: (self.buttonPress(event),
                            setattr(self, 'flag_r', True),
                            (self.onRelease(self), self.canvas.delete('all'), self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw'), setattr(self, 'drawn_shape', None), setattr(self, 'previous_point', None), setattr(self, 'coords', []), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.unbind('<B1-Motion>'), self.canvas.unbind('<B3-Motion>'), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.rectangleTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.rectangleTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.bind('<B3-Motion>', lambda event: (self.rectangleMotion(event, 3),
                                                       self.onMotion(self, event),
                                                       self.onMotionButton(self, event)))
        self.canvas.bind('<ButtonRelease-3>', lambda event: (self.drawRectangle(event, 3),
                            setattr(self, 'changed', True),
                            self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                            self.onRelease(self),
                            setattr(self, 'flag_r', False)))

    def triangleTool(self):
        if self.active_frame_option:
            self.active_frame_option.pack_forget()
        if self.active_toplevel_text:
            self.active_toplevel_text.exitWindow()
        if not self.draw_toolbar_toplevel:
            self.active_frame_option = self.draw_toolbar.frame_option_filling
            self.active_frame_option.pack(fill='both', expand=True)
        else:
            self.active_frame_option = self.draw_toolbar_toplevel.draw_toolbar.frame_option_filling
            self.active_frame_option.pack(fill='both', expand=True)
        self.flag_l=False
        self.flag_r=False
        self.drawn_shape=None
        self.canvas.bind('<ButtonPress-1>', lambda event: (self.buttonPress(event),
                            setattr(self, 'flag_l', True),
                            (self.onRelease(self), self.canvas.delete('all'), self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw'), setattr(self, 'drawn_shape', None), setattr(self, 'previous_point', None), setattr(self, 'coords', []), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.unbind('<B1-Motion>'), self.canvas.unbind('<B3-Motion>'), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.triangleTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.triangleTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.bind('<B1-Motion>', lambda event: (self.triangleMotion(event, 1),
                                                       self.onMotion(self, event),
                                                       self.onMotionButton(self, event)))
        self.canvas.bind('<ButtonRelease-1>', lambda event: (self.drawTriangle(event, 1),
                            setattr(self, 'changed', True),
                            self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                            self.onRelease(self),
                            setattr(self, 'flag_l', False)))

        self.canvas.bind('<ButtonPress-3>', lambda event: (self.buttonPress(event),
                            setattr(self, 'flag_r', True),
                            (self.onRelease(self), self.canvas.delete('all'), self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw'), setattr(self, 'drawn_shape', None), setattr(self, 'previous_point', None), setattr(self, 'coords', []), self.canvas.bind('<ButtonPress-3>', lambda event: setattr(self, 'flag_r', True)), self.canvas.bind('<ButtonPress-1>', lambda event: setattr(self, 'flag_l', True)), self.canvas.unbind('<B1-Motion>'), self.canvas.unbind('<B3-Motion>'), self.canvas.bind('<ButtonRelease-1>', lambda event: (setattr(self, 'flag_l', False), self.triangleTool() if not self.flag_l and not self.flag_r else False)), self.canvas.bind('<ButtonRelease-3>', lambda event: (setattr(self, 'flag_r', False), self.triangleTool() if not self.flag_l and not self.flag_r else False))) if self.flag_l and self.flag_r else False))
        self.canvas.bind('<B3-Motion>', lambda event: (self.triangleMotion(event, 3),
                                                       self.onMotion(self, event),
                                                       self.onMotionButton(self, event)))
        self.canvas.bind('<ButtonRelease-3>', lambda event: (self.drawTriangle(event, 3),
                            setattr(self, 'changed', True),
                            self.master.title('*{} - {}'.format(self.file_name, self.name_app)),
                            self.onRelease(self),
                            setattr(self, 'flag_r', False)))

    def pencilPress(self, event, state):
        if state==1:
            color=self.choose_color
        else:
            color=self.service_color
        x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
        y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
        self.canvas.create_oval(x-0.5, y-0.5, x+0.5, y+0.5, fill=color, width=0)
        self.previous_point=x, y
        self.coords.append(x)
        self.coords.append(y)

    def pencilMotion(self, event, state):
        if state==1:
            color=self.choose_color
        else:
            color=self.service_color
        try:
            x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
            y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
            xOld, yOld=self.previous_point
            self.canvas.create_line(xOld, yOld, x, y, smooth=1, fill=color, width=1, capstyle=tk.ROUND)
            self.coords.append(x)
            self.coords.append(y)
            self.previous_point=x, y
        except:
            pass

    def eraserPress(self, event):
        x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
        y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
        width=self.eraser_width/2
        self.canvas.create_oval(x-width, y-width, x+width, y+width, fill=self.bg_color, width=0)
        self.previous_point=x, y
        self.coords.append(x)
        self.coords.append(y)

    def eraserMotion(self, event):
        x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
        y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
        xOld, yOld=self.previous_point
        self.canvas.create_line(xOld, yOld, x, y, smooth=1, fill=self.bg_color, width=self.eraser_width, capstyle=tk.ROUND)
        self.coords.append(x)
        self.coords.append(y)
        self.previous_point=x, y

    def brushPress(self, event, state):
        if state==1:
            color=self.choose_color
        else:
            color=self.service_color
        x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
        y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
        width=self.width_brush/2
        self.canvas.create_oval(x-width, y-width, x+width, y+width, fill=color, width=0)
        self.previous_point=x, y
        self.coords.append(x)
        self.coords.append(y)

    def brushMotion(self, event, state):
        if state==1:
            color=self.choose_color
        else:
            color=self.service_color
        try:
            x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
            y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
            xOld, yOld=self.previous_point
            self.canvas.create_line(xOld, yOld, x, y, smooth=1, fill=color, width=self.width_brush, capstyle=tk.ROUND)
            self.coords.append(x)
            self.coords.append(y)
            self.previous_point=x, y
        except:
            pass

    def lineMotion(self, event, state):
        if state==1:
            color=self.choose_color
        else:
            color=self.service_color
        try:
            x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
            y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
            xOld, yOld=self.previous_point
            if not self.drawn_shape:
                self.drawn_shape=self.canvas.create_line(xOld, yOld, x, y, capstyle=tk.ROUND,
                                                     width=self.width, fill=color)
            else:
                self.canvas.coords(self.drawn_shape, xOld, yOld, x, y)
                self.coords=[xOld, yOld, x, y]
        except:
            pass

    def ovalMotion(self, event, state):
        if state==1:
            color_outline=self.choose_color
            color_fill=self.service_color
        else:
            color_outline=self.service_color
            color_fill=self.choose_color
        try:
            x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
            y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
            xOld, yOld=self.previous_point
            if not self.drawn_shape:
                if self.option_fill == 'fill':
                    color_fill=color_outline
                    color_outline = ''
                    self.drawn_shape = self.canvas.create_oval(xOld, yOld, x, y, width=self.width,
                                                               outline=color_outline, fill=color_fill)
                else:
                    if self.option_fill=='outline':
                        color_fill=''
                    self.drawn_shape=self.canvas.create_oval(xOld, yOld, x, y, width=self.width,
                                                         outline=color_outline, fill=color_fill)
            else:
                self.canvas.coords(self.drawn_shape, xOld, yOld, x, y)
                self.coords=[xOld, yOld, x, y]
        except:
            pass

    def rectangleMotion(self, event, state):
        if state==1:
            color_outline=self.choose_color
            color_fill=self.service_color
        else:
            color_outline=self.service_color
            color_fill=self.choose_color
        try:
            x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
            y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
            xOld, yOld=self.previous_point
            if not self.drawn_shape:
                if self.option_fill == 'fill':
                    color_fill=color_outline
                    color_outline = ''
                    self.drawn_shape = self.canvas.create_rectangle(xOld, yOld, x, y, width=self.width,
                                                                    outline=color_outline, fill=color_fill)
                else:
                    if self.option_fill=='outline':
                        color_fill=''
                    self.drawn_shape=self.canvas.create_rectangle(xOld, yOld, x, y, width=self.width,
                                                         outline=color_outline, fill=color_fill)
            else:
                self.canvas.coords(self.drawn_shape, xOld, yOld, x, y)
                self.coords=[xOld, yOld, x, y]
        except:
            pass

    def triangleMotion(self, event, state):
        if state==1:
            color_outline=self.choose_color
            color_fill=self.service_color
        else:
            color_outline=self.service_color
            color_fill=self.choose_color
        try:
            x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
            y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
            xOld, yOld=self.previous_point
            if not self.drawn_shape:
                if self.option_fill == 'fill':
                    color_fill=color_outline
                    color_outline = ''
                    self.drawn_shape = self.canvas.create_polygon(xOld, yOld, xOld + (x - xOld) // 2, y, x, yOld,
                                                                  width=self.width, fill=color_fill,
                                                                  outline=color_outline)
                else:
                    if self.option_fill=='outline':
                        color_fill=''
                    self.drawn_shape=self.canvas.create_polygon(xOld, yOld, xOld+(x-xOld)//2, y, x, yOld,
                                        width=self.width, fill=color_fill, outline=color_outline)
            else:
                self.canvas.coords(self.drawn_shape, xOld, yOld, xOld+(x-xOld)//2, y, x, yOld)
                self.coords=[xOld, yOld, x, y]
        except:
            pass

    def buttonPress(self, event):
        x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
        y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
        self.previous_point=x, y

    def createTextWidget(self, event):
        x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
        y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
        self.text_widget=self.canvas.create_text(x, y, text=self.text, fill=self.choose_color,
                        font=(self.type_font, self.size_font, self.outline_font), anchor='nw')
        self.coords.append(x)
        self.coords.append(y)

    def drawText(self, event=None):
        if self.coords and self.text_widget:
            self.canvas.image=draw.text(self.image, self.coords, self.text,
                        (self.type_font, round(self.size_font*self.master.call('tk', 'scaling')),
                         self.outline_font), self.choose_color)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
            self.text_widget=False
            self.coords=[]
            self.changed = True
            self.master.title('*{} - {}'.format(self.file_name, self.name_app)),

    def drawPencil(self, event, state):
        if state==1:
            color=self.choose_color
        else:
            color=self.service_color
        try:
            '''self.image =self.canvas.postscript(colormode='color')
            self.image=Image.open(io.BytesIO(self.image.encode('utf-8')))
            self.image.
            self.image=self.image.convert('RGB')
            self.canvas.image=ImageTk.PhotoImage(self.image)
            self.image.show('Изображение')'''
            draw.pencilPress(self.image, (self.coords[0], self.coords[1]), color, 1)
            self.canvas.image=draw.pencilMotion(self.image, self.coords, color, 1)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        except:
            pass
        self.previous_point=[]
        self.coords=[]

    def drawEraser(self, event):
        try:
            draw.pencilPress(self.image, (self.coords[0], self.coords[1]), self.bg_color, self.eraser_width)
            self.canvas.image=draw.pencilMotion(self.image, self.coords, self.bg_color, self.eraser_width)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        except:
            pass
        self.previous_point=[]
        self.coords=[]

    def drawBrush(self, event, state):
        if state==1:
            color=self.choose_color
        else:
            color=self.service_color
        try:
            draw.pencilPress(self.image, (self.coords[0], self.coords[1]), color, self.width_brush)
            self.canvas.image=draw.pencilMotion(self.image, self.coords, color, self.width_brush)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        except:
            pass
        self.previous_point=[]
        self.coords=[]

    def drawFloodfill(self, event, state):
        if state==1:
            color=self.choose_color
        else:
            color=self.service_color
        self.canvas.config(cursor="wait")
        x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
        y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
        self.canvas.image=draw.floodfill(self.image, (x, y), color)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        self.canvas.config(cursor="tcross")

    def pipetteGet(self, event, state):
        x=event.x+self.scrollbar_x.get()[0]*self.scrollregion[2]
        y=event.y+self.scrollbar_y.get()[0]*self.scrollregion[3]
        if state==1:
            self.choose_color=draw.getpixel(self.image, (x, y))
            self.image_custom_color=init.createColorImage(self.choose_color, (20, 20))
            if not self.colorbar_toplevel:
                self.colorbar.btn_custom_color.config(image=self.image_custom_color)
            else:
                self.colorbar_toplevel.colorbar.btn_custom_color.config(image=self.image_custom_color)
        else:
            self.service_color=draw.getpixel(self.image, (x, y))
            self.image_invert_color = init.createColorImage(self.service_color, (20, 20))
            if not self.colorbar_toplevel:
                self.colorbar.btn_invert_color.config(image=self.image_invert_color)
            else:
                self.colorbar_toplevel.colorbar.btn_invert_color.config(image=self.image_invert_color)

    def drawLine(self, event, state):
        if state==1:
            color=self.choose_color
        else:
            color=self.service_color
        try:
            self.canvas.image=draw.line(self.image, self.coords, color, self.width)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        except:
            pass
        self.previous_point=[]
        self.coords=[]
        self.drawn_shape=None

    def drawOval(self, event, state):
        if state==1:
            color_outline=self.choose_color
            color_fill=self.service_color
        else:
            color_outline=self.service_color
            color_fill=self.choose_color
        try:
            if self.option_fill == 'fill':
                color_fill=color_outline
                color_outline = None
                self.canvas.image = draw.oval(self.image, self.coords, color_outline, color_fill, self.width)
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
            else:
                if self.option_fill=='outline':
                    color_fill=None
                self.canvas.image=draw.oval(self.image, self.coords, color_outline, color_fill, self.width)
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        except:
            pass
        self.previous_point=[]
        self.coords=[]
        self.drawn_shape=None

    def drawRectangle(self, event, state):
        if state==1:
            color_outline=self.choose_color
            color_fill=self.service_color
        else:
            color_outline=self.service_color
            color_fill=self.choose_color
        try:
            if self.option_fill == 'fill':
                color_fill=color_outline
                color_outline = None
                self.canvas.image = draw.rectangle(self.image, self.coords, color_outline, color_fill, self.width)
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
            else:
                if self.option_fill=='outline':
                    color_fill=None
                self.canvas.image=draw.rectangle(self.image, self.coords, color_outline, color_fill, self.width)
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        except:
            pass
        self.previous_point=[]
        self.coords=[]
        self.drawn_shape=None

    def drawTriangle(self, event, state):
        if state==1:
            color_outline=self.choose_color
            color_fill=self.service_color
        else:
            color_outline=self.service_color
            color_fill=self.choose_color
        try:
            if self.option_fill == 'fill':
                color_fill=color_outline
                color_outline = None
                self.canvas.image = draw.triangle(self.image, self.coords, color_outline, color_fill, self.width)
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
            else:
                if self.option_fill=='outline':
                    color_fill=None
                self.canvas.image=draw.triangle(self.image, self.coords, color_outline, color_fill, self.width)
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
        except:
            pass
        self.previous_point=[]
        self.coords=[]
        self.drawn_shape=None

    def flipImageLeftRight(self):
        self.image=self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.canvas.delete("all")
        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")
        self.changed = True
        self.master.title('*{} - {}'.format(self.file_name, self.name_app))

    def flipImageTopBottom(self):
        self.image=self.image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        self.canvas.delete("all")
        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")
        self.changed = True
        self.master.title('*{} - {}'.format(self.file_name, self.name_app))

    def rotateImage(self):
        self.image=self.image.rotate(-90, expand=True)
        self.scrollregion = (0, 0, self.image.size[0], self.image.size[1])
        self.canvas.config(width=self.image.size[0], height=self.image.size[1],
                           scrollregion=self.scrollregion)
        self.canvas.delete("all")
        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")
        self.changed = True
        self.master.title('*{} - {}'.format(self.file_name, self.name_app))

    def invertImageColors(self):
        self.image=draw.inverImageColor(self.image)
        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")
        self.changed = True
        self.master.title('*{} - {}'.format(self.file_name, self.name_app))

if __name__ == "__main__":
    root = ThemedTk()
    root.withdraw()
    root.state("zoomed")
    root.geometry("540x420")
    root.minsize(360, 340)

    root.style = ThemedStyle()
    root.style.theme_use("default")

    app = App(root)
    root.deiconify()
    root.mainloop()