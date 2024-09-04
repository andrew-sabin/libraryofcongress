# Importing Python Libraries
import PySimpleGUI as sg
import openpyxl
import os
# Importing Sort Classification Number Functions from
from sortClassNumfunctions import read_through_excelsheet, setonnewCSV

if __name__ == '__main__':
    # Add your new theme colors and settings
    my_new_theme = {'BACKGROUND': '#e9e5e4',
                    'TEXT': '#000000',
                    'INPUT': '#FFFFFF',
                    'TEXT_INPUT': '#000000',
                    'SCROLL': '#c7e78b',
                    'BUTTON': ('white', '#D73F09'),
                    'PROGRESS': ('#01826B', '#D0D0D0'),
                    'BORDER': 1,
                    'SLIDER_DEPTH': 0,
                    'PROGRESS_DEPTH': 0}

    # Add your dictionary to the PySimpleGUI themes
    sg.theme_add_new('MyNewTheme', my_new_theme)

    # Switch your theme to use the newly added one. You can add spaces to make it more readable
    sg.theme('My New Theme')

    # Fonts and text features
    heading = ''
    sub_heading = 'Georgia'


    layout = [[sg.Text('Excel file you would like to sort:', tooltip='Enter in the exact path '
                                                                     'or Click Browse for the file',
                       font=(sub_heading,14))],
              [sg.InputText(key='--EXCELFILE--'), sg.FileBrowse(file_types=((".xlsx", ".xlsx"), (".csv", ".csv")))],
              [sg.Text('Spreadsheet you would like to sort:', tooltip='The name of the Excel Spreadsheet',
                       font=(sub_heading, 14))],
              [sg.InputText(default_text="Sheet1", key='--SHEET--')],
              [sg.Text('Name of the Permanent Call Number column:', tooltip='Usually named Permanent '
                                                                                         'Call Number or Perm Call #',
                       font=(sub_heading,13))],
              [sg.InputText(default_text="Permanent Call Number", key='--CALLNUM--')],
              [sg.Text('Name of the Description column:', tooltip='Usually named Description',
                       font=(sub_heading,14))],
              [sg.InputText(default_text="Description", key='--DESCRIPTION--')],
              [sg.Text('Name of the new sorted CSV file:', tooltip='This will be where all the sorted'
                                                                                ' values are stored',
                       font=(sub_heading,14))],
              [sg.InputText(key='--NEWCSV--')],
              [sg.Text('New CSV file location:', tooltip='Default location is in the same place as the excel file',
                       font=(sub_heading,14))],
              [sg.InputText(key='--OUTPUT--'), sg.FolderBrowse()],
              [sg.Button('Begin'), sg.Button('Exit')]
              ]
    window = sg.Window('Beaver Library of Congress Sorter', icon='images/favicon.ico', layout=layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
            break
        if event == 'Begin':
            entered_vals = sg.popup_yes_no('Are these entered in values correct?',
                                           'Your Excel File Path:', values['--EXCELFILE--'],
                                           'Output File Path:', values['--OUTPUT--'],
                                           'Your Sheet:', values['--SHEET--'],
                                           'Permanent Call Number Column:', values['--CALLNUM--'], 'Description Column:',
                                           values['--DESCRIPTION--'], 'New CSV FIle Name:', values['--NEWCSV--'],
                                           icon='images/favicon.ico', )
            if entered_vals == 'Yes':
                valid_file = os.path.isfile(values['--EXCELFILE--'])
                valid_path = os.path.isdir(values['--OUTPUT--'])
                if valid_file == False:
                    sg.popup_auto_close("Invalid Filename. Please enter in a valid excel .xlsx file.",
                                        icon='images/favicon.ico')
                else:
                    if valid_path == False:
                        values['--OUTPUT--'] = os.path.dirname(values['--EXCELFILE--'])
                    workbook = openpyxl.load_workbook(values['--EXCELFILE--'])
                    if values['--SHEET--'] not in workbook:
                        sg.popup_auto_close("Spreadsheet not found in excel workbook.", icon='images/favicon.ico')
                    else:
                        if len(values['--NEWCSV--']) == 0:
                            fn_begin = 0
                            fn_end = 0
                            for char in range(len(values['--EXCELFILE--'])-1, -1, -1):
                                if values['--EXCELFILE--'][char] == '/':
                                    fn_begin = char + 1
                                    break
                            for char in range(len(values['--EXCELFILE--'])-1, -1, -1):
                                if values['--EXCELFILE--'][char] == '.':
                                    fn_end = char
                                    break
                            values['--NEWCSV--'] = values['--EXCELFILE--'][fn_begin:fn_end] + '_' \
                                                   +values['--SHEET--'] + "_sorted.csv"
                        elif ".csv" not in values['--NEWCSV--']:
                            values['--NEWCSV--'] = values['--NEWCSV--'] + ".csv"

                        sorted_list = read_through_excelsheet(values['--EXCELFILE--'],
                                                              values['--SHEET--'],
                                                              values['--CALLNUM--'],
                                                              values['--DESCRIPTION--'])
                        if sorted_list[0] == "Invalid" and sorted_list[1] == "Permanent Call Number":
                            sg.popup_error("Invalid Permanent Call Number Column. \n"
                                           "Please Reenter the Call Number Column with the correct name.",
                                           icon='images/favicon.ico')
                        elif sorted_list[0] == "Invalid" and sorted_list[1] == "Description":
                            sg.popup_error("Invalid Description Column. \n"
                                           "Please Reenter the Call Number Column with the correct name.",
                                           icon='images/favicon.ico')
                        else:
                            print("Completed Spreadsheet Processing and Sorting")
                            print("Placing items onto new spreadsheet...")
                            try:
                                setonnewCSV(sorted_list[0], sorted_list[1], values['--NEWCSV--'], values['--OUTPUT--'])
                                sg.popup_auto_close("Finished sorting! Window will close in 2 seconds.",
                                                    icon='images/favicon.ico')
                            except  Exception as exeption:
                                sg.popup_error("Cannot Write To CSV File\n"
                                               "The named CSV file might be open.\n"
                                               "Please close out of the CSV file or rename the desired CSV file.",
                                               icon='images/favicon.ico')
                            print("Set new sorted list onto the new CSV sheet")

            else:
                sg.popup_auto_close('Please reenter your desired values.', icon='images/favicon.ico')


    window.close()

