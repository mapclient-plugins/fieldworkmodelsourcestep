
'''
MAP Client Plugin Step
'''
import os

from PySide import QtGui
from PySide import QtCore

from mountpoints.workflowstep import WorkflowStepMountPoint
from fieldworkmodelsourcestep.configuredialog import ConfigureDialog

from fieldwork.field import geometric_field

class fieldworkmodelsourceStep(WorkflowStepMountPoint):
    '''
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    '''

    def __init__(self, location):
        super(fieldworkmodelsourceStep, self).__init__('Fieldwork Model Source', location)
        self._configured = False # A step cannot be executed until it has been configured.
        self._category = 'Input'
        # Add any other initialisation code here:
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'String'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'String'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'String'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'String'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'ju#fieldworkmodel'))
        self._config = {}
        self._config['identifier'] = ''
        self._config['GF Filename'] = ''
        self._config['ensemble filename'] = ''
        self._config['mesh filename'] = ''
        self._config['path'] = ''
        
        self._GF = None
        self._GFFilename = None
        self._ensFilename = None
        self._meshFilename = None
        self._path = None

    def execute(self):
        '''
        Add your code here that will kick off the execution of the step.
        Make sure you call the _doneExecution() method when finished.  This method
        may be connected up to a button in a widget for example.
        '''
        # Put your execute step code here before calling the '_doneExecution' method.
        if self._GFFilename!=None:
            gfFilename = self._GFFilename
        else:
            gfFilename = self._config['GF Filename']

        if self._ensFilename!=None:
            ensFilename = self._ensFilename
        elif self._config['ensemble filename']==None:
            ensFilename = None
        else:
            ensFilename = self._config['ensemble filename']

        if self._meshFilename!=None:
            meshFilename = self._meshFilename
        elif self._config['mesh filename']==None:
            meshFilename = None
        else:
            meshFilename = self._config['mesh filename']

        if self._path!=None:
            path = self._path
        elif self._config['path']==None:
            path = ''
        else:
            path = self._config['path']

        self._GF = geometric_field.load_geometric_field(gfFilename, ensFilename, meshFilename, path=path)
        self._doneExecution()

    def setPortData(self, index, dataIn):
        '''
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        '''

        if index == 0:
            self._GFFilenames = dataIn # String
        elif index == 1:
            self._ensFilenames = dataIn # String
        elif index == 2:
            self._meshFilenames = dataIn # String
        else:
            self._path = dataIn

    def getPortData(self, index):
        '''
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.
        '''
        return self._GF # ju#fieldworkmodel

    def configure(self):
        '''
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        '''
        dlg = ConfigureDialog()
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)
        
        if dlg.exec_():
            self._config = dlg.getConfig()
        
        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        '''
        The identifier is a string that must be unique within a workflow.
        '''
        return self._config['identifier']

    def setIdentifier(self, identifier):
        '''
        The framework will set the identifier for this step when it is loaded.
        '''
        self._config['identifier'] = identifier

    def serialize(self, location):
        '''
        Add code to serialize this step to disk.  The filename should
        use the step identifier (received from getIdentifier()) to keep it
        unique within the workflow.  The suggested name for the file on
        disk is:
            filename = getIdentifier() + '.conf'
        '''
        configuration_file = os.path.join(location, self.getIdentifier() + '.conf')
        conf = QtCore.QSettings(configuration_file, QtCore.QSettings.IniFormat)
        conf.beginGroup('config')
        conf.setValue('identifier', self._config['identifier'])
        conf.setValue('GF Filename', self._config['GF Filename'])
        conf.setValue('ensemble filename', self._config['ensemble filename'])
        conf.setValue('mesh filename', self._config['mesh filename'])
        conf.setValue('path', self._config['path'])
        conf.endGroup()


    def deserialize(self, location):
        '''
        Add code to deserialize this step from disk.  As with the serialize 
        method the filename should use the step identifier.  Obviously the 
        filename used here should be the same as the one used by the
        serialize method.
        '''
        configuration_file = os.path.join(location, self.getIdentifier() + '.conf')
        conf = QtCore.QSettings(configuration_file, QtCore.QSettings.IniFormat)
        conf.beginGroup('config')
        self._config['identifier'] = conf.value('identifier', '')
        self._config['GF Filename'] = conf.value('GF Filename', '')
        self._config['ensemble filename'] = conf.value('ensemble filename', '')
        self._config['mesh filename'] = conf.value('mesh filename', '')
        self._config['path'] = conf.value('path', '')
        conf.endGroup()

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()


