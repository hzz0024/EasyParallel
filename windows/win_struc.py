from PyQt5 import QtGui
import PyQt5.sip
from PyQt5.QtWidgets import (QWidget, QProgressBar, QPushButton, QApplication, QHBoxLayout, QTextEdit, QMessageBox, QLabel)
from PyQt5.QtCore import QBasicTimer, Qt, QFileInfo
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
import time
import datetime
import os
import sys
import subprocess
import os
import multiprocessing
from multiprocessing import Process
from multiprocessing import Pool
import glob
from pathlib import Path, PureWindowsPath
import random

def _winpath(s):
    return str(PureWindowsPath(Path(s)))

def _path_join(a, b):
    return a + '/' + b

def _read_file(_f, num=10):
    re = ''
    with open(_f, 'r') as f:
        lines = f.readlines()
        for i, l in enumerate(lines):
            l = l.strip('-')
            if i<num and l != '\n':
                re += l
    re = re.strip('-')
    return re
    
class App(QWidget):
    
    def __init__(self):
        super().__init__()  
        self.initUI()
        self._init_params()
        

    def _init_params(self):
        self.base_dir = ''    
        self.INFILE = ''
        self.mainparams = ''
        self.extraparams = ''
        self.k1 = -1
        self.k2 = -1
        self.process_num = 4
        self.finished = 0
        self.run_num = 4
        self.rpath = '.'

    def initUI(self):   


        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(15, 210, 450, 25)

        self.btn = QPushButton('Start', self)
        self.btn.move(290, 250)
        self.btn.clicked.connect(self.doAction)

        self.k_label1 = QLabel(self)
        self.k_label1.setText('MAXPOPS (K):')
        self.k_label1.move(10, 40)
        self.k_label1.resize(150, 30)
        self.k_label2 = QLabel(self)
        self.k_label2.setText('---')
        self.k_label2.move(270, 40)
        self.k_label2.resize(40, 30)
       

        self.k1_textbox = QTextEdit(self)
        self.k1_textbox.move(170, 40)
        self.k1_textbox.resize(100, 30)
        self.k2_textbox = QTextEdit(self)
        self.k2_textbox.move(300, 40)
        self.k2_textbox.resize(100, 30)

        self.core_label = QLabel(self)
        self.core_label.setText('Processer:')
        self.core_label.move(10, 90)
        self.core_label.resize(150, 30)
        self.core_label1 = QLabel(self)
        self.core_label1.setText('(Default is 4)')
        self.core_label1.move(250, 90)
        self.core_label1.resize(200, 30)
        self.core_textbox = QTextEdit(self)
        self.core_textbox.move(150, 90)
        self.core_textbox.resize(80, 30)

        self.run_label = QLabel(self)
        self.run_label.setText('# of Run:')
        self.run_label.move(10, 140)
        self.run_label.resize(100, 30)
        self.run_label1 = QLabel(self)
        self.run_label1.setText('(Default is 4)')
        self.run_label1.move(250, 140)
        self.run_label1.resize(200, 40)
        self.run_textbox = QTextEdit(self)
        self.run_textbox.move(130, 140)
        self.run_textbox.resize(90, 30)


        self.timer = QBasicTimer()
        self.step = 0
        
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('STRUCTURE')
        self.resize(1200, 600)
        
        #self.openFileNameDialog()
        #self.openFileNamesDialog()
        #self.saveFileDialog()

        #self.quitButton = QPushButton('QUIT', self)
        #self.quitButton.move(400, 230)

        self.select_dir = QPushButton('Base Dir', self)
        self.select_dir.move(920, 360)
        self.select_dir.clicked.connect(self.open_dir)
        self.dir_textbox = QTextEdit(self)
        self.dir_textbox.move(10, 365)
        self.dir_textbox.resize(900,30)

        self.uploadButton_INFILE = QPushButton('INFILE' + ' UPLOAD', self)
        self.uploadButton_INFILE.move(920, 410)
        self.uploadButton_INFILE.clicked.connect(lambda: self.open('INFILE'))
        self.INFILE_textbox = QTextEdit(self)
        self.INFILE_textbox.move(10, 415)
        self.INFILE_textbox.resize(900,30)

        self.uploadButton_mainparams = QPushButton('mainparams' + ' UPLOAD', self)
        self.uploadButton_mainparams.move(920, 460)
        self.uploadButton_mainparams.clicked.connect(lambda: self.open('mainparams'))
        self.mainparams_textbox = QTextEdit(self)
        self.mainparams_textbox.move(10, 465)
        self.mainparams_textbox.resize(900,30)

        
        self.uploadButton_extraparams = QPushButton('extraparams' + ' UPLOAD', self)
        self.uploadButton_extraparams.move(920, 510)
        self.uploadButton_extraparams.clicked.connect(lambda: self.open('extraparams'))
        self.extraparams_textbox = QTextEdit(self)
        self.extraparams_textbox.move(10, 515)
        self.extraparams_textbox.resize(900,30)


        self.cmd_textbox0 = QLabel(self)
        self.cmd_textbox0.setText('Commands are shown below:')
        self.cmd_textbox0.move(450, 10)
        self.cmd_textbox0.resize(400,20)

        self.cmd_textbox = QLabel(self)
        self.cmd_textbox.setStyleSheet("font: 8pt")
        self.cmd_textbox.setWordWrap(True)
        self.cmd_textbox.move(450, 30)
        self.cmd_textbox.resize(700,200)
        self.cmd_textbox.setAlignment(Qt.AlignTop)
        
        
        self.show()

     
    def open(self, _key):
        
        filename = QFileDialog.getOpenFileName(self, 'Open File', self.rpath)
        
        print(_key)
        print('Path file :'+str(filename)) 
        if _key == 'mainparams':
            #self.mainparams = filename[0]  
            self.mainparams_textbox.setText(filename[0])
        elif _key == 'extraparams':
            #self.extraparams = filename[0]
            self.extraparams_textbox.setText(filename[0])
        elif _key == 'INFILE':
            #self.INFILE = filename[0]
            self.INFILE_textbox.setText(filename[0])

    def open_dir(self):
        _dir= QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        self.dir_textbox.setText(_dir)
        self.rpath = _dir


    

    def doAction(self):

        if self.finished != 0 and self.finished < 100:
            self.btn.setText('Wait please...')

        else:         
            error = []

            k1 = self.k1_textbox.toPlainText()
            k2 = self.k2_textbox.toPlainText()
            process_num = self.core_textbox.toPlainText()
            run_num = self.run_textbox.toPlainText()


            if process_num:
                try:
                    self.process_num = int(process_num)
                except:
                    error.append('Processor is not valid!')

            if k1:
                try:
                    self.k1 = int(k1)
                except:
                    error.append('K1 is not valid!')
            else:
                error.append('K1 is empty!')

            if k2:
                try:
                    self.k2 = int(k2)
                except:
                    error.append('K2 is not valid!')
            else:
                error.append('K2 is empty!')

            if run_num:
                try:
                    self.run_num = int(run_num)
                except:
                    error.append('# of Run is not valid!')



            base_dir = self.dir_textbox.toPlainText()
            if base_dir:
                if base_dir.startswith('file:///'):
                    base_dir = base_dir.strip()[8:]
                self.base_dir = base_dir
            else:
                #self.base_dir = 'c:/con sole'
                error.append('Base Dir is empty!')

            INFILE = self.INFILE_textbox.toPlainText()
            if INFILE:
                if INFILE.startswith('file:///'):
                    INFILE = INFILE.strip()[8:]
                self.INFILE = INFILE
            else:
                #self.INFILE = 'c:/con sole/testdata1'
                error.append('INFILE is empty!')

            mainparams = self.mainparams_textbox.toPlainText()
            if mainparams:
                if mainparams.startswith('file:///'):
                    mainparams = mainparams.strip()[8:]
                self.mainparams = mainparams
            else:
                #self.mainparams = 'c:/con sole/mainparams'
                error.append('mainparams is empty!')

            extraparams = self.extraparams_textbox.toPlainText()
            if extraparams:
                if extraparams.startswith('file:///'):
                    extraparams = extraparams.strip()[8:]
                self.extraparams = extraparams
            else:
                #self.extraparams = 'c:/con sole/extraparams'
                error.append('extraparams is empty!')

            if error:
                QMessageBox.about(self, 'Alert', '\n'.join(error))
            else:

                #remove output folders from last run
                folders = [_winpath(_) for _ in glob.glob(self.base_dir+'/output*')]
                if folders:
                    print(['rd', '/s', '/q'] + folders)
                    subprocess.call(['rd', '/s', '/q'] + folders, shell = True)
                folders = [_winpath(_) for _ in glob.glob(self.base_dir+'/stdout*')]
                if folders:
                    print(['rd', '/s', '/q'] + folders)
                    subprocess.call(['rd', '/s', '/q'] + folders, shell = True)

                validation = True
                if False and self.k1 == self.k2 and self.k1>0 and self.k2>0:

                    total_time = self.run(self.k1)
                    try:
                        _std = self.base_dir + '/' + 'stdout_k%s'%str(self.k1)
                        for _num in range(1, self.run_num+1):
                            _f = _std + '/' + 'stdout_run_%s.txt'%str(_num)
                            if not _read_file(_f).startswith('STRUCTURE'):
                                validation = False
                                print(_f + 'is wrong')
                                break

                        _out = self.base_dir + '/' + 'output_k%s'%str(self.k1)
                        for _num in range(1, self.run_num+1):
                            _f = _out + '/' + 'run_%s_f'%str(_num)
                            if not _read_file(_f).startswith('STRUCTURE'):
                                validation = False
                                print(_f + 'is wrong')
                                break
                    except Exception as e:
                        print(str(e))
                        validation = False

                    if not validation:
                        print('total time:' + str(total_time) + '. files validation:' + str(validation))
                        QMessageBox.about(self, 'Alert', 'You are propbably having an error. \nPlease check ' + self.base_dir + '/stdout' )
                    else:
                        time_msg = '\nParallel execution time %s'%str(datetime.timedelta(seconds=total_time)) 
                
        
                        QMessageBox.about(self, 'Job done!', 'Please check folder\n' + self.outdir + '\n' + _path_join(self.base_dir, 'stdout') + time_msg)
                elif self.k2 >= self.k1 and self.k1>0 and self.k2>0:
                    total_time = 0
                    joblist = []
                    for _k in range(self.k1, self.k2+1):
                        jobs, param_dict = self.run(_k)
                        joblist.extend(jobs)
                    
                    total_time = self.run_all(joblist, param_dict)

                    
                    try:
                        _std = self.base_dir + '/' + 'stdout'
                        n_task = self.run_num * (self.k2 - self.k1 + 1)
                        for _num in range(1, n_task+1):
                            _f = _std + '/' + 'stdout_run_%s.txt'%str(_num)
                            if not _read_file(_f).startswith('STRUCTURE'):
                                validation = False
                                print(_f + 'is wrong')
                                break

                        _out = self.base_dir + '/' + 'output'
                        for _k in range(self.k1, self.k2+1):
                            
                            for _num in range(1, self.run_num+1):
                                _f = _out + '/' + 'run_k{0}_{1}_f'.format(_k, _num)
                                if not _read_file(_f).startswith('STRUCTURE'):
                                    validation = False
                                    print(_f + 'is wrong')
                                    break

                    except Exception as e:
                        print('Validation checking:' + str(e))
                        validation = False
                    

                    if not validation:
                        QMessageBox.about(self, 'Alert', 'You are propbably having an error. \nPlease check ' + self.base_dir + '/stdout')
                    else:
                        time_msg = '\nParallel execution time %s'%str(datetime.timedelta(seconds=total_time)) 
        
                        QMessageBox.about(self, 'Job done!', 'Please check folder\n' + self.outdir + '\n' + _path_join(self.base_dir, 'stdout') + time_msg)
                else:
                    QMessageBox.about(self, 'Alert', 'K1 %s --- K2 %s is not valid!'%(str(k1), str(k2)))

            
                self.btn.setText('Start')
                self.cmd_textbox.setText('')
                self.pbar.setValue(0)
                self._init_params()
                

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
 
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)
 
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)


    def del_files_in_folder(self, directory):
        for anyfile in os.listdir(directory):
            file_path = _path_join(directory, anyfile)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)    
            except Exception as e:
                print(e)
                
        

    def run(self, k=-1):  

    


        self.outdir = _path_join(self.base_dir, 'output') #create output folders at the location of structure exe file
        
        self.stdout_dir = _path_join(self.base_dir, 'stdout')

      
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)
        else:
            self.del_files_in_folder(self.outdir)
    
      
        if not os.path.exists(self.stdout_dir):
            os.makedirs(self.stdout_dir)
        else:
            self.del_files_in_folder(self.stdout_dir)

        '''
        Command line parameters prevail over mainparams file according to the code of structure
        '''
       
        param_dict = {}
        param_dict['INFILE'] = self.INFILE
        param_dict['mainparams'] = self.mainparams
        param_dict['extraparams'] = self.extraparams
        param_dict['base_dir'] = self.base_dir
        param_dict['outdir'] = self.outdir
        if k != -1:
            param_dict['k'] = k


        INFILE = param_dict['INFILE']
        outdir = param_dict['outdir']
        base_dir = param_dict['base_dir']
        mainparams = param_dict['mainparams']
        extraparams = param_dict['extraparams']
        stdout_dir = _path_join(base_dir, 'stdout')



        '''
        inputs
        '''

        jobs = []
        for i in range(self.run_num):
            proc_name = 'run_k{0}_{1}'.format(param_dict['k'], i+1)
            cmd = [base_dir+'/structure', '-i', INFILE, '-o', _path_join(self.outdir,proc_name), '-m', mainparams, '-e', extraparams]

            if 'k' in param_dict:
                cmd.extend(['-K', str(param_dict['k'])])
                #cmd += ' -K %d'%param_dict['k']

            r1 = random.random()
            r2 = random.random()
            r = 10000*int(r1*32767) + int(r2*32767)
            cmd.extend(['-D', str(r)])  

            jobs.append(cmd)

        return jobs, param_dict
 
      
    def run_all(self, joblist, param_dict):  

    


        self.outdir = _path_join(self.base_dir, 'output') #create output folders at the location of structure exe file
        self.stdout_dir = _path_join(self.base_dir, 'stdout')
     
        

        n_task = len(joblist)



        st = time.time()
        args = [['run_%d'%(i+1) , job, self.base_dir] for i, job in enumerate(joblist)]


        with Pool(processes=self.process_num) as pool:
            pcmds = []
            for _progress, _ in enumerate(pool.imap_unordered(_worker, args)):
                pcmds.append(' '.join(args[_progress][1]))
                if len(pcmds) == self.process_num: 
                    QApplication.processEvents() 
                    self.cmd_textbox.setText('\n'.join(pcmds))
                    pcmds = []
                    print(_progress)
                    print(n_task)
                    self.pbar.setValue((_progress+1)*(100/n_task))
                    QApplication.processEvents()
            self.cmd_textbox.setText('\n'.join(pcmds))
            self.pbar.setValue(n_task*(100/n_task))
            QApplication.processEvents()
        
  
        ed = time.time()
        total_time = ed-st
        print('Parallel Total time:'+str(total_time))
        return int(total_time)
       
def _worker(arg):
    proc_name, cmd, base_dir = arg
    print(proc_name)

    stdout_dir = _path_join(base_dir, 'stdout')
    
    with open(_path_join(stdout_dir, 'stdout_%s.txt'%proc_name), "w") as f:
        subprocess.call(cmd, shell=True, stdout=f, stderr=f) 
    


    
    outfile =  cmd[4] + '_f'
    with open(outfile, 'r') as f:
        ls = f.readlines()
    a = ls[11].replace('Command line arguments:','').strip()
    b = ' '.join(cmd).strip()
    assert a == b
    
   

        
if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())