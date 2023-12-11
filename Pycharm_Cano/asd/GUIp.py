from SerializeFile import *
from Motorcycle import *
import PySimpleGUI as sg
import operator

fMotorcycles = open('Motorcycles.csv', 'a+')

lMotorcycles = []

readMotorcycle('Motorcycles.csv', lMotorcycles)


def addMotorcycle(motorcycles_list, table_data, new_motorcycle):
    motorcycles_list.append(new_motorcycle)
    saveMotorcycle("Motorcycles.csv", new_motorcycle)
    table_data.append([new_motorcycle.ID, new_motorcycle.brand, new_motorcycle.model,
                       new_motorcycle.year, new_motorcycle.price, new_motorcycle.posFile])


def deleteMotorcycle(motorcycles_list, table_data, row_index):
    pos_in_file = table_data[row_index][-1]
    motorcycle_to_delete = None
    for motorcycle in motorcycles_list:
        if motorcycle.motorcycleInPos(pos_in_file):
            motorcycle_to_delete = motorcycle
            break
    if motorcycle_to_delete is not None:
        motorcycles_list.remove(motorcycle_to_delete)
        table_data.remove(table_data[row_index])
        motorcycle_to_delete.erased = True
        modifyMotorcycle(fMotorcycles, motorcycle_to_delete)


def updateMotorcycle(motorcycles_list, row_data, pos_in_file):
    motorcycle_to_update = None
    for motorcycle in motorcycles_list:
        if motorcycle.motorcycleInPos(pos_in_file):
            motorcycle_to_update = motorcycle
            break
    if motorcycle_to_update is not None:
        motorcycle_to_update.setMotorcycle(row_data[1], row_data[2], row_data[3], row_data[4], row_data[5])
        modifyMotorcycle(fMotorcycles, motorcycle_to_update)


def sortTable(table, cols):
    """Sort a table by multiple columns."""
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sortTable', 'Exception in sortTable', e)
    return table


def sort_table_by_column(table, col):
    """Sort a table by a specific column"""
    try:
        return sorted(table, key=operator.itemgetter(col))
    except Exception as e:
        sg.popup_error('Error in sort_table_by_column', 'Exception in sort_table_by_column', e)
        return table


def sort_table_and_save(filename, column_to_sort):
    try:
        data = pd.read_csv(filename)
        sorted_data = data.sort_values(by=column_to_sort)

        with open('sorted_data.txt', 'w') as txt_file:
            txt_file.write(sorted_data.to_string(index=False))

        sg.popup('Sorted data has been saved to sorted_data.txt')
    except pd.errors.EmptyDataError:
        print("The CSV file is empty.")
    except FileNotFoundError:
        print(f"The file {filename} was not found.")


def interface():
    sg.theme('Black')
    sg.set_options(font=('Arial', 14))

    table_data = []
    row_to_update = []

    for motorcycle in lMotorcycles:
        if not motorcycle.erased:
            table_data.append([motorcycle.ID, motorcycle.brand, motorcycle.model,
                               motorcycle.year, motorcycle.price, motorcycle.posFile])

    layout = [
        [sg.Push(), sg.Text('Motorcycle CRUD'), sg.Push()],
        *[[sg.Text(text), sg.Push(), sg.Input(key=key)] for key, text in Motorcycle.fields.items()],
        [sg.Push()] + [sg.Button(button) for button in ('Add', 'Delete', 'Modify', 'Clear')] + [sg.Push()],
        [sg.Table(values=table_data, headings=Motorcycle.headings, max_col_width=50, num_rows=10,
                  display_row_numbers=False, justification='center', enable_events=True,
                  enable_click_events=True, vertical_scroll_only=False,
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE, expand_x=True, bind_return_key=True, key='-Table-')],
        [sg.Button('Purge'), sg.Push(), sg.Button('Sort File')],
    ]

    window = sg.Window('Motorcycle Management with Files', layout, finalize=True)
    window['-PosFile-'].update(disabled=True)
    window['-Table-'].bind("<Double-Button-1>", " Double")

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'Add':
            validate = True

            if validate:
                new_motorcycle = Motorcycle(values['-ID-'], values['-Brand-'], values['-Model-'],
                                            values['-Year-'], values['-Price-'], -1)
                addMotorcycle(lMotorcycles, table_data, new_motorcycle)
                window['-Table-'].update(table_data)

        if event == 'Delete':
            if len(values['-Table-']) > 0:
                deleteMotorcycle(lMotorcycles, table_data, values['-Table-'][0])
                window['-Table-'].update(table_data)

        if event == '-Table- Double':
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-ID-'].update(disabled=True)
                window['-ID-'].update(str(table_data[row][0]))
                window['-Brand-'].update(str(table_data[row][1]))
                window['-Model-'].update(str(table_data[row][2]))
                window['-Year-'].update(str(table_data[row][3]))
                window['-Price-'].update(str(table_data[row][4]))
                window['-PosFile-'].update(str(table_data[row][5]))

        if event == 'Clear':
            window['-ID-'].update(disabled=False)
            window['-ID-'].update('')
            window['-Brand-'].update('')
            window['-Model-'].update('')
            window['-Year-'].update('')
            window['-Price-'].update('')
            window['-PosFile-'].update('')

        if event == 'Modify':
            validate = True

            if validate:
                for motorcycle in lMotorcycles:
                    if motorcycle.motorcycleInPos(values['-PosFile-']):
                        if values['-PosFile-']:  # Verificar si no es una cadena vacía
                            row_to_update = motorcycle
                            row_to_update.setMotorcycle(values['-Brand-'], values['-Model-'], values['-Year-'],
                                                        values['-Price-'])
                            break
                        else:
                            print("PosFile cannot be an empty string.")
                            break
                else:
                    print("PosFile not found in the motorcycles list.")

                updateMotorcycle(row_to_update)
                window['-Table-'].update(table_data)
                window['-ID-'].update(disabled=False)

        if event == 'Sort File':
            # Determine which column to sort by (you may want to retrieve this from user input)
            column_to_sort = 'Price'  # For example, sort by price, change this as needed

            # Sort the table_data and save to a text file
            sort_table_and_save('Motorcycles.csv', column_to_sort)

            # Update the table_data with the sorted data
            table_data = sort_table_by_column(table_data, column_to_sort)

            # Update the Table element in the GUI
            window['-Table-'].update(table_data)

        if isinstance(event, tuple):
            print(event)
            print(values)

            if event[0] == '-Table-':
                if event[2][0] == -1:
                    col_num_clicked = event[2][1]
                    table_data = sortTable(table_data, (col_num_clicked, 0))
                    window['-Table-'].update(table_data)

    window.close()


interface()
fMotorcycles.close()
