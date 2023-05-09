# ///
# The OxiAge web application is licensed under the CC BY 4.0 license: https://creativecommons.org/licenses/by/4.0/
# author: Katarzyna Jonak <k.jonak@ibb.waw.pl>
# web application: oxiage.ibb.waw.pl
# ///

import mysql.connector

def DBgetOrganismNames(mydb: mysql.connector):
    dbAccess = mydb.cursor()
    sql = 'SELECT Name, Short from organism'
    dbAccess.execute(sql)
    return dbAccess.fetchall()

def DBgetGeneAndProteinNames(mydb: mysql.connector, ID_organism: int, geneOrProteinName: str):
    dbAccess = mydb.cursor()
    sql = f'SELECT p.Gene FROM protein p WHERE p.ID_Organism=%(ID_organism)s and p.Gene like %(geneOrProteinName)s ' \
          f'UNION SELECT p.UniProt FROM protein p WHERE p.ID_Organism=%(ID_organism)s and p.UniProt ' \
          f'like %(geneOrProteinName)s'
    dbAccess.execute(sql, {'ID_organism': int(ID_organism), 'geneOrProteinName': '%' + geneOrProteinName + '%'})
    return dbAccess.fetchall()

def DBgetProteinsGenesNames(mydb: mysql.connector):
    dbAccess = mydb.cursor()
    sql = 'SELECT Gene, UniProt from protein'
    dbAccess.execute(sql)
    return dbAccess.fetchall()

def DBgetGeneAndProteinNamesAll(mydb: mysql.connector, ID_organism: int, geneOrProteinName: str):
    dbAccess = mydb.cursor()
    sql = f'SELECT p.UniProt, p.ID FROM protein p WHERE p.ID_Organism=%(ID_organism)s and p.Gene ' \
          f'like %(geneOrProteinName)s UNION ALL SELECT p.UniProt, p.ID FROM protein p WHERE ' \
          f'p.ID_Organism=%(ID_organism)s and p.UniProt like %(geneOrProteinName)s'
    dbAccess.execute(sql, {'ID_organism': int(ID_organism), 'geneOrProteinName': geneOrProteinName})
    return dbAccess.fetchall()

def DBgetGeneAndProteinNamesFinal(mydb: mysql.connector, geneOrProteinName: str):
    dbAccess = mydb.cursor()
    sql = f'SELECT p.UniProt, p.ID FROM protein p WHERE p.Gene like %(geneOrProteinName)s UNION ALL SELECT ' \
          f'p.UniProt, p.ID FROM protein p WHERE p.UniProt like %(geneOrProteinName)s'
    dbAccess.execute(sql, {'geneOrProteinName': geneOrProteinName})
    return dbAccess.fetchall()

def DBgetCommonNamesAllOrto(mydb: mysql.connector, commonNames: str):
    dbAccess = mydb.cursor()
    sql = f'SELECT p.UniProt, p.Gene, o.Name, o.Short FROM protein p JOIN organism o ON p.ID_Organism=o.ID WHERE ' \
          f'p.UniProt like %(commonNames)s'
    dbAccess.execute(sql, {'commonNames': commonNames})
    return dbAccess.fetchall()

def DBgetCellularCompartment(mydb: mysql.connector, ID_organism: int, cellComponent: str):
    dbAccess = mydb.cursor()
    sql = f'SELECT cn.ComponentName FROM protein p JOIN componentname cn JOIN component_protein cp JOIN organism o ' \
          f'ON cp.ID_ComponentName=cn.ID AND cp.ID_Protein=p.ID AND p.ID_Organism=o.ID WHERE ' \
          f'p.ID_Organism=%(ID_organism)s AND cn.ComponentName like %(cellComponent)s'
    dbAccess.execute(sql, {'ID_organism': int(ID_organism), 'cellComponent': '%' + cellComponent + '%'})
    return dbAccess.fetchall()

