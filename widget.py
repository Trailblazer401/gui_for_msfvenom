# This Python file uses the following encoding: utf-8
import sys, os, subprocess, re, platform, multiprocessing

from PySide6.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget
from options import ARCH, FORMAT, ENCODER, PAYLOAD, PLATFORM

class Widget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # some vars
        self.payload_count = 1
        self.payload_common_name = ""
        # self.exec_path = ""
        self.params = ""
        self.selected_save_path = ""
        self.payload_param = {
            'LHOST'         :    '',
            'LPORT'         :    '4444',
            'payload'       :    '',
            'platform'      :    '',
            'format'        :    '',
            'encoder'       :    '',
            'smallest'      :    0,
            'iteration'     :    '',
            'arch'          :    '',
            'encrypt'       :    '',
            'encrypt-key'   :    '',
            'out'           :    ''
        }
        # const
        self.PATH_MAX_LENGTH = 48

        # init qt gui
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # check install path
        # self.get_metasploit_install_path()
        # self.show_error_and_exit("test exit")

        # init combo box list items
        self.ui.comboBox_payload_type.addItems(self.payload_filter(PAYLOAD))
        self.ui.comboBox_arch.addItems(ARCH)
        self.ui.comboBox_encoder.addItems(ENCODER)
        self.ui.comboBox_format.addItems(FORMAT)
        self.ui.comboBox_platform.addItems(PLATFORM)

        # bind slot func
        self.bind_functions()

    def bind_functions(self):
        self.ui.lineEdit_ip_addr.editingFinished.connect(self.input_ip)
        self.ui.lineEdit_port.editingFinished.connect(self.input_port)
        self.ui.toolButton_save_path.clicked.connect(self.get_path)
        self.ui.spinBox_iteration.valueChanged.connect(self.input_iteration)
        self.ui.toolButton_key.clicked.connect(self.get_encrypt_key_file)
        self.ui.checkBox_smallest.stateChanged.connect(self.enable_smallest)
        self.ui.comboBox_platform.currentIndexChanged.connect(self.select_platform)
        self.ui.comboBox_payload_type.currentIndexChanged.connect(self.select_payload)
        self.ui.comboBox_arch.currentIndexChanged.connect(self.select_arch)
        self.ui.comboBox_format.currentIndexChanged.connect(self.select_format)
        self.ui.comboBox_encoder.currentIndexChanged.connect(self.select_encoder)
        self.ui.comboBox_encrypt.currentIndexChanged.connect(self.select_encrypt)
        self.ui.spinBox_count.valueChanged.connect(self.get_count)
        self.ui.pushButton_generate.clicked.connect(self.generate_payload)

        # function test
        # self.ui.lineEdit_ip_addr.editingFinished.connect(lambda: self.test_print("lineEdit lose focus"))
        # self.ui.pushButton_generate.clicked.connect(lambda: self.status_output())
        # self.ui.pushButton_generate.clicked.connect(self.generate_payload)
        # self.ui.pushButton_generate.clicked.connect(lambda: self.test_print("button pushed"))

    # input param

    def input_ip(self):
        self.payload_param['LHOST'] = self.ui.lineEdit_ip_addr.text()

    def input_port(self):
        if self.ui.lineEdit_port.text():
            self.payload_param['LPORT'] = self.ui.lineEdit_port.text()

    # main param

    def select_payload(self):
        self.payload_param['payload'] = self.ui.comboBox_payload_type.currentText()

    def select_format(self):
        self.payload_param['format'] = self.ui.comboBox_format.currentText()

    def select_platform(self):
        self.payload_param['platform'] = self.ui.comboBox_platform.currentText()
        # if self.payload_param['payload'] == '':
        #     selected_platform = self.ui.comboBox_platform.currentText()
        #     update_payloads = self.match_keywords(selected_platform, PAYLOAD)
        #     self.ui.comboBox_payload_type.clear()
        #     self.ui.comboBox_payload_type.addItems(update_payloads)

    def select_encoder(self):
        self.payload_param['encoder'] = self.ui.comboBox_encoder.currentText()

    def get_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog  # 使用QFileDialog而不是系统原生对话框

        selected_directory = QFileDialog.getExistingDirectory(self, "选择载荷文件存储路径", options=options)

        if selected_directory:
            # self.payload_param['out'] = selected_directory
            self.selected_save_path = selected_directory
            # self.save_path = selected_directory
            # print(f"选择的存储路径：{self.save_path}")
            if len(selected_directory) >= self.PATH_MAX_LENGTH:
                selected_directory = '.../' + selected_directory[:(self.PATH_MAX_LENGTH - 6)]

            self.ui.lineEdit_save_path.clear()
            self.ui.lineEdit_save_path.setText(selected_directory)

    # sub param

    def select_arch(self):
        self.payload_param['arch'] = self.ui.comboBox_arch.currentText()

    def input_iteration(self):
        self.payload_param['iteration'] = str(self.ui.spinBox_iteration.value())

    def enable_smallest(self, state):
        # self.smallest = 1
        if state == 2:  # Qt.Checked
            self.payload_param['smallest'] = 1
        else:
            self.payload_param['smallest'] = 0

    def set_payload_file_name(self, iteration):
        # if not self.ui.checkBox_file_name.isChecked():
            # self.generate_random_file_name()
        # else:
        self.payload_common_name = self.ui.lineEdit_file_name.text()
        pattern = r"([a-zA-Z0-9_]+)(\..+)"
        matches = re.match(pattern, self.payload_common_name)

        if matches:
            file_prefix = matches.group(1)
            file_extension = matches.group(2)
            # print("File Prefix:", file_prefix)
            # print("File Extension:", file_extension)
        else:
            print("Pattern not matched.")

        # self.payload_param['out'] = self.payload_param['out'] + self.payload_common_name
        if iteration:
            self.payload_common_name = file_prefix + '_' + str(iteration) + file_extension
        self.payload_param['out'] = os.path.join(self.selected_save_path, self.payload_common_name)

    def select_encrypt(self):
        self.payload_param['encrypt'] = self.ui.comboBox_encrypt.currentText()

    def get_encrypt_key_file(self):
        selected_file, file_type = QFileDialog.getOpenFileName(None, "选择密钥文件", "", "All Files (*)")

        if selected_file:
            self.payload_param['encrypt-key'] = selected_file
            # self.key_file_path = selected_file
            # print(f"选择的存储路径：{self.save_path}")
            filename = os.path.basename(selected_file)
            self.ui.label_key.clear()
            self.ui.label_key.setText(filename)

    def get_count(self):
        self.payload_count = int(self.ui.spinBox_count.value())

    # main function
    
    def generate_payload(self):
        if self.ui.spinBox_count.value() == 1:
            self.generate_payload_single()
        else:
            self.generate_payload_multi(self.ui.spinBox_count.value())

    def generate_payload_single(self):

        # # 参数列表
        # args = ['arg1', 'arg2', 'arg3']
        self.set_payload_file_name(0)
        # # 构建调用命令
        # command = ['ruby', ruby_script_path] + args

        self.gather_params()
        command = 'msfvenom ' + self.params
        print(command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

        # 获取输出和错误信息
        output, error = process.communicate()

        # 打印输出和错误信息
        self.ui.textBrowser_output.clear()
        self.ui.textBrowser_output.append(output)
        self.ui.textBrowser_output.append(error)
        # print("Output:", output)
        # print("Error:", error)

        # 检查返回码
        if process.returncode == 0:
            print("Bash script executed successfully.")
        else:
            print("Error executing Ruby script. Return code:", process.returncode)

    def generate_payload_multi(self, count):

        self.ui.textBrowser_output.clear()

        for i in range(1, count+1):

            self.set_payload_file_name(i)
            # # 构建调用命令
            # command = ['ruby', ruby_script_path] + args

            self.gather_params()
            command = 'msfvenom ' + self.params
            print(command)
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

            # 获取输出和错误信息
            output, error = process.communicate()

            # 打印输出和错误信息
            # self.ui.textBrowser_output.append
            self.ui.textBrowser_output.append(output)
            self.ui.textBrowser_output.append(error)
            self.ui.textBrowser_output.append('\n')
            # print("Output:", output)
            # print("Error:", error)

            # 检查返回码
            if process.returncode == 0:
                print("Bash script executed successfully.")
            else:
                print("Error executing Ruby script. Return code:", process.returncode)
                self.ui.textBrowser_output.append(f"发生错误：{process.returncode} , 生成过程中止")
                break
    
    def generate_payload_mp(self, count):
        None

    def gather_params(self):
        parse_list = []
        for key, value in self.payload_param.items():
        # 如果value不为空，则添加到参数列表中
            if value:
                if key == 'smallest':
                    parse_list.extend([f'--{key}'])
                    continue
                if key == 'LHOST' or key == 'LPORT':
                    parse_list.extend([f'{key}={str(value)}'])
                    continue
                parse_list.extend([f'--{key}', str(value)])

         # 使用空格连接参数列表中的元素
        self.params = ' '.join(parse_list)
        # print(self.params)
        # return parse_line_args

    def match_keywords(self, keyword, contents_list):
        pattern = re.compile(fr"\b{keyword}\b")
        matching_data = [item for item in contents_list if re.search(pattern, item)]
        return matching_data
            
    def status_output(self, status):
        self.status = status
        self.ui.textBrowser_output.append(str(self.status))

    # def update_combo_box(self, QComboBox, items):
    #     self.items = items
    #     QComboBox.clear()
    #     QComboBox.addItems(items)

    def test_print(self, msg):
        self.msg = str(msg)
        print(msg)

    def payload_filter(self, payload_raw):
        pattern = re.compile(r'.*(bind|reverse).*')
        payload_nondt = []
        for item in payload_raw:
            match = pattern.match(item)
            if match:
                payload_nondt.append(item)
        return payload_nondt
    
    # def generate_random_file_name(self):
    #     letters_and_digits = string.ascii_letters + string.digits
    #     random_string = ''.join(random.choice(letters_and_digits) for _ in range(10))
    #     self.payload_common_name = random_string


def get_metasploit_install_path(qt_widget):
    try:
        system = platform.system()
        if system in ["Windows", "windows"]:
            # 使用 where 命令查找 msfconsole 可执行文件
            # result = os.popen('where msfconsole').read()
            result = subprocess.run(['where msfconsole'], stdout=subprocess.PIPE, text=True, shell=True)
        if system in ["linux", "Linux", "Darwin", "darwin"]:
            # result = os.popen('which msfconsole').read()
            result = subprocess.run(['which msfconsole'], stdout=subprocess.PIPE, text=True, shell=True)
            # result = subprocess.run(['which pwd'], stdout=subprocess.PIPE, text=True)
        else:
            # throw exception
            show_error(qt_widget, "不支持的操作系统")
            return 0
            # None
        # 获取第一行的路径
        # path = os.path.dirname(result.stdout)
        # return os.path.dirname(path)
        # self.exec_path = str(os.path.dirname(path))
        # if os.path.exists(os.path.abspath(result.stdout)):
        if os.path.exists(os.path.dirname(result.stdout)):
            return 1
        else:
            show_error(qt_widget, "无效路径\n请确保Metasploit Framework已正确安装并添加到路径")
            return 0

    except Exception as e:
        # print(f"Error: {e}")
        show_error(qt_widget, str(e) + "\n请确保Metasploit Framework已正确安装并添加到路径")
        return 0
        # return None
    
def show_error(qt_widget, error_message):
    # 弹出警告窗口
    QMessageBox.critical(qt_widget, "执行异常", f"发生错误:\n{error_message}")
    # 关闭应用程序
    # QApplication.quit()
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    # show_error(widget, 'test')
    # if 0:
    if get_metasploit_install_path(widget):
        widget.show()
        sys.exit(app.exec())
    app.quit()

   