import markovify

def createMessage():

    with open("corpus.txt") as gdq:
        gdqText = gdq.read()

    with open("don.txt") as don:
        donText = don.read()

    gdqTextModel = markovify.Text(gdqText)
    donTextModel = markovify.Text(donText)
    combinedModel = markovify.combine([gdqTextModel, donTextModel], [1, 1])

    return combinedModel.make_sentence()

