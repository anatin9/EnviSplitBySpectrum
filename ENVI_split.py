import struct
import os, sys, getopt

readVars = {}
lowWav = []
lowSmoothing = []
highWav = []
highSmoothing = []


def writeImgFiles(filename, outFile, dim):
  os.makedirs("Output", exist_ok=True)
  f = open(filename, 'rb')
  pic1 = open("Output/"+outFile + "_1_img", 'ab')
  pic2 = open("Output/"+outFile + "_2_img", 'ab')
  for line in range(dim["lines"]):
    pic1.write(f.read(4))
    pic2.write(f.read(4))
    for band in range(dim["bands"]):
      for sample in range(dim["samples"]):
        if band < 213:
          pic1.write(f.read(4))
        else:
          pic2.write(f.read(4))
      
  pic1.close()
  pic2.close()
  f.close()


def readHdrFile(infile):
  with open(infile) as myfile:
    for line in myfile:
      name, var = line.partition("=")[::2]
      readVars[name.strip()] = var.strip()
      
  wav = [float(x) for x in readVars["wavelength"].strip(" { } ").replace(" , ", ",").split(",")]
  smoothing = [float(x) for x in readVars["smoothing factors"].strip(" { } ").replace(" , ", ",").split(",")]
  lines = readVars["lines"]
  samples = readVars["samples"]
  bands = readVars["bands"]
  fileDimen = {"lines":int(readVars["lines"]),"samples":int(readVars["samples"]),"bands":int(readVars["bands"])}
  lowWav.append(wav[:int(len(wav)/2)])
  lowSmoothing.append(smoothing[:int(len(wav)/2)])
  highWav.append(wav[int(len(wav)/2):])
  highSmoothing.append(smoothing[int(len(wav)/2):])
  return fileDimen


def makeHdrFiles(fileName):
  try:	
    os.makedirs("Output", exist_ok=True)
  except FileExistsError:
    pass
  hdr1 = open("Output/" + fileName + "_1.hdr", 'w')
  hdr2 = open("Output/" + fileName + "_2.hdr", 'w')
  writeHdrFiles(hdr1, lowSmoothing, lowWav)
  writeHdrFiles(hdr2, highSmoothing, highWav)
  hdr1.close()
  hdr2.close()
  
  
def writeHdrFiles(ofile, smoothing, wav):
  print(len(wav[0]))
  ofile.write(readVars["file type"]+'\n')
  ofile.writelines("description = " + readVars["description"]+'\n')
  ofile.writelines("  }\n")
  ofile.writelines("samples = " + readVars["samples"]+'\n')
  ofile.writelines("lines = " + readVars["lines"]+'\n')
  ofile.writelines("bands = " + str(len(wav[0])) +'\n')
  ofile.writelines("header offset = " + readVars["header offset"]+'\n')
  ofile.writelines("file type = " + readVars["file type"]+'\n')
  ofile.writelines("data type = " + readVars["data type"]+'\n')
  ofile.writelines("interleave = " + readVars["interleave"]+'\n')
  ofile.writelines("byte order = " + readVars["byte order"]+'\n')
  ofile.writelines("map info = " + readVars["map info"]+'\n')
  ofile.writelines("wavelength units = " + readVars["wavelength units"]+'\n')
  ofile.writelines("smoothing factors = { " + ' , '.join(map(str, smoothing)).strip("[]").replace(',', ' , ') + " }\n")
  ofile.writelines("data ignore value = " + readVars["data ignore value"]+'\n')
  ofile.writelines("wavelength = { " + ','.join(map(str, wav)).strip("[]").replace(',', ' , ') + " }\n")
  ofile.writelines("fwhm = " + readVars["fwhm"]+'\n')
  
  
def main(argv):
  inputImgFile = ''
  inputHdrFile = ''
  outFile = 'splitFile'
  try:
    opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile"])
  except getopt.GetoptError:
    print('-i <inputfile>')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('-i <inputfile>')
      sys.exit()  
    elif opt in ("-i", "--ifile"):
      if arg[-4:] == "_img":
        inputImgFile = arg
        inputHdrFile = inputImgFile+".hdr"
      elif arg[-4:] == ".hdr":
        inputHdrFile = arg
        inputImgFile = inputHdrFile[:-4]
      else:
        print("File name or extension not recognized. Provide file ending in \'_img\' or \'.hdr\'")
        sys.exit(2)
  
  fileDimen = readHdrFile(inputHdrFile)
  makeHdrFiles(outFile)
  writeImgFiles(inputImgFile, outFile, fileDimen)
      	

if __name__ =="__main__":
  main(sys.argv[1:])


