from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests as REQ
import email.utils as eut

from scraper_gui import *

#-----

def write_image_bytes(path, content):
    with open(path, 'wb') as image_file:
        image_file.write(content)

def writeline_to_failed_CSV(path, line):
    with open(path, 'a') as failed_file:
        failed_file.write(line + '\n')

def writeline_to_resumeinfo_file(info):
    with open('resumeinfo.csv', 'w') as resumeinfo_file:
        resumeinfo_file.write(info + '\n')

#--------


class MessageBox:
    def showMessage_InvalidRange(form):
        msg = QtWidgets.QMessageBox(form)
        msg.setText('Please select a valid range between 0 and 2176782335.')
        msg.setWindowTitle('Invalid range!')
        msg.setWindowIcon(QtGui.QIcon('robot.ico'))
        msg.exec_()

    def showMessage_SelectFolder(form):
        msg = QtWidgets.QMessageBox(form)
        msg.setText('Select an output folder first.')
        msg.setWindowTitle('No folder specified!')
        msg.setWindowIcon(QtGui.QIcon('robot.ico'))
        msg.exec_()


class Application:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = Form(self)
        self.UI = Ui_MainWindow()
        self.UI.setupUi(self.MainWindow, self)
        # Check for resuming...
        self.downloader_thread = Thread(target=self.startDownloading)
        self.folder_count = 1
        self.UI.setResumeCapability()

    def showWindow(self):
        self.is_window_closed = False
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    def validate_Date(self, date_text):
        year, month, day = eut.parsedate(date_text)[:3]
        if self.UI.dateEdit.date() <= QtCore.QDate(year, month, day):
            return True
        return False

    def create_new_folder(self, folder_name):
        if os.path.isdir(self.UI.dirpath_lineEdit.text() + '/' + folder_name) == False:
            os.mkdir(self.UI.dirpath_lineEdit.text() + '/' + folder_name)
        return folder_name

    def check_internet_connection(self):
        try:
            REQ.get('https://ismyinternetworking.com/')
            return True
        except:
            pass
        return False

    def start_DownloaderThread(self):
        if int(self.UI.startNumber_lineEdit.text()) > int(self.UI.endNumber_lineEdit.text()) or int(self.UI.endNumber_lineEdit.text()) > 2176782335:
            MessageBox.showMessage_InvalidRange(self.MainWindow)
            return
        if self.UI.dirpath_lineEdit.text() == '':
            MessageBox.showMessage_SelectFolder(self.MainWindow)
            return
        self.UI.startDownloader_Button.setEnabled(False)
        self.downloader_thread = Thread(target=self.startDownloading)
        self.downloader_thread.start()

    def startDownloading(self):
        start_lineNo = int(self.UI.startNumber_lineEdit.text())
        end_lineNo = int(self.UI.endNumber_lineEdit.text())
        #
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('start-maximized')
        #
        downloaded_count = 0
        remaining_count = end_lineNo - start_lineNo + 1
        self.UI.status_label.setText('Status: Opening chrome...')
        self.UI.downloadedCount_label.setText('Downloaded: 0')
        self.UI.remainingCount_label.setText('Remaining: ' + str(remaining_count))
        #
        driver = webdriver.Chrome(options=chrome_options)
        self.UI.status_label.setText('Status: Starting the downloads...')
        # E:/file_gen/
        input_file = open('sixchar.csv', 'r')
        input_file.seek(8 * start_lineNo)
        #----------------
        saved_count = 0
        folder_count = self.folder_count
        folder_name = 'f' + str(folder_count)
        self.create_new_folder(folder_name)
        for current_lineNo in range(start_lineNo, end_lineNo + 1):
            if self.is_window_closed == True:
                driver.quit()
                input_file.close()
                return
            if self.check_internet_connection() == False:
                driver.quit()
                input_file.close()
                self.UI.showInternetConnectionError()
                return
            #------------------------------------------
            image_name = input_file.readline().strip()
            try:
                self.UI.status_label.setText('Status: Navigating to https://prnt.sc/' + image_name)
                driver.get('https://prnt.sc/' + image_name)
                image_url = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'screenshot-image'))).get_attribute('src')
                #
                self.UI.status_label.setText('Status: GET request to image...')
                response = REQ.get(image_url)
                if not 'image' in response.headers['content-type']:
                    raise Exception
                image_extension = '.png'
                if response.headers['content-type'] == 'image/jpg' or response.headers['content-type'] == 'image/jpeg':
                    image_extension = '.jpg'
                #------------SAVING------------------------
                if self.validate_Date(response.headers['Last-Modified']) == True:
                    write_image_bytes(self.UI.dirpath_lineEdit.text() + '/' + folder_name + '/' + image_name + image_extension, response.content)
                    self.UI.status_label.setText('Status: Saved ' + image_name + image_extension)
                    downloaded_count += 1
                    self.UI.downloadedCount_label.setText('Downloaded: ' + str(downloaded_count))
                    remaining_count -= 1
                    self.UI.remainingCount_label.setText('Remaining: ' + str(remaining_count))
                    saved_count += 1
                else:
                    self.UI.status_label.setText('Status: Image was older, so skipped...')
                if saved_count == 50000:
                    saved_count = 0
                    folder_count += 1
                    folder_name = 'f' + str(folder_count)
                    self.UI.status_label.setText('Status: Creating new folder...')
                    self.create_new_folder(folder_name)
            except Exception as e:
                print(e)
                self.UI.status_label.setText('Status: Image ' + image_name + ' was unavailable.')
                writeline_to_failed_CSV(self.UI.dirpath_lineEdit.text() + '/Failed.csv', str(current_lineNo) + ',' + image_name)
            # resuming-file---
            writeline_to_resumeinfo_file(str(current_lineNo + 1) + ',' + str(end_lineNo) + ',' + self.UI.dateEdit.date().toString() + ',' + self.UI.dirpath_lineEdit.text() + ',' + str(folder_count + 1))
        #--------------------
        input_file.close()
        driver.quit()
        os.remove('resumeinfo.csv')
        self.folder_count = folder_count + 1
        self.UI.setNext_SuggestedRange(end_lineNo + 1)


#=====================================================================

def main():
    downloaderApp = Application()
    downloaderApp.showWindow()

if __name__ == '__main__':
    main()