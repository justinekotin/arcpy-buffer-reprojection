
import arcpy

arcpy.env.workspace = r"C:\Users\justi\OneDrive\Desktop\Evaluation1\EVALUATION\EVALUATION_E2\EVALUATION_E2DONNEES"
arcpy.env.overwriteOutput = True

Couche_ProjetPVT = arcpy.GetParameterAsText(0)
Couche_Transformateurs = arcpy.GetParameterAsText(1)

ProjetPVT_avec_criteres_ok = []
ProjetPVT_avec_criteres_projection_ok = []

Distance = [200, 400, 600, 800] ## une modification à été effectuer ici
 
for dist in Distance: ## Ajout de la boucle for
    distance = "{0} Meters".format(dist) ## une modification à été effectuer ici
    Nom_Sortie_Buffer = 'Buffer_{0}m'.format(dist) # une modification à été effectuer ici
    Nom_Sortie_SelectbyLocation = 'ProjetPVT_{0}'.format(Nom_Sortie_Buffer)
    arcpy.analysis.Buffer(Couche_Transformateurs, Nom_Sortie_Buffer, distance)

    select = arcpy.management.SelectLayerByLocation(Couche_ProjetPVT, "INTERSECT", Nom_Sortie_Buffer)

    output = arcpy.management.CopyFeatures(select, Nom_Sortie_SelectbyLocation)

    ProjetPVT_avec_criteres_ok.extend(output)

    Couche_Sortie_SpatialReference = arcpy.Describe(Nom_Sortie_SelectbyLocation).spatialReference.name

    Projection_RGF93 = 'PROJECTION_RGF93.prj'
    Projection_WGS84 = 'PROJECTION_WGS84.prj'

    Nom_Sortie_Reprojection = 'WGS84_{0}'.format(Nom_Sortie_SelectbyLocation)

    if Couche_Sortie_SpatialReference == 'Unknown':
        arcpy.management.DefineProjection(Nom_Sortie_SelectbyLocation, Projection_RGF93)
        arcpy.management.Project(Nom_Sortie_SelectbyLocation, Nom_Sortie_Reprojection, Projection_WGS84)

    elif Couche_Sortie_SpatialReference == 'RGF_1993_Lambert_93':
        arcpy.management.Project(Nom_Sortie_SelectbyLocation, Nom_Sortie_Reprojection, Projection_WGS84)

    print(Nom_Sortie_Reprojection)

ProjetPVT_avec_criteres_projection_ok = arcpy.ListFeatureClasses('WGS84_*')
