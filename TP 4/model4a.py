# Generar el número de idiomas en cada país usando el WLMS del model1 y
# intersecarlo con el shp de países.
# Se utiliza el archivo langa.shp descargado de: worldgeodatasets.com/language
# y también se utiliza el shp de: http://www.naturalearthdata.com/downloads/%2010m-cultural-vectors/10m-admin-0-countries/

#Importo los paquetes necesarios
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Model4a(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_wlds', 'fixgeo_wlds', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Intersection', 'intersection', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        #######################################################################
        # Fix geometries - wlds
        #######################################################################
        # Arreglo las geometrías del shapefile que generamos en el model1
        alg_params = {
            'INPUT': 'C:/Users/felip/Documents/UdeSA/Maestría/Herramientas computacionales/Clase 4/output/clean.shp',
            'OUTPUT': parameters['Fixgeo_wlds']
        }
        outputs['FixGeometriesWlds'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_wlds'] = outputs['FixGeometriesWlds']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Fix geometries - countries
        #######################################################################
        # Arreglo las geometrías del shapefile sobre países
        alg_params = {
            'INPUT': 'C:/Users/felip/Documents/UdeSA/Maestría/Herramientas computacionales/Clase 4/Input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_countries']
        }
        outputs['FixGeometriesCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['FixGeometriesCountries']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Intersection
        #######################################################################
        # Intersección entre los dos shps de países y idiomas
        alg_params = {
            'INPUT': outputs['FixGeometriesWlds']['OUTPUT'],
            'INPUT_FIELDS': ['GID'],
            'OVERLAY': outputs['FixGeometriesCountries']['OUTPUT'],
            'OVERLAY_FIELDS': ['ADMIN'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': parameters['Intersection']
        }
        outputs['Intersection'] = processing.run('native:intersection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Intersection'] = outputs['Intersection']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Statistics by categories
        #######################################################################
        # Generar el número de idiomas para cada país y exportarlo como un csv
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['ADMIN'],
            'INPUT': outputs['Intersection']['OUTPUT'],
            'OUTPUT': 'C:/Users/felip/Documents/UdeSA/Maestría/Herramientas computacionales/Clase 4/output/languages_by_country.csv',
            'VALUES_FIELD_NAME': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['StatisticsByCategories'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'model4a'

    def displayName(self):
        return 'model4a'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4a()
