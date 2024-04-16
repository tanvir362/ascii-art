import cv2


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

