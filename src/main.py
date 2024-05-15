import PySimpleGUI as sg
import glob
import subprocess
import os
import webbrowser


# Function to find the latest 'result-' file
def find_latest_result_file():
    list_of_files = glob.glob('result-*')  # * means all if you need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


# Define the layout of the GUI
layout = [
    [sg.Text('Enter IP or Hostname:'), sg.InputText(key='IP_HOSTNAME')],
    [sg.Button('Scan Ports'), sg.Button('Generate HTML')],
    [sg.Multiline(key='RESULTS', size=(60, 20))]
    # Add a divider and text to the layout
]
layout.extend([
    [sg.HorizontalSeparator()],
    [sg.Text('If you want to know more about these ports and their vulnerabilities click \n\'Generate HTML\' and then '
             'you can click on the port number which will \rtake you to the details page')]
])

# Create the window
window = sg.Window('Port Scanner GUI', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Scan Ports':
        # Run the scan_ports script using the provided IP/Hostname
        subprocess.run(['bash', 'scan_ports', values['IP_HOSTNAME']])
        # Find and display the latest 'result-' file content
        latest_result_file = find_latest_result_file()
        with open(latest_result_file, 'r') as file:
            window['RESULTS'].update(file.read())
    elif event == 'Generate HTML':
        # Find the latest 'result-' file
        latest_result_file = find_latest_result_file()
        # Run the generate_html script using the latest 'result-' file
        subprocess.run(['bash', 'generate_html', latest_result_file])
        webbrowser.open('scan_result.html')

# Close the window
window.close()
