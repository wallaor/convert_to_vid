import tkinter as tk
import random

def form_random_frame(width, height):
    colorMatrix = [[0 for x in range(width)] for y in range(height)]  # создаем пустую матрицу цветов, заполняем её значениями из тайлов
    for y in range(height):
        for x in range(width):
            colorMatrix[y][x] = random.choice(["yellow","black","red","white"])
    return colorMatrix

def bytes_to_hex_color(byte):
    out_int = byte*4
    out_hex = hex(out_int)[2:]
    if len(out_hex) == 1:
        out_hex = "0" + out_hex
    return out_hex

def form_frame_by_hex_set(width, height, hex_list):
    colorMatrix = [[0 for x in range(width)] for y in range(height)]
    offset = 0
    for y in range(height):
        for x in range(width):
            red_bytes = hex_list[(y*width)+x+offset]
            green_bytes = hex_list[(y*width)+x+offset+1]
            blue_bytes = hex_list[(y*width)+x+offset+2]
            red_hex = bytes_to_hex_color(red_bytes)
            green_hex = bytes_to_hex_color(green_bytes)
            blue_hex = bytes_to_hex_color(blue_bytes)
            colorcode = f"#{red_hex}{green_hex}{blue_hex}"
            offset+=2
            colorMatrix[y][x] = colorcode
    return colorMatrix

def form_frame_by_palette(width, height, palette, encoded_frame):
    colorMatrix = [[0 for x in range(width)] for y in range(height)]
    for y in range(height):
        for x in range(width):
            colorMatrix[y][x] = palette[encoded_frame[(y*width) + x]]
    return colorMatrix

def draw_frame(number_of_frame, scaler, colorMatrix):     # 320 200
    width = len(colorMatrix[0])
    height = len(colorMatrix)
    root = tk.Tk()                  # объявляем само окно
    root.title(f"frame {str(number_of_frame)}")     # задаем окну название
    canvas = tk.Canvas(root, width=width*scaler, height=height*scaler)   # создаем внутри главного окна (root) канвас
    for y in range(height):
        for x in range(width):
            x0, y0 = x * scaler, y * scaler
            x1, y1 = x0 + scaler, y0 + scaler
            canvas.create_rectangle(x0, y0, x1, y1, fill = colorMatrix[y][x], width = 0, outline="")
    canvas.pack()
    root.mainloop()
    color_palette = []
    for string in colorMatrix:
        color_palette = color_palette + string
    return color_palette

if __name__ == "__main__":
    draw_frame(1, 3, form_random_frame(320, 200))
    #byteset = b'\x01\x01\x00\x08\x0b\n\x06\x0e\x06\x05\x07\x06\x0f\x11\x11\x07\x08\x04\x08\x0e\x0f\x1b#+\x10\x16\x13\x11\x16\x10"*/")*\r\x15\x16\x10\x17\x04\x12\x10\x04\x0c\x11\x12\x1e1\x08\x16!"\x1a\x1f#\x17\x1d#\x1d\x1f\x1e\x1f \x18\x0c\x0e\x04<><49=\x04\x04\x04\x0e\x0f\n\x18\x1a\x1c:?4664!\x1b\x07\x1c\x19\x0798\x1e83\x10\n\x0c\r???:6\x16\x15\x1a\x1e\x11\x12\t\x17\'\x05\x19\x17\x05\x0e\x0c\x03\x12\x16\x19\x1b)*\x0b\x0c\x08\r\x0e\x0f\x12\x1a\x1a\x13\x1c\x1d\x05\x04\x01\x15\x16\x17/8>\x0c\x1e\x0b\x0c\x18\n$+2!)2/59,49\x1e"&\x1e!#;?? &)\x1d$)\x1a\x1c\x1e+04(.3\x04\x0b\x04)17\x11\x15\x17%+/%**2=?1:?\x15\x1b!\x1b"&\x18$%\x1f%#"&\x1a\x15\x19\x12\x18\x18\x0c\x0e\x12\x18-+\x10.*\x0b);# =\x1f\x16\x1e\x1d \'-\x1d%--5<\r\x11\x15\x1e\x18\x03\x1c\x15\x02\x16\x1a\x19\x11,\x11\x0f$\x0e \x1f\x0f%\x1f\x08%/6\x12\x17\x1d%#\x0e\x1d+,\x0f\x17\x18\x15.\x11\x18\x1c\x10\x1d\x1b\r%+#+,\x18\x15\x16\x0e\x16\x14\x08\x0b\x0e\x0b\x18;\x18\x19*\x19 &&\x07\x13\x07,=,(..6>?\x0c\n\x02\x17\x13\x04\x1c! \x18\x1d\x1a\x0e\x14\x12\x01\x03\x04,$\x08?>\x1e?>\x16!\x1a\x037.\n*%\r$\'\x0e?=\x105/\x0f%\x1d\x03?9\x04?4\x04/$\x03*!\x03<.\x035)\x03??\x04?=\t5*\x07;/\x07>5\t>7\x0f \x1e\x0b\'"\x07\x1c\x1c\t8,\x04?9\x10?8\n;4\x0415\x07??\x1a#& //\x1b)+\x1a33223)\x08\x0e\x03$$\x122(\x0414\x1c\x12\x1f\x08\x15\x17\t\x1c2\x1e?;\x072>50,\x0f(;&\x142\x13\x11)\x10\x1b\x1d\x0f"(\'?>(\x17\x16\x03.8#04\x192)\x08*.\x0f55\x10->*\x1e \x11(&\x0f\x16\x1b\x0875\x0620\x06%2\x07"\'\x1d&\'\x16=>+(. =>748:\x19!\x1e\x08\x08\x07\x15\x10\x07\x0f\x12\x07\x14\x15\x0b!\x16\x04\x0f\x0f\x071-\x0b\'\'\x0c\x1f!\x0c#"\n+)\x0b\x16\x0e\x03\x19\x15\x08\x03\x07\x01$\x18\x04&$\n\x1c\x13\x04! \t02\x0b4,\t)\x1c\x0482\x0b\x15\x12\n,\x1f\x053%\x060 \x04\x19\x18\x0f\x0e\x11\x0c\x1b\x1b\x11\x13\x16\x14\x1a\x1b\x17\x1f \x1c.+\x17<6\x1264\x13+-+(\'\x14,+$9;:\x1e\x1c\x12%"\x15;9\x1b>=0((\x1740\x19! \x15??#54\x19<8\x17-\'\x1643"<9#+<>!/8%5=\x0e\x19\x05$7\x07\x17!&\x1a&-\x1d*3-??\x02\x03\x02'
    #draw_frame(1, 3, form_frame_by_hex_set(16, 16, byteset))