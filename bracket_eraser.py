import os
import tkinter
import os.path
import glob
import pypandoc
#from pypandoc.pandoc_download import download_pandoc
#download_pandoc()
import citeproc
from citeproc import CitationStylesStyle, CitationStylesBibliography
input("cliquez sur une touche pour sélectionner le coffre de vos notes")
from tkinter.filedialog import askdirectory
path = askdirectory()
if not any(File.endswith('.md') for File in os.listdir(path)):
    print("pas de note trouvée dans ce dossier, chargez une note en markdown présente ailleurs")
    from tkinter.filedialog import askopenfilename
    path2 = askopenfilename(filetypes=[("Markdown notes", "*.md")])
else:
    from tkinter import *
    from tkinter import filedialog as fd
    filename = fd.askopenfilename(initialdir=path, filetypes = (('markdown notes', '*.md'),('All files', '*.*')))
notepath = os.path.basename(filename)
notefull = notepath.split('.')
selected_note = notefull[0]
noteext = notefull[1]
print("vous avez choisi la note intitulée", selected_note)
# importing easygui module
import easygui
from easygui import *
from pathlib import Path
choices = ["oui","non"]
msg = "votre note contient-elle une bibliographie ?"
reply = choicebox(msg, choices = choices)
print("You selected : ", end = "")
if reply == "oui":
    extension = "*.bib"
# Get a list of all files with the specified extension in the folder and its subfolders
    files = [f for f in glob.glob(path + "/**/" + extension, recursive=True)]
    if files:

# Print the list of files
        for i, fname in enumerate(files):
        #for count,value in enumerate(files, start=1):
            #print(count, value)
            #bibfiles = os.path.basename(fname)
            #print("{0}: {1}".format(i+1,bibfiles))
            #print("{0}: {1}".format(i+1,files))
            print(f"{i+1}.{fname}")
        selected_bib = int(input("Choose a file by its index: "))
        print(f"You chose: {files[selected_bib-1]}")
        
    else:
        print('pas trouvé de fichier bib dans votre coffre, voulez-vous en charger un?')
        choices2 = ["oui","non"]
        msg2 = "choisissez entre les deux options"
        reply2 = choicebox(msg2, choices = choices2)
        if reply2 == "oui":
            from tkinter.filedialog import askopenfilename
            selected_bib = askopenfilename(filetypes=[("fichier biblio", "*.bib")])

    choices_csl = ["oui","non"]
    msg_csl = "votre dossier contient-il une feuille de style pour votre bibliographie ?"
    reply_csl = choicebox(msg_csl, choices = choices_csl)
    print("You selected : ", end = "")
    if reply_csl == "oui":
        extension_csl = "*.csl"
# Get a list of all files with the specified extension in the folder and its subfolders
        files_csl = [f for f in glob.glob(path + "/**/" + extension_csl, recursive=True)]
        if files_csl:
            # Print the list of files
            for i, fname_csl in enumerate(files_csl):
            #for count,value in enumerate(files, start=1):
            #print(count, value)
            #bibfiles = os.path.basename(fname)
            #print("{0}: {1}".format(i+1,bibfiles))
            #print("{0}: {1}".format(i+1,files))
                print(f"{i+1}.{fname_csl}")
            style_path_int = int(input("choisissez une feuille de style parmi celles-ci: "))
            print(f"You chose: {files_csl[style_path_int-1]}")
        if files_csl is None or reply == "non":
            print("trois feuilles de style vont automatiquement se charger")
else:
    with open(filename, 'r') as file2 :
        filedata = file2.read()
        print(filedata)

# Replace the target string
        filedata = filedata.replace('[[', '').replace(']]','')
        print(filedata)

# Write the file out again
        with open('file.txt', 'w') as file2:
            file2.write(filedata)
# convert modified file into open document file
style_path = str(style_path_int)
style = CitationStylesStyle(style_path)
# style_path = path of bibliographic style (for instance ieee)
biblio = CitationStylesBibliography(style, selected_bib)
pdf_text = pypandoc.convert_text(filedata, 'pdf', format='md', outputfile='pdf_text.pdf', extra_args=['--citeproc', f'--bibliography=biblio'])

# delete file text
os.remove('file.txt')
    
if reply == "non":
    print("pandoc sans biblio")