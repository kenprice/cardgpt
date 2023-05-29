import json
from flask import Flask, render_template, request, Markup, session
import openai

###########################################################
# CARD GENERATOR
###########################################################
openai.api_key = "YOUR API KEY HERE"

prompt = '''Create a .json file with playing cards for a trading card game. Follow these rules for each key:

"name" (string): The card's name must include a pun. Also something oddly specific.
"attack" (integer, range 1-5): Assign a value representing the card's attack power.
"hp" (integer, range 1-15): Assign a value representing the card's health points.
"cost" (integer, range 0-3): Assign a value representing the card's cost to play. Stronger cards should cost more, though powerful spells can come in weak packages, maybe for a low cost if the have to work with other cards in the series.
"flavortext" (string): Add a funny statement or joke related to the card.
"type" (string): spell effect, monster,artifact, or tile. Each cards series must include a few from each of these.
"effect" (string): description of what the card does in the game as its effect.
"unicodegfx" (string): Choose a Unicode Egyptian hieroglyphic character.
"atkseq" (array of integers): An array of 8 random integers between 0 and 255.
"cardart" (string): Describe the vivid picture on the card in two memorable sentences.
"family" (string):groups cards together for effects, i.e. "scientist", "princess","undead", Each series does not have more than two families
Make sure to use as few tokens as possible to describe the instructions for each key.

Make a series of 3 cards as an array. Make a set themed around the fear of aliens implanting things under your skin or government surveilence.
'''

def generate_art(card):
    url = None
    try:
        card_art_res = openai.Image.create(
            prompt="TCG card art, digital art. " + card["cardart"],
            n=1,
            size="256x256",
        )
        url = card_art_res["data"][0]["url"]
        print(url)
    except Exception as ex:
        print(ex)
        # Exceptions are most often caused by "unsafe" words in the prompt, so ignore
        pass
    return url

def generate_cards():
    print("Generating cards...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": prompt},
            ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content


    print(result)
    cards = json.loads(result)

    for card in cards:
        print("Generating art...")
        card["cardarturl"] = generate_art(card)

    print("Done!")
    return cards


###########################################################
# WEB SERVER
###########################################################
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    cards = generate_cards()
    return render_template("index.html", cards=cards)

if __name__ == '__main__':
  app.run(debug=False)
