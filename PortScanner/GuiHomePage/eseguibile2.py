import tkinter
from PIL import Image, ImageTk #Perchè di base tkinter non supporta .jpeg e .png
import subprocess #serve a collegare pagine esterne


#Funzione PageSwap
def ApriPortScanner():
    finestra.destroy()
    subprocess.run(["python", "GUIportscanner.py"])
    


#Finestra Default
finestra = tkinter.Tk()
finestra.title("Home Page")
finestra.geometry("400x600")
finestra.configure(bg="#e7cf8a")
frame = tkinter.Frame(bg="#e7cf8a") #Container

#Gestione Immagine
Img = Image.open("Grifone.png")
Img_dimensione = Img.resize((200, 200))
Img_tk = ImageTk.PhotoImage(Img_dimensione)


#Creazione Widget
BottonePort = tkinter.Button(frame, text="Port Scanner", width=16, height=3, font=("Arial", 18), bg="black", fg="#e7cf8a", command=ApriPortScanner)
BottoneRequest = tkinter.Button(frame, text="Web Request", width=16, height=3, font=("Arial", 18), bg="black", fg="#e7cf8a" )
BottoneChiSiamo = tkinter.Button(frame, text="Chi siamo", width=16, height=3, font=("Arial", 18), bg="black", fg="#e7cf8a")
ImgGrifone = tkinter.Label(frame, image=Img_tk, bg="#e7cf8a")



#Posizionameto Widget
ImgGrifone.grid(row=0)
BottonePort.grid(row=1, column=0, columnspan=2)
BottoneRequest.grid(row=2, column=0, columnspan=2, pady=8)
BottoneChiSiamo.grid(row=3, column=0, columnspan=2)


frame.pack(side="top", pady=40)


#MainLoop
finestra.mainloop()
