#!/usr/bin/env python

from distutils.core import setup

setup(name='documentStyle',
      version='0.1.1',
      description='Document Styling Classes',
      author='Lloyd Konneker',
      author_email='bootch@nc.rr.com',
      url='https://github.com/bootchk/documentStyle',
      packages=['documentStyle', 
                'documentStyle.formation',
                'documentStyle.formation.instrumentFormation',
                'documentStyle.formation.instrumentFormation.textFormation', 
                'documentStyle.instrument',
                'documentStyle.model',
                'documentStyle.styler',
                'documentStyle.styleSheet',
                'documentStyle.styleWrapper',
                'documentStyle.styling',
                'documentStyle.userInterface',
                'documentStyle.userInterface.layout',
                'documentStyle.userInterface.listview',
                'documentStyle.userInterface.styleDialog',
                'documentStyle.userInterface.resettableControls',
                'documentStyle.userInterface.resettableControls.stylePickerWidget',
                ],
     )