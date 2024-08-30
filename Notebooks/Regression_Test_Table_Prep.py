# Databricks notebook source
from pyspark.sql.types import StructType, StructField, StringType, LongType, BooleanType
from pyspark.sql.functions import to_date, max, col, lower

# COMMAND ----------

fact_idw_dyn_cash_activity_raw_full_dict = {
    "pace_masterdbo_code_values": "SQL_IDW/Pace_Masterdbo_Code_Values/archive/",
    "securitydbo_xreference": "SQL_IDW/Securitydbo_Xreference/archive/",
    "securitydbo_security_master": "SQL_IDW/Securitydbo_Security_Master/archive/",
    "securitydbo_security_master_detail": "SQL_IDW/Securitydbo_Security_Master_Detail/archive/",
    "securitydbo_secmaster_detail_ext": "SQL_IDW/Securitydbo_Secmaster_Detail_Ext/archive/",
    "rulesdbo_entity": "SQL_IDW/Rulesdbo_Entity/archive/",
    "rulesdbo_entity_extention": "SQL_IDW/Rulesdbo_Entity_Extention/archive/",
    "pace_masterdbo_interfaces": "SQL_IDW/Pace_Masterdbo_Interfaces/archive/",
    "pace_masterdbo_codes": "SQL_IDW/Pace_Masterdbo_Codes/archive/",
    "rulesdbo_entity_xreference": "SQL_IDW/Rulesdbo_Entity_Xreference/archive/",
    "rulesdbo_entity_extention_detail": "SQL_IDW/Rulesdbo_Entity_Extention_Detail/archive/",
}
fact_idw_dyn_cash_activity_raw_delta_dict = {
    "cashdbo_cash_activity_data": "SQL_IDW/Cashdbo_Cash_Activity/archive/data/"
}

# COMMAND ----------

from pyspark.sql.functions import broadcast

def get_latest_raw_dataset(raw_path, file_type):
    if file_type == 'raw':
        files = dbutils.fs.ls(f'abfss://raw@stadlsidpdevcanc.dfs.core.windows.net/{raw_path}')
        files_df = spark.createDataFrame(files)
        filtered_files_df = files_df.filter(~col("path").contains("QA"))
        max_modification_time = filtered_files_df.agg(max("modificationTime")).collect()[0][0]
        max_modification_path = filtered_files_df.filter(col("modificationTime") == max_modification_time).select("path").first()[0]
        return max_modification_path
    if file_type == 'qa':
        files = dbutils.fs.ls(f'abfss://raw@stadlsidpdevcanc.dfs.core.windows.net/{raw_path}')
        files_df = spark.createDataFrame(files)
        filtered_files_df = files_df.filter(col("path").contains("INITIAL"))
        max_modification_time = filtered_files_df.agg(max("modificationTime")).collect()[0][0]
        max_modification_path = filtered_files_df.filter(col("modificationTime") == max_modification_time).select("path").first()[0]
        return max_modification_path

def read_parquet_dataset(file_path, infer_schema=True):
    return spark.read.format('parquet').option('header', 'true').option('inferSchema', str(infer_schema)).load(file_path)

def process_files(files_dict, file_type):
    df_dict = {}
    for variable_name, path in files_dict.items():
        print(f"Processing {variable_name}")
        latest_file = get_latest_raw_dataset(path, file_type)
        df = read_parquet_dataset(latest_file)
        df_dict[f'{file_type}_{variable_name}_df'] = df
    return df_dict

# Assuming fact_idw_dyn_cash_activity_raw_full_dict and fact_idw_dyn_cash_activity_raw_delta_dict are defined in a previous cell
raw_df_dict = process_files(fact_idw_dyn_cash_activity_raw_full_dict, 'raw')
qa_df_dict = process_files(fact_idw_dyn_cash_activity_raw_delta_dict, 'qa')

# COMMAND ----------

reg_df_list = []
modify = False

# COMMAND ----------

from pyspark.sql import functions as F    
if modify:
    reg_cashdbo_cash_activity_df = qa_df_dict['qa_cashdbo_cash_activity_data_df'].filter("CASH_INT  in (22224210, 22224214)")
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("TRANS_QUANTITY", F.when(F.col("CASH_INT") == 22224210, 1).otherwise(F.col("TRANS_QUANTITY")))
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("PRICE", F.when(F.col("CASH_INT") == 22224210, 200).otherwise(F.col("PRICE")))
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("SECURITY_ALIAS", F.expr("CAST('999' AS STRING) || CAST(SECURITY_ALIAS AS STRING)").cast("decimal(38, 18)"))
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("CASH_INT", F.expr("CAST('9' AS STRING) || CAST(CASH_INT AS STRING)").cast("decimal(38, 18)"))
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("SRC_INTFC_INST", F.lit(158).cast("decimal(38, 18)"))
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("ENTITY_ID", F.concat(F.lit("QA_"), "ENTITY_ID"))
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("UPDATE_SOURCE", F.concat(F.lit("QA_"), "UPDATE_SOURCE"))
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("STAR_TAG25", F.lit("QA99E1R2CI701HJA-7"))
else:
    reg_cashdbo_cash_activity_df = qa_df_dict['qa_cashdbo_cash_activity_data_df'].filter("CASH_INT  in (22224210, 22224214, 17717149)")
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("SECURITY_ALIAS", F.expr("CAST('999' AS STRING) || CAST(SECURITY_ALIAS AS STRING)").cast("decimal(38, 18)"))
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("CASH_INT", F.expr("CAST('9' AS STRING) || CAST(CASH_INT AS STRING)").cast("decimal(38, 18)"))
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("SRC_INTFC_INST", F.lit(158).cast("decimal(38, 18)"))    
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("ENTITY_ID", F.concat(F.lit("QA_"), "ENTITY_ID"))
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("UPDATE_SOURCE", F.concat(F.lit("QA_"), "UPDATE_SOURCE"))
    reg_cashdbo_cash_activity_df = reg_cashdbo_cash_activity_df.withColumn("STAR_TAG25", F.lit("QA99E1R2CI701HJA-7"))

reg_df_list.append('reg_cashdbo_cash_activity_df')

# COMMAND ----------


delete_conditions = (F.col("ENTITY_ID").contains("QA_") | F.col("UPDATE_SOURCE").contains("QA_"))
db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.cashdbo_cash_activity").filter(delete_conditions)