def DBgetCellularComponentNamesAll(mydb: mysql.connector, ID_organism: int, cellComponent: str):
    dbAccess = mydb.cursor()
    sql = f'SELECT p.UniProt, p.Gene, cn.ComponentName, cn.ComponentGONumber,p.Protein, p.Length, p.CysNo, p.CysPos, ' \
          f'p.CysMotifs, p.RefPdb, p.RefString, p.OrgDatabase, o.Name, o.Short FROM protein p JOIN componentname cn ' \
          f'JOIN component_protein cp JOIN organism o ON cp.ID_ComponentName=cn.ID AND cp.ID_Protein=p.ID AND ' \
          f'p.ID_Organism=o.ID WHERE p.ID_Organism=%(ID_organism)s AND cn.ComponentName like %(cellComponent)s'
    dbAccess.execute(sql, {'ID_organism': int(ID_organism), 'cellComponent': cellComponent})
    return dbAccess.fetchall()

def DBgetBiologicalProcess(mydb: mysql.connector, ID_organism: int, biolProcess: str):
    dbAccess = mydb.cursor()
    sql = f'SELECT pn.ProcessName FROM protein p JOIN processname pn JOIN process_protein pp JOIN organism o ON ' \
          f'pp.ID_ProcessName=pn.ID AND pp.ID_Protein=p.ID AND p.ID_Organism=o.ID WHERE ' \
          f'p.ID_Organism=%(ID_organism)s AND pn.ProcessName like %(biolProcess)s'
    dbAccess.execute(sql, {'ID_organism': int(ID_organism), 'biolProcess': '%' + biolProcess + '%'})
    return dbAccess.fetchall()

def DBgetBiologicalProcessNamesAll(mydb: mysql.connector, ID_organism: int, biolProcess: str):
    dbAccess = mydb.cursor()
    sql = f'SELECT p.UniProt, p.Gene, pn.ProcessName, pn.ProcessGONumber,p.Protein, p.Length, p.CysNo, p.CysPos, ' \
          f'p.CysMotifs, p.RefPdb, p.RefString, p.OrgDatabase, o.Name, o.Short FROM protein p JOIN processname pn ' \
          f'JOIN process_protein pp JOIN organism o ON pp.ID_ProcessName=pn.ID AND pp.ID_Protein=p.ID AND ' \
          f'p.ID_Organism=o.ID WHERE p.ID_Organism=%(ID_organism)s AND pn.ProcessName like %(biolProcess)s'
    dbAccess.execute(sql, {'ID_organism': int(ID_organism), 'biolProcess': biolProcess})
    return dbAccess.fetchall()

def DBgetMolecularFunction(mydb: mysql.connector, ID_organism: int, molFunction: str):
    dbAccess = mydb.cursor()
    sql = f'SELECT fn.FunctionName FROM protein p JOIN functionname fn JOIN function_protein fp JOIN organism o ' \
          f'ON fp.ID_FunctionName=fn.ID AND fp.ID_Protein=p.ID AND p.ID_Organism=o.ID WHERE ' \
          f'p.ID_Organism=%(ID_organism)s AND fn.FunctionName like %(molFunction)s'
    dbAccess.execute(sql, {'ID_organism': int(ID_organism), 'molFunction': '%' + molFunction + '%'})
    return dbAccess.fetchall()

def DBgetMolecularFunctionNamesAll(mydb: mysql.connector, ID_organism: int, molFunction: str):
    dbAccess = mydb.cursor()
    sql = f'SELECT p.UniProt, p.Gene, fn.FunctionName, fn.FunctionGONumber,p.Protein, p.Length, p.CysNo, p.CysPos, ' \
          f'p.CysMotifs, p.RefPdb, p.RefString, p.OrgDatabase, o.Name, o.Short FROM protein p JOIN functionname fn ' \
          f'JOIN function_protein fp JOIN organism o ON fp.ID_FunctionName=fn.ID AND fp.ID_Protein=p.ID AND ' \
          f'p.ID_Organism=o.ID WHERE p.ID_Organism=%(ID_organism)s AND fn.FunctionName like %(molFunction)s'
    dbAccess.execute(sql, {'ID_organism': int(ID_organism), 'molFunction': molFunction})
    return dbAccess.fetchall()

