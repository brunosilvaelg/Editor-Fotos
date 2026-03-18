import os
import io
import threading
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageDraw, ImageOps
from rembg import remove

def create_circular_image(input_image: Image, size: int):
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    img_fitted = ImageOps.contain(input_image, (size, size), method=Image.Resampling.LANCZOS)
    
    img_w, img_h = img_fitted.size
    offset_x = (size - img_w) // 2
    offset_y = (size - img_h) // 2
    canvas.paste(img_fitted, (offset_x, offset_y), mask=img_fitted if img_fitted.mode == 'RGBA' else None)

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    final_white_bg = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    final_white_bg.paste(canvas, (0, 0), mask=mask)

    return final_white_bg

class EditorApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Editor de Fotos Circular")
        self.geometry("450x450")
        self.resizable(False, False)

        self.size_var = ttk.IntVar(value=400)
        self.format_var = ttk.StringVar(value="PNG")

        self.create_widgets()

    def create_widgets(self):
        title_label = ttk.Label(self, text="Remover Fundo e Criar Círculo", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=20)

        size_frame = ttk.LabelFrame(self, text="Tamanho da Imagem")
        size_frame.pack(fill=X, padx=20, pady=10)
        ttk.Radiobutton(size_frame, text="100x100 pixels", variable=self.size_var, value=100).pack(side=LEFT, padx=10, pady=10)
        ttk.Radiobutton(size_frame, text="400x400 pixels", variable=self.size_var, value=400).pack(side=LEFT, padx=10, pady=10)

        format_frame = ttk.LabelFrame(self, text="Formato de Exportação")
        format_frame.pack(fill=X, padx=20, pady=10)
        ttk.Radiobutton(format_frame, text="PNG (Qualidade Máxima)", variable=self.format_var, value="PNG").pack(side=LEFT, padx=10, pady=10)
        ttk.Radiobutton(format_frame, text="JPG (Arquivo Menor)", variable=self.format_var, value="JPG").pack(side=LEFT, padx=10, pady=10)

        self.process_btn = ttk.Button(self, text="Selecionar Imagens e Processar", bootstyle=SUCCESS, command=self.start_processing_thread)
        self.process_btn.pack(pady=20, fill=X, padx=20)

        self.progress = ttk.Progressbar(self, bootstyle=INFO, mode='determinate')
        self.progress.pack(fill=X, padx=20, pady=5)

        self.status_label = ttk.Label(self, text="Aguardando arquivos...", font=("Helvetica", 10))
        self.status_label.pack(pady=5)

    def start_processing_thread(self):
        file_paths = filedialog.askopenfilenames(
            title="Escolha as imagens",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
        )
        
        if not file_paths:
            return

        save_dir = filedialog.askdirectory(title="Escolha a pasta para salvar os resultados")
        
        if not save_dir:
            return

        self.process_btn.config(state=DISABLED)
        self.progress['maximum'] = len(file_paths)
        self.progress['value'] = 0

        thread = threading.Thread(target=self.process_images, args=(file_paths, save_dir))
        thread.daemon = True
        thread.start()

    def process_images(self, file_paths, save_dir):
        target_size = self.size_var.get()
        export_format = self.format_var.get()

        for i, file_path in enumerate(file_paths):
            filename = os.path.basename(file_path)
            self.status_label.config(text=f"Processando: {filename}")
            
            try:
                with open(file_path, 'rb') as f:
                    input_image_bytes = f.read()

                input_image = Image.open(io.BytesIO(input_image_bytes)).convert("RGBA")
                output_nobg_bytes = remove(input_image_bytes)
                output_nobg = Image.open(io.BytesIO(output_nobg_bytes))

                final_image = create_circular_image(output_nobg, target_size)

                base_name = os.path.splitext(filename)[0]
                
                if export_format == "PNG":
                    save_path = os.path.join(save_dir, f"{base_name}_circulo_{target_size}.png")
                    final_image.save(save_path, format="PNG")
                else:
                    save_path = os.path.join(save_dir, f"{base_name}_circulo_{target_size}.jpg")
                    final_rgb = final_image.convert("RGB")
                    final_rgb.save(save_path, format="JPEG", quality=95)

            except Exception as e:
                print(f"Erro ao processar {filename}: {e}")

            self.progress['value'] = i + 1
            self.update_idletasks()

        self.status_label.config(text="Processamento concluído com sucesso!")
        self.process_btn.config(state=NORMAL)
        messagebox.showinfo("Concluído", "Todas as imagens foram processadas e salvas na pasta escolhida.")

if __name__ == "__main__":
    app = EditorApp()
    app.mainloop()