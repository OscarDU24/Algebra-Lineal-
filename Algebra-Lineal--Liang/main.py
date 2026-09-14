import tkinter as tk
from ui.dashboard import Dashboard 

def main():
    root = tk.Tk()
    
    root.title("Calculadoras Matemáticas - FIA")
    root.geometry("980x780")
    root.resizable(False, False) 
    
    app = Dashboard(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()