if not modify:
    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")

    spark.sql("""
        DELETE FROM `db-dev-ei`.enriched_idw_eagle.cashdbo_cash_activity
        WHERE ENTITY_ID IN (SELECT ENTITY_ID FROM temp_view_to_delete)
        OR UPDATE_SOURCE IN (SELECT UPDATE_SOURCE FROM temp_view_to_delete)
    """)

db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.cashdbo_cash_activity").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

reg_rulesdbo_entity_df = raw_df_dict['raw_rulesdbo_entity_df'].filter('ENTITY_ID  in ("SUTTONEQ", "BAGLANSL", "IMP032D")')
reg_rulesdbo_entity_df = reg_rulesdbo_entity_df.withColumn("ENTITY_ID", F.concat(F.lit("QA_"), "ENTITY_ID"))
reg_rulesdbo_entity_df = reg_rulesdbo_entity_df.withColumn("UPD_USER", F.concat(F.lit("QA_"), "UPD_USER"))

reg_df_list.append('reg_rulesdbo_entity_df')

# COMMAND ----------

delete_conditions = (F.col("ENTITY_ID").contains("QA_") | F.col("UPD_USER").contains("QA_"))
db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity").filter(delete_conditions)


if not modify:

    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")

    spark.sql("""
        DELETE FROM `db-dev-ei`.enriched_idw_eagle.rulesdbo_entity
        WHERE ENTITY_ID IN (SELECT ENTITY_ID FROM temp_view_to_delete)
        OR UPD_USER IN (SELECT UPD_USER FROM temp_view_to_delete)
    """)

db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

reg_rulesdbo_entity_xreference_df = raw_df_dict['raw_rulesdbo_entity_xreference_df'].filter('ENTITY_ID  in ("SUTTONEQ", "BAGLANSL", "IMP032D")')
reg_rulesdbo_entity_xreference_df = reg_rulesdbo_entity_xreference_df.withColumn("ENTITY_ID", F.concat(F.lit("QA_"), "ENTITY_ID"))
reg_rulesdbo_entity_xreference_df = reg_rulesdbo_entity_xreference_df.withColumn("XREF_ACCOUNT_ID", F.concat(F.lit("QA_"), "XREF_ACCOUNT_ID"))
reg_rulesdbo_entity_xreference_df = reg_rulesdbo_entity_xreference_df.withColumn("XREF_ACCOUNT_ID_TYPE", F.concat(F.lit("QA_"), "XREF_ACCOUNT_ID_TYPE"))
reg_rulesdbo_entity_xreference_df = reg_rulesdbo_entity_xreference_df.withColumn("UPDATE_SOURCE", F.concat(F.lit("QA_"), "UPDATE_SOURCE"))
reg_rulesdbo_entity_xreference_df = reg_rulesdbo_entity_xreference_df.withColumn("INSTANCE", F.expr("CAST('999' AS STRING) || CAST(INSTANCE AS STRING)").cast("double"))

reg_df_list.append('reg_rulesdbo_entity_xreference_df')

# COMMAND ----------

delete_conditions = (F.col("ENTITY_ID").contains("QA_") | F.col("XREF_ACCOUNT_ID").contains("QA_") | F.col("XREF_ACCOUNT_ID_TYPE").contains("QA_") | F.col("UPDATE_SOURCE").contains("QA_"))
db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_xreference").filter(delete_conditions)

if not modify:

    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")

    spark.sql("""
        DELETE FROM `db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_xreference
        WHERE ENTITY_ID IN (SELECT ENTITY_ID FROM temp_view_to_delete)
        OR XREF_ACCOUNT_ID IN (SELECT XREF_ACCOUNT_ID FROM temp_view_to_delete)
        OR XREF_ACCOUNT_ID_TYPE IN (SELECT XREF_ACCOUNT_ID_TYPE FROM temp_view_to_delete)
        OR UPDATE_SOURCE IN (SELECT UPDATE_SOURCE FROM temp_view_to_delete)
    """)

db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_xreference").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

reg_pace_masterdbo_code_values_df = raw_df_dict['raw_pace_masterdbo_code_values_df'].filter('Instance in (23229,23832,26079,26134,31076)')
reg_pace_masterdbo_code_values_df = reg_pace_masterdbo_code_values_df.withColumn("INSTANCE", F.expr("CAST('999' AS STRING) || CAST(INSTANCE AS STRING)").cast("double"))
reg_pace_masterdbo_code_values_df = reg_pace_masterdbo_code_values_df.withColumn("CODE_INST", F.expr("CAST('999' AS STRING) || CAST(CODE_INST AS STRING)").cast("double"))
reg_pace_masterdbo_code_values_df = reg_pace_masterdbo_code_values_df.withColumn("SHORT_DESC", F.concat(F.lit("QA_"), "SHORT_DESC"))
reg_pace_masterdbo_code_values_df = reg_pace_masterdbo_code_values_df.withColumn("LONG_DESC", F.concat(F.lit("QA_"), "LONG_DESC"))
reg_pace_masterdbo_code_values_df = reg_pace_masterdbo_code_values_df.withColumn("UPD_OPER", F.concat(F.lit("QA_"), "UPD_OPER"))

reg_df_list.append('reg_pace_masterdbo_code_values_df')

# COMMAND ----------

delete_conditions = (F.col("SHORT_DESC").contains("QA_") | F.col("LONG_DESC").contains("QA_") | F.col("UPD_OPER").contains("QA_"))
db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.pace_masterdbo_code_values").filter(delete_conditions)
if not modify:


    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")

    spark.sql("""
        DELETE FROM `db-dev-ei`.enriched_idw_eagle.pace_masterdbo_code_values
        WHERE CODE_INST IN (SELECT CODE_INST FROM temp_view_to_delete)
        OR SHORT_DESC IN (SELECT SHORT_DESC FROM temp_view_to_delete)
        OR LONG_DESC IN (SELECT LONG_DESC FROM temp_view_to_delete)
        OR UPD_OPER IN (SELECT UPD_OPER FROM temp_view_to_delete)
    """)

db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.pace_masterdbo_code_values").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

