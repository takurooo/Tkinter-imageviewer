 #--------------------------------------------------------
 # import
 #--------------------------------------------------------
import os
import glob
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfd

 #--------------------------------------------------------
 # defines
 #--------------------------------------------------------
MAIN_DISPLAY_SIZE = "800x600"

 #--------------------------------------------------------
 # functions
 #--------------------------------------------------------
class ImageViewer():
    CANVAS_WIDTH = 600
    CANVAS_HEIGHT = 450

    def __init__(self, master):
        self.parent = master
        self.parent.title("ImageViewer")
        self.parent.resizable(width=tk.TRUE, height=tk.TRUE)
        self.parent.bind("<Left>", self.prev)
        self.parent.bind("<Right>", self.next)

        self.init_menubar()

        self.init_imageviewer()

    def init_menubar(self):
        menubar = tk.Menu(self.parent)
        self.parent.configure(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Dir", underline=0, menu=file_menu)
        file_menu.add_command(label="Open", underline=0, command=self.open_dir)


    def init_imageviewer(self):
        # main frame
        self.mframe = tk.Frame(self.parent)
        self.mframe.pack(fill=tk.BOTH, expand=1)

        # image frame
        self.iframe = tk.Frame(self.mframe)
        self.iframe.pack()
        self.image_canvas = tk.Canvas(self.iframe, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,cursor='plus')
        self.image_canvas.pack(pady=0, anchor=tk.N)

        # control frame
        self.cframe = tk.Frame(self.mframe)
        self.cframe.pack(side=tk.TOP, padx=5, pady=10)
        self.prev_button = ttk.Button(self.cframe, text='<<', width=10, command=self.prev)
        self.prev_button.pack(side = tk.LEFT, padx=5)
        self.next_button = ttk.Button(self.cframe, text='>>', width=10, command=self.next)
        self.next_button.pack(side = tk.LEFT, padx=5)

        self.images = list()
        self.image_maxreso = dict()
        self.image_tk = None
        self.image_dir = None
        self.image_idx = 0
        self.image_cnt = 0

    def delete(self):
        # delete str in entrybox.
        self.dir_entry.delete(0, tk.END)

    def prev(self, event=None):
        if 0 < self.image_idx:
            self.image_idx -= 1
            self.show_image(self.image_idx)

    def next(self, event=None):
        if self.image_idx < (self.image_cnt-1):
            self.image_idx += 1
            self.show_image(self.image_idx)

    def show_image(self, idx):
        DISP_X = 0
        DISP_Y = 0

        if idx < 0 or idx >= self.image_cnt:
            raise ValueError("imageidx invalid")

        new_canvas_widht = max(self.image_maxreso["width"], self.CANVAS_WIDTH)
        new_canvas_height = max(self.image_maxreso["height"], self.CANVAS_HEIGHT)
        self.image_canvas.config(width=new_canvas_widht, height=new_canvas_height)

        self.image_tk = ImageTk.PhotoImage(self.images[idx])
        self.image_canvas.create_image(DISP_X, DISP_Y, image=self.image_tk, anchor=tk.NW)

    def open_dir(self):
        self.image_dir = tkfd.askdirectory()

        if self.image_dir == "":
            return

        if not os.path.exists(self.image_dir):
            tkmsg.showwarning("Warning", message="{} doesn't exist.".format(self.image_dir))
            return

        if not os.path.isdir(self.image_dir):
            tkmsg.showwarning("Warning", message="{} isn't dir.".format(self.image_dir))
            return

        image_paths = list()
        accepted_ext = (".jpeg", '.jpg', '.png')
        for ext in accepted_ext:
            image_paths.extend(glob.glob(os.path.join(self.image_dir, "*"+ext)))

        self.images = list()
        self.image_maxreso["height"] = 0
        self.image_maxreso["width"] = 0
        for image_path in image_paths:
            self.images.append(Image.open(image_path))
            height = self.images[-1].height
            width = self.images[-1].width
            if self.image_maxreso["height"] < height and self.image_maxreso["width"] < width:
                self.image_maxreso["height"] = height
                self.image_maxreso["width"] = width

        image_cnt = len(self.images)
        if image_cnt == 0:
            tkmsg.showwarning("Warning", message="image doesn't exist.")
            return

        self.image_idx = 0
        self.image_cnt = image_cnt

        self.show_image(self.image_idx)

#--------------------------------------------------------
 # main
 #--------------------------------------------------------
if __name__ == '__main__':
    root = tk.Tk()
    ImageViewer(root)
    root.resizable(width=True, height=True)
    root.geometry(MAIN_DISPLAY_SIZE)
    root.mainloop()
