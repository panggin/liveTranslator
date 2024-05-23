class Color:
    def __init__(self, r=0, g=0, b=0):
        self.red = r
        self.green = g
        self.blue = b


class StyleSheet:
    backgroundColor = Color(50,50,50)
    textColor = Color(255,255,255)
    textSize = 16

    default_style = ''
    transparent_style = ''

    def update_style_sheet() :
        StyleSheet.default_style = f'''background-color: rgba({StyleSheet.backgroundColor.red}, {StyleSheet.backgroundColor.green}, {StyleSheet.backgroundColor.blue}, 255); 
                            color: rgb({StyleSheet.textColor.red}, {StyleSheet.textColor.green}, {StyleSheet.textColor.blue}); 
                            font-family: Arial; 
                            font-size: {StyleSheet.textSize}px;'''

        StyleSheet.transparent_style = f'''background-color: rgba({StyleSheet.backgroundColor.red}, {StyleSheet.backgroundColor.green}, {StyleSheet.backgroundColor.blue}, 50); 
                            color: transparent;
                            font-family: Arial; 
                            font-size: {StyleSheet.textSize}px;'''

StyleSheet.update_style_sheet()