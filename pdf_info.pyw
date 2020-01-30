import PyPDF2
import pathlib


class PDFInfo:
    def __init__(self, file):
        self.file = open(file, 'rb')
        self.pdf = PyPDF2.PdfFileReader(self.file, strict=False)
        self.page_count = self.pdf.getNumPages()
        self.trim_size = self.pdf.getPage(0).trimBox
        self.bleed_size = self.pdf.getPage(0).bleedBox
        self.file.close()

        # Get dimensions and convert points to inches.
        self.page_width = (self.trim_size[2] - self.trim_size[0]) / 72
        self.page_height = (self.trim_size[3] - self.trim_size[1]) / 72
        self.bleed_width = (self.bleed_size[2] - self.bleed_size[0]) / 72
        self.bleed_height = (self.bleed_size[3] - self.bleed_size[1]) / 72
        self.bleed_amount = abs(self.bleed_size[0] - self.trim_size[0]) / 72


if __name__ == '__main__':
    p = pathlib.Path.cwd()
    directory_name = p.name
    file_list = list(p.glob('*.pdf'))
    with open(f'{directory_name}.csv', 'w', encoding='utf-8') as f:
        print(f'"File Name","Page Count","Trim","Bleed","Bleed Amount"', file=f)
        for pdf in file_list:
            info = PDFInfo(pdf)
            record = f'"{pdf.name}",' \
                     f'"{info.page_count}",' \
                     f'"{info.page_width:0.2f} x {info.page_height:0.2f}",' \
                     f'"{info.bleed_width:0.2f} x {info.bleed_height:0.2f}",' \
                     f'"{info.bleed_amount}"'
            print(record, file=f)
            del info
