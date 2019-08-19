from PyQt5 import QtGui
from PyQt5.QtWidgets import (QWidget, QProgressBar, QPushButton, QApplication, QHBoxLayout, QTextEdit, QMessageBox, QLabel)
from PyQt5.QtCore import QBasicTimer
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
from PyQt5.QtCore import Qt

def _w(s):
    return s.replace(' ', '\ ')

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
        self.exefilename = 'newhybsng'
        self.rpath = '.'

    def initUI(self):   

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(15, 180, 220, 25)

        self.btn = QPushButton('Start', self)
        self.btn.move(165, 200)
        self.btn.clicked.connect(self.doAction)

        self.burnin_label = QLabel(self)
        self.burnin_label.setText('Burnin:')
        self.burnin_label.move(10, 40)
        self.burnin_label.resize(50, 20)
        self.sweeps_label = QLabel(self)
        self.sweeps_label.setText('Sweeps:')
        self.sweeps_label.move(120, 40)
        self.sweeps_label.resize(50, 20)
       

        self.burnin_textbox = QTextEdit(self)
        self.burnin_textbox.move(60, 40)
        self.burnin_textbox.resize(50, 20)
        self.sweeps_textbox = QTextEdit(self)
        self.sweeps_textbox.move(175, 40)
        self.sweeps_textbox.resize(50, 20)

        self.core_label = QLabel(self)
        self.core_label.setText('Processer:')
        self.core_label.move(10, 90)
        self.core_label.resize(100, 20)
        self.core_label1 = QLabel(self)
        self.core_label1.setText('(Default is 4)')
        self.core_label1.move(150, 90)
        self.core_label1.resize(100, 20)
        self.core_textbox = QTextEdit(self)
        self.core_textbox.move(80, 90)
        self.core_textbox.resize(50, 20)

        self.run_label = QLabel(self)
        self.run_label.setText('# of Run:')
        self.run_label.move(10, 140)
        self.run_label.resize(100, 20)
        self.run_label1 = QLabel(self)
        self.run_label1.setText('(Default is 1)')
        self.run_label1.move(150, 140)
        self.run_label1.resize(100, 20)
        self.run_textbox = QTextEdit(self)
        self.run_textbox.move(80, 140)
        self.run_textbox.resize(50, 20)

        
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('NEWHYBRIDS')
        self.resize(860, 400)
        
        #self.openFileNameDialog()
        #self.openFileNamesDialog()
        #self.saveFileDialog()

        #self.quitButton = QPushButton('QUIT', self)
        #self.quitButton.move(400, 230)

        self.select_dir = QPushButton('Base Dir', self)
        self.select_dir.move(620, 260)
        self.select_dir.clicked.connect(self.open_dir)
        self.dir_textbox = QTextEdit(self)
        self.dir_textbox.move(10, 265)
        self.dir_textbox.resize(600,20)

        self.uploadButton_INFILE = QPushButton('INFILE' + ' UPLOAD', self)
        self.uploadButton_INFILE.move(620, 310)
        self.uploadButton_INFILE.clicked.connect(lambda: self.open('INFILE'))
        self.INFILE_textbox = QTextEdit(self)
        self.INFILE_textbox.move(10, 315)
        self.INFILE_textbox.resize(600,20)

        
        self.uploadButton_gtyp_cat_file = QPushButton('gtyp_cat_file' + ' UPLOAD', self)
        self.uploadButton_gtyp_cat_file.move(620, 360)
        self.uploadButton_gtyp_cat_file.clicked.connect(lambda: self.open('gtyp_cat_file'))
        self.gtyp_cat_file_textbox = QTextEdit(self)
        self.gtyp_cat_file_textbox.move(10, 365)
        self.gtyp_cat_file_textbox.resize(600,20)

        '''
        self.uploadButton_extraparams = QPushButton('extraparams' + ' UPLOAD', self)
        self.uploadButton_extraparams.move(620, 550)
        self.uploadButton_extraparams.clicked.connect(lambda: self.open('extraparams'))
        self.extraparams_textbox = QTextEdit(self)
        self.extraparams_textbox.move(10, 555)
        self.extraparams_textbox.resize(600,20)
        '''

        self.cmd_textbox0 = QLabel(self)
        self.cmd_textbox0.setText('Commands are shown below:')
        self.cmd_textbox0.move(250, 10)
        self.cmd_textbox0.resize(200,20)

        self.cmd_textbox = QLabel(self)
        self.cmd_textbox.setStyleSheet("font: 8pt")
        self.cmd_textbox.setWordWrap(True)
        self.cmd_textbox.move(250, 40)
        self.cmd_textbox.resize(600,200)
        self.cmd_textbox.setAlignment(Qt.AlignTop)
        
        
        self.show()

     
    def open(self, _key):
        filename = QFileDialog.getOpenFileName(self, 'Open File', self.rpath)
        print(_key)
        print('Path file :'+str(filename)) 
        if _key == 'gtyp_cat_file':
            self.gtyp_cat_file_textbox.setText(filename[0])
        elif _key == 'extraparams':
            self.extraparams_textbox.setText(filename[0])
        elif _key == 'INFILE':

            self.INFILE_textbox.setText(filename[0])

    def open_dir(self):
        _dir= QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\', QFileDialog.ShowDirsOnly)
        self.dir_textbox.setText(_dir)
        self.rpath = _dir

    def open_gtyp_cat_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')
        print('Path file :'+str(filename)) 
        self.gtyp_cat_file = filename[0] 

    def open_gtyp_cat_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File', '.')
        print('Path file :'+str(filename)) 
        self.gtyp_cat_file = filename[0] 


    

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
                    error.append('Processor is not valid!')

            if burnin:
                try:
                    self.burnin = int(burnin)
                except:
                    error.append('Burnin is not valid!')
            else:
                error.append('Burnin is empty!')

            if sweeps:
                try:
                    self.sweeps = int(sweeps)
                except:
                    error.append('Sweeps is not valid!')
            else:
                error.append('Sweeps is empty!')

            if run_num:
                try:
                    self.run_num = int(run_num)
                except:
                    error.append('# of Run is not valid!')


            base_dir = self.dir_textbox.toPlainText()
            if base_dir:
                if base_dir.startswith('file://'):
                    base_dir = base_dir.strip()[7:]
                    base_dir = base_dir.rstrip('/')
                self.base_dir = base_dir
            else:
                #self.base_dir = '/Users/wenluwang/Documents/parallel_structure/newhybrids'
                error.append('Base Dir is empty!')

            INFILE = self.INFILE_textbox.toPlainText()
            if INFILE:
                if INFILE.startswith('file://'):
                    INFILE = INFILE.strip()[7:]
                self.INFILE = INFILE
            else:
                #self.INFILE = '/Users/wenluwang/Documents/parallel_structure/newhybrids/test_data/TestDat.txt'
                error.append('INFILE is empty!')

            
            gtyp_cat_file = self.gtyp_cat_file_textbox.toPlainText()
            if gtyp_cat_file:
                if gtyp_cat_file.startswith('file://'):
                    gtyp_cat_file = gtyp_cat_file.strip()[7:]
                self.gtyp_cat_file = gtyp_cat_file
            else:
                #pass
                error.append('gtyp_cat_file is empty!')

            '''
            extraparams = self.extraparams_textbox.toPlainText()
            if extraparams:
                self.extraparams = extraparams
            else:
                pass
                #error.append('extraparams is empty!')
            '''
             

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
                                verror.append(_f + ' does not exists.')

                        #validation = all([os.path.exists(_out + '/' + _filename) for _filename in _filenames])

                except Exception as e:
                    print('Hybrid validation exception.' + str(e))
                    validation = False



                if not validation:
                    QMessageBox.about(self, 'Alert', 'You are propbably having an error. \nPlease check ' + os.path.join(self.base_dir, 'stdout') + '\n' + '\n'.join(verror))
                else:
                    time_msg = '\nParallel execution time %s'%str(datetime.timedelta(seconds=total_time)) 
    
                    QMessageBox.about(self, 'Job done!', 'Please check folder\n' + self.outdir + '\n' + os.path.join(self.base_dir, 'stdout') + time_msg)
               
                print('Validation:'+ str(validation))
            
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
        import os, shutil
        for anyfile in os.listdir(directory):
            file_path = os.path.join(directory, anyfile)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)    
            except Exception as e:
                print(e)
                
        

    def run(self):  
        
        TEST_NO_PARALLEL = False

        self.outdir = os.path.join(self.base_dir, 'output') #create output folders at the location of structure exe file
        
        directory = os.path.join(self.base_dir, 'stdout')
       
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            self.del_files_in_folder(directory)
        
        #directory = os.path.join(self.base_dir, 'output')
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
        # 1. remove all output folders
        subprocess.call(['rm -r {0}/output_run_*'.format(_w(self.base_dir))], shell = True)

        st = time.time()
        for batch in range(n_batch):
             
            start = batch*batch_size
            end = min(start+batch_size, n_task)
            res = manager.list()

            # 2. create tmp folders
            for i in range(start, end):
                #tmp_dir = self.base_dir + '_run_%d'%(i+1)
                #subprocess.call(['mkdir {0}'.format(_w(tmp_dir))], shell = True)
                #subprocess.call(['cp {0}/{1} {2}/'.format(_w(self.base_dir), self.exefilename, _w(tmp_dir))], shell = True)
                subprocess.call(['mkdir {0}/output_run_{1}'.format(_w(self.base_dir), i+1)], shell = True)


                      
            CMD = '{0} -d {1} --no-gui'.format(self.exefilename, self.INFILE)

            if 'sweeps' in param_dict:
                CMD += ' --num-sweeps %d'%param_dict['sweeps']
            if 'burnin' in param_dict:
                CMD += ' --burn-in %d'%param_dict['burnin']
            if 'gtyp_cat_file' in param_dict:
                CMD += ' --gtyp-cat-file {0}'.format(_w(param_dict['gtyp_cat_file']))


            
            cmds = [str(i+1) + ': ' + CMD for i in range(start,end)]
            
            #cmds = [str(i+1) + ': {0} -d {1} --no-gui'.format(self.exefilename, self.INFILE) for i in range(start,end)]
          
  
            self.cmd_textbox.setText('Running commands...')



            QApplication.processEvents()
            QApplication.processEvents()
            

            self.cmd_textbox.setText('\n'.join(cmds))

            QApplication.processEvents()
            QApplication.processEvents()

            procs = [Process(target=self._worker, args=('run_%d'%(i+1), res, param_dict)) for i in range(start,end)]
            
            for p in procs:
                p.start()
            for p in procs: 
                p.join()

            self.finished += sum(res) 

            '''
            for i in range(start, end):
                tmp_dir = self.base_dir + '_run_%d'%(i+1)
                subprocess.call(['cp {0}/aa-* {1}/output_run_{2}/'.format(_w(tmp_dir), _w(self.base_dir), i+1)], shell = True)
                subprocess.call(['rm -r {0}'.format(_w(tmp_dir))], shell = True)
            '''

            self.pbar.setValue(self.finished*(100/n_task))

        ed = time.time()
        total_time = ed-st
        print('Parallel Total time:'+str(total_time))
        return int(total_time)
       
    def _worker(self, proc_name, res, param_dict):
        print(proc_name)
        
        INFILE = param_dict['INFILE']
        outdir = param_dict['outdir']
        base_dir = param_dict['base_dir']
        #gtyp_cat_file = param_dict['gtyp_cat_file']
        #extraparams = param_dict['extraparams']
        stdout_dir = os.path.join(base_dir, 'stdout')


        #tmp_dir = base_dir + '_%s'%proc_name
        tmp_dir = base_dir+ '/output_' + proc_name

        base_dir = self.base_dir.replace(' ', '\ ')
        cmd = base_dir+'/{0} -d {1} --no-gui'.format(self.exefilename, _w(INFILE))
        if 'sweeps' in param_dict:
            cmd += ' --num-sweeps %d'%param_dict['sweeps']
        if 'burnin' in param_dict:
            cmd += ' --burn-in %d'%param_dict['burnin']
        if 'gtyp_cat_file' in param_dict:
            cmd += ' --gtyp-cat-file {0}'.format(_w(param_dict['gtyp_cat_file']))

        print(cmd)
        
        with open(os.path.join(stdout_dir, 'stdout_%s.txt'%proc_name), "w") as f:
            subprocess.call([cmd], cwd=tmp_dir, shell = True, stdout=f, stderr=f) 
        
        res.append(1)

   

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())