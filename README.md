# databricks-com.databricks.spark.sqldw

## Goal: 
From within databricks load data from SQL datawarehouse with own Azure Active Directory credentials, without giving developers ADMIN privileges.

## Prerequisites:
In order to use AAD credentials for the authentification with the SQL datawarehouse, ADAL4J with all dependencies is required. Attaching the jars to the cluster did not work for me. Therefore, I uploaded all Jars (which can be found on this repo) to '/dbfs/FileStore/tables'.
Then I created a script with the following content and placed in /dbfs/databricks/init/adal4j-install.sh, such that it is run on startup.

```
#!/bin/bash
cp /dbfs/FileStore/tables/*.jar /mnt/driver-daemon/jars/
cp /dbfs/FileStore/tables/*.jar /mnt/jars/driver-daemon/
```

## Behaviour
In order to see all that happens under the hood with `com.databricks.spark.sqldw`, I was made (temporary) server admin.

In example.py we see two code blocks / cells.
1. The first cell loads the data in a lazy way, only meta data is read from the SQL datawarehouse by running `set fmtonly on`
The resulting SQL actions of this commands can be found in the EXCEL file run_as_admin.xlsx also in this Repo.
2. When the second cell is run, the following things happen in order. 
* A temporary scoped credential is created in our SQL datawarehouse with the blobstorage credentials.
* An external datasource is created with these credentials
* An external Fileformat is created 
* An external table is created for the previously created data source, with the created format
* The created tables, formats and datasources are dropped.

## Problem
In order to execute the steps (and thus our script) successfully the used AAD user needs at least ADMIN privileges. In other words, just to read data from our SQL warehouse, NOT read permission but ADMIN permission is required. This is unwanted. Rather, we would like to give our Developers (mostly data scienstist) less privileges. However, with the current setup this is not possible. 

Possibly a bug and already reported to microsoft: Only as server admin I could run the code succesfully. Corresponding to microsoft docs, at least CONTROL permission is required to execute commands. However, with CONTROL permission on database, I could not execute the CREATE SCOPED CREDENTIAL command.

## Ideal situation
Ideally we set up a blobstorage dedicated for the transfer of data between our SQL Datawarehouse and Databricks. This blobstorage is fixed and will not change. Then our admin creates the required scoped credential with the credentials for this blobstorage. Furhtermore he would create the external data source and the required external file format. 

If these objects are already in the database, we just have to point to these, and the required permissions on our database for a developer can be much lower. 

## Solution
The above situation requires that the elements of the following query (which also can be found in the excel file) can be set using options in databricks. It should be possible to set the EXTERNAL DATA SOURCE to be used, as well as the FILE_FORMAT. 

```
CREATE EXTERNAL TABLE tmp_databricks_2018_09_12_08_32_07_183_e95b63e23eba485db33292928ee407e7_external_table
WITH
(
    LOCATION = '/tmp/2018-09-12/08-32-07-183/3f439cc9-5d60-4414-b785-70f8ad3e72a2/',
    DATA_SOURCE = tmp_databricks_2018_09_12_08_32_07_183_e95b63e23eba485db33292928ee407e7_data_source,
    FILE_FORMAT = tmp_databricks_2018_09_12_08_32_07_183_e95b63e23eba485db33292928ee407e7_file_format,
    REJECT_TYPE = VALUE,
    REJECT_VALUE = 0
)
AS SELECT ProgramName" FROM (SELECT TOP 21 * FROM (SELECT  * FROM (select ProgramName from mgt.programparameter) AS "sqldw_connector_source_query" ) AS "subquery_0" ) q 
```
