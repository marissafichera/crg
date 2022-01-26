import pandas as pd
import numpy as np
import os
import sys
import arcpy
from arcpy import env
from arcpy.sa import *

import pyproj


arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True


def check_for_constituents(df, constituents):
    new_con = []
    columns_in_df = df.columns
    for constituent in constituents:
        for col in columns_in_df:
            if constituent == col:
                print('constituent {} found in spreadsheet'.format(constituent))
                new_con.append(constituent)
                break
        else:
            print('constituent {} NOT found in spreadsheet'.format(constituent))

    print(new_con)

    return new_con


def create_feature_class_GIS(folder, file, region, element, date):
    env.workspace = r'E:\__phd\water_quality_portal.gdb'
    env.outputCoordinateSystem = arcpy.SpatialReference("NAD 1983 UTM Zone 13N")
    # table = pd.read_csv(os.path.join(folder, data_csv))


    ##make XYevent layer
    in_Table = "{}\{}".format(folder, file)
    x_coords = 'Easting'
    y_coords = 'Northing'
    # z_coords = ''
    out_Layer = 'wqp_{}{}{}_event'.format(region, element, date)
    saved_Layer = 'wqp_{}{}{}_lyr.lyr'.format(region, element, date)

    # Make the XY event layer...
    arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, env.outputCoordinateSystem)


    # Save to a layer file
    arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)


    ##featureclass to feature class
    inputfc = out_Layer
    outfc = 'wqp_{}_{}_{}'.format(region, element, date)
    arcpy.FeatureClassToFeatureClass_conversion(inputfc, env.workspace, outfc)


def get_isotopes(df, region, date):
    df_rename = df.rename(columns={'Carbon-14': 'Carbon14', 'Deuterium/Hydrogen ratio': 'Deuterium_Hydrogen_ratio',
                                   'Helium-3/helium-4 error': 'Helium3_helium4error', 'Helium-3/helium-4 ratio': 'Helium3_helium4ratio',
                                   'Helium-4': 'Helium4', 'Oxygen-18/Oxygen-16 ratio': 'Oxygen18_Oxygen16ratio',
                                   'Strontium-87/Strontium-86, ratio': 'Strontium87_Strontium86_ratio'})

    constituents = ['ActivityIdentifier', 'LatitudeMeasure', 'LongitudeMeasure', 'Easting', 'Northing', 'ActivityMediaSubdivisionName',
                      'ActivityStartDate', 'Carbon14', 'Deuterium_Hydrogen_ratio', 'Helium3_helium4error',
                      'Helium3_helium4ratio', 'Helium4', 'Oxygen18_Oxygen16ratio', 'Strontium87_Strontium86_ratio', 'Tritium']
    columns = check_for_constituents(df_rename, constituents)

    df_isotopes = df_rename[columns]

    out_element_name = 'isotopes'
    out_folder = r'\\agustin\homes\mfichera\My Documents\_phd\data\water\WQP_01142022\03_specificdatapulls'
    out_elements_file = 'WQP03_{}_{}_{}.csv'.format(region, out_element_name, date)
    df_isotopes.to_csv(os.path.join(out_folder, out_elements_file))
    return df_isotopes, out_folder, out_elements_file, out_element_name


def get_BFClTDS(df, region, date):
    constituents = ['ActivityIdentifier', 'LatitudeMeasure', 'LongitudeMeasure', 'Easting', 'Northing', 'ActivityMediaSubdivisionName',
                   'pH', 'Temperature, water', 'Boron', 'Fluoride', 'Chloride', 'Total dissolved solids']
    columns = check_for_constituents(df, constituents)
    df_other = df[columns]

    out_element_name = 'B_F_Cl_TDS'
    out_folder = r'\\agustin\homes\mfichera\My Documents\_phd\data\water\WQP_01142022\03_specificdatapulls'
    out_elements_file = 'WQP03_{}_{}_{}.csv'.format(region, out_element_name, date)
    df_other.to_csv(os.path.join(out_folder, out_elements_file))
    return df_other, out_folder, out_elements_file, out_element_name


def get_ClBr(df, region, date):
    constituents = ['ActivityIdentifier', 'LatitudeMeasure', 'LongitudeMeasure', 'Easting', 'Northing', 'ActivityMediaSubdivisionName',
                   'pH', 'Temperature, water', 'Bromide', 'Chloride', 'Total dissolved solids']
    columns = check_for_constituents(df, constituents)
    df_other = df[columns]

    out_element_name = 'ClBr'
    out_folder = r'\\agustin\homes\mfichera\My Documents\_phd\data\water\WQP_01142022\03_specificdatapulls'
    out_elements_file = 'WQP03_{}_{}_{}.csv'.format(region, out_element_name, date)
    df_other.to_csv(os.path.join(out_folder, out_elements_file))
    return df_other, out_folder, out_elements_file, out_element_name


