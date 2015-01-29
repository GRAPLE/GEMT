#!/usr/bin/env python
import os
from os import listdir
from os.path import isdir, isfile, join
import zipfile, tarfile
import subprocess
import argparse
import logging
import shutil

CONFIG = {
    'SimsPerJob' : '5',
    'RunR' : 'False',
    'Rmain' : 'RunSimulation.R',
    'Rexe' : 'C:\\Program Files\\R\\R-3.1.0\\bin\\Rscript.exe',
    'LogFile' : 'graple.log',
}

RUNCMD = '''C:\Python27\python.exe Graple.py -r\n'''

SUBMIT = '''universe=vanilla
executable=Condor\Run.cmd
output=Scratch\\\\sim$(Process).out
error=Scratch\\\\sim$(Process).err
log=Scratch\\\\sim$(Process).log
requirements=(Memory >= 512) && (TARGET.Arch == "X86_64") && (TARGET.OpSys == "WINDOWS")
transfer_input_files=Scratch\job$(Process).bz2.tar, Graple\Graple.py
transfer_output_files=Results.bz2.tar
transfer_output_remaps="Results.bz2.tar=Results\\\\Results$(Process).bz2.tar"
should_transfer_files=YES
when_to_transfer_output=ON_EXIT
notification=never'''


