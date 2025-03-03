import cv2


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class AsciiArt:
    # denser = """@&%QWNM0gB$#DR8mHXKAUbGOpV4d9h6PkqwSE2]ayjxY5Zoen[ult13If}C{iF|(7J)vTLs?z/*cr!+<>;=^,_:'-.` """[::-1]
    denser = 'Ñ@#W$9876543210?!abc;:+=-,._ '[::-1]
    
    def __init__(self, path, width=130, height=130):
        self.orginal = cv2.imread(path)
        self.max_width = width
        self.max_height = height

        self.resized = self.adjust_size()
        self.gray = cv2.cvtColor(self.resized, cv2.COLOR_RGBA2GRAY)


    def adjust_size(self):
        w, h = self.orginal.shape[1], self.orginal.shape[0]
        wh_ratio = w / h

        is_adjusted = False
        if w>self.max_width:
            w = self.max_width
            h = int(w / wh_ratio)

            is_adjusted = True

        if h>self.max_height:
            h = self.max_height
            w = int(h*wh_ratio)

            is_adjusted = True

        if is_adjusted:
            return cv2.resize(self.orginal, (w, h))

        return self.orginal

    def display(self):
        img = self.gray
        
        width = img.shape[1]
        height = img.shape[0]

        img_rows_text = []

        for row in img:
            line = []
            for v in row:
                ch = self.denser[round(translate(v, 0, 255, 0, len(self.denser)-1))]
                line.append(ch)

            img_rows_text.append("".join(line))

        template = f"""<html><head><link rel="stylesheet" href="display.css"/></head><body>{"<br>".join(img_rows_text).replace(' ', '&nbsp')}</body></html>"""

        with open('display.html', 'w') as file:
            file.write(template)

    def color_display(self):
        width = self.gray.shape[1]
        height = self.gray.shape[0]

        img_rows_text = []

        for i, row in enumerate(self.gray):
            line = []
            for j, v in enumerate(row):
                ch = self.denser[round(translate(v, 0, 255, 0, len(self.denser)-1))]

                if ch == ' ':
                    line.append('&nbsp')

                else:
                    color = '#'+''.join(f"{cp:02X}" for cp in self.resized[i][j][::-1])
                    line.append(f'<span style="color:{color}">{ch}</span>')

            img_rows_text.append("".join(line))

        template = f"""<html><head><link rel="stylesheet" href="display.css"/></head><body>{"<br>".join(img_rows_text)}</body></html>"""

        with open('display.html', 'w') as file:
            file.write(template)

    

if __name__ == '__main__':

    # art = AsciiArt('images/tanvir_face.png', 550, 550)
    art = AsciiArt('images/tanvir.jpg', 100, 100)
    # art.display() # black and white
    art.color_display() # colored