def get_piper_elements(df, region, date):
    # piper column names for WQP data = 'Calcium', 'Magnesium', 'Sodium', 'Potassium', 'Sodium plus potassium'
        # 'Bicarbonate', 'Carbonate', 'Alkalinity', 'Sulfate', 'Chloride', 'Total dissolved solids'

    constituents = ['ActivityIdentifier', 'LatitudeMeasure', 'LongitudeMeasure', 'Easting', 'Northing', 'ActivityMediaSubdivisionName',
                   'pH', 'Temperature, water', 'Calcium', 'Magnesium', 'Sodium', 'Potassium', 'Sodium plus potassium',
                    'Bicarbonate', 'Carbonate', 'Alkalinity', 'Sulfate', 'Chloride', 'Total dissolved solids']
    columns = check_for_constituents(df, constituents)
    df_piper = df[columns]

    # df_piper = df[['ActivityIdentifier', 'LatitudeMeasure', 'LongitudeMeasure', 'Easting', 'Northing', 'ActivityMediaSubdivisionName',
    #                'pH', 'Temperature, water', 'Calcium', 'Magnesium', 'Sodium', 'Potassium', 'Sodium plus potassium',
    #                 'Bicarbonate', 'Carbonate', 'Alkalinity', 'Sulfate', 'Chloride', 'Total dissolved solids']]
    out_element_name = 'piper'
    out_folder = r'\\agustin\homes\mfichera\My Documents\_phd\data\water\WQP_01142022\03_specificdatapulls'
    out_elements_file = 'WQP03_{}_{}_{}.csv'.format(region, out_element_name, date)
    df_piper.to_csv(os.path.join(out_folder, out_elements_file))
    return df_piper, out_folder, out_elements_file, out_element_name


def get_all(df, region, date):
    # piper column names for WQP data = 'Calcium', 'Magnesium', 'Sodium', 'Potassium', 'Sodium plus potassium'
        # 'Bicarbonate', 'Carbonate', 'Alkalinity', 'Sulfate', 'Chloride', 'Total dissolved solids'

    # df_piper = df[['ActivityIdentifier', 'LatitudeMeasure', 'LongitudeMeasure', 'Easting', 'Northing', 'ActivityMediaSubdivisionName',
    #                'pH', 'Temperature, water', 'Calcium', 'Magnesium', 'Sodium', 'Potassium', 'Sodium plus potassium',
    #                 'Bicarbonate', 'Carbonate', 'Alkalinity', 'Sulfate', 'Chloride', 'Total dissolved solids']]
    out_element_name = 'all'
    out_folder = r'\\agustin\homes\mfichera\My Documents\_phd\data\water\WQP_01142022\03b_pullalldatafrompivot'
    out_elements_file = 'WQP03b_{}_{}_{}.csv'.format(region, out_element_name, date)
    df.to_csv(os.path.join(out_folder, out_elements_file))
    return df, out_folder, out_elements_file, out_element_name


def run_pivot(df, region, elements, date):

    df_p = df.pivot_table(index=['ActivityIdentifier', 'LatitudeMeasure', 'LongitudeMeasure', 'Easting', 'Northing',
                                 'ActivityMediaSubdivisionName', 'ActivityStartDate'],
                         columns=['Characteristic'], values='Result').reset_index()

    # print(df_p)
    out_folder = r'\\agustin\homes\mfichera\My Documents\_phd\data\water\WQP_01142022\02_pivotdatacopies'
    out_filename = 'WQP02_{}_{}_pivoted_{}.csv'.format(region, elements, date)
    df_p.to_csv(os.path.join(out_folder, out_filename))
    return df_p


def copy_original_data(og_data, region, elements):
    root_out = r'\\agustin\homes\mfichera\My Documents\_phd\data\water\WQP_01142022\01_originaldatacopies'
    working_data = 'WQP01_{}_{}_working.csv'.format(region, elements)
    og_data.to_csv(os.path.join(root_out, working_data))
    return og_data


def aggregate_data_by_element(datalist, element):
    df_agg = pd.concat[datalist[1, :]]
    df_agg.to_csv('if you make it this far omg')


def aggregate_data_all(datalist):
    print(datalist)
    df_agg = pd.concat([datalist])
    df_agg.to_csv('once again if you made it this far congrats, now fix this')


