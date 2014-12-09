
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush

import documentStyle.config as config



class AdaptedBrushModel(object):
  '''
  Mimics a PyQt5 enum: has "values" attribute that is a dictionary
  '''
  def __init__(self):
    qtEnum = Qt # PySide qtEnum = Qt.BrushStyle
    """
    PySide
    self.values = {"None": BrushStyleWrapper(qtEnum.NoBrush),
                   "Solid": BrushStyleWrapper(qtEnum.SolidPattern),
                   "Half dense": BrushStyleWrapper(qtEnum.Dense4Pattern),
                   "Quadrule": BrushStyleWrapper(qtEnum.CrossPattern),
                   "Crosshatch": BrushStyleWrapper(qtEnum.DiagCrossPattern),}
    """# BrushModel = AdaptedBrushModel()
    self.values = {config.i18ns.NoneName : qtEnum.NoBrush,
                   config.i18ns.Solid : qtEnum.SolidPattern,
                   config.i18ns.HalfDense : qtEnum.Dense4Pattern,
                   config.i18ns.Quadrule : qtEnum.CrossPattern,
                   config.i18ns.Crosshatch : qtEnum.DiagCrossPattern,}
    # TODO more values
    """
    Qt.Dense1Pattern   2   Extremely dense brush pattern.
Qt.Dense2Pattern   3   Very dense brush pattern.
Qt.Dense3Pattern   4   Somewhat dense brush pattern.
Qt.Dense4Pattern   5   Half dense brush pattern.
Qt.Dense5Pattern   6   Somewhat sparse brush pattern.
Qt.Dense6Pattern   7   Very sparse brush pattern.
Qt.Dense7Pattern   8   Extremely sparse brush pattern.
Qt.HorPattern   9   Horizontal lines.
Qt.VerPattern   10   Vertical lines.
Qt.CrossPattern   11   Crossing horizontal and vertical lines.
Qt.BDiagPattern   12   Backward diagonal lines.
Qt.FDiagPattern   13   Forward diagonal lines.
Qt.DiagCrossPattern   14   Crossing diagonal lines.
Qt.LinearGradientPattern   15   Linear gradient (set using a dedicated QBrush constructor).
Qt.ConicalGradientPattern   17   Conical gradient (set using a dedicated QBrush constructor).
Qt.RadialGradientPattern   16   Radial gradient (set using a dedicated QBrush constructor).
Qt.TexturePattern
    """
  
  
  def default(self):
    '''
    A new brush has default style.
    '''
    # PySide return BrushStyleWrapper(QBrush().style())
    return QBrush().style()
