"""
Model exported as python.
Name : model1
Group : 
With QGIS : 32208
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsCoordinateReferenceSystem
import processing


class Model1(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Agrisuit', 'agrisuit', createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Counties', 'counties', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Zonal', 'Zonal', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Warp (reproject)
        alg_params = {
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': 'G:/Mi unidad/UdeSA Maestria en Economia/Segundo Trimestre/Herramientas/Clase 4/input/suit/suit/hdr.adf',
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,  # Nearest Neighbour
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Agrisuit']
        }
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Agrisuit'] = outputs['WarpReproject']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Drop field(s)
        alg_params = {
            'COLUMN': ['GID_0','NAME_0','GID_1','GID_2','HASC_2','CC_2','TYPE_2','NL_NAME 2','VARNAME_2','NL_NAME_1','NL_NAME_2',' ENGTYPE_2'],
            'INPUT': 'G:/Mi unidad/UdeSA Maestria en Economia/Segundo Trimestre/Herramientas/Clase 4/input/gadm41_USA_shp/gadm41_USA_2.shp',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Add autoincremental field
        alg_params = {
            'FIELD_NAME': 'cid',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['DropFields']['OUTPUT'],
            'MODULUS': None,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 1,
            'OUTPUT': parameters['Counties']
        }
        outputs['AddAutoincrementalField'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Counties'] = outputs['AddAutoincrementalField']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Zonal statistics
        alg_params = {
            'COLUMN_PREFIX': '_',
            'INPUT': outputs['AddAutoincrementalField']['OUTPUT'],
            'INPUT_RASTER': outputs['WarpReproject']['OUTPUT'],
            'RASTER_BAND': 1,
            'STATISTICS': [2],  # Mean
            'OUTPUT': parameters['Zonal']
        }
        outputs['ZonalStatistics'] = processing.run('native:zonalstatisticsfb', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Zonal'] = outputs['ZonalStatistics']['OUTPUT']
        return results

    def name(self):
        return 'model1'

    def displayName(self):
        return 'model1'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model1()
