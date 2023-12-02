db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'blog-flask'
    }
sql = "CREATE TABLE if not exists `users` ( `id` int(11) NOT NULL AUTO_INCREMENT, `email` varchar(255) COLLATE utf8_bin NOT NULL, `name` varchar(255) COLLATE utf8_bin NOT NULL, `password` varchar(255) COLLATE utf8_bin NOT NULL, PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1 ;"

sql_blog = "CREATE TABLE if not exists `articles` ( `id` int(11) NOT NULL AUTO_INCREMENT, `titre` varchar(255) COLLATE utf8_bin NOT NULL, `content` text COLLATE utf8_bin NOT NULL, `user_id` int(11) COLLATE utf8_bin NOT NULL, `created_at` date COLLATE utf8_bin NOT NULL, PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1 ;"
