
class Normalizer:
    def normalize(self, value):
        raise NotImplementedError("normalize method not implemented")

class RGB_Normalizer(Normalizer):
    def normalize(self, value) -> tuple:
        tot = value[0] + value[1] + value[2]
        r = value[0] * 255 / tot
        g = value[1] * 255 / tot
        b = value[2] * 255 / tot
        return (r, g, b)
