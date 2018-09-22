package com.big.data.call.mapreduce.util;

import com.mysql.jdbc.util.LRUCache;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

public class SQLUtil {

    private static Log LOG = LogFactory.getLog (SQLUtil.class);

    private static LRUCache cache = new LRUCache(500);

    public static void insert(String tableName, Map<String, Object> colMap) throws SQLException {
        Connection conn = JDBCUtil.getConnection ();
        conn.setAutoCommit (false);
        System.out.println(tableName+"\t"+colMap);
        PreparedStatement statement = prepareStatement (conn, SqlType.INSERT, tableName, colMap, null);
        statement.execute ();
        conn.commit ();
        conn.setAutoCommit (true);
        conn.close ();
    }

    public static void update(String tableName, Map<String, Object> colMap, Map<String, Object> criteriaMap) throws SQLException {
        Connection conn = JDBCUtil.getConnection ();
        conn.setAutoCommit (false);
        PreparedStatement statement = prepareStatement (conn, SqlType.UPDATE, tableName, colMap, criteriaMap);
        statement.execute ();
        conn.commit ();
        conn.setAutoCommit (true);
        conn.close ();
    }

    public static String select(String tableName, List<String> cols, Map<String, Object> criteriaMap) throws SQLException {
        Connection conn = JDBCUtil.getConnection ();
        PreparedStatement statement = prepareStatement (conn, SqlType.SELECT, tableName, cols, criteriaMap);
        String sql = getSQL (conn, SqlType.SELECT, tableName, cols, criteriaMap);
        ResultSet resultSet = statement.executeQuery ();

        String id = null;

        if(resultSet.next ()) {
            if ("tb_call".equals (tableName)) {
                id = resultSet.getObject ("id_date_contact") + "";
            } else {
                id = resultSet.getInt ("id") + "";
            }
        }
        conn.close ();
        return id;
    }

    public static void insertOrUpdate(String tableName,Map<String, Object> colMap,Map<String, Object> criteriaMap) throws SQLException {

        String queryCol = "id_date_contact";
        String id = select (tableName, Arrays.asList (new String[]{queryCol}), criteriaMap);

        if(id!=null){
            update(tableName,colMap,criteriaMap);
        }else{
            insert(tableName,colMap);
        }
    }

    public static String getOrInsertGet(String tableName, String queryId, Map<String, Object> colMap) throws SQLException {

        Object id = cache.get (queryId);

        if (id == null) {
            System.out.println(tableName+"\t"+colMap);
            insert (tableName, colMap);
            id = select (tableName, Arrays.asList (new String[]{"id"}), colMap);
            cache.put (queryId,id);
        }

        return id.toString ();
    }

    private static PreparedStatement prepareStatement(Connection conn,SqlType type, String tableName, Object args, Map<String, Object> criteriaMap) throws SQLException {

        PreparedStatement statement = null;
        StringBuilder sql = new StringBuilder ();

        if (type.equals (SqlType.INSERT)) {
            Map<String, Object> argsMap = ( Map<String, Object> ) args;
            String keySetStr = argsMap.keySet ().toString ();
            String valListStr = argsMap.values ().toString ();
            sql.append ("INSERT INTO ").append (tableName)
                    .append ("(").append (keySetStr.substring (1, keySetStr.length () - 1)).append (")")
                    .append ("VALUE(").append (valListStr.substring (1, valListStr.length () - 1)).append (")");

        } else if (type.equals (SqlType.UPDATE)) {
            Map<String, Object> argsMap = ( Map<String, Object> ) args;
            String keyEntrySetStr = argsMap.entrySet ().toString ();
            String critEntrySetStr = criteriaMap.entrySet ().toString ().replaceAll (","," AND ");

            sql.append ("UPDATE ").append (tableName).append (" SET ")
                    .append (keyEntrySetStr.substring (1, keyEntrySetStr.length () - 1))
                    .append (" WHERE ").append (critEntrySetStr.substring (1, critEntrySetStr.length () - 1));

        } else if (type.equals (SqlType.SELECT)) {
            String colsStr = (( List<String> ) args).toString ();
            String critEntrySetStr = criteriaMap.entrySet ().toString ().replaceAll (","," AND ");

            sql.append ("SELECT ").append (colsStr.substring (1, colsStr.length () - 1)).append (" FROM ").append (tableName)
                    .append (" WHERE ").append (critEntrySetStr.substring (1, critEntrySetStr.length () - 1));

        } else if (type.equals (SqlType.DELETE)) {
            String critEntrySetStr = criteriaMap.entrySet ().toString ().replaceAll (","," AND ");

            sql.append ("DELETE ").append (" FROM ").append (tableName)
                    .append (" WHERE ").append (critEntrySetStr.substring (1, critEntrySetStr.length () - 1));
        }


        statement = conn.prepareStatement (sql.toString ());

        return statement;
    }

    private static  String getSQL(Connection conn,SqlType type, String tableName, Object args, Map<String, Object> criteriaMap) throws SQLException {

        StringBuilder sql = new StringBuilder ();

        if (type.equals (SqlType.INSERT)) {
            Map<String, Object> argsMap = ( Map<String, Object> ) args;
            String keySetStr = argsMap.keySet ().toString ();
            String valListStr = argsMap.values ().toString ();
            sql.append ("INSERT INTO ").append (tableName)
                    .append ("(").append (keySetStr.substring (1, keySetStr.length () - 1)).append (")")
                    .append ("VALUE(").append (valListStr.substring (1, valListStr.length () - 1)).append (")");

        } else if (type.equals (SqlType.UPDATE)) {
            Map<String, Object> argsMap = ( Map<String, Object> ) args;
            String keyEntrySetStr = argsMap.entrySet ().toString ();
            String critEntrySetStr = criteriaMap.entrySet ().toString ().replaceAll (","," AND ");

            sql.append ("UPDATE ").append (tableName).append (" SET ")
                    .append (keyEntrySetStr.substring (1, keyEntrySetStr.length () - 1))
                    .append (" WHERE ").append (critEntrySetStr.substring (1, critEntrySetStr.length () - 1));

        } else if (type.equals (SqlType.SELECT)) {
            String colsStr = (( List<String> ) args).toString ();
            String critEntrySetStr = criteriaMap.entrySet ().toString ().replaceAll (","," AND ");

            sql.append ("SELECT ").append (colsStr.substring (1, colsStr.length () - 1)).append (" FROM ").append (tableName)
                    .append (" WHERE ").append (critEntrySetStr.substring (1, critEntrySetStr.length () - 1));

        } else if (type.equals (SqlType.DELETE)) {
            String critEntrySetStr = criteriaMap.entrySet ().toString ().replaceAll (","," AND ");

            sql.append ("DELETE ").append (" FROM ").append (tableName)
                    .append (" WHERE ").append (critEntrySetStr.substring (1, critEntrySetStr.length () - 1));
        }

        System.out.println(sql);

        return sql.toString ();
    }


    enum SqlType {
        SELECT, INSERT, UPDATE, DELETE;
    }

}
