from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from funciones.Segmentacion import *


class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.buildUI()
        self.parent.config(menu=self.menubar)

    def buildUI(self):

        self.parent.title("segmentacion ")
        self.pack()

        self.menubar = Menu(root)

        self.filemenu = Menu(self.menubar, tearoff=0)

        self.filemenu.add_command(label="Abrir", command=self.loadFile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Salir", command=self.parent.quit)

        self.menubar.add_cascade(label="Archivo", menu=self.filemenu)
        self.menubar.add_command(label="Discontinuidad", command=lambda: self.procesar("D"))
        self.menubar.add_command(label="Similitud", command=lambda: self.procesar("S"))
        self.filtersmenu = Menu(self.menubar, tearoff=0)

        canvasContainer = Frame(self.parent)
        canvasContainer.pack(side=TOP)
        self.canvas = Canvas(canvasContainer, width=50, height=50)
        self.canvas.pack(side=LEFT, padx=5, pady=15)
        self.edit_canvas = Canvas(canvasContainer, width=50, height=50)
        self.edit_canvas.pack(side=RIGHT, padx=5, pady=15)

        scaleContainer = Frame(self.parent)
        scaleContainer.pack(side=BOTTOM)
        # componentes de nivel
        self.w = Label(root, text="nivel")
        self.label = Label(root, textvariable="datos", relief=RAISED)
        return

    def updateCanvas(self, i, original=False):
        i = Image.open(i)
        w, h = i.size
        self.editImage = ImageTk.PhotoImage(i)
        self.edit_canvas.configure(width=w, height=h)
        self.edit_canvas.create_image(w / 2, h / 2, image=self.editImage)
        if(original):
            self.canvasImage = self.editImage
            self.canvas.configure(width=w, height=h)
            self.canvas.create_image(w / 2, h / 2, image=self.canvasImage)
        return

    def loadFile(self):
        global image, lastImage
        filename = askopenfilename(filetypes=[
                                   ("JPEG", "*.jpg"),
                                   ("JPEG", "*.jpeg"),
                                   ("PNG", "*.png")])
        if(filename):
            try:
                image = filename
                lastImage = image
                print(image)
                self.updateCanvas(image, original=True)

            except:
                print("Error opening file or file does not exists")
                showerror("Open Source File", "Failed to read file\n'%s'" % filename)
        return

    def procesar(self, tipo):
        self.imagen = Imagen(image, 'L')
        if(tipo == "D"):
            self.imagen = Discontinuidad(self.imagen)
        elif(tipo == "S"):
            self.imagen = Similitud(self.imagen)
        print("-------------------------------------------------------------------------------------------------------")
        app.updateCanvas("new.png")


root = Tk()
app = App(root)
image, lastImage = None, None
root.mainloop()
