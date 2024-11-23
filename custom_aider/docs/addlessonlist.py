import glob
basehtmlfilename = "markdown-viewer-with-filelist.html"
outfilename = "index.html"

with open(basehtmlfilename, 'r', encoding="utf8") as readfile:
    outfiletxt = readfile.read()
    
filenames = glob.glob('*.md')
fns=''
for fname in filenames:
    fns=fns + '"' + fname + '"' + ',\n'
print(fns)

with open(outfilename, 'w', encoding="utf8") as outfile:    
    outfiletxt = outfiletxt.replace('<<<<<<lessons>>>>>>',fns)
    outfile.write(outfiletxt)