def main():
    root = r'\\agustin\homes\mfichera\My Documents\_phd\data\water\WQP_01142022\00_originaldatadownloads'

    prefix = '00_wqp_'

    ## Some of these run through twice to pull different specific data from the same file
    ps = ['ALL_SWcorner_01242022', 'Cl_Br_sococo_01202022', 'isotopes_01202022', 'piper_eastRG_01142022',
          'piper_lajencia_01142022', 'piper_lomasdelascanas_01142022', 'piper_westRG_01142022', 'ALL_SEcorner_01262022',
          'piper_eastRG_01142022', 'piper_lajencia_01142022', 'piper_lomasdelascanas_01142022', 'piper_westRG_01142022']

    elements = ['ALL', 'Cl_Br', 'isotopes', 'piper', 'piper', 'piper', 'piper', 'ALL', 'ALL', 'ALL', 'ALL', 'ALL']

    regions = ['SWcorner', 'SocoCo', 'SocoCo', 'eastRG', 'LJB', 'LDLC', 'westRG', 'SEcorner', 'eastRG', 'LJB', 'LDLC',
               'westRG']

    date = '01262022'

    # hold the data files to be aggregated based on element
    all_aggregate = []
    piper_aggregate = []
    BFClTDS_aggregate = []
    ClBr_aggregate = []
    isotopes_aggregate = []

    for p, region, element in zip(ps, regions, elements):
        print(p, region, element)
        p = '{}{}.csv'.format(prefix, p)
        data = pd.read_csv(os.path.join(root, p))
        og_data = pd.DataFrame(data)
        df = copy_original_data(og_data, region, element)
        print('file = ', p)
        # print(df)

        #change coords to UTM
        print('translating coordinates from lat/long to UTM of {}'.format(p))
        lon = df['LongitudeMeasure']
        lat = df['LatitudeMeasure']
        projection = pyproj.Proj(proj='utm', zone=13, ellps='WGS84')
        e, n = projection(lon, lat)

        df['Easting'] = e
        df['Northing'] = n
        print('done translating coordinates into UTM of {}'.format(p))

        # print(df.columns)
        print('FILE = {} --------- PROCESS = PIVOT'.format(p))
        df_p = run_pivot(df, region, element, date)

        # run all the sheets through the aggregate everything function:
        print('FILE = {} --------- PROCESS = STORE ALL DATA FROM CURRENT FILE (all_aggregate())'.format(p))
        df_data, out_folder, out_elements_file, out_element_name = get_all(df_p, region, date)
        all_aggregate.append(df_data)

        print('FILE = {} -------- PROCESS = EXTRACT SPECIFIC ELEMENTS ---- ELEMENTS = {}'.format(p, element))

        # get specific chemical data for use in piper diagrams and/or plotting in GIS, create GIS feature class
        if element == 'piper' or element == 'ALL':
            print('elements = {} ===== either PIPER or ALL, getting piper data'.format(element))
            df_data, out_folder, out_elements_file, out_element_name = get_piper_elements(df_p, region, date)
            create_feature_class_GIS(out_folder, out_elements_file, region, out_element_name, date)
            piper_aggregate.append(df_data)
        if element == 'B_F_Cl_TDS' or element == 'ALL':
            print('elements = {} ===== either B_F_Cl_TDS or ALL, getting B_F_Cl_TDS data'.format(element))
            df_data, out_folder, out_elements_file, out_element_name = get_BFClTDS(df_p, region, date)
            create_feature_class_GIS(out_folder, out_elements_file, region, out_element_name, date)
            BFClTDS_aggregate.append(df_data)
        if element == 'Cl_Br' or element == 'ALL':
            print('elements = {} ===== either ClBr or ALL, getting ClBr data'.format(element))
            df_data, out_folder, out_elements_file, out_element_name = get_ClBr(df_p, region, date)
            create_feature_class_GIS(out_folder, out_elements_file, region, out_element_name, date)
            ClBr_aggregate.append(df_data)
        if element == 'isotopes' or element == 'ALL':
            print('elements = {} ===== either isotopes or ALL, getting isotopes data'.format(element))
            df_data, out_folder, out_elements_file, out_element_name = get_isotopes(df_p, region, date)
            create_feature_class_GIS(out_folder, out_elements_file, region, out_element_name, date)
            isotopes_aggregate.append(df_data)
            break
    else:
        print('FILE NOT READ OR DOES NOT HAVE ELEMENTS')

    dl = [piper_aggregate, BFClTDS_aggregate, ClBr_aggregate, isotopes_aggregate]
    els = ['piper', 'bfcltds', 'clbr', 'isotopes']
    aggregate_data_all(all_aggregate)
    for item, el in zip(dl, els):
        aggregate_data_by_element(item, el)



if __name__ == '__main__':
    main()