def DBgetUNIProtNames(mydb: mysql.connector, UniGeneIDList):
    dbAccess = mydb.cursor()
    sql = 'SELECT o.UniProt_OrgA FROM ortology o WHERE o.UniProt_OrgB IN ('
    vals = {}
    readyToRemove = False
    counter = 1
    for uni in UniGeneIDList:
        sql += '%(UniGeneIDName' + str(counter) + ')s,'
        readyToRemove = True
        vals['UniGeneIDName' + str(counter)] = uni
        counter = counter + 1
    if readyToRemove:
        sql = sql[:len(sql) - 1]
        sql += ')'
    dbAccess.execute(sql, vals)
    return dbAccess.fetchall()

def DBgetOrtologyProteinNames(mydb: mysql.connector, UniProtIDS):
    dbAccess = mydb.cursor()
    sql = f'SELECT o.Name, o.Short, o.Latin, p.Gene, p.UniProt, p.Protein, p.Length, p.CysNo, p.CysPos, p.CysMotifs, ' \
          f'p.RefPdb, p.RefString, p.OrgDatabase FROM protein p JOIN organism o ON p.ID_Organism=o.ID WHERE ' \
          f'p.UniProt IN ('
    vals = {}
    readyToRemove = False
    counter = 1
    for uni in UniProtIDS:
        sql += '%(UniProtName' + str(counter) + ')s,'
        readyToRemove = True
        vals['UniProtName' + str(counter)] = uni
        counter = counter + 1
    if readyToRemove:
        sql = sql[:len(sql) - 1]
        sql += ')'
    dbAccess.execute(sql, vals)
    return dbAccess.fetchall()

def DBgetAlignmentForUniProt(mydb: mysql.connector, UniProtIDS):
    dbAccess = mydb.cursor()
    sql = f'SELECT o.Short, p.Gene, p.Alignment, p.ID, c.CysID, c.Positions, c.Order, p.Sequence, p.UniProt FROM ' \
          f'protein p LEFT JOIN cysteine c ON c.ID_Protein=p.ID JOIN organism o ON p.ID_Organism=o.ID WHERE ' \
          f'p.UniProt IN ('
    vals = {}
    readyToRemove = False
    counter = 1
    for uni in UniProtIDS:
        sql += '%(UniProtName' + str(counter) + ')s,'
        readyToRemove = True
        vals['UniProtName' + str(counter)] = uni
        counter = counter + 1
    if readyToRemove:
        sql = sql[:len(sql) - 1]
        sql += ')'
    dbAccess.execute(sql, vals)
    return dbAccess.fetchall()

def DBgetProteinInfo(mydb: mysql.connector, UniProtIDS):
    dbAccess = mydb.cursor()
    sql = f'SELECT p.ID, p.UniProt, p.Gene, p.Protein, p.Information, p.RefPdb, p.RefString, p.OrgDatabase, ' \
          f'o.Name, o.Latin, o.Short, p.Length, p.CysNo, p.CysPos, p.CysMotifs FROM protein p JOIN organism o ' \
          f'ON p.ID_Organism=o.ID WHERE p.UniProt IN ('
    vals = {}
    readyToRemove = False
    counter = 1
    for uni in UniProtIDS:
        sql += '%(UniProtName' + str(counter) + ')s,'
        readyToRemove = True
        vals['UniProtName' + str(counter)] = uni
        counter = counter + 1
    if readyToRemove:
        sql = sql[:len(sql) - 1]
        sql += ')'
    dbAccess.execute(sql, vals)
    return dbAccess.fetchall()

