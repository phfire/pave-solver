
class Layer:
    def __init__(self, name, height):
        self.name = name
        self.height = height


class Pave:
    def __init__(self, layer1, layer2, layer3):
        self.numberOfnastilki = 3
        self.layers = [layer1, layer2, layer3]

    def getTotalDepth(self):
        totalDepth = 0
        for layer in self.layers:
            totalDepth = totalDepth + layer.height
        return totalDepth


pave_layer_default_elastics = {
    "pluten_asfaltobeton": 1200,
    "nepluten_asfaltobeton": 1000,
    "troshen": 800
}

alphabetTable = [
    "a", "b"
]

def get_pave(ground_depth_of_freezing):
    pave_sample = Pave(Layer("pluten_asfaltobeton", 4), Layer("nepluten_asfaltobeton", 6), Layer("troshen", 10))
    setElasticMudles(pave_sample)
    return pave_sample

def calculateFirstLayerElasticModule(elastic_value, first_layer_height):
    # Using only the alphabetTable, the elastic_value of the first layer and the first_layer_height
    # some other functions and nomogram returns some value
    return 100

def calculateNextLayerElastic(firstLayerElasticValue, secontLayerHeight):
    # Using only the alphabetTable, the elastic_value of the first layer and the first_layer_height
    # some other functions and nomogram returns some value
    return 100

def setElasticMudles(pave_sample):
    first_layer = pave_sample.layers[0]
    first_layer_elastic_value = pave_layer_default_elastics[first_layer.name]
    firstLayerElasticValue = calculateFirstLayerElasticModule(first_layer_elastic_value, first_layer.height)



get_pave(75)