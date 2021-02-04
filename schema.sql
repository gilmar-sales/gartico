DROP TABLE IF EXISTS `usuarios`;

CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(120) NOT NULL,
  `senha` varchar(120) NOT NULL,
  `nickname` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `categorias`;

CREATE TABLE `categorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `categorias` WRITE;
INSERT INTO `categorias` VALUES (1,'anime'),(2,'alimento'),(4,'filme'),(5,'veiculo');
UNLOCK TABLES;

DROP TABLE IF EXISTS `subcategorias`;

CREATE TABLE `subcategorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(120) NOT NULL,
  `id_categoria` int NOT NULL,
  PRIMARY KEY (`id`,`id_categoria`),
  KEY `id_categoria_fk_idx` (`id_categoria`),
  CONSTRAINT `id_categoria_fk` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `subcategorias` WRITE;
INSERT INTO `subcategorias` VALUES (1,'Naruto',1),(1,'Fruta',2),(1,'Filmes Geeks',4),(1,'Terrestre',5),(2,'Dragon Ball',1),(2,'Verdura',2),(2,'Marítmo',5),(3,'Legume',2),(3,'Áereo',5),(4,'Bebidas',2);
UNLOCK TABLES;

DROP TABLE IF EXISTS `objetos`;

CREATE TABLE `objetos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(120) NOT NULL,
  `id_categoria` int NOT NULL,
  `id_subcategoria` int NOT NULL,
  PRIMARY KEY (`id`,`id_categoria`,`id_subcategoria`),
  KEY `objeto_categoria_fk_idx` (`id_categoria`),
  KEY `objeto_subcategoria_fk_idx` (`id_subcategoria`),
  CONSTRAINT `objeto_categoria_fk` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id`),
  CONSTRAINT `objeto_subcategoria_fk` FOREIGN KEY (`id_subcategoria`) REFERENCES `subcategorias` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `objetos` WRITE;

INSERT INTO `objetos` VALUES (1,'Sasuke',1,1),(2,'Maçã',2,1),(3,'Uva',2,1),(4,'Laranja',2,1),(5,'Abacate',2,1),(6,'Melancia',2,1),(7,'Manga',2,1),(8,'Alface',2,2),(9,'Cebolinha',2,2),(10,'Couve',2,2),(11,'Repolho',2,2),(12,'Brócolis',2,2),(13,'Abóbora',2,3),(14,'Abobrinha',2,3),(15,'Beterraba',2,3),(16,'Pepino',2,3),(17,'Quiabo',2,3),(18,'Berinjela',2,3),(19,'Gandalf',4,1),(20,'Gollum',4,1),(21,'Frodo',4,1),(22,'Harry',4,1),(23,'Voldemort',4,1),(24,'Snape',4,1),(25,'Yoda',4,1),(26,'Luke Skywalker',4,1),(27,'Darth Vader',4,1),(30,'Carro',5,1),(31,'Moto',5,1),(32,'Ônibus',5,1),(33,'Navio',5,2),(34,'Lancha',5,2),(35,'JetSki',5,2),(36,'Avião',5,3),(37,'Helicóptero',5,3),(38,'Mochila a Jato',5,3),(39,'Naruto',1,1),(40,'Sakura',1,1),(41,'Kakashi',1,1),(42,'Madara',1,1),(43,'Pain',1,1),(44,'Goku',1,2),(45,'Cell',1,2),(46,'Vegeta',1,2),(47,'Mr Satan',1,2),(48,'Majin Boo',1,2),(49,'Videl',1,2),(50,'Yamcha',1,2),(51,'Tio do Ramen',1,1);

UNLOCK TABLES;