class Graple:
    def __init__(self,):
        self.SetupLogger()
        self.ParseArgs()
        if 'SimRoot' in CONFIG:
            self.top_dir = CONFIG['SimRoot']
        else:
            #self.top_dir, base_dir = os.path.split(os.getcwd())
            self.top_dir = os.getcwd()
        self.ScriptsDir = 'Scripts'
        self.GlmDir = 'GLM'
        self.SimsDir = 'Sims'
        self.CondorDir = 'Condor'
        self.TempDir = 'Scratch'
        self.ResultsDir = 'Results'

        self.ZipBasename = join(self.top_dir, self.TempDir)
        #if not isdir(self.ZipBasename):
        #    os.mkdir(self.ZipBasename)
        self.ZipBasename = join(self.ZipBasename, 'job')

    def ParseArgs(self,):
        self.parser = argparse.ArgumentParser(prog='Graple', description='Helper program to prep, run & collect sim results')
        self.parser.add_argument('-p', '--prep', dest='prep', action='store_true', help='Creates a series archives each containing a batch of simulations')
        self.parser.add_argument('-r', '--run', dest='run', action='store_true', help='Unpacks archives and executes simulations')
        self.parser.add_argument('-f', '--fixup', dest='fixup', action='store_true', help='Puts the output of each Sim into its orignial source folder')
        self.parser.add_argument('-m', '--mkdirs', dest='mkdirs', action='store_true', help='Creates the working folder structure')
        
    def isCreateWorkingFolders(self):
        if self.parser.parse_args().mkdirs:
            return True

    def isSimPrep(self,):
        arg = self.parser.parse_args()
        if arg.prep or (not arg.prep and not arg.run and not arg.fixup and not arg.mkdirs):
            return True
        else: return False

    def isSimRun(self,):
        if self.parser.parse_args().run:
            return True
        else: return False

    def isSimFixup(self,):
        if self.parser.parse_args().fixup:
            return True
        else: return False

    def SetupLogger(self,):
        self.logger = logging.getLogger('GRAPLE')
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(CONFIG['LogFile'])
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s:%(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        # add the handlers to logger
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def CreateWorkingFolders(self, NumSims=3):
        os.chdir(self.top_dir)
        if not isdir(self.ScriptsDir):
            os.mkdir(self.ScriptsDir)
        
        if not isdir(self.GlmDir):
            os.mkdir(self.GlmDir)
        
        if not isdir(self.TempDir):
            os.mkdir(self.TempDir)

        if not isdir(self.CondorDir):
            os.mkdir(self.CondorDir)

        if not isdir(self.SimsDir):
            os.mkdir(self.SimsDir)

        if not isdir(self.ResultsDir):
            os.mkdir(self.ResultsDir)

        os.chdir(self.SimsDir)
        for i in range(NumSims):
            if not isdir('Sim' + str(i)):
                os.mkdir('Sim' + str(i))

    def ZipDir(self, path, archiver):
        for root, dirs, files in os.walk(path):
            for file in files:
                archiver.write(os.path.join(root, file))

    def CreateJob(self, SimDirList, JobName):
        ## Creates a single job ZIP file
        os.chdir(self.top_dir)
        with tarfile.open(JobName, 'w:bz2', compresslevel=9) as tar:
            tar.add(self.ScriptsDir)
            tar.add(self.GlmDir)
            for adir in SimDirList:
                tar.add(adir)

    def SimPrep(self):
        ## Creates the series of job archives
        SimsForJob = []
        count = 0
        jobSuffix = 0
        os.chdir(self.top_dir)
        #build the list of Simxxx dirs to add to the job archives
        for dir in listdir(self.SimsDir):
            fqdn = join(self.SimsDir, dir)
            if isdir(fqdn):
                SimsForJob.append(fqdn)
                count += 1  #count is used to limit how many sims are packed into a job
            if count % int(CONFIG['SimsPerJob']) == 0:
                jn = self.ZipBasename + str(jobSuffix) + '.bz2.tar'
                jobSuffix += 1
                self.CreateJob(SimsForJob, jn)  
                SimsForJob = []
        if len(SimsForJob) > 0:
            jn = self.ZipBasename + str(jobSuffix) + '.bz2.tar'
            jobSuffix += 1
            self.CreateJob(SimsForJob, jn)
            SimsForJob = []
        queueStr = '\nQueue ' + str(jobSuffix)
        submitFile = open(join(self.CondorDir, 'jobs.submit'), 'w')
        submitFile.write(SUBMIT)
        submitFile.write(queueStr)
        submitFile.close()
        runFile = open(join(self.CondorDir, 'run.cmd'), 'w')
        runFile.write(RUNCMD)
        runFile.close()

        subprocess.call(['condor_submit', join(self.CondorDir, 'jobs.submit')])

        
    def SimRun(self,):
        ## Runs a single job on the Condor execute node and packages the
        ## results that are returned to the client.
        rexe = CONFIG['Rexe']
        topdir = os.getcwd()
        glm = join(join(topdir, 'GLM'), 'glm.exe',)
        rscript = join(join(topdir, 'Scripts'), CONFIG['Rmain'])
              
        for JobName in listdir('.'):
            if isfile(JobName) and JobName.endswith('.bz2.tar'):
                with tarfile.open(JobName, 'r') as tar:
                    tar.extractall()
                break
        for d in listdir(self.SimsDir):
            simdir = join(self.SimsDir, d)
            if isdir(simdir):
                os.chdir(simdir)
                os.mkdir('Results')
                res = subprocess.call([glm])
                if CONFIG[RunR] == 'True':
                    res = subprocess.call([rexe, rscript])
                os.chdir(topdir)
        
        with tarfile.open('Results.bz2.tar', 'w') as tar:
            for d in listdir('Sims'):
                #resultsdir = join(join(join(topdir, 'Sims'), d), 'Results')
                resultsdir = join(join('Sims', d), 'Results')
                if isdir(resultsdir):
                    tar.add(resultsdir)


    def SimFixup(self,):
        ## Unpacks the result archives on the client side and cleans 
        ## up unused directories.
        os.chdir(join(self.top_dir, self.ResultsDir))
        for f in listdir('.'):
            if f.endswith('.bz2.tar'):
                with tarfile.open(f, 'r') as tar:
                    tar.extractall()
                os.remove(f)
        shutil.rmtree(join(self.top_dir, self.TempDir))
        shutil.rmtree(join(self.top_dir, self.CondorDir))

if __name__ == '__main__':
    sm = Graple()
    if sm.isCreateWorkingFolders():
        sm.CreateWorkingFolders()
    if sm.isSimPrep():
        sm.SimPrep()
    if sm.isSimRun():
        sm.SimRun()
    if sm.isSimFixup():
        sm.SimFixup()
