from TkinterWrapper import *


class RGBContainer(object):
    def __init__(self,parrent_canvas,color=None):
        self.__setup_variables(parrent_canvas)
        if not(color is None):
            self.__save_color(color)
            
    def __setup_variables(self,parrent_canvas):
        self.rgb=(0,0,0)
        self.parrent_canvas=parrent_canvas
        
    def __save_color(self,color):
        if type(color).__name__=="str":
            self.rgb=self.parrent_canvas.winfo_rgb(color)
            self.rgb=(self.rgb[0],self.rgb[1],self.rgb[2])
        elif type(color).__name__=="tuple":
            self.rgb=(color[0]*256,color[1]*256,color[2]*256)
        # add hex conversion latter
        
    def get_value(self,rgb=None):
        if rgb.lower()=='r':
            return self.rgb[0]
        elif rgb.lower()=='g':
            return self.rgb[1]
        elif rgb.lower()=='b':
            return self.rgb[2]
        elif rgb is None:
            return self.rgb
        
        
class ArithmeticSequence(object):
    def __init__(self,start_value=None,end_value=None,number_of_terms=None):
        self.configure(start_value,end_value,number_of_terms)
            
    def configure(self,start_value=None,end_value=None,number_of_terms=None):
        if not(start_value is None) and not(end_value is None) and not(number_of_terms is None):
            self.number_of_terms=number_of_terms
            self.__make_explicit_formula(start_value,end_value)
        
    def __make_explicit_formula(self,start_value,end_value):
        rate=(end_value-start_value)/(self.number_of_terms)
        self.explicit_formula=lambda n: start_value+(rate*n)
        
    def evaluate_for(self,number):
        if number<self.number_of_terms:
            return self.explicit_formula(number)
        
        
class CanvasGradient(object):
    def __init__(self,canvas,start_color,stop_color):
        self.canvas=canvas
        self.configure(start_color,stop_color)
        self.canvas.bind("<Configure>",lambda *args: self.__redraw_gradient(),add="+")
        
    def configure(self,start_color,stop_color):
        self.start_color=RGBContainer(self.canvas,start_color)
        self.stop_color=RGBContainer(self.canvas,stop_color)
        self.r_sequence=ArithmeticSequence()
        self.g_sequence=ArithmeticSequence()
        self.b_sequence=ArithmeticSequence()
        self.__redraw_gradient()
        
    def __redraw_gradient(self):
        self.__update_sequences()
        self.__draw_gradient()
        
    def __update_sequences(self):
        self.r_sequence.configure(self.start_color.get_value('r'),self.stop_color.get_value('r'),self.canvas.winfo_width())
        self.b_sequence.configure(self.start_color.get_value('b'),self.stop_color.get_value('b'),self.canvas.winfo_width())
        self.g_sequence.configure(self.start_color.get_value('g'),self.stop_color.get_value('g'),self.canvas.winfo_width())
        
    def __draw_gradient(self):
        self.canvas.delete("Gradient")
        for x in range(1,self.canvas.winfo_width()):
            r=int(self.r_sequence.evaluate_for(x))
            g=int(self.g_sequence.evaluate_for(x))
            b=int(self.b_sequence.evaluate_for(x))
            rgb_string="#{0:04x}{1:04x}{2:04x}".format(r,g,b)
            self.canvas.create_line(x,0,x,self.canvas.winfo_height(),fill=rgb_string,tags=("Gradient"))
        self.canvas.tag_lower("Gradient")
        self.canvas.update()


class App(Window):
    def __init__(self,name):
        super(App, self).__init__(name,False,"grey96")
        super(App, self).geometry("500x200+0+0")
        self.__setup_canvas()
        self.__setup_info_row()
        
    def __setup_canvas(self):
        self.canvas=WindowCanvas(self,100,100,PackStyle(side="top",fill='both',expand=True)) 
        self.canvas_gradient=CanvasGradient(self.canvas,'black','white')
        
    def __setup_info_row(self):
        self.left_rgb_label=WindowLabel(self,"R:000 G:000 B:000",PackStyle(side="left",padx=50))
        self.run_button=WindowButton(self,"Run Gradients!",self.__run_gradients,PackStyle(side="left"))
        self.right_rgb_label=WindowLabel(self,"R:000 G:000 B:000",PackStyle(side="left",padx=50))
        self.left_rgb_label.configure(fg="grey10",bg="grey96",font=("MsSans","14","normal"))
        self.right_rgb_label.configure(fg="grey10",bg="grey96",font=("MsSans","14","normal"))
        
    def __run_gradients(self):
        for x in range(0,256):
            self.canvas_gradient.configure((0,0,x),(0,0,256-x))
            self.__update_rgb_label("left",0,0,x)
            self.__update_rgb_label("right",0,0,256-x)
        for x in range(0,256):
            self.canvas_gradient.configure((0,x,0),(0,256-x,0))
            self.__update_rgb_label("left",0,x,0)
            self.__update_rgb_label("right",0,256-x,0)
        for x in range(0,256):
            self.canvas_gradient.configure((x,0,0),(256-x,0,0))
            self.__update_rgb_label("left",x,0,0)
            self.__update_rgb_label("right",256-x,0,0)
        for x in range(0,256):
            self.canvas_gradient.configure((abs(x),abs(x-128),abs(x-256)),(abs(x-256),abs(x-128),abs(x)))
            self.__update_rgb_label("left",abs(x),abs(x-128),abs(x-256))
            self.__update_rgb_label("right",abs(x-256),abs(x-128),abs(x))
        self.__add_gradient_run_info()
        
    def __update_rgb_label(self,side,r,g,b):
        if side.lower()=="left":
            self.left_rgb_label.configure(text="R:{0:03} G:{1:03} B:{2:03}".format(r,g,b))
        else:
            self.right_rgb_label.configure(text="R:{0:03} G:{1:03} B:{2:03}".format(r,g,b))
        
    def __add_gradient_run_info(self):
        self.canvas.create_text(self.canvas.winfo_width()/2,self.canvas.winfo_height()/2,fill="White",
                                text="Run was Successfull!",font=("MsSans","20","italic"),tags=("Info"))
        self.canvas.update()
        self.after(1000,lambda: self.canvas.delete("Info"))
        
app=App("Gradient Test")
app.mainloop()
