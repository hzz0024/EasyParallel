from PyQt5 import QtGui
import PyQt5.sip
from PyQt5.QtWidgets import (QWidget, QProgressBar, QPushButton, QApplication, QHBoxLayout, QTextEdit, QMessageBox, QLabel)
from PyQt5.QtCore import QBasicTimer, Qt
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
import glob
from pathlib import Path, PureWindowsPath

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
        self.gtyp_cat_file = ''
        self.extraparams = ''
        self.burnin = -1
        self.sweeps = -1
        self.process_num = 4
        self.finished = 0
        self.run_num = 1
        self.exefilename = 'newhybrids'
        self.rpath = '.'

    def initUI(self):   


        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(15, 210, 450, 25)

        self.btn = QPushButton('Start', self)
        self.btn.move(290, 250)
        self.btn.clicked.connect(self.doAction)

        self.burnin_label = QLabel(self)
        self.burnin_label.setText('Burnin:')
        self.burnin_label.move(10, 40)
        self.burnin_label.resize(100, 30)
        self.sweeps_label = QLabel(self)
        self.sweeps_label.setText('Sweeps:')
        self.sweeps_label.move(230, 40)
        self.sweeps_label.resize(100, 30)
       

        self.burnin_textbox = QTextEdit(self)
        self.burnin_textbox.move(90, 40)
        self.burnin_textbox.resize(120, 30)
        self.sweeps_textbox = QTextEdit(self)
        self.sweeps_textbox.move(320, 40)
        self.sweeps_textbox.resize(120, 30)

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
        self.core_textbox.resize(70, 30)

        self.run_label = QLabel(self)
        self.run_label.setText('# of Run:')
        self.run_label.move(10, 140)
        self.run_label.resize(100, 30)
        self.run_label1 = QLabel(self)
        self.run_label1.setText('(Default is 1)')
        self.run_label1.move(250, 140)
        self.run_label1.resize(200, 30)
        self.run_textbox = QTextEdit(self)
        self.run_textbox.move(120,140)
        self.run_textbox.resize(100, 30)


        self.timer = QBasicTimer()
        self.step = 0
        
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('newhybrids')
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

        
        self.uploadButton_gtyp_cat_file = QPushButton('gtyp_cat_file' + ' UPLOAD', self)
        self.uploadButton_gtyp_cat_file.move(920, 460)
        self.uploadButton_gtyp_cat_file.clicked.connect(lambda: self.open('gtyp_cat_file'))
        self.gtyp_cat_file_textbox = QTextEdit(self)
        self.gtyp_cat_file_textbox.move(10, 465)
        self.gtyp_cat_file_textbox.resize(900,30)

        '''
        self.uploadButton_extraparams = QPushButton('extraparams' + ' UPLOAD', self)
        self.uploadButton_extraparams.move(920, 550)
        self.uploadButton_extraparams.clicked.connect(lambda: self.open('extraparams'))
        self.extraparams_textbox = QTextEdit(self)
        self.extraparams_textbox.move(10, 555)
        self.extraparams_textbox.resize(900,30)
        '''

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
        if _key == 'gtyp_cat_file':
            #self.gtyp_cat_file = filename[0]  
            self.gtyp_cat_file_textbox.setText(filename[0])
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

            burnin = self.burnin_textbox.toPlainText()
            sweeps = self.sweeps_textbox.toPlainText()
            process_num = self.core_textbox.toPlainText()
            run_num = self.run_textbox.toPlainText()


            if process_num:
                try:
                    self.process_num = int(process_num)
                except:
                    error.append('# Processer is not valid!')

            if burnin:
                try:
                    self.burnin = int(burnin)
                except: 
                    error.append('Burnin is empty!')
            else:
                error.append('Burnin is empty!')

            if sweeps:
                try: 
                    self.sweeps = int(sweeps)
                except:
                    error.append('Sweeps is empty!')
            else:
                error.append('Sweeps is empty!')

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
                #self.base_dir = 'c:/newhybrid'
                error.append('Base Dir is empty!')

            INFILE = self.INFILE_textbox.toPlainText()
            if INFILE:
                if INFILE.startswith('file:///'):
                    INFILE = INFILE.strip()[8:]
                self.INFILE = INFILE
            else:
                #self.INFILE = 'c:/newhybrid/test_data/TestDatWithOptions.txt'
                error.append('INFILE is empty!')

            
            gtyp_cat_file = self.gtyp_cat_file_textbox.toPlainText()
            if gtyp_cat_file:
                if gtyp_cat_file.startswith('file:///'):
                    gtyp_cat_file = gtyp_cat_file.strip()[8:]
                self.gtyp_cat_file = gtyp_cat_file
            else:
                #pass
                #self.gtyp_cat_file = 'c:/newhybrid/gtyp_cat_file'
                error.append('gtyp_cat_file is empty!')


            if error:
                QMessageBox.about(self, 'Alert', '\n'.join(error))
            else:
        
                total_time = self.run()
                validation = True
                verror = []
                try:
                    #validate stdout
                    _std = self.base_dir + '/' + 'stdout'
                    for _num in range(1, self.run_num+1):
                        _f = _std + '/' + 'stdout_run_%s.txt'%str(_num)
                        if not _read_file(_f).startswith('COMM_LINE_OPTS'):
                            validation = False
                            break

                    #validate generated files
                    for _num in range(1, self.run_num+1):
                        _out = self.base_dir + '/' + 'output_run_%s'%str(_num)
                        _filenames = ['aa-EchoedGtypFreqCats.txt', 'aa-LociAndAlleles.txt', 'aa-Pi.aves', \
                                        'aa-Pi.hist', 'aa-PofZ.txt', 'aa-ScaledLikelihood.txt', \
                                        'aa-Theta.hist', 'aa-ThetaAverages.txt']
                        for _filename in _filenames:
                            _f = _out + '/' + _filename
                            if not os.path.exists(_f):
                                validation = False
                                verror.append(_f + ' does not exist.')

                except Exception as e:
                    print('Hybrid validation exception.' + str(e))
                    validation = False


                if not validation:
                    QMessageBox.about(self, 'Alert', 'You are propbably having an error. \nPlease check ' + \
                        self.base_dir + '/stdout' + ' and ' + self.base_dir + '/output\n' + '\n'.join(verror))
                else:
                    time_msg = '\nParallel execution time %s'%str(datetime.timedelta(seconds=total_time)) 
    
                    QMessageBox.about(self, 'Job done!', 'Please check folder\n' + self.outdir + '\n' + _path_join(self.base_dir, 'stdout') + time_msg)
               
            
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
                

    def run(self):  
    
        TEST_NO_PARALLEL = False

        self.outdir = _path_join(self.base_dir, 'output') #create output folders at the location of structure exe file
        
        directory = _path_join(self.base_dir, 'stdout')
       
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            self.del_files_in_folder(directory)
        
        #directory = _path_join(self.base_dir, 'output')
        #if not os.path.exists(directory):
        #    os.makedirs(directory)
        #else:
        #    self.del_files_in_folder(directory)

        '''
        Command line parameters prevail over gtyp_cat_file file according to the code of structure
        '''
       
        param_dict = {}
        param_dict['INFILE'] = self.INFILE
        if self.gtyp_cat_file:
            param_dict['gtyp_cat_file'] = self.gtyp_cat_file
        param_dict['extraparams'] = self.extraparams
        param_dict['base_dir'] = self.base_dir
        param_dict['outdir'] = self.outdir
        if self.sweeps != -1:
            param_dict['sweeps'] = self.sweeps
        if self.burnin != -1:
            param_dict['burnin'] = self.burnin

        '''
        inputs
        '''
 
        n_task = self.run_num

        if TEST_NO_PARALLEL:
            st = time.time()
            for i in range(n_task):
                _worker('run_%i'%(i+1), [], param_dict)
            ed = time.time()
            print('NO parallel Total time:'+str(ed-st))
        
        batch_size = self.process_num
        n_batch = int((n_task+batch_size-1) / batch_size)

        manager = multiprocessing.Manager()
        res = manager.list()

        #1: remove output_run_i from last run

        folders = [_winpath(_) for _ in glob.glob(self.base_dir+'/output_run_*')]
        if folders:
            print(['rd', '/s', '/q'] + folders)
            subprocess.call(['rd', '/s', '/q'] + folders, shell = True)
        

        st = time.time()
        print(n_task)
        for batch in range(n_batch):
            
            start = batch*batch_size
            end = min(start+batch_size, n_task)
            res = manager.list()

            #print cmd
            CMD = ': {0}/{1} --no-gui -d {2} '.format(param_dict['base_dir'], self.exefilename, param_dict['INFILE'])
            if 'sweeps' in param_dict:
                CMD += ' --num-sweeps %d'%param_dict['sweeps']
            if 'burnin' in param_dict:
                CMD += ' --burn-in %d'%param_dict['burnin']
            if 'gtyp_cat_file' in param_dict:
                CMD += ' --gtyp-cat-file {0}'.format(param_dict['gtyp_cat_file'])

            cmds = [str(i+1) + ': ' + CMD for i in range(start,end)]
            

            #2: create tmp copies
            
            for i in range(start, end):
                #tmp_dir = self.base_dir + '_run_%d'%(i+1)
                #print(['mkdir', _winpath(tmp_dir)])
                #subprocess.call(['mkdir', _winpath(tmp_dir)], shell=True)
                #print(['copy', _winpath(self.base_dir+'/'+self.exefilename+'.exe'), _winpath(tmp_dir+'/')])
                #subprocess.call(['copy', _winpath(self.base_dir+'/'+self.exefilename+'.exe'), _winpath(tmp_dir+'/')], shell=True)
                print(['mkdir', _winpath('{0}/output_run_{1}'.format(self.base_dir, i+1))])
                subprocess.call(['mkdir', _winpath('{0}/output_run_{1}'.format(self.base_dir, i+1))], shell=True)
            

            self.cmd_textbox.setText('\n'.join(cmds))

            QApplication.processEvents() 
            QApplication.processEvents() 
            QApplication.processEvents() 

            procs = [Process(target=_worker, args=('run_%d'%(i+1), res, param_dict, self.exefilename)) for i in range(start,end)]
            
            for p in procs:
                p.start()
            for p in procs: 
                p.join()
            self.finished += sum(res) 
            
            #3: move generated files to outout_run_i, remove tmp copies

            '''
            for i in range(start, end):
                tmp_dir = self.base_dir + '_run_%d'%(i+1)
                files = [_winpath(_) for _ in glob.glob('{0}/aa-*'.format(tmp_dir))]
                for _f in files:
                    print(['copy', _f, '{0}/output_run_{1}/'.format(self.base_dir, i+1)])
                    subprocess.call(['copy', _f, _winpath('{0}/output_run_{1}/'.format(self.base_dir, i+1))], shell=True)
                print(['rd','/s', '/q', _winpath(tmp_dir)])
                subprocess.call(['rd', '/s', '/q', _winpath(tmp_dir)], shell=True)
            '''

            self.pbar.setValue(self.finished*(100/n_task))

        ed = time.time()
        total_time = ed-st
        print('Parallel Total time:'+str(total_time))
        return int(total_time)
       