def DBgetGOComponentNames(mydb: mysql.connector, IDProteins):
    dbAccess = mydb.cursor()
    sql = f'SELECT p.UniProt, cn.ComponentName, cn.ComponentGONumber FROM component_protein cp JOIN ' \
          f'componentname cn ON cp.ID_ComponentName=cn.ID JOIN protein p ON p.ID=cp.ID_Protein WHERE cp.ID_Protein IN ('
    vals = {}
    readyToRemove = False
    counter = 1
    for uni in IDProteins:
        sql += '%(IDProteinName' + str(counter) + ')s,'
        readyToRemove = True
        vals['IDProteinName' + str(counter)] = uni
        counter = counter + 1
    if readyToRemove:
        sql = sql[:len(sql) - 1]
        sql += ')'
    dbAccess.execute(sql, vals)
    return dbAccess.fetchall()

def DBgetGOFunctionNames(mydb: mysql.connector, IDProteins):
    dbAccess = mydb.cursor()
    sql = f'SELECT p.UniProt, fn.FunctionName, fn.FunctionGONumber FROM function_protein fp JOIN ' \
          f'functionname fn ON fp.ID_FunctionName=fn.ID JOIN protein p ON p.ID=fp.ID_Protein WHERE fp.ID_Protein IN ('
    vals = {}
    readyToRemove = False
    counter = 1
    for uni in IDProteins:
        sql += '%(IDProteinName' + str(counter) + ')s,'
        readyToRemove = True
        vals['IDProteinName' + str(counter)] = uni
        counter = counter + 1
    if readyToRemove:
        sql = sql[:len(sql) - 1]
        sql += ')'
    dbAccess.execute(sql, vals)
    return dbAccess.fetchall()

def DBgetGOProcessNames(mydb: mysql.connector, IDProteins):
    dbAccess = mydb.cursor()
    sql = f'SELECT p.UniProt, pn.ProcessName, pn.ProcessGONumber FROM process_protein pp JOIN ' \
          f'processname pn ON pp.ID_ProcessName=pn.ID JOIN protein p ON p.ID=pp.ID_Protein WHERE pp.ID_Protein IN ('
    vals = {}
    readyToRemove = False
    counter = 1
    for uni in IDProteins:
        sql += '%(IDProteinName' + str(counter) + ')s,'
        readyToRemove = True
        vals['IDProteinName' + str(counter)] = uni
        counter = counter + 1
    if readyToRemove:
        sql = sql[:len(sql) - 1]
        sql += ')'
    dbAccess.execute(sql, vals)
    return dbAccess.fetchall()

def DBgetDataForGraphsForUniProtmydb(mydb: mysql.connector, UniProtIDS):
    dbAccess = mydb.cursor()
    sql = f'SELECT o.Short, p.Gene, p.ID, c.CysID, c.ID, c.Positions, c.Order, ' \
          f'IF(ox.OxiMeanValue != "ni" AND ox.OxiMeanValue != "ND", ROUND(ox.OxiMeanValue,2), ox.OxiMeanValue), ' \
          f'IF(ox.OxiSD != "ni", ROUND(ox.OxiSD,2), ox.OxiSD), ox.Repetition, ox.Isoform, ox.ID_Sample, ' \
          f's.SampleName, s.ID_Experiment, e.Experiment, e.Strain, e.ID_Publication, pub.Author, pub.Journal, ' \
          f'pub.Year, pub.DOI, s.NoForGraph, e.Detail, p.UniProt ' \
          f'FROM protein p JOIN cysteine c ON c.ID_Protein=p.ID JOIN organism o ON p.ID_Organism=o.ID JOIN ' \
          f'oxidation ox ON ox.ID_Cysteine=c.ID JOIN sample s ON ox.ID_Sample=s.ID JOIN experiment e ON ' \
          f'e.ID=s.ID_Experiment LEFT JOIN publication pub ON e.ID_Publication=pub.ID WHERE p.UniProt IN ('
    vals = {}
    readyToRemove = False
    counter = 1
    for uni in UniProtIDS:
        sql += '%(UniProtIDName' + str(counter) + ')s,'
        readyToRemove = True
        vals['UniProtIDName' + str(counter)] = uni
        counter = counter + 1
    if readyToRemove:
        sql = sql[:len(sql) - 1]
        sql += ') ORDER BY e.ID, p.ID, c.ID, s.NoForGraph'
    dbAccess.execute(sql, vals)
    return dbAccess.fetchall()