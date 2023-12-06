import java.sql.*;

public class Test {
    public static void main(String arg[])
    {
        Connection connection = null;
        try {
            Class.forName("org.mariadb.jdbc.Driver");
            connection = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/defaultdb",
                "looker",
                "does_not_matter"
            );

            Statement statement;
            statement = connection.createStatement();

            ResultSet resultSet;
            resultSet = statement.executeQuery(
                """
                SELECT
                    (DATE(CONVERT_TZ(poc2.date,'UTC','America/Los_Angeles'))) AS `poc2.date`,
                    SUM(poc2.revenue)  AS `poc2.revenue`
                FROM poc2
                    WHERE (poc2.foo) = 123 AND (poc2.bar) = 'ABC'
                GROUP BY
                    1
                ORDER BY
                    1
                LIMIT 5000
                """
            );

            String date;
            String revenue;

            while (resultSet.next()) {
                date = resultSet.getString("date");
                revenue = resultSet.getString("revenue");
                System.out.println(
                    "Date : " + date
                    + " Revenue : " + revenue
                );
            }
            resultSet.close();
            statement.close();
            connection.close();
        }
        catch (Exception exception) {
            exception.printStackTrace();
        }
    }
}
