from PIL import Image, ImageTk, ImageDraw, ImageColor, ImageFont, ImageOps

def pencilPress(image, coords, fill, width):
    draw=ImageDraw.Draw(image)
    x, y=coords[0], coords[1]
    width/=2
    draw.ellipse((x-width, y-width, x+width, y+width), fill=fill, width=0)
    image=ImageTk.PhotoImage(image)
    return image

def pencilMotion(image, coords, fill, width):
    draw=ImageDraw.Draw(image)
    x, y=coords[-2], coords[-1]
    draw.line(coords, fill=fill, width=width, joint='curve')
    draw.ellipse((x-width/2, y-width/2, x+width/2, y+width/2), fill=fill, width=0)
    image=ImageTk.PhotoImage(image)
    return image

def floodfill(image, coords, fill):
    ImageDraw.floodfill(image, coords, ImageColor.getrgb(fill), thresh=10)
    image=ImageTk.PhotoImage(image)
    return image

def line(image, coords, fill, width):
    draw=ImageDraw.Draw(image)
    draw.line(coords, fill=fill, width=width, joint='curve')
    width/=3
    draw.ellipse((coords[0]-width, coords[1]-width, coords[0]+width,
                coords[1]+width), fill=fill, width=0)
    draw.ellipse((coords[2]-width, coords[3]-width, coords[2]+width,
                coords[3]+width), fill=fill, width=0)
    image=ImageTk.PhotoImage(image)
    return image

def oval(image, coords, outline, fill, width):
    draw=ImageDraw.Draw(image)
    coords=[min(coords[0], coords[2]), min(coords[1], coords[3]),
            max(coords[0], coords[2]), max(coords[1], coords[3])]
    draw.ellipse(coords, fill=fill, outline=outline, width=width)
    image=ImageTk.PhotoImage(image)
    return image

def rectangle(image, coords, outline, fill, width):
    draw=ImageDraw.Draw(image)
    coords=[min(coords[0], coords[2]), min(coords[1], coords[3]),
            max(coords[0], coords[2]), max(coords[1], coords[3])]
    draw.rectangle(coords, fill=fill, outline=outline, width=width)
    image=ImageTk.PhotoImage(image)
    return image

def triangle(image, coords, outline, fill, width):
    draw=ImageDraw.Draw(image)
    xOld, yOld, x, y=coords
    coords=[xOld, yOld, xOld+(x-xOld)//2, y, x, yOld]
    draw.polygon(coords, fill=fill, outline=outline)
    coords.append(xOld)
    coords.append(yOld)
    if outline:
        draw.line(coords, fill=outline, joint="curve", width=width)
        width/=3
        draw.ellipse((x-width, yOld-width, x+width, yOld+width), fill=outline, width=0)
        draw.ellipse((xOld-width, yOld-width, xOld+width, yOld+width), fill=outline, width=0)
        draw.ellipse((xOld+(x-xOld)//2-width, y-width, xOld+(x-xOld)//2+width, y+width),
                         fill=outline, width=0)
    image=ImageTk.PhotoImage(image)
    return image    

def text(image, coords, text, font, fill):
    draw=ImageDraw.Draw(image)
    type_font=font[0]
    size_font=int(font[1])
    outline_font=font[2]
    arial=['C:\Windows\Fonts\ARIALN.TTF', 'C:\Windows\Fonts\ARIALNB.TTF',
            r'C:\Windows\Fonts\ARIALNI.TTF', 'C:\Windows\Fonts\ARIALNBI.TTF']
    times=[r'C:\Windows\Fonts\times.ttf', r'C:\Windows\Fonts\timesbd.ttf',
            r'C:\Windows\Fonts\timesi.ttf', r'C:\Windows\Fonts\timesbi.ttf']
    calibri=[r'C:\Windows\Fonts\calibri.ttf', r'C:\Windows\Fonts\calibrib.ttf',
            r'C:\Windows\Fonts\calibrii.ttf', r'C:\Windows\Fonts\calibriz.ttf']
    segoe=[r'C:\Windows\Fonts\segoeui.ttf', r'C:\Windows\Fonts\segoeuib.ttf',
            r'C:\Windows\Fonts\segoeuii.ttf', r'C:\Windows\Fonts\segoeuiz.ttf']
    comic=[r'C:\Windows\Fonts\comic.ttf', r'C:\Windows\Fonts\comicbd.ttf',
            r'C:\Windows\Fonts\comici.ttf', r'C:\Windows\Fonts\comicz.ttf']
    courier=[r'C:\Windows\Fonts\cour.ttf', r'C:\Windows\Fonts\courbd.ttf',
            r'C:\Windows\Fonts\couri.ttf', r'C:\Windows\Fonts\courbi.ttf']
    if 'normal' in outline_font and 'roman' in outline_font:
        i=0
    elif  'bold' in outline_font and 'roman' in outline_font:
        i=1
    elif  'normal' in outline_font and 'italic' in outline_font:
        i=2
    elif  'bold' in outline_font and 'italic' in outline_font:
        i=3
    if type_font=='Arial':
        font_draw=arial[i]
    elif type_font=='Times New Roman':
        font_draw=times[i]
    elif type_font=='Calibri':
        font_draw=calibri[i]
    elif type_font=='Segoe UI':
        font_draw=segoe[i]
    elif type_font=='Comic Sans Ms':
        font_draw=comic[i]
    elif type_font == 'Courier':
        font_draw=courier[i]
    font_draw=ImageFont.truetype(font_draw, size_font)
    if text:
        draw.text(coords ,text=text, fill=fill, font=font_draw, encoding='Unicode')
    image=ImageTk.PhotoImage(image)
    return image  
        
def getpixel(image, coords): 
    return '#%02x%02x%02x' % image.getpixel((coords))

def inverImageColor(image):
    image = ImageOps.invert(image)
    return image