if modify:
    reg_securitydbo_secmaster_detail_ext_df = raw_df_dict['raw_securitydbo_secmaster_detail_ext_df'].filter('SECURITY_ALIAS in (2718.000000000000000000, 1729.000000000000000000)')
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("SECURITY_ALIAS", F.expr("CAST('999' AS STRING) || CAST(SECURITY_ALIAS AS STRING)").cast("double"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("GICS_SECTOR", F.expr("CAST('999' AS STRING) || CAST(GICS_SECTOR AS STRING)").cast("double"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("SOURCE_NAME", F.concat(F.lit("QA_"), "SOURCE_NAME"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("GICS_SECTOR", F.concat(F.lit("999"), "GICS_SECTOR"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("GICS_INDUSTRY_GROUP", F.concat(F.lit("999"), "GICS_INDUSTRY_GROUP"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("GICS_INDUSTRY", F.concat(F.lit("999"), "GICS_INDUSTRY"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("GICS_SUB_INDUSTRY", F.concat(F.lit("999"), "GICS_SUB_INDUSTRY"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("UPDATE_SOURCE", F.concat(F.lit("QA_"), "UPDATE_SOURCE"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("PRICE_TYPE", F.when(F.col("SECURITY_ALIAS") == 9991729.0, F.lit("B")).otherwise(F.col("PRICE_TYPE")))
else:
    reg_securitydbo_secmaster_detail_ext_df = raw_df_dict['raw_securitydbo_secmaster_detail_ext_df'].filter('SECURITY_ALIAS in (2718.000000000000000000, 1729.000000000000000000, 153.000000000000000000)')
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("SECURITY_ALIAS", F.expr("CAST('999' AS STRING) || CAST(SECURITY_ALIAS AS STRING)").cast("double"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("GICS_SECTOR", F.expr("CAST('999' AS STRING) || CAST(GICS_SECTOR AS STRING)").cast("double"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("SOURCE_NAME", F.concat(F.lit("QA_"), "SOURCE_NAME"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("GICS_SECTOR", F.concat(F.lit("999"), "GICS_SECTOR"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("GICS_INDUSTRY_GROUP", F.concat(F.lit("999"), "GICS_INDUSTRY_GROUP"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("GICS_INDUSTRY", F.concat(F.lit("999"), "GICS_INDUSTRY"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("GICS_SUB_INDUSTRY", F.concat(F.lit("999"), "GICS_SUB_INDUSTRY"))
    reg_securitydbo_secmaster_detail_ext_df = reg_securitydbo_secmaster_detail_ext_df.withColumn("UPDATE_SOURCE", F.concat(F.lit("QA_"), "UPDATE_SOURCE"))

reg_df_list.append('reg_securitydbo_secmaster_detail_ext_df')

# COMMAND ----------

delete_conditions = (F.col("UPDATE_SOURCE").contains("QA_") | F.col("SOURCE_NAME").contains("QA_"))
db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.securitydbo_secmaster_detail_ext").filter(delete_conditions)

if not modify:


    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")

    spark.sql("""
        DELETE FROM `db-dev-ei`.enriched_idw_eagle.securitydbo_secmaster_detail_ext
        WHERE SECURITY_ALIAS IN (SELECT SECURITY_ALIAS FROM temp_view_to_delete)
        OR UPDATE_SOURCE IN (SELECT UPDATE_SOURCE FROM temp_view_to_delete)
        OR SOURCE_NAME IN (SELECT SOURCE_NAME FROM temp_view_to_delete)
    """)

db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.securitydbo_secmaster_detail_ext").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

reg_securitydbo_security_master_df = raw_df_dict['raw_securitydbo_security_master_df'].filter('SECURITY_ALIAS in (2718.000000000000000000, 1729.000000000000000000, 153.000000000000000000)')
reg_securitydbo_security_master_df = reg_securitydbo_security_master_df.withColumn("SECURITY_ALIAS", F.expr("CAST('999' AS STRING) || CAST(SECURITY_ALIAS AS STRING)").cast("double"))
reg_securitydbo_security_master_df = reg_securitydbo_security_master_df.withColumn("ISSUE_NAME", F.concat(F.lit("QA_"), "ISSUE_NAME"))
reg_securitydbo_security_master_df = reg_securitydbo_security_master_df.withColumn("UPDATE_SOURCE", F.concat(F.lit("QA_"), "UPDATE_SOURCE"))
reg_securitydbo_security_master_df = reg_securitydbo_security_master_df.withColumn("SOURCE_NAME", F.concat(F.lit("QA_"), "SOURCE_NAME"))

reg_df_list.append('reg_securitydbo_security_master_df')

# COMMAND ----------

delete_conditions = (F.col("UPDATE_SOURCE").contains("QA_") | F.col("SOURCE_NAME").contains("QA_") | F.col("ISSUE_NAME").contains("QA_"))
db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.securitydbo_security_master").filter(delete_conditions)

if not modify:

    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")

    spark.sql("""
        DELETE FROM `db-dev-ei`.enriched_idw_eagle.securitydbo_security_master
        WHERE SECURITY_ALIAS IN (SELECT SECURITY_ALIAS FROM temp_view_to_delete)
        OR UPDATE_SOURCE IN (SELECT UPDATE_SOURCE FROM temp_view_to_delete)
        OR SOURCE_NAME IN (SELECT SOURCE_NAME FROM temp_view_to_delete)
        OR ISSUE_NAME IN (SELECT ISSUE_NAME FROM temp_view_to_delete)
    """)

db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.securitydbo_security_master").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

reg_securitydbo_security_master_detail_df = raw_df_dict['raw_securitydbo_security_master_detail_df'].filter('SECURITY_ALIAS in (2718.000000000000000000, 1729.000000000000000000, 153.000000000000000000)')
reg_securitydbo_security_master_detail_df = reg_securitydbo_security_master_detail_df.withColumn("SECURITY_ALIAS", F.expr("CAST('999' AS STRING) || CAST(SECURITY_ALIAS AS STRING)").cast("double"))
reg_securitydbo_security_master_detail_df = reg_securitydbo_security_master_detail_df.withColumn("UPDATE_SOURCE", F.concat(F.lit("QA_"), "UPDATE_SOURCE"))
reg_securitydbo_security_master_detail_df = reg_securitydbo_security_master_detail_df.withColumn("SOURCE_NAME", F.concat(F.lit("QA_"), "SOURCE_NAME"))
reg_securitydbo_security_master_detail_df = reg_securitydbo_security_master_detail_df.withColumn("UPD_USER", F.concat(F.lit("QA_"), "UPD_USER"))

reg_df_list.append('reg_securitydbo_security_master_detail_df')

# COMMAND ----------

delete_conditions = (F.col("UPDATE_SOURCE").contains("QA_") | F.col("SOURCE_NAME").contains("QA_") | F.col("UPD_USER").contains("QA_"))
db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.securitydbo_security_master_detail").filter(delete_conditions)

if not modify:

    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")

    spark.sql("""
        DELETE FROM `db-dev-ei`.enriched_idw_eagle.securitydbo_security_master_detail
        WHERE SECURITY_ALIAS IN (SELECT SECURITY_ALIAS FROM temp_view_to_delete)
        OR UPDATE_SOURCE IN (SELECT UPDATE_SOURCE FROM temp_view_to_delete)
        OR SOURCE_NAME IN (SELECT SOURCE_NAME FROM temp_view_to_delete)
        OR UPD_USER IN (SELECT UPD_USER FROM temp_view_to_delete)
    """)

db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.securitydbo_security_master_detail").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

reg_securitydbo_xreference_df = raw_df_dict['raw_securitydbo_xreference_df'].filter('SECURITY_ALIAS in (2718.000000000000000000, 1729.000000000000000000, 153.000000000000000000)')

reg_securitydbo_xreference_df = reg_securitydbo_xreference_df.withColumn("SECURITY_ALIAS", F.expr("CAST('999' AS STRING) || CAST(SECURITY_ALIAS AS STRING)").cast("double"))
reg_securitydbo_xreference_df = reg_securitydbo_xreference_df.withColumn("XREF_SECURITY_ALIAS", F.expr("CAST('999' AS STRING) || CAST(XREF_SECURITY_ALIAS AS STRING)").cast("double"))
reg_securitydbo_xreference_df = reg_securitydbo_xreference_df.withColumn("XREF_SECURITY_ID", F.concat(F.lit("QA_"), "XREF_SECURITY_ID"))
reg_securitydbo_xreference_df = reg_securitydbo_xreference_df.withColumn("XREF_TYPE", F.concat(F.lit("QA_"), "XREF_TYPE"))
reg_securitydbo_xreference_df = reg_securitydbo_xreference_df.withColumn("UPDATE_SOURCE", F.concat(F.lit("QA_"), "UPDATE_SOURCE"))




reg_df_list.append('reg_securitydbo_xreference_df')

# COMMAND ----------

delete_conditions = (F.col("XREF_TYPE").contains("QA_") | F.col("UPDATE_SOURCE").contains("QA_"))
db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.securitydbo_xreference").filter(delete_conditions)
if not modify:

    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")

    spark.sql("""
        DELETE FROM `db-dev-ei`.enriched_idw_eagle.securitydbo_xreference
        WHERE SECURITY_ALIAS IN (SELECT SECURITY_ALIAS FROM temp_view_to_delete)
        OR XREF_SECURITY_ALIAS IN (SELECT XREF_SECURITY_ALIAS FROM temp_view_to_delete)
        OR XREF_SECURITY_ID IN (SELECT XREF_SECURITY_ID FROM temp_view_to_delete)
        OR XREF_TYPE IN (SELECT XREF_TYPE FROM temp_view_to_delete)
        OR UPDATE_SOURCE IN (SELECT UPDATE_SOURCE FROM temp_view_to_delete)
    """)

db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.securitydbo_xreference").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

reg_pace_masterdbo_codes_df = raw_df_dict['raw_pace_masterdbo_codes_df'].filter('Instance in (300242,10397,300342,300325,300325)')
reg_pace_masterdbo_codes_df = reg_pace_masterdbo_codes_df.withColumn("INSTANCE", F.expr("CAST('999' AS STRING) || CAST(INSTANCE AS STRING)").cast("double"))
reg_pace_masterdbo_codes_df = reg_pace_masterdbo_codes_df.withColumn("UPD_OPER", F.concat(F.lit("QA_"), "UPD_OPER"))
reg_pace_masterdbo_codes_df = reg_pace_masterdbo_codes_df.withColumn("SHORT_DESC", F.concat(F.lit("QA_"), "SHORT_DESC"))
reg_pace_masterdbo_codes_df = reg_pace_masterdbo_codes_df.withColumn("LONG_DESC", F.concat(F.lit("QA_"), "LONG_DESC"))

reg_df_list.append('reg_pace_masterdbo_codes_df')

# COMMAND ----------

delete_conditions = (F.col("INSTANCE").contains("QA_") | F.col("UPD_OPER").contains("QA_") | F.col("SHORT_DESC").contains("QA_") | F.col("LONG_DESC").contains("QA_"))
db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.pace_masterdbo_codes").filter(delete_conditions)
if not modify:

    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")

    spark.sql("""
        DELETE FROM `db-dev-ei`.enriched_idw_eagle.pace_masterdbo_codes
        WHERE INSTANCE IN (SELECT INSTANCE FROM temp_view_to_delete)
        OR UPD_OPER IN (SELECT UPD_OPER FROM temp_view_to_delete)
        OR SHORT_DESC IN (SELECT SHORT_DESC FROM temp_view_to_delete)
        OR LONG_DESC IN (SELECT LONG_DESC FROM temp_view_to_delete)
    """)

db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.pace_masterdbo_codes").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

reg_rulesdbo_entity_extention_detail_df = raw_df_dict['raw_rulesdbo_entity_extention_detail_df'].filter('ENTITY_ID  in ("SUTTONEQ", "BAGLANSL", "IMP032D")')
reg_rulesdbo_entity_extention_detail_df = reg_rulesdbo_entity_extention_detail_df.withColumn("ENTITY_ID", F.concat(F.lit("QA_"), "ENTITY_ID"))
reg_rulesdbo_entity_extention_detail_df = reg_rulesdbo_entity_extention_detail_df.withColumn("UPDATE_USER", F.concat(F.lit("QA_"), "UPDATE_USER"))

reg_df_list.append('reg_rulesdbo_entity_extention_detail_df')

# COMMAND ----------

delete_conditions = (F.col("ENTITY_ID").contains("QA_") | F.col("UPDATE_USER").contains("QA_"))
db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_extention_detail").filter(delete_conditions)
if not modify:

    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")

    spark.sql("""
        DELETE FROM `db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_extention_detail
        WHERE ENTITY_ID IN (SELECT ENTITY_ID FROM temp_view_to_delete)
        OR UPDATE_USER IN (SELECT UPDATE_USER FROM temp_view_to_delete)
    """)

db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_extention_detail").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

reg_rulesdbo_entity_extention_df = raw_df_dict['raw_rulesdbo_entity_extention_df'].filter('ENTITY_ID  in ("SUTTONEQ", "BAGLANSL", "IMP032D")')
reg_rulesdbo_entity_extention_df = reg_rulesdbo_entity_extention_df.withColumn("ENTITY_ID", F.concat(F.lit("QA_"), "ENTITY_ID"))
reg_rulesdbo_entity_extention_df = reg_rulesdbo_entity_extention_df.withColumn("UPDATE_SOURCE", F.concat(F.lit("QA_"), "UPDATE_SOURCE"))
reg_rulesdbo_entity_extention_df = reg_rulesdbo_entity_extention_df.withColumn("UPD_USER", F.concat(F.lit("QA_"), "UPD_USER"))

reg_df_list.append('reg_rulesdbo_entity_extention_df')

# COMMAND ----------

delete_conditions = (F.col("ENTITY_ID").contains("QA_") | F.col("UPD_USER").contains("QA_"))

db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_extention").filter(delete_conditions)

if not modify:


    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")

    spark.sql("""
        DELETE FROM `db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_extention
        WHERE ENTITY_ID IN (SELECT ENTITY_ID FROM temp_view_to_delete)
        OR UPD_USER IN (SELECT UPD_USER FROM temp_view_to_delete)
    """)

db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_extention").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

def collect_distinct_values(df, column_names):
    """
    Collects distinct values from specified columns of a DataFrame.
    
    Parameters:
    - df: The DataFrame to process.
    - column_names: A list of column names to collect distinct values from.
    
    Returns:
    A set of distinct values from the specified columns.
    """
    results = set()
    for column_name in column_names:
        try:
            selected_data = df.select(column_name).distinct().collect()
            for row in selected_data:
                results.add(row[column_name])
        except Exception as e:
            pass
            # print(f"Error processing column {column_name}: {e}")
    return results

# List of column names to check for distinct values
column_names = ["SOURCE_NAME", "UPD_OPER", "UPDATE_SOURCE"]

# Initialize an empty set to store results
all_results = set()

# Assuming reg_df_list is a list of DataFrame names as strings
for df_name in reg_df_list:
    df = eval(df_name)  # Evaluate the DataFrame name to get the DataFrame object
    distinct_values = collect_distinct_values(df, column_names)
    all_results.update(distinct_values)

# Convert the set to a list if needed
results = list(all_results)

# COMMAND ----------

reg_pace_masterdbo_interfaces_df = raw_df_dict['raw_pace_masterdbo_interfaces_df'].withColumn("SHORT_DESC", F.concat(F.lit("QA_"), "SHORT_DESC")).filter(F.col("SHORT_DESC").isin(results))
reg_pace_masterdbo_interfaces_df = reg_pace_masterdbo_interfaces_df.withColumn("INSTANCE", F.expr("CAST('999' AS STRING) || CAST(INSTANCE AS STRING)").cast("double"))
reg_pace_masterdbo_interfaces_df = reg_pace_masterdbo_interfaces_df.withColumn("LONG_DESC", F.concat(F.lit("QA_"), "LONG_DESC"))
reg_pace_masterdbo_interfaces_df = reg_pace_masterdbo_interfaces_df.withColumn("UPD_USER", F.concat(F.lit("QA_"), "UPD_USER"))

reg_df_list.append('reg_pace_masterdbo_interfaces_df')

# COMMAND ----------

delete_condition = col("SHORT_DESC").isin(results)
db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.pace_masterdbo_interfaces").filter(delete_condition)
if not modify:

    # Assuming Delta Lake is in use for the ability to perform deletes
    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")
    spark.sql("""
        DELETE FROM `db-dev-ei`.enriched_idw_eagle.pace_masterdbo_interfaces
        WHERE SHORT_DESC IN (SELECT SHORT_DESC FROM temp_view_to_delete)
    """)
db_df_to_delete = spark.table("`db-dev-ei`.enriched_idw_eagle.pace_masterdbo_interfaces").filter(delete_condition)
display(db_df_to_delete.count())

# COMMAND ----------

delete_conditions = col("PORTFOLIO_ID").contains("QA_")
db_df_to_delete = spark.table("`db-dev-ei`.curated_common.dim_portfolio").filter(delete_conditions)

# Assuming Delta Lake is in use for the ability to perform deletes and modify is set to false
if not modify:
    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")
    spark.sql("""
        DELETE FROM `db-dev-ei`.curated_common.dim_portfolio
        WHERE PORTFOLIO_ID IN (SELECT PORTFOLIO_ID FROM temp_view_to_delete)
    """)
db_df_to_delete = spark.table("`db-dev-ei`.curated_common.dim_portfolio").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

delete_conditions = col("IMCO_SECURITY_ALIAS_ID").isin(['9992718','9991729','999153' ])
db_df_to_delete = spark.table("`db-dev-ei`.curated_common.dim_security").filter(delete_conditions)

if not modify:
    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")
    spark.sql("""
        DELETE FROM `db-dev-ei`.curated_common.dim_security
        WHERE IMCO_SECURITY_ALIAS_ID IN (SELECT IMCO_SECURITY_ALIAS_ID FROM temp_view_to_delete) 
    """)
db_df_to_delete = spark.table("`db-dev-ei`.curated_common.dim_security").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

delete_conditions = col("IDW_CASH_INT").isin(999304067, 999304083, 999304097, 999304555, 99923604421, 917717149, 922224214, 922224210)
db_df_to_delete = spark.table("`db-dev-ei`.curated_common.fact_idw_dyn_cash_activity").filter(delete_conditions)

# Assuming Delta Lake is in use for the ability to perform deletes and modify is set to false
if not modify:
    db_df_to_delete.createOrReplaceTempView("temp_view_to_delete")
    spark.sql("""
        DELETE FROM `db-dev-ei`.curated_common.fact_idw_dyn_cash_activity
        WHERE IDW_CASH_INT IN (SELECT IDW_CASH_INT FROM temp_view_to_delete)
    """)
db_df_to_delete = spark.table("`db-dev-ei`.curated_common.fact_idw_dyn_cash_activity").filter(delete_conditions)
display(db_df_to_delete.count())

# COMMAND ----------

if modify:
    reg_df_list = ['reg_cashdbo_cash_activity_df','reg_securitydbo_secmaster_detail_ext_df']
    print(reg_df_list)

# COMMAND ----------

from datetime import datetime
import re

reg_file_names = [item.replace('reg_', '').replace('_df', '') for item in reg_df_list]
for file_name in reg_file_names:
    dbutils.fs.mkdirs(f"abfss://qastatic@stadlsidpdevcanc.dfs.core.windows.net/regression_testing/{file_name}")
    if file_name != "cashdbo_cash_activity":
        print(file_name)       
        raw_df = raw_df_dict[f'raw_{file_name}_df']
        reg_df = eval(f'reg_{file_name}_df')
        combined_df = raw_df.union(reg_df)
        output_file_name = f"{file_name.title()}_QA_FULL_{datetime.now().strftime('%Y-%m-%d')}"
        output_file_path_qa = f"abfss://qastatic@stadlsidpdevcanc.dfs.core.windows.net/regression_testing/{file_name}/{output_file_name}"
        output_file_path_raw = f"abfss://raw@stadlsidpdevcanc.dfs.core.windows.net/SQL_IDW/{file_name.title()}/current/{output_file_name}"
        combined_df.coalesce(1).write.mode("overwrite").parquet(output_file_path_raw)
        combined_df.coalesce(1).write.mode("overwrite").parquet(output_file_path_qa)
        print(raw_df.count(), reg_df.count(), combined_df.count())

        dbutils.fs.rm(f"{output_file_path_raw}.parquet", recurse=True)
        dbutils.fs.rm(f"{output_file_path_qa}.parquet", recurse=True)
        
        files_qa = dbutils.fs.ls(output_file_path_qa)
        parquet_file = [file for file in files_qa if re.match(r'.*\.parquet$', file.name)]

        if parquet_file:
            source_path = parquet_file[0].path
            desired_file_path = f"{output_file_path_qa.rstrip('/')}.parquet"  
            dbutils.fs.mv(source_path, desired_file_path)
            dbutils.fs.rm(output_file_path_qa, recurse=True)

        files_raw = dbutils.fs.ls(output_file_path_raw)
        parquet_file = [file for file in files_raw if re.match(r'.*\.parquet$', file.name)]
        
        if parquet_file:
            
            source_path = parquet_file[0].path
            desired_file_path = f"{output_file_path_raw.rstrip('/')}.parquet"  
            dbutils.fs.mv(source_path, desired_file_path)
            dbutils.fs.rm(output_file_path_raw, recurse=True)
    else:
        print(file_name)     
        dbutils.fs.mkdirs(f"abfss://qastatic@stadlsidpdevcanc.dfs.core.windows.net/regression_testing/{file_name}/pk")
        dbutils.fs.mkdirs(f"abfss://qastatic@stadlsidpdevcanc.dfs.core.windows.net/regression_testing/{file_name}/data")
        output_file_name = f"{file_name.title()}_QA_DELTA_{datetime.now().strftime('%Y-%m-%d')}"
        output_file_path_qa_pk = f"abfss://qastatic@stadlsidpdevcanc.dfs.core.windows.net/regression_testing/{file_name}/pk/{output_file_name}"
        output_file_path_qa_data = f"abfss://qastatic@stadlsidpdevcanc.dfs.core.windows.net/regression_testing/{file_name}/data/{output_file_name}"
        output_file_path_raw_pk = f"abfss://raw@stadlsidpdevcanc.dfs.core.windows.net/SQL_IDW/{file_name.title()}/current/pk/{output_file_name}"
        output_file_path_raw_data = f"abfss://raw@stadlsidpdevcanc.dfs.core.windows.net/SQL_IDW/{file_name.title()}/current/data/{output_file_name}"
        
        reg_df = eval(f'reg_{file_name}_df')
        reg_df_pk = reg_df.select("CASH_INT")
        
        files = dbutils.fs.ls(f'abfss://raw@stadlsidpdevcanc.dfs.core.windows.net/SQL_IDW/{file_name.title()}/archive/pk')
        files_df = spark.createDataFrame(files)
        max_modification_time = files_df.filter(~files_df.path.contains("QA")).select(max("modificationTime")).collect()[0][0]
        max_modification_path = files_df.filter((files_df.modificationTime == max_modification_time) & (~files_df.path.contains("QA"))).select("path").collect()[0][0]        
        raw_df_pk = spark.read.format("parquet").option("header", "true").option("maxRowsInMemory", 20).option("inferSchema", "true").load(max_modification_path).select("CASH_INT")

        combined_pk_df = raw_df_pk.union(reg_df_pk)
        combined_pk_df = combined_pk_df.select("CASH_INT").distinct()

        dbutils.fs.rm(output_file_path_qa_data, recurse=True)
        dbutils.fs.rm(output_file_path_raw_data, recurse=True)
        dbutils.fs.rm(output_file_path_qa_pk, recurse=True)
        dbutils.fs.rm(output_file_path_raw_pk, recurse=True)

        combined_pk_df.coalesce(1).write.mode("overwrite").parquet(output_file_path_raw_pk)
        combined_pk_df.coalesce(1).write.mode("overwrite").parquet(output_file_path_qa_pk)
        print(raw_df_pk.count(), reg_df_pk.count(), combined_pk_df.count())

        reg_df.coalesce(1).write.mode("overwrite").parquet(output_file_path_raw_data)
        reg_df.coalesce(1).write.mode("overwrite").parquet(output_file_path_qa_data)
        
        files = dbutils.fs.ls(output_file_path_raw_pk)
        parquet_file_pk = [file for file in files if re.match(r'.*\.parquet$', file.name)]
        if parquet_file_pk:
            source_path = parquet_file_pk[0].path
            desired_file_path = f"{output_file_path_raw_pk.rstrip('/')}.parquet" 
            dbutils.fs.mv(source_path, desired_file_path)
            dbutils.fs.rm(output_file_path_raw_pk, recurse=True)

        files = dbutils.fs.ls(output_file_path_qa_pk)
        parquet_file_pk = [file for file in files if re.match(r'.*\.parquet$', file.name)]
        if parquet_file_pk:
            source_path = parquet_file_pk[0].path
            desired_file_path = f"{output_file_path_qa_pk.rstrip('/')}.parquet"  
            dbutils.fs.mv(source_path, desired_file_path)
            dbutils.fs.rm(output_file_path_qa_pk, recurse=True)
            
            
        files = dbutils.fs.ls(output_file_path_raw_data)
        parquet_file_data = [file for file in files if re.match(r'.*\.parquet$', file.name)]
        if parquet_file_data:
            source_path = parquet_file_data[0].path
            desired_file_path = f"{output_file_path_raw_data.rstrip('/')}.parquet"  
            dbutils.fs.mv(source_path, desired_file_path)
            dbutils.fs.rm(output_file_path_raw_data, recurse=True)

        files = dbutils.fs.ls(output_file_path_qa_data)
        parquet_file_data = [file for file in files if re.match(r'.*\.parquet$', file.name)]
        if parquet_file_data:
            source_path = parquet_file_data[0].path
            desired_file_path = f"{output_file_path_qa_data.rstrip('/')}.parquet" 
            dbutils.fs.mv(source_path, desired_file_path)
            dbutils.fs.rm(output_file_path_qa_data, recurse=True)

            
        


# COMMAND ----------

from pyspark.sql.functions import col

# Define a list of tuples with table names and their delete conditions
tables_with_conditions = [
    ("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_extention", (col("ENTITY_ID").contains("QA_") | col("UPD_USER").contains("QA_"))),
    # ("`db-dev-ei`.enriched_idw_eagle.pace_masterdbo_interfaces", col("SHORT_DESC").isin(results)),
    ("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_extention_detail", (col("ENTITY_ID").contains("QA_") | col("UPDATE_USER").contains("QA_"))),
    ("`db-dev-ei`.enriched_idw_eagle.pace_masterdbo_codes", (col("INSTANCE").contains("QA_") | col("UPD_OPER").contains("QA_") | col("SHORT_DESC").contains("QA_") | col("LONG_DESC").contains("QA_"))),
    ("`db-dev-ei`.enriched_idw_eagle.securitydbo_xreference", (col("XREF_TYPE").contains("QA_") | col("UPDATE_SOURCE").contains("QA_"))),
    ("`db-dev-ei`.enriched_idw_eagle.securitydbo_security_master_detail", (col("UPDATE_SOURCE").contains("QA_") | col("SOURCE_NAME").contains("QA_") | col("UPD_USER").contains("QA_"))),
    ("`db-dev-ei`.enriched_idw_eagle.securitydbo_security_master", (col("UPDATE_SOURCE").contains("QA_") | col("SOURCE_NAME").contains("QA_") | col("ISSUE_NAME").contains("QA_"))),
    ("`db-dev-ei`.enriched_idw_eagle.securitydbo_secmaster_detail_ext", (col("UPDATE_SOURCE").contains("QA_") | col("SOURCE_NAME").contains("QA_"))),
    ("`db-dev-ei`.enriched_idw_eagle.pace_masterdbo_code_values", (col("SHORT_DESC").contains("QA_") | col("LONG_DESC").contains("QA_") | col("UPD_OPER").contains("QA_"))),
    ("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_xreference", (col("ENTITY_ID").contains("QA_") | col("XREF_ACCOUNT_ID").contains("QA_") | col("XREF_ACCOUNT_ID_TYPE").contains("QA_") | col("UPDATE_SOURCE").contains("QA_"))),
    ("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity", (col("ENTITY_ID").contains("QA_") | col("UPD_USER").contains("QA_"))),
    ("`db-dev-ei`.enriched_idw_eagle.cashdbo_cash_activity", (col("ENTITY_ID").contains("QA_") | col("UPDATE_SOURCE").contains("QA_"))),
    ("`db-dev-ei`.curated_common.dim_portfolio", col("PORTFOLIO_ID").contains("QA_")),
    ("`db-dev-ei`.curated_common.dim_security", col("IMCO_Security_Alias_ID").isin(['9992718','9991729','999153'])),
    ("`db-dev-ei`.curated_common.fact_idw_dyn_cash_activity", col("IDW_CASH_INT").isin([999304067, 999304083, 999304097, 999304555, 99923604421, 917717149, 922224214, 922224210]))
]

# Iterate over the list, filter each table based on its delete condition, and display the filtered DataFrame
for table_name, delete_condition in tables_with_conditions:
    db_df_to_delete = spark.table(table_name).filter(delete_condition)
    print(table_name)
    display(db_df_to_delete)

# COMMAND ----------

df = spark.table("`db-dev-ei`.enriched_idw_eagle.performdbo_perf_sec_returns").filter("Is_Src_Current == true")

# COMMAND ----------

from pyspark.sql import functions as F

df = df.withColumn("update_date_2", F.date_format(df["UPDATE_DATE"], "yyyy_MM"))

# COMMAND ----------

df.select('update_date_2').distinct().count()

# COMMAND ----------

from pyspark.sql import DataFrame

def save_large_dataframe(df: DataFrame, path: str):
    # Adjust the number of partitions based on your dataset and cluster size
    # Use repartition if you need to increase the number of partitions or change partitioning columns
    # df = df.repartition("partitionColumn")
    
    # Use coalesce if reducing the number of partitions without shuffling data
    df = df.coalesce(10)  # Adjust the number based on your scenario
    
    # Write the DataFrame to Parquet format, partitioned by a suitable column
    df.write.format("parquet") \
        .option("compression", "snappy") \
        .partitionBy("update_date_2") \
        .mode("overwrite") \
        .save(path)

# Example usage
save_large_dataframe(df, f"abfss://qastatic@stadlsidpdevcanc.dfs.core.windows.net/test_partition/")

# COMMAND ----------

df = spark.read.format("parquet").load("abfss://qastatic@stadlsidpdevcanc.dfs.core.windows.net/test_partition/")

# COMMAND ----------

display(df.count())

# COMMAND ----------

df = spark.table("`db-dev-ei`.enriched_idw_eagle.rulesdbo_entity_list").filter("Is_Src_Current == true")

# COMMAND ----------

df.select("ENTITY_ID").distinct().count()

# COMMAND ----------

from pyspark.sql import DataFrame

def save_large_dataframe(df: DataFrame, path: str):
    # Adjust the number of partitions based on your dataset and cluster size
    # Use repartition if you need to increase the number of partitions or change partitioning columns
    # df = df.repartition("partitionColumn")
    
    # Use coalesce if reducing the number of partitions without shuffling data
    df = df.coalesce(5)  # Adjust the number based on your scenario
    
    # Write the DataFrame to Parquet format, partitioned by a suitable column
    df.write.format("parquet") \
        .option("compression", "snappy") \
        .partitionBy("ENTITY_ID") \
        .mode("overwrite") \
        .save(path)

# Example usage
save_large_dataframe(df, f"abfss://qastatic@stadlsidpdevcanc.dfs.core.windows.net/test_partition/")

# COMMAND ----------

display(df.count())

# COMMAND ----------


display(spark.table('`db-dev-ei`.enriched_idw_eagle.cashdbo_cash_activity').select("EFFECTIVE_DATE").distinct().orderBy("EFFECTIVE_DATE"))

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, LongType, BooleanType
from pyspark.sql.functions import to_date, max, col, lower

# COMMAND ----------

primay_key_dict = {
    'Fact_Daily_Portfolio_Performance':["DIM_EFFECTIVE_DATE_KEY","DIM_SOURCE_STATUS_KEY", "dim_portfolio_key"]
}

# COMMAND ----------

# MAGIC %run "../../Config"

# COMMAND ----------

from concurrent.futures import ThreadPoolExecutor, as_completed

def get_row_count(tableFullName):
    return spark.table(tableFullName).count()

def get_filtered_row_count(tableFullName):
    try:
        return spark.table(tableFullName).filter("Is_Src_Current == 1").count()
    except Exception:
        try:
            return spark.table(tableFullName).filter("SOURCE_CURRENT_FLAG == 1").count()
        # If the table does not have the column, return the total row count
        except Exception:
            return get_row_count(tableFullName)


def process_table_name(tableName, schema_prefix):
    if not tableName.tableName.startswith(filter_list):
        tableFullName = f"{schema_prefix}.{tableName.tableName}"
        rowCount = get_row_count(tableFullName)
        rowCountFiltered = get_filtered_row_count(tableFullName)
        return (tableName.tableName, rowCount, rowCountFiltered)
    return None

enriched_idw_eagle_table_name_df = spark.sql(f"SHOW TABLES IN `db-{env}-ei`.enriched_idw_eagle")
curated_common_table_name_df = spark.sql(f"SHOW TABLES IN `db-{env}-ei`.curated_common")
filter_list = ('v_', "bridge", "ref", "xref", "rel", "b_", "bv_", "fact_ss", "fact_monthly_net_", "fact_daily_net_","temp_view")

def process_tables_concurrently(df, schema_prefix):
    results = []
    with ThreadPoolExecutor(max_workers=14) as executor:
        future_to_table = {executor.submit(process_table_name, tableName, schema_prefix): tableName for tableName in df.collect()}
        for future in as_completed(future_to_table):
            result = future.result()
            if result:
                results.append(result)
    return results

# Process both DataFrames
results = process_tables_concurrently(enriched_idw_eagle_table_name_df, f"`db-{env}-ei`.enriched_idw_eagle") + \
          process_tables_concurrently(curated_common_table_name_df, f"`db-{env}-ei`.curated_common")

results_df = spark.createDataFrame(results, ["Table Name", "Row Count", "Filtered Row Count"]).orderBy("Table Name")
display(results_df)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM `db-dev-ei`.curated_common.fact_idw_dyn_cash_activity
# MAGIC WHERE TRANSACTION_ID =  '7883CD3E-52C9-4B65-B860-2B8BAC29CBCB'

# COMMAND ----------

# MAGIC %sql
# MAGIC select cast(EFFECTIVE_DATE as date) as EffectiveDate, count(*) as TotalCount
# MAGIC from `db-dev-ei`.enriched_idw_eagle.cashdbo_cash_activity
# MAGIC where is_src_current = 1
# MAGIC group by cast(EFFECTIVE_DATE as date)
# MAGIC order by EffectiveDate DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC select cast(EFFECTIVE_DATE as date) as EffectiveDate, count(*) as TotalCount
# MAGIC from `db-dev-ei`.enriched_idw_eagle.holdingdbo_position_detail
# MAGIC where is_src_current = 1
# MAGIC group by cast(EFFECTIVE_DATE as date)
# MAGIC order by EffectiveDate DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC select cast(UPDATE_DATE as date) as UPDATE_DATE, count(*) as TotalCount
# MAGIC from `db-dev-ei`.enriched_idw_eagle.performdbo_perf_sec_returns
# MAGIC where is_src_current = 1
# MAGIC group by cast(UPDATE_DATE as date)
# MAGIC order by UPDATE_DATE DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC select IMCO_SECURITY_ALIAS_ID, count(*) as RecordsCount
# MAGIC from `db-dev-ei`.curated_common.dim_security
# MAGIC group by IMCO_SECURITY_ALIAS_ID
# MAGIC order by RecordsCount DESC

# COMMAND ----------

# MAGIC %sql
# MAGIC select IDW_CASH_INT, count(*) as RecordsCount
# MAGIC from `db-dev-ei`.curated_common.fact_idw_dyn_cash_activity
# MAGIC group by IDW_CASH_INT
# MAGIC order by RecordsCount DESC

# COMMAND ----------

table_name = "fact_monthly_bmk_performance"

versions_df = spark.sql(f"DESCRIBE HISTORY `db-{env}-ei`.curated_common.{table_name}")
display(versions_df)

# COMMAND ----------

version_number = 54
df_version = (spark.sql(f"SELECT * FROM `db-{env}-ei`.curated_common.`{table_name}` VERSION AS OF {version_number}"))
display(df_version.filter("SOURCE_CURRENT_FLAG = 1").count())

# COMMAND ----------

# MAGIC %sql
# MAGIC select cast(EFFECTIVE_DATE as date) as EffectiveDate, count(*) as TotalCount
# MAGIC from `db-dev-ei`.enriched_idw_eagle.holdingdbo_position_detail
# MAGIC where is_src_current = 1
# MAGIC group by cast(EFFECTIVE_DATE as date)
# MAGIC order by EffectiveDate DESC

# COMMAND ----------

# MAGIC %sql 
# MAGIC SELECT * FROM `db-dev-ei`.enriched_idw_eagle.holdingdbo_position
# MAGIC WHERE ENTITY_ID = 'IMAP210' 
# MAGIC AND POSITION_ID = 438466.000000000000000000	
# MAGIC AND SRC_INTFC_INST = 195.000000000000000000
