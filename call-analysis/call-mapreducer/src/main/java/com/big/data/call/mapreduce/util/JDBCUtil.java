package com.big.data.call.mapreduce.util;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import java.sql.*;

public class JDBCUtil {
    private static final Log logger = LogFactory.getLog (JDBCUtil.class);
    private static final String MYSQL_DRIVER_CLASS = "com.mysql.jdbc.Driver";
    private static final String MYSQL_URL = "jdbc:mysql://localhost:3306/db_telecom?useUnicode=true&characterEncoding=UTF-8";
    private static final String MYSQL_USERNAME = "root";
    private static final String MYSQL_PASSWORD = "root";
    /**
     * 获取Mysql数据库的连接
     * @return
     */
    public static Connection getConnection() throws SQLException {
        try {
            Class.forName(MYSQL_DRIVER_CLASS);

        } catch (ClassNotFoundException e) {

        }
        return DriverManager.getConnection(MYSQL_URL, MYSQL_USERNAME, MYSQL_PASSWORD);
    }

    /**
     * 关闭数据库连接释放资源
     * @param connection
     * @param statement
     * @param resultSet
     */
    public static void close(Connection connection, Statement statement, ResultSet resultSet){
        if(resultSet != null) try {
            resultSet.close();
        } catch (SQLException e) {
        }

        if(statement != null) try {
            statement.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }

        if(connection != null) try {
            connection.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
