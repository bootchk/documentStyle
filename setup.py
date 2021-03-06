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
                'documentStyle.styleProperty',
                'documentStyle.styler',
                'documentStyle.styleSheet',
                'documentStyle.styling',
                'documentStyle.ui',
                'documentStyle.ui.qmlUI',
                'documentStyle.ui.widgetUI',
                'documentStyle.ui.widgetUI.form',
                'documentStyle.ui.layout',
                'documentStyle.ui.resettableControls',
                'documentStyle.ui.resettableControls.stylePickerWidget',
                ],
     )