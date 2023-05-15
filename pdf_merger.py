from PyPDF2 import PdfFileReader, PdfFileMerger
import glob
import natsort

pdfs = glob.glob("pdf/*.pdf")
pdfs = natsort.natsorted(pdfs, reverse=False)
print(pdfs)

merger = PdfFileMerger()

for pdf in pdfs:  # iterate over the list of files
   merger.append(PdfFileReader(pdf), 'rb')

merger.write("Vsechny_grafy.pdf")
merger.close()
