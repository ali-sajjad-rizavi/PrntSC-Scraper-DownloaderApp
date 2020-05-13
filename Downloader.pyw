from threading import Thread
import requests as REQ
from bs4 import BeautifulSoup as BS
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

#---------------

my_headers = {
    'authority': 'prnt.sc',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

#---------------


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
        self.should_stop = False
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

    def stop_buttonClick(self):
        self.UI.stop_Button.setEnabled(False)
        self.UI.stopping_label.setText("Stopping...")
        self.should_stop = True

    def start_DownloaderThread(self):
        if int(self.UI.startNumber_lineEdit.text()) > int(self.UI.endNumber_lineEdit.text()) or int(self.UI.endNumber_lineEdit.text()) > 2176782335:
            MessageBox.showMessage_InvalidRange(self.MainWindow)
            return
        if self.UI.dirpath_lineEdit.text() == '':
            MessageBox.showMessage_SelectFolder(self.MainWindow)
            return
        self.UI.startDownloader_Button.setEnabled(False)
        self.UI.stop_Button.setEnabled(True)
        self.should_stop = False
        self.downloader_thread = Thread(target=self.startDownloading)
        self.downloader_thread.start()

    def startDownloading(self):
        start_lineNo = int(self.UI.startNumber_lineEdit.text())
        end_lineNo = int(self.UI.endNumber_lineEdit.text())
        #
        downloaded_count = 0
        remaining_count = end_lineNo - start_lineNo + 1
        self.UI.status_label.setText('Status: Connecting...')
        self.UI.downloadedCount_label.setText('Downloaded: 0')
        self.UI.remainingCount_label.setText('Remaining: ' + str(remaining_count))
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
                input_file.close()
                return
            #----------STOP--------------
            if self.should_stop == True:
                input_file.close()
                if os.path.isfile('resumeinfo.csv'):
                    os.remove('resumeinfo.csv')
                self.folder_count = 0
                self.UI.stopping_label.setText("")
                self.UI.startDownloader_Button.setEnabled(True)
                self.should_stop == False
                print('Stopped!')
                return
            #------------------------------------------
            image_name = input_file.readline().strip()
            try:
                self.UI.status_label.setText('Status: GET https://prnt.sc/' + image_name)
                image_url = BS(REQ.get('https://prnt.sc/' + image_name, headers=my_headers).text, 'html.parser').find('img', {'id':'screenshot-image'})['src']
                #
                self.UI.status_label.setText('Status: GET request to image...')
                response = REQ.get(image_url, headers=my_headers)
                if not 'image' in response.headers['content-type']:
                    raise Exception
                if len(response.content) == 4267:
                    raise Exception
                image_extension = '.png'
                if response.headers['content-type'] == 'image/jpg' or response.headers['content-type'] == 'image/jpeg':
                    image_extension = '.jpg'
                #------------SAVING------------------------
                if self.validate_Date(response.headers['Last-Modified']) == True:
                    self.UI.status_label.setText('Status: Saving ' + image_name + image_extension)
                    write_image_bytes(self.UI.dirpath_lineEdit.text() + '/' + folder_name + '/' + image_name + image_extension, response.content)
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
        os.remove('resumeinfo.csv')
        self.folder_count = folder_count + 1
        self.UI.setNext_SuggestedRange(end_lineNo + 1)
        print('Finished!')
        self.should_stop = False


#=====================================================================

def main():
    downloaderApp = Application()
    downloaderApp.showWindow()

if __name__ == '__main__':
    main()


#if self.check_internet_connection() == False:
    #driver.quit()
    #input_file.close()
    #self.UI.showInternetConnectionError()
    #return