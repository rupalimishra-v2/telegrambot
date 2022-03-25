import datetime

from fpdf import FPDF
import time
import pandas as pd
import dataframe_image as dfi
from utils import constants
import traceback

"""https://david-kyn.medium.com/workplace-automation-generate-pdf-reports-using-python-fa75c50e7715"""


def csv_to_pdf(file_name, report_by, shilling_partner):
    csv_file_name = file_name + '.csv'
    df = pd.read_csv(csv_file_name)

    grouped_df = df.groupby('Group Name')['Group Name', 'Date', 'Time (in UTC)', 'Shilling Text'].value_counts() \
        .reset_index(name='Texts Count Per Group')

    count_row = df.shape[0]
    i = 0
    while i <= count_row:
        dfi.export(grouped_df[i:i + constants.pdf_page_cell_limit], file_name + str(i) + '.png')
        i += constants.pdf_page_cell_limit

    title = "Daily Social Media Marketing Report"
    width = 210

    pdf = PDF()
    pdf.add_page()

    # Add letter head and title
    create_letterhead(pdf, width, report_by)
    pdf.ln(80)
    create_title(title, pdf)

    write_to_pdf(pdf, "The table below illustrates the daily posts done by " + report_by +
                 " for the awesome project : " + shilling_partner)
    pdf.ln(15)

    # Add table
    j = 0
    while j < i:
        pdf.image(file_name + str(j) + ".png", w=170)
        j += constants.pdf_page_cell_limit
        pdf.add_page()

    pdf.image("/telegrambot/report/images/footer.jpg", 0, 0, width)
    pdf.ln(15)

    pdf.output('/telegrambot/report/pdf_reports/daily_performance_report_' + report_by + '_' +
               datetime.date.today().strftime("%d %B, %Y") + '_' +
               datetime.datetime.now().strftime("%H:%M:%S") + '.pdf', 'F')


def create_letterhead(pdf, width, report_by):
    pdf.image('/telegrambot/report/images/' + report_by + '.jpg', 0, 0, width)


def create_title(title, pdf):
    pdf.set_font('Helvetica', 'b', 30)
    pdf.ln(40)
    pdf.write(5, title)
    pdf.ln(10)

    pdf.set_font('Helvetica', '', 24)
    pdf.set_text_color(r=128, g=128, b=128)
    today = time.strftime("%d/%m/%Y")
    pdf.write(4, f'{today}')

    pdf.ln(10)


def write_to_pdf(pdf, words):
    pdf.set_text_color(r=0, g=0, b=0)
    pdf.set_font('Helvetica', '', 20)

    pdf.write(5, words)


class PDF(FPDF):

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')


if __name__ == '__main__':
    try:
        csv_to_pdf('',
                   constants.shilling_cj_user, constants.elitheum_shilling_partner)
        print('Success')
    except Exception:
        print("Unexpected Error")
        print(traceback.print_exc())
