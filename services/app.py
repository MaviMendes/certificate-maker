import os
from flask import Flask, render_template, request,send_file
from werkzeug.utils import secure_filename
import process
import uuid
import time
from io import BytesIO
import zipfile
import os
import tempfile

id = uuid.uuid4()
id = str(id)

app = Flask(__name__)

# Defining the upload folder
raw_folder = "raw/"

# Configuring the upload folder
app.config['RAW_FOLDER'] = raw_folder

# configuring the allowed extensions
allowed_extension = ['csv']

def check_extension(filename):
    return filename.split('.')[-1] in allowed_extension

# The path for uploading the file
@app.route('/')
def upload_csv():
   return render_template('index.html')

@app.route('/raw', methods = ['POST','GET'])
def uploadfile():
   if request.method == 'POST': # check if the method is post
      f = request.files['csv_file'] # get the file from the files object
      # Saving the file in the required destination
      
      file_name = id+'_'+f.filename

      if check_extension(f.filename):
         f.save(os.path.join(app.config['RAW_FOLDER'] ,secure_filename(file_name))) # this will secure the file
         
         # process the file creating the certificates
         file_name = id+'_'+f.filename
         file_path = 'raw/'+file_name
         process.main(file_path)

         # TO DO -  return a render templlate here, a page with a button to go to the home page
         return render_template('retrieve.html') # Display the page with the download button
      
      else:
         
         return render_template('error.html')
      


# https://www.youtube.com/watch?v=8ZqDKFjW7Vs

# https://stackoverflow.com/questions/53880816/how-do-i-zip-an-entire-folder-with-subfolders-and-serve-it-through-flask-witho

# Implements the download button logic

@app.route('/retrieve-file') # download button will be mapped to here
def zipped_data():
      folder_path = os.path.join(os.getcwd(), 'processed')  # Assuming 'processed' directory is in the same folder as the app code
      with tempfile.NamedTemporaryFile(delete=False) as temp_file: # Temp directory to download the zip to the user Download folder
         zip_file_path = os.path.join(tempfile.gettempdir(), 'certificados.zip')  # Save zip file to the temporary directory
      
      # Create a zip file
      with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
         # Iterate over files in the directory
         for root, dirs, files in os.walk(folder_path):
               for file in files:
                  file_path = os.path.join(root, file)
                  zipf.write(file_path, os.path.relpath(file_path, folder_path))  # Add file to the zip, preserving the relative path
                  
      # Return the zip file to the user
      return send_file(zip_file_path, as_attachment=True)

if __name__=="__main__":
   app.run(debug=True) # running the flask app