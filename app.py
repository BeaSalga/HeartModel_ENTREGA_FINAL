import tkinter as tk
from tkinter import ttk
from main import GraphicsEngine
import random


class App:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Simulador de Ritmos Cardiacos")
        self.ventana.geometry("600x500")
        self.ventana.configure(bg="#f7f7f7")

        self.seleccion = tk.StringVar(value="")
        self.comparacion = tk.StringVar(value="")

        self.frame_principal = tk.Frame(self.ventana, bg="#f7f7f7")
        self.frame_comparacion = tk.Frame(self.ventana, bg="#f7f7f7")

        self.crear_pantalla_principal()
        self.crear_pantalla_comparacion()

        self.mostrar_pantalla_principal()

    def crear_pantalla_principal(self):
        tk.Label(
            self.frame_principal,
            text="Selecciona un ritmo cardíaco o una comparación:",
            font=("Helvetica", 14, "bold"),
            bg="#f7f7f7",
            fg="#333333"
        ).pack(pady=10)

        opciones = ["Normal", "Taquicardia", "Bradicardia", "Arritmia", "Comparación"]
        for opcion in opciones:
            ttk.Button(
                self.frame_principal,
                text=opcion,
                command=lambda o=opcion: self.manejar_seleccion_principal(o),
                style="Custom.TButton",
                width=20
            ).pack(pady=10)

        tk.Button(
            self.frame_principal,
            text="Salir",
            command=self.ventana.destroy,
            bg="#d9534f",
            fg="white",
            font=("Helvetica", 12, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=10
        ).pack(pady=20)

    def crear_pantalla_comparacion(self):
        tk.Label(
            self.frame_comparacion,
            text="Opciones de Comparación:",
            font=("Helvetica", 14, "bold"),
            bg="#f7f7f7",
            fg="#333333"
        ).pack(pady=10)

        comparaciones = ["Normal vs Taquicardia", "Normal vs Bradicardia", "Normal vs Arritmia", "Taquicardia vs Arritmia", "Bradicardia vs Arritmia"]
            
        for comp in comparaciones:
            ttk.Button(
                self.frame_comparacion,
                text=comp,
                command=lambda c=comp: self.seleccionar_comparacion(c),
                style="Custom.TButton",
                width=25
            ).pack(pady=10)

        tk.Button(
            self.frame_comparacion,
            text="Volver",
            command=self.mostrar_pantalla_principal,
            bg="#6c757d",
            fg="white",
            font=("Helvetica", 12, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=10
        ).pack(pady=20)

    def manejar_seleccion_principal(self, opcion):
        self.seleccion.set(opcion)
        if opcion == "Comparación":
            self.mostrar_pantalla_comparacion()
        else:
            self.iniciar_simulacion()

    def mostrar_pantalla_principal(self):
        self.frame_comparacion.pack_forget()
        self.frame_principal.pack(fill="both", expand=True)

    def mostrar_pantalla_comparacion(self):
        self.frame_principal.pack_forget()
        self.frame_comparacion.pack(fill="both", expand=True)

    def seleccionar_comparacion(self, comparacion):
        self.comparacion.set(comparacion)
        self.iniciar_simulacion()

    def generar_arritmia_suavizada(self, longitud=100, rango_latido=(0.7, 1.0), rango_pausa=(0.0, 0.3), prob_latido=0.6, pasos_suavizado=5):
        arritmia = []
        ultimo_valor = random.uniform(*rango_pausa)  # Inicia con un valor dentro del rango de pausas

        while len(arritmia) < longitud:
            if random.random() < prob_latido:
                proximo_valor = random.uniform(*rango_latido)
            else:
                proximo_valor = random.uniform(*rango_pausa)

            if len(arritmia) + pasos_suavizado <= longitud:
                transicion = [
                    ultimo_valor + (proximo_valor - ultimo_valor) * (i / pasos_suavizado)
                    for i in range(pasos_suavizado)
                ]
                arritmia.extend(transicion)
            else:
                arritmia.append(proximo_valor)

            ultimo_valor = proximo_valor

        return arritmia[:longitud]
    
    def generate_model(self, opcion, pos):
        mask = [1] * 100
        if opcion == "Normal":
            ppm = random.randint(60,100)
        elif opcion == "Bradicardia":
            ppm = random.randint(30,60)
        elif opcion == "Taquicardia":
            ppm = random.randint(110,160)
        elif opcion == "Arritmia":
            ppm = random.randint(60,100)
            mask = self.generar_arritmia_suavizada()

        return [pos, (0,0,0), (1,1,1), ppm, mask] 

    def get_model_data(self, opcion, comparacion):
        data, position = [opcion], [(0, -2, -10)]
        if comparacion:
            data = comparacion.split(" vs ")
            position = [(-0.8, -2, -10), (0.8, -2, -10)]

        return [self.generate_model(opt, pos) for opt, pos in zip(data, position)]

    def iniciar_simulacion(self):
        seleccion = self.seleccion.get()
        comparacion = self.comparacion.get()

        if seleccion == "Comparación" and not comparacion:
            tk.messagebox.showerror("Error", "Por favor selecciona una comparación.")
        elif seleccion:
            models_data = self.get_model_data(seleccion, comparacion)
            app = GraphicsEngine(models_data, win_size=(1600, 900))
            app.run()

    def run(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
        


