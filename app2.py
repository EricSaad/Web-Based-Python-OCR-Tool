import os
from flask import Flask, render_template, url_for,request,redirect
#on importe le "microframework" flask pour pouvoir utiliser python sur une page web
import pytesseract
# On importe la librairie PyTesseract qui nous permetera de scanner des images et d'en tirer le texte

import sqlite3



pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


UPLOAD_FOLDER = '/static/uploads/'
#Ou les images seront stoquees

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
#Quel type d'images accepter


app = Flask(__name__)





try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

todb = str()

def ocr_core(filename):
    #Fonction qui permet d'extraire le texte des images
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  
    



    return text
    #on retourne le texte en forme de chaine de characteres

def allowed_file(filename):
    #Fonction qui permet de verifier si l'image a une extension compatible
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ReceiptPage', methods=['GET', 'POST'])
def ReceiptPage():
 if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('Receipt.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('Receipt.html', msg='No file selected')

        if file and allowed_file(file.filename):

            # call the OCR function on it
            extracted_text = ocr_core(file)
            print(extracted_text)

        
            connection = sqlite3.connect('Receipt_String.db')
            cursor = connection.cursor()
            #create table

            command1 = """CREATE TABLE IF NOT EXISTS
            stores(extracted_text TEXT PRIMARY KEY, extracted_text TEXT NOT NULL)"""

            cursor.execute(command1)

            cursor.execute("SELECT * FROM stores")

            results = cursor.fetchall()
            print(results,"wwwwwwwwww")

    

            # extraire le texte et le montrer sur l'ecran
            return render_template('Receipt.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
 elif request.method == 'GET':
          return render_template('Receipt.html')



if __name__ == "__main__":
    app.run(debug = True)