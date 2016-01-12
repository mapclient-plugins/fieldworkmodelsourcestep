
'''
MAP Client Plugin Step
'''
import os
import json

from PySide import QtGui

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.fieldworkmodelsourcestep.configuredialog import ConfigureDialog

from fieldwork.field import geometric_field

class FieldworkModelSourceStep(WorkflowStepMountPoint):
    '''
    Step for loading a fieldwork model from disk.
    '''

    def __init__(self, location):
        super(FieldworkModelSourceStep, self).__init__('Fieldwork Model Source', location)
        self._configured = False # A step cannot be executed until it has been configured.
        self._category = 'Source'
        # Add any other initialisation code here:
        self._icon = QtGui.QImage(':/fieldworkmodelsourcestep/images/fieldworkmodelsourceicon.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'python#string'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'python#string'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'python#string'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'python#string'))
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
        print('GF name:', self._GF.name)

        self._doneExecution()

    def setPortData(self, index, dataIn):
        '''
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.
        '''

        if index == 0:
            self._GFFilename = dataIn # String
        elif index == 1:
            self._ensFilename = dataIn # String
        elif index == 2:
            self._meshFilename = dataIn # String
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

    def serialize(self):
        '''
        Add code to serialize this step to disk. Returns a json string for
        mapclient to serialise.
        '''
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        '''
        Add code to deserialize this step from disk. Parses a json string
        given by mapclient
        '''
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()


