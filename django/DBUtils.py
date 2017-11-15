# -*- coding: utf-8 -*-

from django.db.utils import ProgrammingError
from django.apps import apps
from django.db import DEFAULT_DB_ALIAS, connections
from django.conf import settings



def check_db(db = DEFAULT_DB_ALIAS, create_if_not_exist = False):
	"""
	检查某个在settigs.DATABASES中配置的数据库是否存在
	
	@param db: 与settigs.DATABASES中相匹配的数据库配置（当前仅支持mysql的）
	@param double_check: 是否使用两种不同的方式进行校验
	@return: bool, bool, like as (True, created)
	"""
	#connection = connections[db]
	#try:
	#	cursor = connection.cursor()
	#except ProgrammingError as err:
	#	# https://dev.mysql.com/doc/refman/5.5/en/error-messages-server.html
	#	# Message: Unknown database '%s';
	#	if err.args[0] != 1049:
	#		raise err
	#else:
	#	# 没有错误，说明数据库存在且连上了
	#	# 但是，如果在这时手动删除了该数据库，在这里不能发现，只有最后使得的时候才会发现错误（数据库不存在了）
	#	# 所以这个方法在某些情况下不一定合适
	#	return True, False
	
	# 检查数据库是否存在
	import mysql.connector
	conf = settings.DATABASES[db]
	myconnection = mysql.connector.connect(user = conf["USER"], passwd = conf["PASSWORD"], host = conf["HOST"], port = conf["PORT"])
	myconnection.autocommit = True

	sql = "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA where SCHEMA_NAME = %s;"  # 查询表是否存在
	cursor = myconnection.cursor()
	cursor.execute(sql, (db,))
	
	# 有返回值则表示成功
	if cursor.fetchall():
		myconnection.close()
		return True, False
	
	# 指定的数据库不存在，则不需要自动创建，则直接返回False
	if not create_if_not_exist:
		myconnection.close()
		return False, False
	
	# 数据库没连上，自动创建
	#cursor = myconnection.cursor()
	sql = "CREATE DATABASE IF NOT EXISTS `%s` CHARACTER SET utf8 COLLATE utf8_general_ci;" % db;
	#sql = "CREATE DATABASE IF NOT EXISTS `%s` /*!40100 DEFAULT CHARACTER SET utf8 */;" % db;
	cursor.execute(sql)
	myconnection.close()
	return True, True

def init_app_table(appName, db = DEFAULT_DB_ALIAS):
	"""
	在某个数据库中创建某个app下的表
	
	@param appName: django项目下的app名称
	@param      db: 与settigs.DATABASES中相匹配的数据库配置（当前仅支持mysql的）
	"""
	connection = connections[db]
	app = apps.get_app_config(appName)
	for model in app.get_models():
		with connection.schema_editor() as schema_editor:
			schema_editor.create_model(model)
	return
