from PIL import Image
import argparse

#命令行输入参数处理
parser = argparse.ArgumentParser()
#为了防止字符长宽比导致图像边窄，默认将width和height设置为2：1
parser.add_argument('file')     #输入文件
parser.add_argument('-o', '--output',help="指定输出文件的名字")
parser.add_argument('--width', type = int, default = 100,help="指定输出字符画宽")
parser.add_argument('--height', type = int, default = 50,help="指定输出字符画高")
parser.add_argument('-l','--level',type=int,choices=[0,1],default=0,help="指定字符集复杂程度,数字越高越复杂")

#获取参数
args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

ascii_char0=list("@%*o!: ")
ascii_char1 = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# 将256灰度映射到70个字符上
#计算索引时除256是为了使index最大为69 防止越界
def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    if args.level==0:
        length0 = len(ascii_char0)
        return ascii_char0[int(gray/256.0*length0)]
    elif args.level==1:
        length1=len(ascii_char1)
        return ascii_char1[int(gray/256.0*length1)]
    

if __name__ == '__main__':

    im = Image.open(IMG)
    im = im.resize((WIDTH,HEIGHT), Image.NEAREST)
    # PIL.Image.NEAREST：最低质量， PIL.Image.BILINEAR：双线性，
    #PIL.Image.BICUBIC：三次样条插值，Image.ANTIALIAS：最高质量

    txt = ""

    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j,i)))
        txt += '\n'

    print(txt)

    #字符画输出到文件
    if OUTPUT:
        with open(OUTPUT,'w') as f:
            f.write(txt)
    else:
        with open("output.txt",'w') as f:
            f.write(txt)
