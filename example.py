# Databricks notebook source
# Set credentials for blob storage 
spark.conf.set("fs.azure.account.key.databricksstoragedevweu.blob.core.windows.net", "******accesskey******") 

username = "guido.tournois@icemobile.com" # AAD user with READ permission on database
password = dbutils.secrets.get("guido.tournois@icemobile.com","password")

jdbcString = (
  "jdbc:sqlserver://af-cbi-dev-weu.database.windows.net:1433;database=AF;encrypt=false;"+
  "trustServerCertificate=true;hostNameInCertificate=*.database.windows.net;"+
  "Authentication=ActiveDirectoryPassword;"
)

df = (spark.read.format("com.databricks.spark.sqldw")
                .option("url", jdbcString)
                .option("tempDir", "wasbs://data@databricksstoragedevweu.blob.core.windows.net/tmp")
                .option("forward_spark_azure_storage_credentials", "true")
                .option("user","guido.tournois@icemobile.com")
                .option("password",password)
                .option("query", "select ProgramName from mgt.programparameter")
                .load())

# COMMAND ----------

df.show()

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

# MAGIC %%bash
# MAGIC ls -la ../../dbfs/FileStore/tables/
# MAGIC # rm ../../dbfs/FileStore/tables/azure_sqldb_spark_1_0_0_jar_with_dependencies-d8798.jar
# MAGIC # rm ../../dbfs/FileStore/tables/junit_4_8_1-aac34.jar
# MAGIC # rm ../../dbfs/FileStore/tables/mssql_jdbc_6_4_0_jre8-ebbc3.jar

# COMMAND ----------

# MAGIC %scala
# MAGIC 
# MAGIC import java.sql.Connection;
# MAGIC import java.sql.ResultSet;
# MAGIC import java.sql.Statement;
# MAGIC 
# MAGIC import com.microsoft.sqlserver.jdbc.SQLServerDataSource;
# MAGIC import com.microsoft.sqlserver.jdbc.SQLServerDriver
# MAGIC 
# MAGIC var ds = new SQLServerDataSource();
# MAGIC ds.setServerName("af-cbi-dev-weu.database.windows.net"); // Replace with your server name
# MAGIC ds.setDatabaseName("AF"); // Replace with your database
# MAGIC ds.setUser("guido.tournois@icemobile.com"); // Replace with your user name
# MAGIC ds.setPassword("gT22071988"); // Replace with your password
# MAGIC ds.setAuthentication("ActiveDirectoryPassword");
# MAGIC ds.setHostNameInCertificate("*.database.windows.net");
# MAGIC // ds.setPortNumber(1433);
# MAGIC ds.setTrustServerCertificate(true);
# MAGIC 
# MAGIC var connection = ds.getConnection(); 
# MAGIC var stmt = connection.createStatement();
# MAGIC var res = stmt.executeQuery("SELECT SUSER_SNAME()")
# MAGIC res.

# COMMAND ----------



# COMMAND ----------

