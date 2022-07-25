# Código que calcula la distancia a la costa de los centroides de los países.

#######################################################################
# Importamos todos los paquetes necesarios para model4b
#######################################################################
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Model4b(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterVectorDestination('Distout', 'distout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('Nearout', 'nearout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Country_centroids', 'country_centroids', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Coastout', 'coastout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroidsout', 'centroidsout', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust_dropfields', 'nearest_cat_adjust_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined_dropfields', 'centroids_nearest_coast_joined_dropfields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_lat_lon_drop_fields', 'centroids_lat_lon_drop_fields', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_by_attribute', 'extract_by_attribute', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Extract_vertices', 'extract_vertices', type=QgsProcessing.TypeVectorPoint, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Nearest_cat_adjust', 'nearest_cat_adjust', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lat', 'added_field_cent_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_cent_lon', 'added_field_cent_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lat', 'added_field_coast_lat', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Added_field_coast_lon', 'added_field_coast_lon', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_coast', 'fixgeo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 'fixgeo_countries', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_joined', 'centroids_nearest_coast_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_nearest_coast_distance_joined', 'centroids_nearest_coast_distance_joined', optional=True, type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Centroids_w_coord', 'centroids_w_coord', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Add_geo_coast', 'add_geo_coast', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(21, model_feedback)
        results = {}
        outputs = {}

        #######################################################################
        # Fix geometries - countries
        #######################################################################
        # Importo el shp de los países y arreglo las geometrias para procesar el
        # shapefile
        alg_params = {
            'INPUT': 'C:/Users/felip/Documents/UdeSA/Maestría/Herramientas computacionales/Clase 4/Input/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp',
            'OUTPUT': parameters['Fixgeo_countries']
        }
        outputs['FixGeometriesCountries'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_countries'] = outputs['FixGeometriesCountries']['OUTPUT']

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Fix geometries - coast
        #######################################################################
        # Importo el shp de las costas y arreglo las geometrias para procesar el
        # shapefile
        alg_params = {
            'INPUT': 'C:/Users/felip/Documents/UdeSA/Maestría/Herramientas computacionales/Clase 4/Input/ne_10m_coastline/ne_10m_coastline.shp',
            'OUTPUT': parameters['Fixgeo_coast']
        }
        outputs['FixGeometriesCoast'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Fixgeo_coast'] = outputs['FixGeometriesCoast']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Drop field(s) - fixgeo_coast
        #######################################################################
        # Elimino todas las columnas que no se van a usar de el shp de la costa
        alg_params = {
            'COLUMN': ['scalerank'],
            'INPUT': outputs['FixGeometriesCoast']['OUTPUT'],
            'OUTPUT': parameters['Coastout']
        }
        outputs['DropFieldsFixgeo_coast'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Coastout'] = outputs['DropFieldsFixgeo_coast']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Centroids
        #######################################################################
        # Establezco los centroides para los países
        alg_params = {
            'ALL_PARTS': False,
            'INPUT': outputs['FixGeometriesCountries']['OUTPUT'],
            'OUTPUT': parameters['Country_centroids']
        }
        outputs['Centroids'] = processing.run('native:centroids', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Country_centroids'] = outputs['Centroids']['OUTPUT']

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Add geometry attributes
        #######################################################################
        # Le agrego las coordenadas a los centroides
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': outputs['Centroids']['OUTPUT'],
            'OUTPUT': parameters['Centroids_w_coord']
        }
        outputs['AddGeometryAttributes'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_w_coord'] = outputs['AddGeometryAttributes']['OUTPUT']

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Drop field(s) - centroids_w_coord
        #######################################################################
        # Elimino columnas que no se van a usar de el shp de los centroides con
        # coordenadas
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA'],
            'INPUT': outputs['AddGeometryAttributes']['OUTPUT'],
            'OUTPUT': parameters['Centroidsout']
        }
        outputs['DropFieldsCentroids_w_coord'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroidsout'] = outputs['DropFieldsCentroids_w_coord']['OUTPUT']

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # v.distance
        #######################################################################
        # Busco la distancia mas cercana desde el centroide a la costa
        alg_params = {
            'GRASS_MIN_AREA_PARAMETER': 0.0001,
            'GRASS_OUTPUT_TYPE_PARAMETER': 0,  # auto
            'GRASS_REGION_PARAMETER': None,
            'GRASS_SNAP_TOLERANCE_PARAMETER': -1,
            'GRASS_VECTOR_DSCO': '',
            'GRASS_VECTOR_EXPORT_NOCAT': True,
            'GRASS_VECTOR_LCO': '',
            'column': ['xcoord'],
            'dmax': -1,
            'dmin': -1,
            'from': outputs['DropFieldsCentroids_w_coord']['OUTPUT'],
            'from_type': [0,1,3],  # point,line,area
            'to': outputs['DropFieldsFixgeo_coast']['OUTPUT'],
            'to_column': '',
            'to_type': [0,1,3],  # point,line,area
            'upload': [0],  # cat
            'from_output': parameters['Nearout'],
            'output': parameters['Distout']
        }
        outputs['Vdistance'] = processing.run('grass7:v.distance', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Distout'] = outputs['Vdistance']['output']
        results['Nearout'] = outputs['Vdistance']['from_output']

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Field calculator - cat adjust
        #######################################################################
        # Corregir la variable generada en el paso anterior
        alg_params = {
            'FIELD_LENGTH': 4,
            'FIELD_NAME': 'cat',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 1,  # Integer
            'FORMULA': "attribute($currentfeature,'cat')-1",
            'INPUT': outputs['Vdistance']['from_output'],
            'OUTPUT': parameters['Nearest_cat_adjust']
        }
        outputs['FieldCalculatorCatAdjust'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust'] = outputs['FieldCalculatorCatAdjust']['OUTPUT']

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Drop field(s) - cat_adjust
        #######################################################################
        # Elimino columnas que no voy a usar
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': outputs['FieldCalculatorCatAdjust']['OUTPUT'],
            'OUTPUT': parameters['Nearest_cat_adjust_dropfields']
        }
        outputs['DropFieldsCat_adjust'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nearest_cat_adjust_dropfields'] = outputs['DropFieldsCat_adjust']['OUTPUT']

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Join attributes by field value - centroids y coast
        #######################################################################
        # Merge entre los centroides y la costa usando la columna "ne_10m_adm"
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'ne_10m_adm',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'ne_10m_adm',
            'INPUT': outputs['DropFieldsCentroids_w_coord']['OUTPUT'],
            'INPUT_2': outputs['DropFieldsCat_adjust']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'NON_MATCHING': QgsProcessing.TEMPORARY_OUTPUT,
            'OUTPUT': parameters['Centroids_nearest_coast_joined']
        }
        outputs['JoinAttributesByFieldValueCentroidsYCoast'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined'] = outputs['JoinAttributesByFieldValueCentroidsYCoast']['OUTPUT']

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Drop field(s) - centroids_coast_joined
        #######################################################################
        # Elimino columnas que no se usan de el merge entre centroides y costas
        alg_params = {
            'COLUMN': ['featurecla','scalerank','LABELRANK','SOVEREIGNT','SOV_A3','ADM0_DIF','LEVEL','TYPE','TLC','ADM0_A3','GEOU_DIF','GEOUNIT','GU_A3','SU_DIF','SUBUNIT','SU_A3','BRK_DIFF','NAME','NAME_LONG','BRK_A3','BRK_NAME','BRK_GROUP','ABBREV','POSTAL','FORMAL_EN','FORMAL_FR','NAME_CIAWF','NOTE_ADM0','NOTE_BRK','NAME_SORT','NAME_ALT','MAPCOLOR7','MAPCOLOR8','MAPCOLOR9','MAPCOLOR13','POP_EST','POP_RANK','POP_YEAR','GDP_MD','GDP_YEAR','ECONOMY','INCOME_GRP','FIPS_10','ISO_A2','ISO_A2_EH','ISO_A3_EH','ISO_N3','ISO_N3_EH','UN_A3','WB_A2','WB_A3','WOE_ID','WOE_ID_EH','WOE_NOTE','ADM0_ISO','ADM0_DIFF','ADM0_TLC','ADM0_A3_US','ADM0_A3_FR','ADM0_A3_RU','ADM0_A3_ES','ADM0_A3_CN','ADM0_A3_TW','ADM0_A3_IN','ADM0_A3_NP','ADM0_A3_PK','ADM0_A3_DE','ADM0_A3_GB','ADM0_A3_BR','ADM0_A3_IL','ADM0_A3_PS','ADM0_A3_SA','ADM0_A3_EG','ADM0_A3_MA','ADM0_A3_PT','ADM0_A3_AR','ADM0_A3_JP','ADM0_A3_KO','ADM0_A3_VN','ADM0_A3_TR','ADM0_A3_ID','ADM0_A3_PL','ADM0_A3_GR','ADM0_A3_IT','ADM0_A3_NL','ADM0_A3_SE','ADM0_A3_BD','ADM0_A3_UA','ADM0_A3_UN','ADM0_A3_WB','CONTINENT','REGION_UN','SUBREGION','REGION_WB','NAME_LEN','LONG_LEN','ABBREV_LEN','TINY','HOMEPART','MIN_ZOOM','MIN_LABEL','MAX_LABEL','LABEL_X','LABEL_Y','NE_ID','WIKIDATAID','NAME_AR','NAME_BN','NAME_DE','NAME_EN','NAME_ES','NAME_FA','NAME_FR','NAME_EL','NAME_HE','NAME_HI','NAME_HU','NAME_ID','NAME_IT','NAME_JA','NAME_KO','NAME_NL','NAME_PL','NAME_PT','NAME_RU','NAME_SV','NAME_TR','NAME_UK','NAME_UR','NAME_VI','NAME_ZH','NAME_ZHT','FCLASS_ISO','TLC_DIFF','FCLASS_TLC','FCLASS_US','FCLASS_FR','FCLASS_RU','FCLASS_ES','FCLASS_CN','FCLASS_TW','FCLASS_IN','FCLASS_NP','FCLASS_PK','FCLASS_DE','FCLASS_GB','FCLASS_BR','FCLASS_IL','FCLASS_PS','FCLASS_SA','FCLASS_EG','FCLASS_MA','FCLASS_PT','FCLASS_AR','FCLASS_JP','FCLASS_KO','FCLASS_VN','FCLASS_TR','FCLASS_ID','FCLASS_PL','FCLASS_GR','FCLASS_IT','FCLASS_NL','FCLASS_SE','FCLASS_BD','FCLASS_UA','ADMIN_2','ISO_A3_2'],
            'INPUT': outputs['JoinAttributesByFieldValueCentroidsYCoast']['NON_MATCHING'],
            'OUTPUT': parameters['Centroids_nearest_coast_joined_dropfields']
        }
        outputs['DropFieldsCentroids_coast_joined'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_joined_dropfields'] = outputs['DropFieldsCentroids_coast_joined']['OUTPUT']

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Join attributes by field value - centroids y nearest coast
        #######################################################################
        # Merge entre los centroides y la costa mas cercana usando la columna
        # "cat"
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'cat',
            'FIELDS_TO_COPY': [''],
            'FIELD_2': 'cat',
            'INPUT': outputs['Vdistance']['output'],
            'INPUT_2': outputs['DropFieldsCentroids_coast_joined']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': '',
            'NON_MATCHING': QgsProcessing.TEMPORARY_OUTPUT,
            'OUTPUT': parameters['Centroids_nearest_coast_distance_joined']
        }
        outputs['JoinAttributesByFieldValueCentroidsYNearestCoast'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_nearest_coast_distance_joined'] = outputs['JoinAttributesByFieldValueCentroidsYNearestCoast']['OUTPUT']

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Extract vertices
        #######################################################################
        # Extraigo los vertices de el merge entre centroides y costa más cercana
        alg_params = {
            'INPUT': outputs['JoinAttributesByFieldValueCentroidsYNearestCoast']['NON_MATCHING'],
            'OUTPUT': parameters['Extract_vertices']
        }
        outputs['ExtractVertices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_vertices'] = outputs['ExtractVertices']['OUTPUT']

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Extract by attribute
        #######################################################################
        # Extraer vertices cuando la distancia es > 0 
        alg_params = {
            'FIELD': 'distance',
            'INPUT': outputs['ExtractVertices']['OUTPUT'],
            'OPERATOR': 2,  # >
            'VALUE': '0',
            'FAIL_OUTPUT': QgsProcessing.TEMPORARY_OUTPUT,
            'OUTPUT': parameters['Extract_by_attribute']
        }
        outputs['ExtractByAttribute'] = processing.run('native:extractbyattribute', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Extract_by_attribute'] = outputs['ExtractByAttribute']['OUTPUT']

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Field calculator - cent_lat
        #######################################################################
        # Genero en la shp con la que veniamos trabajando la latitud
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'ycoord')",
            'INPUT': outputs['ExtractByAttribute']['FAIL_OUTPUT'],
            'OUTPUT': parameters['Added_field_cent_lat']
        }
        outputs['FieldCalculatorCent_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lat'] = outputs['FieldCalculatorCent_lat']['OUTPUT']

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Field calculator - cent_lon
        #######################################################################
        # Genero en la shp con la que veniamos trabajando la longitud
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'cent_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'xcoord')",
            'INPUT': outputs['FieldCalculatorCent_lat']['OUTPUT'],
            'OUTPUT': parameters['Added_field_cent_lon']
        }
        outputs['FieldCalculatorCent_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_cent_lon'] = outputs['FieldCalculatorCent_lon']['OUTPUT']

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Drop field(s) - cent_lat_lon
        #######################################################################
        # Elimino las columnas que no se van a usar
        alg_params = {
            'COLUMN': ['fid','cat','xcoord','ycoord','fid_2','cat_2','vertex_index','vertex_part','vertex_part','_index','angle'],
            'INPUT': outputs['FieldCalculatorCent_lon']['OUTPUT'],
            'OUTPUT': parameters['Centroids_lat_lon_drop_fields']
        }
        outputs['DropFieldsCent_lat_lon'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Centroids_lat_lon_drop_fields'] = outputs['DropFieldsCent_lat_lon']['OUTPUT']

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Add geometry attributes - add_geo_coast
        #######################################################################
        # Le agrego los atributos de geometria
        alg_params = {
            'CALC_METHOD': 0,  # Layer CRS
            'INPUT': outputs['DropFieldsCent_lat_lon']['OUTPUT'],
            'OUTPUT': parameters['Add_geo_coast']
        }
        outputs['AddGeometryAttributesAdd_geo_coast'] = processing.run('qgis:exportaddgeometrycolumns', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Add_geo_coast'] = outputs['AddGeometryAttributesAdd_geo_coast']['OUTPUT']

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Field calculator - add_geo_coast_lat
        #######################################################################
        # Genero en la shp con la que veniamos trabajando la latitud
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lat',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'ycoord')",
            'INPUT': outputs['AddGeometryAttributesAdd_geo_coast']['OUTPUT'],
            'OUTPUT': parameters['Added_field_coast_lat']
        }
        outputs['FieldCalculatorAdd_geo_coast_lat'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lat'] = outputs['FieldCalculatorAdd_geo_coast_lat']['OUTPUT']

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Field calculator - add_geo_coast_lon
        #######################################################################
        # Genero en la shp con la que veniamos trabajando la longitud
        alg_params = {
            'FIELD_LENGTH': 10,
            'FIELD_NAME': 'coast_lon',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Float
            'FORMULA': "attribute($currentfeature,'xcoord')",
            'INPUT': outputs['FieldCalculatorAdd_geo_coast_lat']['OUTPUT'],
            'OUTPUT': parameters['Added_field_coast_lon']
        }
        outputs['FieldCalculatorAdd_geo_coast_lon'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Added_field_coast_lon'] = outputs['FieldCalculatorAdd_geo_coast_lon']['OUTPUT']

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        #######################################################################
        # Drop field(s)
        #######################################################################
        # Eliminar las columnas que no se usan
        alg_params = {
            'COLUMN': ['xcoord','ycoord'],
            'INPUT': outputs['FieldCalculatorAdd_geo_coast_lon']['OUTPUT'],
            'OUTPUT': 'C:/Users/felip/Documents/UdeSA/Maestría/Herramientas computacionales/Clase 4/output/csvout.csv',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DropFields'] = processing.run('native:deletecolumn', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'model4b'

    def displayName(self):
        return 'model4b'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4b()
