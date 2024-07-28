class WordFlyweight:
    def __init__(self, font, color):
        self.font = font
        self.color = color

class WordContext:
    def __init__(self, word, position):
        self.word = word
        self.position = position

class WordFactory:
    def __init__(self):
        self.flyweights = {}

    def get_flyweight(self, font, color):
        key = (font, color)
        if key not in self.flyweights:
            self.flyweights[key] = WordFlyweight(font, color)
        return self.flyweights[key]

# Example usage
if __name__ == '__main__':
    factory = WordFactory()

    document = []

    # Adding words with shared font and color attributes
    words = ["Hello", "world", "Hello", "Flyweight"]
    font = "Arial"
    color = "black"

    for i, word in enumerate(words):
        flyweight = factory.get_flyweight(font, color)
        context = WordContext(word, i)
        document.append((flyweight, context))

    # Displaying the document
    for flyweight, context in document:
        print(f"Word: {context.word}, Font: {flyweight.font}, Color: {flyweight.color}, Position: {context.position}")