def _worker(proc_name, res, param_dict, exefilename):
    print(proc_name)
    
    INFILE = param_dict['INFILE']
    outdir = param_dict['outdir']
    base_dir = param_dict['base_dir']
    #gtyp_cat_file = param_dict['gtyp_cat_file']
    #extraparams = param_dict['extraparams']
    stdout_dir = _path_join(base_dir, 'stdout')


    #tmp_dir = base_dir + '_%s'%proc_name
    tmp_dir = base_dir + '/output_%s'%proc_name

    #cmds = [tmp_dir+'/%s'%exefilename, '--no-gui', '-d', INFILE]
    cmds = [base_dir + '/' + exefilename, '--no-gui', '-d', INFILE]
    
    if 'sweeps' in param_dict:
        cmds.extend(['--num-sweeps', str(param_dict['sweeps'])])
    if 'burnin' in param_dict:
        cmds.extend(['--burn-in', str(param_dict['burnin'])])
    if 'gtyp_cat_file' in param_dict:
        cmds.extend(['--gtyp-cat-file', param_dict['gtyp_cat_file']])


    print(cmds)
    with open(_path_join(stdout_dir, 'stdout_%s.txt'%proc_name), "w") as f:
        subprocess.call(cmds, cwd=tmp_dir, shell = True, stdout=f, stderr=f) 
    
    res.append(1)

   

        
if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())